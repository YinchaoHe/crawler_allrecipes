import glob
import json
import os
import csv
import time

import pandas as pd

def read_excel():
    data = pd.read_excel("test.xlsx")
    df = pd.DataFrame(data, columns=['FDCID'])
    df = df.dropna()
    FDCID = []
    for new_FDCID in df['FDCID']:
        flag = 1
        for checked_FDCID in FDCID:
            if checked_FDCID == new_FDCID:
                flag = 0
                break
        if flag == 1:
            FDCID.append(int(new_FDCID))
    result = {}
    result['FDCID'] = FDCID
    with open('FDCID.txt', 'w') as f:
        json.dump(result, f)

def read_cvs():
    fdc_id = []
    with open('sr_legacy_food.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        for row in csv_reader:
            fdc_id.append(row[0])
    result = {}
    result['FDCID'] = fdc_id
    with open('FDCID_1.txt', 'w') as f:
        json.dump(result, f)

def grap_nutritient():
    path = 'original_ingredient_nutrition'
    new_path = 'chosen_ingredient_nutrition'
    try:
        os.mkdir(path)
    except:
        print("the folder exists in the current directory.")
    try:
        os.mkdir(new_path)
    except:
        print("the folder exists in the current directory.")

    with open('FDCID.txt') as f:
        data = json.load(f)
    FDCID = data['FDCID']
    # FDCID = read_cvs()
    for item in FDCID:
        print("the FDCID is: " + str(item))
        url = "https://api.nal.usda.gov/fdc/v1/food/" + str(item) + "?api_key=5XhH6rNR9dLzWtUTVvFIzhupntyAfUmnYHkv4gWF"
        os.system("curl " + url + "> original_ingredient_nutrition/" + str(item) + ".json")
        with open('original_ingredient_nutrition/' + str(item) + '.json') as f:
            data = json.load(f)
        os.remove(path +'/' + str(item) + '.json')
        #time.sleep(20)

        # name = data["description"].replace(" ", "")
        # name = name.replace(",", "_")
        # name = name.replace("/", "_")
        # if os.path.exists(path + '/' + name + '.json') == True:
        #     print(str(item) + "exists.")
        #     continue
        try:
            result = {"ingredient": data["description"],
                      "portion": '100g'}
        except:
            result = {"ingredient": str(item),
                      "portion": '100g'}
        nu_info = {}
        for nutrient_info in data["foodNutrients"]:
            nutrient = nutrient_info['nutrient']
            if nutrient['id'] == 1258 or nutrient['id'] == 1004 or nutrient['id'] == 1253 or nutrient['id'] == 1093 or \
                    nutrient['id'] == 1092 or nutrient['id'] == 2039 or nutrient['id'] == 1079 or nutrient[
                'id'] == 1003 or nutrient[
                'id'] == 2000:
                try:
                    nu_info[nutrient['name']] = str(nutrient_info['amount']) + nutrient['unitName']
                except:
                    nu_info[nutrient['name']] = "NONE"
            if nutrient['id'] == 1106 or nutrient['id'] == 1162 or nutrient['id'] == 1087 or nutrient[
                'id'] == 1089 or \
                    nutrient['id'] == 1165 or nutrient['id'] == 1167 or nutrient['id'] == 1175 or nutrient[
                'id'] == 1090 or nutrient['id'] == 1187:
                try:
                    nu_info[nutrient['name']] = str(nutrient_info['amount']) + nutrient['unitName']
                except:
                    nu_info[nutrient['name']] = "NONE"
        result['nutrition'] = nu_info

        try:
            name = data["description"].replace(" ", "")
            name = name.replace(",", "_")
            name = name.replace("/", "_")
        except:
            name = str(item)
        with open(new_path + '/' + name + '.json', 'w') as f:
            json.dump(result, f)

        with open(path + '/' + name + '.json', 'w') as f:
            json.dump(data, f)


def grap_saturated_fat():
    path = 'sr_legacy_original_ingredient_nutrition/'
    files = glob.glob(path + '*.json')
    error_file = []
    for file in files:
        try:
            with open(file) as f:
                data = json.load(f)
                try:
                    result = {"ingredient": data["description"],
                              "portion": '100g'}
                except:
                    print(data["description"] + ' ERROR')
                nu_info = {}
                for nutrient_info in data["foodNutrients"]:
                    nutrient = nutrient_info['nutrient']
                    if nutrient['id'] == 1258 or nutrient['id'] == 1004 or nutrient['id'] == 1253 or nutrient['id'] == 1093 or nutrient['id'] == 1092 or nutrient['id'] == 2039 or nutrient['id'] == 1079 or nutrient['id'] == 1003 or nutrient[
                    'id'] == 2000:
                        try:
                            nu_info[nutrient['name']] = str(nutrient_info['amount']) + nutrient['unitName']
                        except:
                            nu_info[nutrient['name']] = "NONE"
                    if nutrient['id'] == 1106 or nutrient['id'] == 1162 or nutrient['id'] == 1087 or nutrient[
                        'id'] == 1089 or \
                            nutrient['id'] == 1165 or nutrient['id'] == 1167 or nutrient['id'] == 1175 or nutrient[
                        'id'] == 1090 or nutrient['id'] == 1187:
                        try:
                            nu_info[nutrient['name']] = str(nutrient_info['amount']) + nutrient['unitName']
                        except:
                            nu_info[nutrient['name']] = "NONE"
                result['nutrition'] = nu_info
                try:
                    name = data["description"].replace(" ", "")
                    name = name.replace(",", "_")
                    name = name.replace("/", "_")
                except:
                    name = file.split('/')[-1]

                new_path = 'sr_legacy_chosen_ingredient_nutrition'
                try:
                    os.mkdir(new_path)
                except:
                    print("the folder exists in the current directory.")
                with open(new_path + '/' + name + '.json', 'w') as f:
                    json.dump(result, f)
        except:
            error_file.append(file)
    print(error_file)

def combine(path):

    info = []
    file_list = os.listdir(path)
    for file in file_list:
        with open(path + '/' + file) as f:
            data = json.load(f)
        info.append(data)
    with open('all_ingredients_nutritient.json', 'w') as f:
        json.dump(info, f)

def count():
    file_list = os.listdir('original_ingredient_nutrition')
    print(len(file_list))

def main():
    grap_nutritient()


if __name__ == '__main__':
    main()
