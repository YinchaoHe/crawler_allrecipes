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

def main():
    try:
        path = os.getcwd() + "/images"
        os.mkdir(path)
    except:
        print("the images folder exists in the current directory.")
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--keywords", help="keywords for search, please no space", type=str, required=True)
    parser.add_argument("-l", "--limit", help="the amount of images", type=int, required=True)
    parser.add_argument("-c", "--chromedriver", help="chromedriver", type=str, default="/Users/yinchaohe/Downloads/chromedriver", required=False)
    parser.add_argument("-d", "--image_directory", help="image_directory", type=str, default="rose", required=True)
    args = parser.parse_args()
    crawler_images(args)
    
if __name__ == '__main__':
    main()