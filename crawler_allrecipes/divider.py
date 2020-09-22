import os
import json
from sys import argv
import glob

def main():
    suppath = 'IndianRecipes/*'
    subpath = glob.glob(suppath)
    for path in subpath:
        folderpath = path + '/original_recipes_info/*.json'
        # folderpath = 'IndianSideDish/original_recipes_info/*.json'
        files = glob.glob(folderpath)
        print(files)
        for file in files:
            recipe_json = file
            recipe_folder = recipe_json.split('.')[0]

            with open(recipe_json, 'r') as f:
                recipes = json.load(f)

            try:
                path = 'devidedfiles'
                os.makedirs(path)
            except:
                pass

            try:
                path = path + '/'+recipe_folder
                os.makedirs(path)
            except:
                pass

            for recipe in recipes:
                fname = recipe['recipe_ID']
                ingredients = recipe['ingredients']

                with open(path + '/' + fname, 'a') as f:
                    for row in ingredients:
                        row = row.lower()
                        f.write(row+ '\n')
                    #f.write("\n".join(ingredients).encode('utf8').lower())

            print(recipe_folder)



if __name__ == '__main__':
    main()