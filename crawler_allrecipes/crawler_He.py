import argparse
import unicodedata
import urllib
import urllib.request as req
import bs4
import json
import os
from socket import error as SocketError


def main(start, end):
    try:
        path = "report"
        os.mkdir(path)
    except:
        print("the report folder exists in the current directory.")
    try:
        path = "report/imgs"
        os.mkdir(path)
    except:
        print("the imgs folder exists in the report folder.")

    with open('report/recipes_data.json', 'a+', encoding='utf-8') as jsonfile:
        for i in range(start, end):
            print("Recipe_ID: " + str(i))
            data = get_ingredients(i)
            json.dump(data, jsonfile, ensure_ascii=False)
            jsonfile.write(',')


def get_ingredients(recipe_ID):
    try:
        path = "report/imgs/" + str(recipe_ID)
        os.mkdir(path)
    except:
        print("the recipe was scraped before.")
        return

    try:
        url = "https://www.allrecipes.com/recipe/" + str(recipe_ID)
        request = req.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        })
        with req.urlopen(url) as response:
            html_data = response.read().decode("utf-8")

    except urllib.error.HTTPError as e:
        with open('report/exception_recipe_ID.txt', 'a+') as f:
            result = str(recipe_ID) + " does not have any recipe."
            f.write(result + "\n")
            f.close()
        data = {}
        data['recipe_ID'] = recipe_ID
        data['name'] = "No recipe"
        os.rmdir(path)
        print("No recipe because of ERROR 404")
        return data
    except urllib.error.URLError as e:
        print("URL ERROR")
        print(e.reason)
    except SocketError as e:
        print("SOCKET ERROR")

    #Begin to parse the website

    root = bs4.BeautifulSoup(html_data, "html.parser")
    data = {}
    data['recipe_ID'] = recipe_ID
    try:
        name = root.find("h1", class_="headline heading-content")
        if name is None:
            name = root.find("h1", class_="recipe-summary__h1")
        data['name'] = name.string
    except:
        with open('report/exception_recipe_ID.txt', 'a+') as f:
            result = str(recipe_ID) + " does not have NAME."
            f.write(result + "\n")
            f.close()
        data['name'] = "No name"
        print("No recipe's name")

    try:
        image_sections = root.find_all("a", class_="ugc-photos-link")
        image_url = []
        img_index = 1
        for image_section in image_sections:
            try:
                image = image_section.find("img")
                if image != None:
                    image_src = image["src"]
                    image_url.append(image_src)
                    req.urlretrieve(image_src, path + "/" + str(recipe_ID) + "_" + str(img_index) + ".jpg")
                    img_index += 1
            except:
                continue
        if img_index == 1:
            data['image_url'] = "No Image"
            with open('report/exception_recipe_ID.txt', 'a+') as f:
                result = str(recipe_ID) + " has recipe but does not have any IMGS."
                f.write(result + "\n")
                f.close()
        else:
            data['image_url'] = image_url
    except:
        data['name'] = "No Image"
        print("No Image")

    try:
        ingredients = root.find_all("span", class_="ingredients-item-name")
        array_ingredients = []
        for ingredient in ingredients:
            desc_ingredient = ingredient.string
            desc_ingredient = desc_ingredient.strip()
            desc_ingredient = unicodedata.normalize('NFKC', desc_ingredient)
            array_ingredients.append(desc_ingredient)
        if len(ingredients) == 0:
            ingredients = root.find_all("span", class_="recipe-ingred_txt added")
            array_ingredients = []
            for ingredient in ingredients:
                desc_ingredient = ingredient.string
                array_ingredients.append(desc_ingredient)

        data['ingredients'] = array_ingredients
    except:
        with open('report/exception_recipe_ID.txt', 'a+') as f:
            result = str(recipe_ID) + " does not have any INGREDIENTS."
            f.write(result + "\n")
            f.close()
        data['ingredients'] = "No Ingredients"
        print("No Ingredients")

    try:
        serving_informstions = root.find_all("div", class_="recipe-meta-item")
        serving = []
        for serving_informstion in serving_informstions:
            info = ''
            desc_serving_info = serving_informstion.text
            desc_serving_info = desc_serving_info.strip()
            desc_serving_infos = desc_serving_info.split("\n")
            for desc_serving_info in desc_serving_infos:
                desc_serving_info = desc_serving_info.strip()
                if desc_serving_info.strip():
                    info += desc_serving_info
            serving.append(info)
        data['serving_information'] = serving
    except:
        with open('report/exception_recipe_ID.txt', 'a+') as f:
            result = str(recipe_ID) + " does not have any SERVING INFORMATION."
            f.write(result + "\n")
            f.close()
        data['serving_information'] = "No serving information"
        print("No serving information")

    try:
        nutrition_section = root.find("div", class_="partial recipe-nutrition-section")
        nutrition_section = nutrition_section.find("div", class_="section-body")
        nutrition_infos = nutrition_section.text.split(";")

        nutrition = []
        for nutrition_info in nutrition_infos:
            nutrition_info = nutrition_info.strip() + ";"
            nutrition_info = nutrition_info.replace(".        Full Nutrition;", "")
            nutrition.append(nutrition_info)
        data['nutrition_perServing'] = nutrition
    except:
        with open('report/exception_recipe_ID.txt', 'a+') as f:
            result = str(recipe_ID) + " does not have any NUTRITION INFORMATION."
            f.write(result + "\n")
            f.close()
        data['nutrition_perServing'] = "No nutrition information"
        print("No nutrition information")

    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start", help="the start index of recipe ID", type=int, default="46475", #"274330",
                        required=False)
    parser.add_argument("-e", "--end", help="the end index of recipe ID", type=int, default="46476", required=False)
    args = parser.parse_args()
    main(args.start, args.end)
