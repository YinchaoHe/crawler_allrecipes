# Crawler_images
This web images crawler can only scape images from Bing.com .

## Description
- bing_scraper: this is a third-part labriary, which is maintained by Hardik Vasa, https://github.com/hardikvasa/google-images-download
- example_images: there are some example output images in the folder.
- crawler_images.py: this is the core program to crawl images from Bing.com .
- rename.py: the script is used to rename images because scraped images' name is random.

## Prerequisites
- Chrome browser
- Chromedriver
- Module: request

## Usage
- This is the command line to run crawler:
	* ` python crawler_images.py -k <image_keyword> -l <image_amount> -d <image_directory> -c <chromedriver_path>`

- This is the command line to run rename script:
	* `python rename.py -n <image_folder_name>`


# Cite
See https://github.com/hardikvasa/google-images-download
