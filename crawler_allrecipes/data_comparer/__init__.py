import json


def main():
    with open('veg_subclasses.txt') as f:
        content = f.readlines()
    veg_subclasses_content = [x.strip() for x in content]

    with open('fru_subclasses.txt') as f:
        content = f.readlines()

    fru_subclasses_content = [x.strip() for x in content]

    with open('zeynep_list.txt') as f:
        content = f.readlines()

    zeyneplist_content = [x.strip() for x in content]
    zeynep_content = [x.strip().split(',')[0] for x in content]
    zeynepclass_content = sorted(set(zeynep_content), key=zeynep_content.index)
    totla_amount = len(zeynepclass_content)
    same_amount = 0

    food_list = {}
    for zeynepclass in zeynepclass_content:
        food_list[zeynepclass] = {}

    for zeynepclass in zeynepclass_content:
        subclass = []
        for zeynep in zeyneplist_content:
            if zeynepclass in zeynep:
                subclass.append(zeynep)
        food_list[zeynepclass]['zeynepz_list'] = subclass

    for zeynepclass in zeynepclass_content:
        veg = []
        for veg_subclass in veg_subclasses_content:
            if zeynepclass in veg_subclass:
                veg.append(veg_subclass)
        food_list[zeynepclass]['database_list'] = veg


    for zeynepclass in zeynepclass_content:
        subclass = []
        for fru_subclass in fru_subclasses_content:
            if zeynepclass in fru_subclass:
                subclass.append(fru_subclass)
                food_list[zeynepclass]['database_list'] = subclass

    for key in food_list.keys():
        if len(food_list[key]['database_list']) != 0:
            same_amount += 1
    similarity = 100 * same_amount/totla_amount
    report = "The similarity is about: " + str(similarity) + " %"

    with open('foodlist.json', 'w') as outfile:
        json.dump(food_list, outfile)
    print(report)




if __name__ == '__main__':
    main()