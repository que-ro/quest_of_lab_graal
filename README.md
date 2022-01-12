# quest_of_lab_graal
Spider chivalries that will travel your desired website and search for keywords you are looking for

# How to install it

1 - Make sure you installed python. If not you can follow instructions on this website: https://medium.com/co-learning-lounge/how-to-download-install-python-on-windows-2021-44a707994013
(Program tested with Python 3.8)

2 - Download the scrapy package: In a command line prompt execute: pip install scrapy

3 - Download the selenium package: In a command line prompt execute: pip install selenium

4 - Download the zip of the project at https://github.com/que-ro/quest_of_lab_graal. Click on Code -> Download ZIP

5 - Extract the project

# How to use it
You first need to modify the percelab.py file
To do that, a text editor is sufficient (Notepad++)

1 - Change the start_urls list and fill it with your websites:
start_urls = ['https://www.thesiteIwantToScan.com/', 'https://www.anotherSiteIwantToScan.com/withAMorePreciseStartingUrl/']
!Important! Make sure the urls have a '/' at the end. It is needed for the crawling process

2 - Change the allowed_domains list:
allowed_domains = ['thesiteIwantToScan.com', 'anotherSiteIwantToScan.com']

3 - Change the words_to_search list with your desired words and associate a weight to them
words_to_search = {
        'aWord' : 1,
		'anotherWord' : 1,
        'aMoreImportantWord' : 5,
        'theMostImportantWord' : 10
    }

4 - Open a commande line prompt and navigate to the quest_of_lab_graal folder containing the python scripts.

5 - Execute the command: scrapy crawl percelab

You can add options: 
handle_dynamic_loading=yes or handle_dynamic_loading=y: Will allow the scan of web dynamic loading page, such as page containing list that load when you scroll to the bottom of it.
url_needs_to_contain=thisChainOfCharacters: Will force the spider to only crawl urls containing the chain of characters.

Command line example: scrapy crawl percelab - a handle_dynamic_loading=yes -a url_needs_to_contain=thisChainOfCharacters

6 - Wait until the crawling process has ended and check the result in the output folder.

# Customize
- Handle dynamic loading page: 
Using the feature handle_dynamic_loading will use a webdriver that can wait the loading of a page and scroll to the bottom of a dynamic loading page.
Each loading has a waiting time. This waiting time can be customized in the webutilities.py file. Just change waiting_time_for_dynamic_loading_content to the desired amount of seconds.
The parameter is set at 2s by default.

- Visualize the process:
If you use the handle dynamic loading page feature and you want the bot in action you can do it:
Go to the webutilities.py and comment "chrome_options.add_argument("--headless")" by adding a #.

# Common errors 
Code errors   Description
0001          The chromedriver doesn't support the chrome version you have installed on your computer. Check the chrome version you have and find the adequate webdriver on
              https://chromedriver.chromium.org/downloads. Once downloaded, replace the current driver in the folder webdrivers of the project.