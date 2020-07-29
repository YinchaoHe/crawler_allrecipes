# Crawler_allrecipes
This web crawler is only used for https://www.allrecipes.com/ .

## Description
- report_example: there are some example output files in the folder, such as images and recipes' information.
- batch_process.sh: this is a shell script program to run the python program in a batch. Because you want to crawl a huge recipes amount, it will cause `No space left on device (ERROR 28)`.
- crawler.py: this is the core program to crawl information from the websites.

## How to use the code 
- If the recipes' amount you want to crawl is small, like less than 3000, I recommend you to use this command:
	* `python crawler.py -s [the recipe_ID that you want to begin] -e [the recipe_ID that you want to stop]`
- If the recipes' amount you want to crawl is huge, like greater than 3000, I recommend you to use this command:
	* `sh batch_process.sh`
