import glob
import json
import os
import time
import urllib
import urllib.request as req
import bs4

def main():

    os.system("find . -name original_recipes_info > re_info_path.txt")
    with open("re_info_path.txt") as f:
        paths = f.readlines()
    for path in paths:
        output_path = path.replace('\n', '').split('original_recipes_info')[0]
        output_path = output_path.split('./')[1]
        dir = output_path.split('/') + '_calories_info'
        try:
            os.mkdir(dir)
        except:
            print('this folder exists')
            
        output_path = output_path.replace('/', '_')
        print(output_path)
        # output_path += 'calories_info'
        # try:
        #     os.mkdir(output_path)
        # except:
        #     print("This folder exists")
        path = path.replace('\n', '') + '/'
        files=glob.glob(path + '*')
        calo_info = []
        index = 1
        for file in files:
            print(file)
            with open(file) as info:
                recipes = json.load(info)
                for recipe in recipes:
                    print(recipe['recipe_ID'])
                    calo = get_all_nutrition(recipe)
                    calo_info.append(calo)
            with open(dir + '/' + output_path +  str(index) + '_calories_info.json', 'w') as f:
                json.dump(calo_info, f)
            index += 1
    os.remove('re_info_path.txt')
def get_all_nutrition(data):
    info = {'recipe_ID': data['recipe_ID']}
    try:
        name = data['name'].lower()
        name = name.replace(" ", "-")

        url = "https://www.allrecipes.com/recipe/" + str(data['recipe_ID']) + "/" + name + "/fullrecipenutrition/"
        request = req.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        })
        time.sleep(5)
        try:
            with req.urlopen(url) as response:
                data = response.read().decode("utf-8")
        except:
            return info
    except:
        print("URL ERROR")

    try:
        root = bs4.BeautifulSoup(data, "html.parser")
        nutrition_div = root.find("div", class_="nutrition-top light-underline")
        calo = nutrition_div.text.split('Amount')[1]
        calo = calo.replace("\n", ' ')
        calos = calo.split(':')
        info[calos[0]] = calos[1]


    except:
        print('nutrition error')

    return info
if __name__ == '__main__':
    main()