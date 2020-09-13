import argparse
import unicodedata
import urllib
import urllib.request as req
import bs4
import json
import os
from socket import error as SocketError


def main():
    try:
        country = 'Mexican'
        os.mkdir(country)
    except:
        print("the recipe_type folder exists in the current directory.")

    recipe_infos = {'MexicanAppetizer': 'https://www.allrecipes.com/recipes/1214/world-cuisine/latin-american/mexican/appetizers/',
                   'MexicanMainDish':'https://www.allrecipes.com/recipes/17504/world-cuisine/latin-american/mexican/main-dishes/',
                   'MexicanDrinks':'https://www.allrecipes.com/recipes/15936/world-cuisine/latin-american/mexican/drinks/',
                   'MexicanDessert':'https://www.allrecipes.com/recipes/1217/world-cuisine/latin-american/mexican/desserts/',
                   'MexicanSideDish':'https://www.allrecipes.com/recipes/1526/world-cuisine/latin-american/mexican/side-dishes/',
                   'MexicanSalad':'https://www.allrecipes.com/recipes/17513/world-cuisine/latin-american/mexican/salads/',
                   'MexicanSlowCooker':'https://www.allrecipes.com/recipes/16334/everyday-cooking/slow-cooker/mexican/',
                   'MexicanBread':'https://www.allrecipes.com/recipes/1525/world-cuisine/latin-american/mexican/bread/',
                   'MexicanBurrito':'https://www.allrecipes.com/recipes/1216/world-cuisine/latin-american/mexican/main-dishes/burritos/',
                   'MexicanChileRelleno':'https://www.allrecipes.com/recipes/16085/world-cuisine/latin-american/mexican/main-dishes/chile-rellenos/',
                   'MexicanEnchilada':'https://www.allrecipes.com/recipes/1218/world-cuisine/latin-american/mexican/main-dishes/enchiladas/',
                    'MexicanFajita':'https://www.allrecipes.com/recipes/1220/world-cuisine/latin-american/mexican/main-dishes/fajitas/',
                    'MexicanTaco':'https://www.allrecipes.com/recipes/1219/world-cuisine/latin-american/mexican/main-dishes/tacos/',
                    'MexicanFishTaco':'https://www.allrecipes.com/recipes/16562/world-cuisine/latin-american/mexican/main-dishes/tacos/fish/',
                    'MexicanRice':'https://www.allrecipes.com/recipes/16082/world-cuisine/latin-american/mexican/side-dishes/rice/',
                    'MexicanSoupsandStews':'https://www.allrecipes.com/recipes/1215/world-cuisine/latin-american/mexican/soups-and-stews/',
                    'MexicanQuesadilla':'https://www.allrecipes.com/recipes/1905/world-cuisine/latin-american/mexican/main-dishes/quesadillas/'
    }
    for recipe_info in recipe_infos.keys():
        url = recipe_infos[recipe_info]
        recipe_type = country + '/' +recipe_info
        for i in range(16, 101):
            recipe_ids  = preprocess(i, recipe_type, url)
            if len(recipe_ids) == 0:
                print("This page is empty")
                break
            else:
                crawler_allrecipes(recipe_ids, i, recipe_type)


def preprocess(pagenumber, recipe_type, url):
    print(pagenumber)
    try:
        url = url + '?page=' + str(pagenumber)
        request = req.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        })
        with req.urlopen(url) as response:
            data = response.read().decode("utf-8")

    except urllib.error.HTTPError as e:
        with open(recipe_type + '/exception_recipe_ID.txt', 'a+') as f:
            result = str(1) + " does not have any recipe."
            f.write(result + "\n")
            f.close()
        recipe_ids = []
        return recipe_ids
    except urllib.error.URLError as e:
        print("URL ERROR")
        print(e.reason)
        recipe_ids = []
        return recipe_ids
    except SocketError as e:
        print("SOCKET ERROR")
        recipe_ids = []
        return recipe_ids

    try:
        root = bs4.BeautifulSoup(data, "html.parser")
        recipes = root.find_all("div", class_="recipe-card recipeCard")
        recipe_ids = []
        for recipe in recipes:
            detail = recipe.find('div', class_='recipeCard__detailsContainer')
            detail = detail.find('a', class_='recipeCard__titleLink')
            url = detail['href']
            recipe_id = url.split('/recipe/')[1]
            recipe_id = recipe_id.split('/')[0]
            recipe_ids.append(recipe_id)
        return recipe_ids


    except:
        recipe_ids = []
        return recipe_ids


def crawler_allrecipes(recipe_ids, index, recipe_type):
    try:
        path = recipe_type  # "report"
        os.mkdir(path)
    except:
        print("the recipe_type folder exists in the current directory.")
    try:
        path = recipe_type + '/imgs'  # "report/imgs"
        os.mkdir(path)
    except:
        print("the imgs folder exists in the report folder.")

    try:
        path = recipe_type + '/original_recipes_info'  # "report/original_recipes_info"
        os.mkdir(path)
    except:
        print("the imgs folder exists in the report folder.")

    with open(recipe_type + '/original_recipes_info/' + str(index) + '_recipes_data.json', 'a+',
              encoding='utf-8') as jsonfile:
        # jsonfile.write('[')
        recipes = []
        for i in recipe_ids:
            print("Recipe_ID: " + str(i))
            data = get_ingredients(i, recipe_type)



            # if data['name'] != 'No recipe':
            #     json.dump(data, jsonfile, ensure_ascii=False)
            #     jsonfile.write(',')
            if data['name'] != 'No recipe':
                data['nutrition'] = get_all_nutrition(data)
                recipes.append(data)
        json.dump(recipes, jsonfile, ensure_ascii=False)
        # jsonfile.write(']')


def get_ingredients(recipe_ID, recipe_type):
    try:
        path = recipe_type + "/imgs/" + str(recipe_ID)
        os.mkdir(path)
    except:
        print("the recipe was scraped before.")
        data = {}
        data['recipe_ID'] = recipe_ID
        data['name'] = "No recipe"
        return data

    try:
        url = "https://www.allrecipes.com/recipe/" + str(recipe_ID)
        request = req.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        })
        with req.urlopen(url) as response:
            data = response.read().decode("utf-8")

    except urllib.error.HTTPError as e:
        with open(recipe_type + '/exception_recipe_ID.txt', 'a+') as f:
            result = str(recipe_ID) + " does not have any recipe."
            f.write(result + "\n")
            f.close()
        data = {}
        data['recipe_ID'] = recipe_ID
        data['name'] = "No recipe"
        os.rmdir(path)
        print("No recipe")
        return data
    except urllib.error.URLError as e:
        print("URL ERROR")
        print(e.reason)
    except SocketError as e:
        print("SOCKET ERROR")

    try:
        root = bs4.BeautifulSoup(data, "html.parser")
        image_sections = root.find_all("a", class_="ugc-photos-link")
        name = root.find("h1", class_="headline heading-content")
        ingredients = root.find_all("span", class_="ingredients-item-name")
        serving_informstions = root.find_all("div", class_="recipe-meta-item")
        # nutrition_section = root.find("div", class_="partial recipe-nutrition-section")
        # nutrition_section = nutrition_section.find("div", class_="section-body")
        # nutrition_infos = nutrition_section.text.split(";")
    except:
        with open(recipe_type + '/exception_recipe_ID.txt', 'a+') as f:
            result = str(recipe_ID) + " does not have any recipe."
            f.write(result + "\n")
            f.close()
        data = {}
        data['recipe_ID'] = recipe_ID
        data['name'] = "No recipe"
        os.rmdir(path)
        print("No recipe")
        return data

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
        with open(recipe_type + '/exception_recipe_ID.txt', 'a+') as f:
            result = str(recipe_ID) + " has recipe but does not have any IMGS."
            f.write(result + "\n")
            f.close()

    # nutrition = []
    # for nutrition_info in nutrition_infos:
    #     nutrition_info = nutrition_info.strip() + ";"
    #     nutrition_info = nutrition_info.replace(".        Full Nutrition;", "")
    #     nutrition.append(nutrition_info)

    array_ingredients = []
    for ingredient in ingredients:
        desc_ingredient = ingredient.string
        desc_ingredient = desc_ingredient.strip()
        desc_ingredient = unicodedata.normalize('NFKC', desc_ingredient)
        array_ingredients.append(desc_ingredient)

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

    #nutrition = get_all_nutrition(name.string)
    try:
        data = {}
        data['recipe_ID'] = recipe_ID
        data['name'] = name.string
        data['ingredients'] = array_ingredients
        #data['nutrition_perServing'] = nutrition
        data['serving_information'] = serving
        return data
    except:
        data['name'] = "No recipe"
        return data



def get_all_nutrition(data):
    nutrition = {}
    try:
        name = data['name'].lower()
        name = name.replace(" ", "-")

        url = "https://www.allrecipes.com/recipe/" + str(data['recipe_ID']) + "/" + name + "/fullrecipenutrition/"
        request = req.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        })
        try:
            with req.urlopen(url) as response:
                data = response.read().decode("utf-8")
        except:
            return nutrition
    except urllib.error.URLError as e:
        print("URL ERROR")
        print(e.reason)
    except SocketError as e:
        print("SOCKET ERROR")

    try:
        root = bs4.BeautifulSoup(data, "html.parser")
        nutrition_divs = root.find_all("div", class_="nutrition-row")
        for nutrition_div in nutrition_divs:
            nutrient = nutrition_div.find("span", class_="nutrient-name")
            nutrient = nutrient.text.split(':')
            dv = ''
            if (nutrition_div.find("span", class_="daily-value")):
                dv = nutrition_div.find("span", class_="daily-value")
                dv = ' DV:' + dv.text.replace(' ', '')
            nutrition[nutrient[0]] = nutrient[1].strip() + dv
        return nutrition

    except:
        print('nutrition error')



if __name__ == '__main__':
    main()
