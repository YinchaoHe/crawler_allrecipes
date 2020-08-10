import json

#Delete recipes dictionaries which's name is 'No recipe'
def filter_recipe(start, end):
    index = start
    while index < end:  # index of the last file
        with open('report/' + str(index) + '_recipes_data.json', 'r') as f:
            data = json.load(f)
            with open('new_report/' + str(index) + '_recipes_data.json', 'a+', encoding='utf-8') as jsonfile:
                jsonfile.write('[')
                for i in range(0, len(data)):
                    if data[i]["name"] != 'No recipe':
                        json.dump(data[i], jsonfile, ensure_ascii=False)
                        jsonfile.write(',')
                jsonfile.write(']')
            index += 1

#integrate seperate files into one file
def integration(start, end):
    index = start
    amount = 0
    new_index = 20
    while index < end:  # index of the last file
        with open('new_report/' + str(new_index) + '_recipes_data.json', 'a+', encoding='utf-8') as jsonfile:
            if amount == 0:
                jsonfile.write('[')
            with open('report/' + str(index) + '_recipes_data.json', 'r') as f:
                data = json.load(f)
            for i in range(0, len(data)):
                if data[i]["name"] != 'No recipe':
                    json.dump(data[i], jsonfile, ensure_ascii=False)
                    jsonfile.write(',')
                    amount += 1
            index += 1
            if amount > 250:
                amount = 0
                new_index += 1
                jsonfile.write(']')
                continue

    if amount <= 250:
        with open('new_report/' + str(new_index) + '_recipes_data.json', 'a+', encoding='utf-8') as jsonfile:
            jsonfile.write(']')

#read json file
def reader(index):
    with open('report/' + str(index) + '_recipes_data.json', 'r') as f:
        data = json.load(f)
        for i in range(0, len(data)):
            print(data[i])


def main():
    #filter_recipe(1, 10)
    #integration(1, 10)
    reader(1)


if __name__ == '__main__':
    main()
