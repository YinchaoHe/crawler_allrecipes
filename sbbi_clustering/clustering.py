import csv
import glob
import os
import json
import argparse


#def get_recipe_nutrition():
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--country", help="country information", required=True)
    args = parser.parse_args().country
    csv_columns = ['Total Fat', 'Saturated Fat', 'Cholesterol', 'Sodium', 'Potassium','Total Carbohydrates', 'Dietary Fiber', 'Protein', 'Sugars', 'Vitamin A', 'Vitamin C', 'Calcium', 'Iron', 'Thiamin', 'Niacin', 'Vitamin B6', 'Magnesium', 'Folate']
    folders = glob.glob(args + '/*')
    for folder in folders:
        files = glob.glob(folder + '/*')
        for file in files:
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
                    print(recipe['nutrition'])
                    dict_data.append(recipe['nutrition'])

            csv_file = "recipes_nutrition.csv"
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






if __name__ == '__main__':
    main()
