def main():
    with open('veg_subclasses.txt') as f:
        content = f.readlines()
    veg_subclasses_content = [x.strip() for x in content]

    with open('fru_subclasses.txt') as f:
        content = f.readlines()

    fru_subclasses_content = [x.strip() for x in content]

    with open('zeynep_list.txt') as f:
        content = f.readlines()

    zeynep_content = [x.strip().split(',')[0] for x in content]
    zeynepclass_content = sorted(set(zeynep_content), key=zeynep_content.index)

    food_list = {}
    for zeynepclass in zeynepclass_content:
        food_list[zeynepclass] = {}

    for zeynepclass in zeynepclass_content:
        subclass = []
        for zeynep in zeynep_content:
            if zeynepclass in zeynep:
                subclass.append(zeynepclass)
        food_list[zeynepclass]['zeynepz_list'] = subclass

    for zeynepclass in zeynepclass_content:
        subclass = []
        for veg_subclass in veg_subclasses_content:
            if zeynepclass in veg_subclass:
                subclass.append(veg_subclass)
        food_list[zeynepclass]['database_list'] = subclass

    for zeynepclass in zeynepclass_content:
        subclass = []
        for fru_subclass in fru_subclasses_content:
            if zeynepclass in fru_subclass:
                subclass.append(fru_subclass)
        food_list[zeynepclass]['database_list'] = subclass

    print(food_list)
    # for subclass in veg_subclasses_content:
    #     for zeynep in zeynep_content:
    #         if subclass in zeynep:

    #             print(subclass)
    #             print(zeynep)
    #             print()



if __name__ == '__main__':
    main()