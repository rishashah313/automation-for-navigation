from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
from check_for_LARC import *
from parse_content import *

vocab_for_findByPartialText = []
data_for_knownExternalResources = []    

def load_vocab_for_findByPartialText():
    text_file = open("vocab_for_findByPartialText.txt","r")
    for line in text_file:
            term = line.strip("\n")
            vocab_for_findByPartialText.append(term)

def load_data_for_knownExternalResources():
    text_file = open("data_for_knownExternalResources.txt","r")
    for line in text_file:
            url = line.strip("\n")
            data_for_knownExternalResources.append(url)
    
def load_Data():
    load_vocab_for_findByPartialText()
    load_data_for_knownExternalResources()

class Navigation:
    def __init__(self,root):
        self.root = root
        self.current_queue = []
        self.current_queue_text = []
        self.dictionary = {}
        self.current_path = []
        self.terms_found = []
        self.all_external_resources_found = []
        self.all_pages_mentioning_external_resources = []
        self.dict_extResource_pageItWasFound = {}
        self.dict_extResource_pathToIt = {}
        self.dict_extResource_NoOfClicks= {}
        self.index_of_paths = {}
        self.destination_urls = []
        self.explored = []

    def check_if_parsing_allowed(self, url):
        content = get_text_from_html(url)
        if (content==1):
            return("Invalid")# Invalid content, parsing not allowed
        else:
            return(content)

    def check_keywords(self, content):
        
        flag_and_terms = []
        preprocessed_text = preprocess(content)
        flag_and_terms = match_unigrams_and_bigrams(preprocessed_text)
        return flag_and_terms
    
    def explore_link(self, url):
        
        array_explored = []
        terms_found_temp = []
        current_queue_tracking_no = 0
        external_resource_click = []
        external_resource_path = []
        print("I have started out with the root url that is:")
        print(url)
        path_now = []
        counter_for_paths = 1
        current_path_number = counter_for_paths
        print("The counting for paths has started")
        print("The count right now is")
        print(counter_for_paths)
        links = []
        value = []
        # create current queue
        # add the root url
        if url == self.root:
            self.current_queue.append(url)# root
            self.current_queue_text.append("student health center url")# root
            print("root appended to self.current_queue")
            print("current queue is : {}".format(self.current_queue))
            
            path_now = []
            path_now.append(url)
            self.dictionary.update({counter_for_paths:path_now })
            print("The dictionary has been updated as follows")
            print(self.dictionary)
            path_now = []
            current_path_number = 0
            
                        
            
            
        
        while self.current_queue:
            if(len(self.dictionary)>700):
                print("external_resource_path")
                print(external_resource_path)
                print("external_resource_click")
                print(external_resource_click)
                print("self.dict_extResource_pageItWasFound")
                print(self.dict_extResource_pageItWasFound)
                print("self.dict_extResource_pathToIt")
                print(self.dict_extResource_pathToIt)
                print("self.dict_extResource_NoOfClicks")
                print(self.dict_extResource_NoOfClicks)
                break
            else:
                
                #current_path_number = counter_for_paths
                for k, v in self.dictionary.items():
                    if k not in array_explored:
                        array_explored.append(k)
                        current_path = self.dictionary[k]
                        current_path_number = k
                        break
                        
                    
                
                #print("Entered the while current queue in bfs")
                print("The path no. is {}".format(current_path_number))
                #print("The length of current path is")
                ext_found = False
                external_links = []
                all_links = []
                print("current_queue_tracking_no")
                print(current_queue_tracking_no)
                current_url = self.current_queue.pop(0)
                current_url_Text = self.current_queue_text.pop(0)
                current_queue_tracking_no = current_queue_tracking_no + 1
                #array_explored.append(current_path_number)
                print("Current Url")
                print(current_url)
                print("has been popped")
                driver.get(current_url)
                ext_links = driver.find_elements_by_xpath("//a[@href]")
                for ext_link in ext_links:
                
                    all_links.append(ext_link.get_attribute("href"))
                for link in all_links:
                    if ".edu" not in link:
                    
                
                        external_links.append(link)
                print("########printing all the external links#######")
                print(external_links)
                for el in external_links:
                    for r in data_for_knownExternalResources:
                        if r in el:
                            print("***External Resource***")
                            print(el)
                            ext_found = True
                            if(ext_found):
                                
                                
                                for k,v in self.dictionary.items():
                                    print("here")
                                    temp_path_ext = self.dictionary[k]

                                    if(temp_path_ext[-1] == current_url):#(If the external resource is found on the home page i.e. the root SHC page)
                                        correct_path_ext = temp_path_ext
                                        correct_unique_path_ext = []
                                        for link_member in correct_path_ext:
                                            if link_member not in correct_unique_path_ext:
                                                correct_unique_path_ext.append(link_member)
                                        
                                        print("key")
                                        print(k)
                                        print("This path is getting appended")
                                        print(correct_unique_path_ext)
                                        if el not in self.dict_extResource_pageItWasFound.keys():
                                            self.dict_extResource_pageItWasFound[el] = [current_url]
                                        else:
                                            self.dict_extResource_pageItWasFound[el].append(current_url)
                                            
                                        if el not in self.dict_extResource_pathToIt.keys():
                                            self.dict_extResource_pathToIt[el] = [correct_unique_path_ext]
                                        else:
                                            self.dict_extResource_pathToIt[el].append(correct_unique_path_ext)
                                            
                                        if el not in self.dict_extResource_NoOfClicks.keys():
                                            self.dict_extResource_NoOfClicks[el] = [len(correct_unique_path_ext) - 1]
                                        else:
                                            self.dict_extResource_NoOfClicks[el].append(len(correct_unique_path_ext) - 1)
                                            
                                        
                                        if correct_unique_path_ext not in external_resource_path:
                                            
                                            external_resource_path.append(correct_unique_path_ext)
                                            external_resource_click.append(len(correct_unique_path_ext)-1)
                                            self.all_pages_mentioning_external_resources.append(current_url)
                                            print("all_pages_mentioning_external_resources")
                                            print(self.all_pages_mentioning_external_resources)
                                        break
                                        
                                        
                                    elif(temp_path_ext[-1] == current_url_Text):
                                        print("here again")
                                        correct_path_ext = temp_path_ext
                                        correct_unique_path_ext = []
                                        for link_member in correct_path_ext:
                                            if link_member not in correct_unique_path_ext:
                                                correct_unique_path_ext.append(link_member)
                                        print("key")
                                        print(k)
                                        print("This path is getting appended")
                                        print(correct_unique_path_ext)
                                        if el not in self.dict_extResource_pageItWasFound.keys():
                                            self.dict_extResource_pageItWasFound[el] = [current_url]
                                        else:
                                            self.dict_extResource_pageItWasFound[el].append(current_url)
                                            
                                        if el not in self.dict_extResource_pathToIt.keys():
                                            self.dict_extResource_pathToIt[el] = [correct_unique_path_ext]
                                        else:
                                            self.dict_extResource_pathToIt[el].append(correct_unique_path_ext)
                                            
                                        if el not in self.dict_extResource_NoOfClicks.keys():
                                            self.dict_extResource_NoOfClicks[el] = [len(correct_unique_path_ext) - 1]
                                        else:
                                            self.dict_extResource_NoOfClicks[el].append(len(correct_unique_path_ext) - 1)
                                        if correct_unique_path_ext not in external_resource_path:
                                            external_resource_path.append(correct_unique_path_ext)
                                            external_resource_click.append(len(correct_unique_path_ext)-1)
                                            self.all_pages_mentioning_external_resources.append(current_url)
                                            print("all_pages_mentioning_external_resources")
                                            print(self.all_pages_mentioning_external_resources)
                                        break
                external_links = []
                all_links = []
                

                content = self.check_if_parsing_allowed(current_url)
                if (content != "Invalid"):
                    
                    flag_and_terms = self.check_keywords(content)
                    print("flag_and_terms[0][0]")
                    print(flag_and_terms[0][0])
                    
                    if(flag_and_terms[0][0]):
                        
                            self.destination_urls.append(url)
                            #print("URLs with LARC")
                            #print(self.destination_urls)
                            got_path = False
                            for k,v in self.dictionary.items():
                                temp_path = self.dictionary[k]
                                 
                                if(temp_path[-1] == current_url_Text):
                                    correct_path = temp_path
                                    print("key")
                                    print(k)
                                    break
                                elif(temp_path[-1] == current_url):
                                    correct_path = temp_path
                                    print("key")
                                    print(k)
                                    break
                                   
                            correct_unique_path = []
                            for link_member in correct_path:
                                if link_member not in correct_unique_path:
                                    correct_unique_path.append(link_member)
                               
                        
                            print("Mention found in path {}".format(correct_unique_path))
                            print("Terms found:")
                            for n in range(len(flag_and_terms)):
                                if(flag_and_terms[n][1]):
                                    print(flag_and_terms[n][1])
                                    if (flag_and_terms[n][2] == ""):
                                        terms_found_temp.append(flag_and_terms[n][1])
                                if(flag_and_terms[n][2]):
                                    print(flag_and_terms[n][2])
                                    term_found = flag_and_terms[n][1] + " " + flag_and_terms[n][2]
                                    terms_found_temp.append(term_found)

                            for term in terms_found_temp:
                                if term not in self.terms_found:
                                    self.terms_found.append(term)
                            print("Terms found array:")
                            print(self.terms_found)
                            
                            print("No of clicks: {}" .format(len(correct_unique_path)-1))
                            flag_and_terms = []
                            self.destination_urls = []
                            print("external_resource_path")
                            print(external_resource_path)
                            print("external_resource_click")
                            print(external_resource_click)
                            print("self.dict_extResource_pageItWasFound")
                            print(self.dict_extResource_pageItWasFound)
                            print("self.dict_extResource_pathToIt")
                            print(self.dict_extResource_pathToIt)
                            print("self.dict_extResource_NoOfClicks")
                            print(self.dict_extResource_NoOfClicks)
                            break
                            
                    else:
                            print("I am exploring the links")
                            for partialText in vocab_for_findByPartialText:
                                links_found_by_partialText = driver.find_elements_by_partial_link_text(partialText)
                                if len(links_found_by_partialText) != 0:
                                    for link_found_by_partialText in links_found_by_partialText:
                                        links.append(link_found_by_partialText)
                                        print(link_found_by_partialText.get_attribute("href"))
                                        print(link_found_by_partialText.text)
                            
                            
                            print("This is the total no. of links got in url %s" % (current_url))
                            print(len(links))

                            found_linkTexts = []
                            found_linkHrefs = []
                            found_linkDict = {}
                            for link in links: 

            
                                try:
                                    
                                    #link.send_keys(Keys.CONTROL + Keys.RETURN)
                                    print(link.get_attribute("href"))
                                    
                                    print(link.text)
                                    
                                    if "mail" not in link.get_attribute("href") and ".pdf" not in link.get_attribute("href") and "javascript" not in link.get_attribute("href") and "facebook" not in link.get_attribute("href") and ".PDF" not in link.get_attribute("href"):
                                        if link.text not in found_linkTexts:
                                            found_linkTexts.append(link.text)
                                            found_linkHrefs.append(link.get_attribute("href"))
                                            found_linkDict[link.text] = link.get_attribute("href")
                                        
                                    
                                except:
                                    continue
                            print("spawn_length")
                            
                            spawn_length = len(found_linkTexts)
                            print(spawn_length)
                            for i in range(spawn_length):
                                for r in current_path:
                                    path_now.append(r)
                                if found_linkTexts[i] not in path_now:
                                    path_now.append(found_linkTexts[i])
                                    counter_for_paths = counter_for_paths + 1
                                    self.dictionary.update({counter_for_paths:path_now })
                                    path_now = []
                                else:
                                    continue

                            print("self.dictionary")
                            print(self.dictionary)
                            
                            for i,k in enumerate(found_linkHrefs):
                                if k not in self.current_queue:
                                
                                    self.current_queue.append(k)
                                    self.current_queue_text.append(found_linkTexts[i])
                      
                                
                            found_linkTexts = []
                            found_linkHrefs = []
                            found_linkDict = {}
                            links = []
                            
                                    
              
                            print("self.current_queue")
                            print(self.current_queue)
                            print("self.current_queue_text")
                            print(self.current_queue_text)
                        
                
                else:
                    print("The current url skipped from any action due to invalid parsing content")
                    print("self.current_queue")
                    print(self.current_queue)
        


if __name__=='__main__':
    load_Data() 
    driver = webdriver.Chrome(executable_path=r"C:\Users\risha\Downloads\chromedriver_win32\chromedriver.exe")
    num = 0
    x = 1
    url_file = open("check SHC.txt", "r")
    while(x == 1):
        
        for url in url_file:
            url = url.strip("\n")
            num = str(num)
            obj = "num" + num
            print(obj)
            obj = Navigation(url)
            obj.explore_link(url)
            num = int(num)
            num = num + 1
            x = int(input("Go on to next University? y/n 1/0 "))
