import scrapy
import re
import hashlib
import os

class PercelabSpider(scrapy.Spider):

    # Spider name
    name = 'percelab'
    
    # Websites to scan
    allowed_domains = ['usias.fr']
    start_urls = ['https://www.usias.fr/fellows/fellows-2021/']
    
    # Words to search for with corresponding weights
    words_to_search = {
        'transcriptomique' : 1,
        'transciptomic' : 1,
        'single cell' : 1,
        'cellule unique' : 1,
        'cellules uniques' : 1,
        'cellule individuelle' : 1,
        'cellules individulles' : 1,
        'single cell RNA' : 1,
        'scRNA' : 1,
        'cancer' : 1,
        'glioblastom' : 1,
        'machine learning' : 1,
        'apprentissage automatisé' : 1,
        'intelligence artificielle' : 1,
        'tSNE' : 1,
        'cNMF' : 1,
        'bioinformatique' : 1,
        'bio-informatique' : 1,
        'bioinformatic' : 1,
        'aptamère' : 1,
        'aptamer' : 1
    }
    
    # List of file formats used for url filtering
    file_formats = [
        '.png',
        '.jpg',
        '.jpeg',
        '.jfif',
        '.pjpeg',
        '.pjp',
        '.svg',
        '.pdf',
        '.docx',
        '.xlsx',
        '.xlsm',
        '.gif',
        '.webp',
        '.txt',
        '.doc',
        '.ppt',
        '.pptx'
    ]
    
    
    # Constructor of the spider
    def __init__(self, handle_dynamic_loading = 'f', url_needs_to_contain = '', *args,**kwargs):
    
        # Invoke parent constructor
        super(PercelabSpider, self).__init__(*args, **kwargs)
        
        # Init boolean to handle dynamic loading page
        self.handle_dynamic_loading = (handle_dynamic_loading == 'y' or handle_dynamic_loading == 'yes')
        
        # Init url filter parameters
        self.url_needs_to_contain = url_needs_to_contain
        
        # Init boolean checking if there is a url filter
        self.has_url_filter = (self.url_needs_to_contain != '')

    
    # Method called to process each request
    def parse(self, response):
        
        # Get new links to visit
        list_links = response.xpath('/html/body//a/@href').extract();
        list_filtered_formated_links = self.get_filtered_and_formated_links(response.request.url, list_links)
         
        # Calculate score of the page
        page_score = self.get_scan_score(response)
        
        # Add page to csv file
        self.write_score_to_csv(page_score, response.request.url)
        
        # Crawl to next page        
        for url in list_filtered_formated_links:
                yield scrapy.Request(url, callback=self.parse)
            
 
               
    # Get filtered and formated links from a list of links
    def get_filtered_and_formated_links(self, base_url, list_links):
        
        # List that will be returned
        list_filtered_formated_links = []
        
        # Url prefix regex pattern
        urlprefix_regex_pattern = 'https\:\/\/.*?\/'
        
        # Search of the pattern in the base url
        urlprefix_match = re.search(urlprefix_regex_pattern, base_url, re.IGNORECASE)
        
        # If found, get url prefix
        if urlprefix_match:
            url_prefix = urlprefix_match[0]
        # Else return empty list
        else:
            return []
        
        # Loop on list of entry links
        for link in list_links:

            # Filter url based on user argument
            if(self.has_url_filter and not self.url_needs_to_contain in link):
                pass
                
            # Filter url to pictures
            elif(any(pic_format in link for pic_format in PercelabSpider.file_formats)):
                pass
            
            # Case absolute url
            elif(link.startswith(url_prefix)):
                list_filtered_formated_links.append(link)
            
            # Case relative url starting with /
            elif(link.startswith('/')):
                list_filtered_formated_links.append(url_prefix[:-1] + link)
                
            # Case other https
            elif(link.startswith('http')):
                pass
                
            # Case other relative urls
            else:
                list_filtered_formated_links.append(url_prefix + link)
                
        # Return list
        return list_filtered_formated_links
        
        
    # Get score of the page
    def get_scan_score(self, response):
    
        # Score of the page
        score = 0
        
        # Text of the page
        page_text_content = ' '.join(response.xpath('//text()').extract())
        
        # All words in lowercase
        page_text_content = page_text_content.lower()
        
        # Loop on the pair of wanted words and their weights
        for word, weight in PercelabSpider.words_to_search.items():
        
            # The word is lowercased just in case
            word_lowercase = word.lower()
            
            # Number of occurences of the word
            nb_occ_word = page_text_content.count(word_lowercase)
            
            # Add to score
            score = score + ( nb_occ_word * weight )
            
        # Return score
        return score
        
        
    # Write score to csv file
    def write_score_to_csv(self, score, url):
        
        # Name of the file
        filename = 'output/list_url_scores_' + self.get_words_dict_hash() + '.csv'
        
        # Check if exist or create file
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Open file
        with open(filename, 'a+') as file:
        
            # Append line
            file.write(url + ';' + str(score) + '\n')
        
        
    # Get Hash from dictionnary of words of interest
    def get_words_dict_hash(self):
    
        # Variable containing all the dict in one string
        joined_dict = ''
    
        # Loop on the dictionnary
        for word, weight in PercelabSpider.words_to_search.items():
            joined_dict = joined_dict + word + str(weight)
        
        # Encode unicode character
        joined_dict = joined_dict.encode('utf-8')
        
        # Hash object
        hash_obj = hashlib.md5(joined_dict)
        
        # Return hash in hex
        return hash_obj.hexdigest()
                
    
    
