from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
import csv
import pandas as pd
import numpy as np
from check_for_LARC import *
from Response_Code import *
from parse_content_selenium import *
import re
from selenium.common.exceptions import TimeoutException
from Output import *
from Extract import *
from queue_of_links import *
from navigation_information import *

vocab_for_findByPartialText = []
data_for_ExternalResources = []
data_for_generalExternalResources = []
data_for_specificallyWomensHealthRelatedResources = []
womensHealth_Related_Vocab = []

def read_text_file(textfile):
    text_file = open(textfile, "r")
    read_vocab = [line.strip("\n") for line in text_file]
    return read_vocab

womensHealth_related_vocab = read_text_file("WomensHealth_Related_Vocab.txt")
vocab_for_findByPartialText = read_text_file("vocab_for_findByPartialText.txt")

class Navigation:

    def __init__(self,root):
        self.root = root
        self.current_queue = []
        self.current_queue_text = []
        self.visited_queue = []
        self.dictionary = {}
        self.current_path = []
        self.terms_found = []
        self.get_html_with_Selenium = False
        self.scraping_attempted = False
        self.TimeOutException_flag = False
        self.LARCflag_and_terms = []
        self.LARC_found = False

    def explore_link(self, url):

        num_URLs_popped = 0
        print("Started out with the root url that is: {}".format(url))
        navigation_info = Navigation_Information()
        current_path_number = navigation_info.counter_for_paths
        # Start The counting for paths
        print("The count is")
        print(navigation_info.counter_for_paths)
        # create current queue
        queue = Queue_of_Links()
        # add the root url
        if url == self.root:
            queue.add_to_queue(url,"student health center url")
            print("root appended to queue.current_queue")
            print("current queue is : {}".format(queue.current_queue))
            dictionary = navigation_info.update_dictionary_of_paths(url)
            print(dictionary)

        while queue.current_queue:
            if num_URLs_popped>25:
                content = '-'
                navigation_info.generate_result(df, num, self.root, self.LARC_found, self.LARCflag_and_terms, current_url, current_url_Text,
                                                content)

                break
            else:
                current_path = navigation_info.get_current_path()
                print("num_URLs_popped(No of urls that have been popped until now)")#No of urls that have been popped until now
                print(num_URLs_popped)
                current_url, current_url_Text = queue.pop_from_queue()
                num_URLs_popped = num_URLs_popped + 1
                print("Current Url")
                print(current_url)
                print("has been popped")
                ExtractObject = Extract(driver, current_url)

                response_code = check_response_code(current_url)
                
                if (response_code == 1):
                    print("Exception while getting content with requests library")

                elif (response_code == 400) or (response_code == 401) or (response_code == 402) or (response_code == 403) or (response_code == 405) or (response_code == 406) or (response_code == 407) or (response_code == 408):
                    print("Error response code while while getting content with requests library")

                elif (response_code == 0):
                    print("Okay to get content with requests library")
                self.scraping_attempted = True

                content = ExtractObject.get_content()
                if content == 1:
                    print("Exception") #probably to many get requests to a website from same IP, and a timer or skip this URL or end the program
                    continue

                external_links = ExtractObject.get_ext_links()
                print("########printing all the external links#######")
                print(external_links)

                self.LARCflag_and_terms = navigation_info.check_for_LARC(content)
                self.LARC_found = self.LARCflag_and_terms[0][0]
                if self.LARC_found:
                    navigation_info.generate_result(df, num, self.root, self.LARC_found, self.LARCflag_and_terms, current_url, current_url_Text, content)
                    break

                else:
                    print("Exploring these links form the current page")# A mention of LARC was not found on the current page and it is now exploring all the links on the current page that could lead you to LARC resources
                    links = ExtractObject.get_links_byPartialText(vocab_for_findByPartialText)
                    print("This is the total no. of links got in url %s" % (current_url))
                    print(len(links))

                    found_linkTexts = []
                    found_linkHrefs = []
                    found_linkDict = {}

                    for link in links:
                        try:
                            link_valid = ExtractObject.check_link(link)
                            if link_valid == True:
                                if link.text not in found_linkTexts:
                                    found_linkTexts.append(link.text)
                                    found_linkHrefs.append(link.get_attribute("href"))
                                    found_linkDict[link.text] = link.get_attribute("href")
                        except:
                            continue
                    print("spawn_length(considers unique links)")

                    spawn_length = len(found_linkTexts)
                    print(spawn_length)
                    dictionary = navigation_info.update_dictionary_of_paths("_", spawn_length, found_linkTexts)
                    print("dictionary")
                    print(dictionary)

                    for i,k in enumerate(found_linkHrefs):
                        if k not in queue.current_queue:
                            queue.add_to_queue(k, found_linkTexts[i])

                    found_linkTexts = []
                    found_linkHrefs = []
                    found_linkDict = {}
                    links = []
                    print("queue.current_queue")
                    print(queue.current_queue)
                    print("queue.current_queue_text")
                    print(queue.current_queue_text)

        #Out of the bfs loop
        print("out of the loop")

        if(queue.current_queue == []):
            print("Nothing to write to file")
            current_url = '-'
            current_url_Text = '-'
            content = '-'
            navigation_info.generate_result(df, num, self.root, self.LARC_found, self.LARCflag_and_terms, current_url,
                                            current_url_Text,
                                            content)

        if self.TimeOutException_flag == True:
            if self.scraping_attempted == True:
                current_url = '-'
                current_url_Text = '-'
                content = '-'
                navigation_info.generate_result(df, num, self.root, self.LARC_found, self.LARCflag_and_terms, current_url, current_url_Text, content)

            else:
                current_url = '-'
                current_url_Text = '-'
                content = '-'
                print("Nothing to write to file")
                navigation_info.generate_result(df, num, self.root, self.LARC_found, self.LARCflag_and_terms,current_url, current_url_Text, content)


if __name__=='__main__':

    driver = webdriver.Chrome(executable_path=r"C:\Users\risha\Downloads\chromedriver_win32\chromedriver.exe")
    num = 0
    x = 1
    df = Output.create_df()
    url_file = open("input_file.txt", "r")

    for url in url_file:
            url = url.strip("\n")
            num = str(num)
            obj = "num" + num
            print(obj)
            obj = Navigation(url)
            obj.explore_link(url)
            num = int(num)
            num = num + 1

