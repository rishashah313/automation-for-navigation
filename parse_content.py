from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
import requests
def get_text_from_html(url):
    
    try:
            page = requests.get(url)        #to extract page from website
            html_code = page.content        #to extract html code from page
    except Exception as e:
            print(e)
            return(1)
            
    try:
            soup = BeautifulSoup(html_code, 'html.parser')  #Parse html code
    
            texts = soup.findAll(text=True)                 #find all text
                  
            text_from_html = ' '.join(texts)                   #join all text
            text_extracted = text_from_html.encode("utf-8") 
            text_extracted = str(text_extracted)
            words_tokenized = word_tokenize(text_extracted)
            return words_tokenized
                  
     
    except Exception as e:
            print(e)
            return(1)
    
