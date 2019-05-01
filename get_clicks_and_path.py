from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
from check_for_LARC import *
from parse_content import *



class Navigation:
    def __init__(self,root):
        self.root = root
        self.current_queue = []
        self.current_queue_text = []
        self.dictionary = {}
        self.current_path = []
        self.terms_found = []
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
        
        
        preprocessed_text = preprocess(content)
        flag_and_terms = match_unigrams_and_bigrams(preprocessed_text)
        return flag_and_terms[0]# return the flag whether found or not

    

    def explore_link(self, url):

        array_explored = []
        current_queue_tracking_no = 0
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
            #"path"+str(counter_for_paths)
            path_now = []
            path_now.append(url)
            self.dictionary.update({counter_for_paths:path_now })
            print("The dictionary has been updated as follows")
            print(self.dictionary)
            path_now = []
            
                        
            
            

        while self.current_queue:
            #current_path_number = counter_for_paths
            for k, v in self.dictionary.items():
                if k not in array_explored:
                    array_explored.append(k)
                    current_path = self.dictionary[k]
                    current_path_number = k
                    break
                    
                
            
            #print("Entered the while current queue in bfs")
            print("The path no. is {}".format(current_path_number))
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

            content = self.check_if_parsing_allowed(current_url)
            if (content != "Invalid"):
            
                found = self.check_keywords(content)
                
                if(found):
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
                            
                                
                            
                        
                        print("Mention found in path {}".format(correct_path))
                        print(correct_path)
                        print("No of clicks: {}" .format(len(correct_path)-1))
                        
                        self.destination_urls = []
                        break
                        
                else:
                        print("I am exploring the links")
                        links1 = driver.find_elements_by_partial_link_text("Services")
                        links2 = driver.find_elements_by_partial_link_text("Clinic")
                        links3 = driver.find_elements_by_partial_link_text("Women")
                        links4 = driver.find_elements_by_partial_link_text("Health")
                        links5 = driver.find_elements_by_partial_link_text("Birth")
                        links6 = driver.find_elements_by_partial_link_text("Resources")
                        links7 = driver.find_elements_by_partial_link_text("Links")
                        links8 = driver.find_elements_by_partial_link_text("Online")
                        links9 = driver.find_elements_by_partial_link_text("Contraception")
                        links10 = driver.find_elements_by_partial_link_text("SERVICES")
                        links11 = driver.find_elements_by_partial_link_text("Medical")
                        links12 = driver.find_elements_by_partial_link_text("Sex")
                        links13 = driver.find_elements_by_partial_link_text("Care")
                        links14 = driver.find_elements_by_partial_link_text("Birth Control")
                        links15 = driver.find_elements_by_partial_link_text("Contraceptive")

                        if len(links1) != 0:
                            for l1 in links1:
                                links.append(l1)
                                print(l1.get_attribute("href"))
                                
                                print(l1.text)
                                
                        if len(links2) != 0:
                            for l2 in links2:
                                links.append(l2)
                                print(l2.get_attribute("href"))
                                
                                print(l2.text)

                        if len(links3) != 0:
                            for l3 in links3:
                                links.append(l3)
                                print(l3.get_attribute("href"))
                                
                                print(l3.text)

                        if len(links4) != 0:
                            for l4 in links4:
                                links.append(l4)
                                print(l4.get_attribute("href"))
                                
                                print(l4.text)
                                
                        if len(links5) != 0:
                            for l5 in links5:
                                links.append(l5)
                                print(l5.get_attribute("href"))
                                
                                print(l5.text)
                                
                        if len(links6) != 0:
                            for l6 in links6:
                                links.append(l6)
                                print(l6.get_attribute("href"))
                                
                                print(l6.text)
                                
                        if len(links7) != 0:
                            for l7 in links7:
                                links.append(l7)
                                print(l7.get_attribute("href"))
                                
                                print(l7.text)
                                
                        if len(links8) != 0:
                            for l8 in links8:
                                links.append(l8)
                                print(l8.get_attribute("href"))
                                
                                print(l8.text)

                        if len(links9) != 0:
                            for l9 in links9:
                                links.append(l9)
                                print(l9.get_attribute("href"))
                                
                                print(l9.text)

                        if len(links10) != 0:
                            for l10 in links10:
                                links.append(l10)
                                print(l10.get_attribute("href"))
                                
                                print(l10.text)

                        if len(links11) != 0:
                            for l11 in links11:
                                links.append(l11)
                                print(l11.get_attribute("href"))
                                
                                print(l11.text)

                        if len(links12) != 0:
                            for l12 in links12:
                                links.append(l12)
                                print(l12.get_attribute("href"))
                                
                                print(l12.text)

                        if len(links13) != 0:
                            for l13 in links13:
                                links.append(l13)
                                print(l13.get_attribute("href"))
                                
                                print(l13.text)

                        if len(links14) != 0:
                            for l14 in links14:
                                links.append(l14)
                                print(l14.get_attribute("href"))
                                
                                print(l14.text)

                        if len(links15) != 0:
                            for l15 in links15:
                                links.append(l15)
                                print(l15.get_attribute("href"))
                                
                                print(l15.text)

                        print("This is the total no. of links got in url %s" % (current_url))
                        print(len(links))

                        found_linkTexts = []
                        found_linkHrefs = []
                        found_linkDict = {}
                        for link in links: 

        
                            try:
                                
                                #link.send_keys(Keys.CONTROL + Keys.RETURN)
                                print(link.get_attribute("href"))
                                #print("before link text")
                                print(link.text)
                                #print("after link text")
                                if "mail" not in link.get_attribute("href") and ".pdf" not in link.get_attribute("href") and "facebook" not in link.get_attribute("href") and ".PDF" not in link.get_attribute("href"):
                                    if link.text not in found_linkTexts:
                                        found_linkTexts.append(link.text)
                                        found_linkHrefs.append(link.get_attribute("href"))
                                        found_linkDict[link.text] = link.get_attribute("href")
                                    
                                '''
                                if link.get_attribute("href") not in self.current_queue:
                                    
                                    self.current_queue.append(link.get_attribute("href"))
                                    
                                '''
                                
                                
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

                        """
                        for k in found_linkHrefs:
                            if k not in self.current_queue:
                            
                                self.current_queue.append(k)
                        """                        
                            
                        found_linkTexts = []
                        found_linkHrefs = []
                        found_linkDict = {}
                        links = []
                        links1 = []
                        links2 = []
                        links3 = []
                        links4 = []
                        links5 = []
                        links6 = []
                        links7 = []
                        links8 = []
                        links9 = []
                        links10 = []
                        links11 = []
                        links12 = []
                        links13 = []
                        links14 = []
                        links15 = []
                        
                                

                        
                        print("self.current_queue")
                        print(self.current_queue)
                        print("self.current_queue_text")
                        print(self.current_queue_text)
                    
            
            else:
                print("The current url skipped from any action due to invalid parsing content")
                print("self.current_queue")
                print(self.current_queue)
    


if __name__=='__main__':
    driver = webdriver.Chrome(executable_path=r"C:\Users\risha\Downloads\chromedriver_win32\chromedriver.exe")
    num = 0
    x = 1
    url_file = open("text_file.txt", "r")
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
