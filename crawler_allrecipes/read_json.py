import argparse
import json

#Delete recipes dictionaries which's name is 'No recipe'
def filter_recipe(start, end):
    index = start
    while index < end:  # index of the last file
        with open('report/original_recipes_info/' + str(index) + '_recipes_data.json', 'r') as f:
            data = json.load(f)
            with open('report/' + str(index) + '_recipes_data.json', 'a+', encoding='utf-8') as jsonfile:
                jsonfile.write('[')
                for i in range(0, len(data)):
                    if data[i]["name"] != 'No recipe':
                        json.dump(data[i], jsonfile, ensure_ascii=False)
                        jsonfile.write(',')
                jsonfile.write(']')
            index += 1

#integrate seperate files into one file
def integration(start, end, number):
    index = start
    amount = 0
    new_index = number
    while index <= end:  # index of the last file
        with open('report/' + str(new_index) + '_recipes_data.json', 'a+', encoding='utf-8') as jsonfile:
            if amount == 0:
                jsonfile.write('[')
            with open('report/original_recipes_info/' + str(index) + '_recipes_data.json', 'r') as f:
                data = json.load(f)
            for i in range(0, len(data)):
                if data[i]["name"] != 'No recipe':
                    json.dump(data[i], jsonfile, ensure_ascii=False)
                    jsonfile.write(',')
                    amount += 1
            index += 1
            if amount > 250:
                jsonfile.write(']')
                amount = 0
                new_index += 1
                continue

    if amount <= 250:
        with open('report/' + str(new_index) + '_recipes_data.json', 'a+', encoding='utf-8') as jsonfile:
            jsonfile.write(']')

#read json file
def reader(index):
    with open('report/original_recipes_info/' + str(index) + '_recipes_data.json', 'r') as f:
        data = json.load(f)
        for i in range(0, len(data)):
            print(data[i])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--function", help="choose a function that you want", type=str,
                        required=True)
    parser.add_argument("-s", "--start", help="the start index of recipe ID", type=int, default="1", required=False)
    parser.add_argument("-e", "--end", help="the end index of recipe ID", type=int, default="2", required=False)
    parser.add_argument("-i", "--index", help="the index of recipe json file", default="1", type=int, required=False)
    args = parser.parse_args()
    if args.function == "filt":
        filter_recipe(args.start, args.end)
    elif args.function == "integrate":
        integration(args.start, args.end, args.index)
    elif args.function == "read":
        for i in (args.start, args.end):
            print(i)
            reader(i)
    else:
        print("only three funtions: filt, integrate, read")
    #    print(i)
    #    reader(i)



if __name__ == '__main__':
    main()
