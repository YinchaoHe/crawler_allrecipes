import argparse
import os

from bing_scraper import bing_scraper
def crawler_images(args):
    response = bing_scraper.googleimagesdownload()
    url = "https://www.bing.com/images/search?q=" + args.keywords.replace(' ', "%20")
    arguments = {"url": url,
                 "limit": args.limit,
                 "chromedriver": args.chromedriver,
                 "image_directory": args.image_directory,
                 "download": 'download',
                 }
    response.download(arguments)

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

def main():
    try:
        path = os.getcwd() + "/images"
        os.mkdir(path)
    except:
        print("the images folder exists in the current directory.")
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--keywords", help="keywords for search, please no space", type=str, default= 'rose', required=False)
    parser.add_argument("-l", "--limit", help="the amount of images", type=int, default=20, required=False)
    parser.add_argument("-c", "--chromedriver", help="chromedriver", type=str, default="/Users/yinchaohe/Downloads/chromedriver", required=False)
    parser.add_argument("-d", "--image_directory", help="image_directory", type=str, default="rose", required=False)
    args = parser.parse_args()
    keywords = ['watermelon+fruit', 'raw+tilapia', 'tofu+block', 'tomatillo', 'tomato', 'raw+trout+fillet',
                'raw+turkey+breast+tenderloin', 'raw+turkey+ground', 'turnip+green', 'turnip+white', 'vegetable+oil+spread']
    for keyword in keywords:
        args.keywords =  keyword
        args.image_directory = keyword
        crawler_images(args)
        rename_sig_in(keyword)

if __name__ == '__main__':
    main()
