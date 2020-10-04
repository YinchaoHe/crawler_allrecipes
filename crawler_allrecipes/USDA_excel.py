import json
import os

import pandas as pd


def main():
    try:
        os.mkdir('result')
    except:
        print("the folder exists in the current directory.")

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

    for item in FDCID:
        url = "https://api.nal.usda.gov/fdc/v1/food/" + str(item) + "?api_key=DEMO_KEY"
        os.system("curl " + url + "> result/" + str(item) + ".json")
        with open('result/' + str(item) + '.json') as f:
            data = json.load(f)
        os.remove('result/' + str(item) + '.json')

        try:
            result = {"ingredient": data["description"],
                      "portion": '100g'}
            name = data["description"].replace(" ", "")
            name = name.replace(",", "_")
        except:
            result = {"ingredient": item,
                      "portion": '100g'}
            name = str(item)
            
        nu_info = {}
        for nutrient_info in data["foodNutrients"]:
            nutrient = nutrient_info['nutrient']
            if nutrient['id'] == 1004 or nutrient['id'] == 1253 or nutrient['id'] == 1093 or nutrient['id'] == 1092 or \
                    nutrient['id'] == 2039 or nutrient['id'] == 1079 or nutrient['id'] == 1003 or nutrient[
                'id'] == 2000:
                nu_info[nutrient['name']] = str(nutrient['rank'] / 100) + nutrient['unitName']
            if nutrient['id'] == 1106 or nutrient['id'] == 1162 or nutrient['id'] == 1087 or nutrient['id'] == 1089 or \
                    nutrient['id'] == 1165 or nutrient['id'] == 1167 or nutrient['id'] == 1175 or nutrient[
                'id'] == 1090 or nutrient['id'] == 1187:
                nu_info[nutrient['name']] = str(nutrient['rank'] / 100) + nutrient['unitName']
        result['nutrition'] = nu_info

        with open('result/' + name + '.json', 'w') as f:
            json.dump(result, f)


if __name__ == '__main__':
    main()
