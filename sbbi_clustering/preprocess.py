import argparse
import csv
import glob
import json
import os
import shutil

def extract_text_files(country):
    os.system("find . -name original_recipes_info > re_info_path.txt")
    try:
        os.mkdir(country)
    except:
        print('this folder exists')
    with open("re_info_path.txt") as f:
        paths = f.readlines()
    for path in paths:
        output_path = path.replace('\n', '').split('original_recipes_info')[0]
        output_path = output_path.split('./')[1]
        dir = output_path.split('/')[0] + '_text_info'
        dir = country + '/' + dir
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





def nutrition_json2cvs(country):
    #get all recipes' calories information
    all_recipes_calo = {}
    calo_path = 'world_cuisine_extend_calories'
    if os.path.isdir(calo_path):
        os.chdir(calo_path)
        calo_folders = glob.glob( country + '*')
    else:
        print("Please add a folder called world_cuisine_extend_calories")

    for calo_folder in calo_folders:
        os.chdir(calo_folder)
        calo_files = glob.glob('*')
        for calo_file in calo_files:
            with open(calo_file, 'r') as f:
                recipes_calo = json.load(f)
                for recipe_calo in recipes_calo:
                    calo = []
                    for key in recipe_calo.keys():
                        calo.append(int(recipe_calo[key]))
                    try:
                        all_recipes_calo[str(calo[0])] = calo[1]
                    except:
                        all_recipes_calo[str(calo[0])] = 1000000000000000

    #get other nutrition informtion
    root_path = os.getcwd()
    root_path = root_path.split('/world_cuisine_extend_calories')[0]
    os.chdir(root_path)
    csv_columns = ['Recipe_ID', 'calories', 'Total Fat', 'Saturated Fat', 'Cholesterol', 'Sodium', 'Potassium','Total Carbohydrates', 'Dietary Fiber', 'Protein', 'Sugars', 'Vitamin A', 'Vitamin C', 'Calcium', 'Iron', 'Thiamin', 'Niacin', 'Vitamin B6', 'Magnesium', 'Folate']
    folders = glob.glob(country + '/*')
    for folder in folders:
        print(folders)
        files = glob.glob(folder + '/*')
        for file in files:
            print(file)
            with open(file, 'r') as f:
                recipes = json.load(f)
            dict_data = []
            for recipe in recipes:
                if (len(recipe['nutrition']) > 0):
                    for key in recipe['nutrition'].keys():
                        if 'mcg' in recipe['nutrition'][key]:
                            recipe['nutrition'][key] = recipe['nutrition'][key].split('mcg')[0]
                        elif 'mg' in recipe['nutrition'][key]:
                            recipe['nutrition'][key] = recipe['nutrition'][key].split('mg')[0]
                        elif 'g' in recipe['nutrition'][key]:
                            recipe['nutrition'][key] = recipe['nutrition'][key].split('g')[0]
                        elif 'IU' in recipe['nutrition'][key]:
                            recipe['nutrition'][key] = recipe['nutrition'][key].split('IU')[0]
                    recipe['nutrition']['Recipe_ID'] = recipe['recipe_ID']
                    recipe['nutrition']['calories'] = all_recipes_calo[recipe['recipe_ID']]
                    dict_data.append(recipe['nutrition'])

            csv_file =  country + '/' + country + "_recipes_nutrition.csv"
            if os.path.isfile(csv_file):
                try:
                    with open(csv_file, 'a+') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                        for data in dict_data:
                            writer.writerow(data)
                except IOError:
                    print("I/O error")
            else:
                try:
                    with open(csv_file, 'w') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                        writer.writeheader()
                        for data in dict_data:
                            writer.writerow(data)
                except IOError:
                    print("I/O error")

            with open( country + '/' +country+'_integration_all_calo.json', 'w') as f:
                json.dump(all_recipes_calo, f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--country", help="country information", required=True)
    parser.add_argument("-n", "--nutrition", help="nutrition information", default=False)
    country = parser.parse_args().country
    isNutrition = parser.parse_args().nutrition
    if isNutrition == False:
        extract_text_files(country)
    else:
        nutrition_json2cvs(country)

if __name__ == '__main__':
    main()