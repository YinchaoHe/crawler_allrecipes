import glob
import os
import json
import shutil


def get_recipe_nutrition():
    with open('data/original_recipes_info/1_recipes_data.json', 'r') as f:
        recipes = json.load(f)
    for recipe in recipes:
        print(recipe['nutrition'])

def main():
    os.system("find . -name original_recipes_info > re_info_path.txt")
    with open("re_info_path.txt") as f:
        paths = f.readlines()
    for path in paths:
        output_path = path.replace('\n', '').split('original_recipes_info')[0]
        output_path = output_path.split('./')[1]
        dir = output_path.split('/')[0] + '_recipes_text_info'
        try:
            os.mkdir(dir)
        except:
            print('this folder exists')
        output_path = output_path.replace('/', '_')
        print(output_path)
        path = path.replace('\n', '') + '/'
        files=glob.glob(path + '*')
        for file in files:
            directory = output_path
            filename = file.split('/')[-1]
            directory += filename
            shutil.move(file, dir + '/' + directory)


if __name__ == '__main__':
    main()
