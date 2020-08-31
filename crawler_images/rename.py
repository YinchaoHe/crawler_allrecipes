import os
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", help="image folder name", type=str, default= 'rose', required=False)
    args = parser.parse_args()
    ingredient_type = args.name
    if 'multi' in ingredient_type:
        path = "images/" + ingredient_type
        filelist = os.listdir(path)
        for file in filelist:
            try:
                rename_multi_in(ingredient_type,file)
            except:
                print("No this folder")
    else:
        rename_sig_in(ingredient_type)

def rename_multi_in(ingredient_type, subtype):
    path= "images/" + ingredient_type +'/' + subtype
    name= subtype
    startNumber= '1'
    fileType= '.jpg'
    print("rename files as: "+name+startNumber+fileType)
    count=0
    filelist=os.listdir(path)
    for files in filelist:
        Olddir=os.path.join(path,files)
        if os.path.isdir(Olddir):
            continue
        Newdir=os.path.join(path,name+str(count+int(startNumber))+fileType)
        os.rename(Olddir,Newdir)
        count+=1
    print("Totally rename "+str(count)+" files")

def rename_sig_in(ingredient_type):
    path = "images/" + ingredient_type
    name = ingredient_type
    startNumber = '1'
    fileType = '.jpg'
    print("rename files as: "+name+startNumber+fileType)
    count=0
    filelist=os.listdir(path)
    for files in filelist:
        Olddir=os.path.join(path,files)
        if os.path.isdir(Olddir):
            continue
        Newdir=os.path.join(path,name+str(count+int(startNumber))+fileType)
        os.rename(Olddir,Newdir)
        count+=1
    print("Totally rename "+str(count)+" files")

if __name__ == '__main__':
    main()
