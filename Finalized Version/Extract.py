"""
Extract information from the webpages
"""

from selenium import webdriver
from bs4 import BeautifulSoup
from bs4.element import Comment
import re
from selenium.common.exceptions import TimeoutException



omit_list = ["mail",".pdf",".PDF","javascript","facebook","paws","mp4","mov"]
class Extract:

    def __init__(self, driver, current_url):

        self.all_links = []
        self.external_links = []
        self.driverObject = driver
        self.current_url = current_url
        try:
            self.driverObject.get(self.current_url)
        except TimeoutException as e:
            print("TimeoutException while trying to get url")
            self.TimeOutException_flag = True

    @staticmethod
    def get_visible_tags(element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def get_all_links(self):
        try:
            links = self.driverObject.find_elements_by_xpath("//a[@href]")
            for link in links:
                self.all_links.append(link.get_attribute("href"))
        except:
            print("except")

        return self.all_links

    def get_ext_links(self):
        links = self.get_all_links()
        for link in links:
            if ".edu" not in link:
                self.external_links.append(link)
        return self.external_links


    def get_content(self):
        content = ''
        try:
            html = self.driverObject.page_source
        except Exception as e:
            print(e)
            print("Exception while getting content with selenium")
            return 1
        try:
            soup = BeautifulSoup(html, 'html.parser')  # Parse html code
            texts = soup.findAll(text=True)  # find all text
            visible_texts = filter(Extract.get_visible_tags, texts)
            content = u" ".join(t.strip() for t in visible_texts)
            content = content.encode("utf-8")
            content = str(content)
        except Exception as e:
            print(e)
            print("Exception while parsing content")
        return content

    def get_links_byPartialText(self, vocab_for_findByPartialText):
        links = []
        for partialText in vocab_for_findByPartialText:
            links_found_by_partialText = self.driverObject.find_elements_by_partial_link_text(partialText)
            if len(links_found_by_partialText) != 0:
                for link_found_by_partialText in links_found_by_partialText:
                    links.append(link_found_by_partialText)
                    print(link_found_by_partialText.text)
                    print(link_found_by_partialText.get_attribute("href"))
        return links


    def check_link(self, link):
        valid_link_Bool = False
        for string in omit_list:
            if string not in link.get_attribute("href"): # this is prevent invalid results
                if ".edu" in link.get_attribute("href"): # this is to prevent external resources from getting in the queues
                    valid_link_Bool = True

        return valid_link_Bool