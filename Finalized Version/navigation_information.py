from check_for_LARC import *
from Output import *

"""
All of the information along the course of navigation is stored and processed here
"""

class Navigation_Information:

    def __init__(self):
        self.dictionary_of_paths = {}
        self.counter_for_paths = 1
        self.current_path = []
        self.explored_path_numbers = []
        self.womens_health_sections = []
        self.womens_health_sections_links = []
        self.WomenRelatedSection_Flag = False
        self.LARC_present_flag = False
        self.path_to_LARC = []
        self.terms_found = []
        self.url_with_LARC = "-"
        self.num_of_clicks = "-"

    def get_current_path(self):
        for path_number, path in self.dictionary_of_paths.items():
            if path_number not in self.explored_path_numbers:
                self.explored_path_numbers.append(path_number)
                self.current_path = self.dictionary_of_paths[path_number]
                current_path_number = path_number
                break
        return self.current_path


    def update_dictionary_of_paths(self,url = None,spawn_length = None, found_linkTexts = None):
        path_now = []
        if spawn_length == None and found_linkTexts == None:
            path_now.append(url)
            self.dictionary_of_paths.update({self.counter_for_paths: path_now})
            print("The dictionary has been updated as follows")
            print(self.dictionary_of_paths)
            self.counter_for_paths = self.counter_for_paths + 1
        else:
            for i in range(spawn_length):
                for r in self.current_path:
                    path_now.append(r)
                if found_linkTexts[i] not in path_now:
                    path_now.append(found_linkTexts[i])

                    self.dictionary_of_paths.update({self.counter_for_paths: path_now})
                    self.counter_for_paths = self.counter_for_paths + 1
                    path_now = []
                else:
                    continue
        return self.dictionary_of_paths


    def find_womensHealthSections(self, womensHealth_Related_Vocab, found_linkHrefs, found_linkTexts):
        for i,k in enumerate(found_linkHrefs):
            for womenRelatedTerm in womensHealth_Related_Vocab:
                if womenRelatedTerm in found_linkTexts[i]:
                    self.WomenRelatedSection_Flag = True
                    if found_linkTexts[i] not in self.womens_health_sections:
                        self.womens_health_sections.append(found_linkTexts[i])
                        self.womens_health_sections_links.append(k)
        return self.WomenRelatedSection_Flag, self.womens_health_sections, self.womens_health_sections_links

    def check_for_LARC(self, content):
        flag_and_terms = check_unigrams_and_bigrams(content)
        self.LARC_present_flag = flag_and_terms[0][0]
        return flag_and_terms

    def generate_result(self, df, num, SHC_url, LARCflag, flag_and_terms, current_url, current_url_Text,content):
        if (LARCflag):

            self.path_to_LARC = self.get_path_to_LARC(current_url, current_url_Text)
            self.terms_found = self.get_LARCterms_found(flag_and_terms)
            self.num_of_clicks = self.get_num_clicks_to_LARC()
            self.url_with_LARC = current_url

            fields_to_write=[SHC_url, flag_and_terms[0][0], self.terms_found, self.num_of_clicks,
                                 self.path_to_LARC, self.url_with_LARC, self.WomenRelatedSection_Flag,
                                 self.womens_health_sections,
                                 self.womens_health_sections_links, content]

            Output.write_to_file(df, num, fields_to_write)

        else:

            fields_to_write = [SHC_url, flag_and_terms[0][0], self.terms_found, self.num_of_clicks,
                               self.path_to_LARC, self.url_with_LARC, self.WomenRelatedSection_Flag,
                               self.womens_health_sections,
                               self.womens_health_sections_links, content]

            Output.write_to_file(df, num, fields_to_write)



    def get_path_to_LARC(self,current_url, current_url_Text):
        got_path = False
        for k, v in self.dictionary_of_paths.items():
            temp_path = self.dictionary_of_paths[k]

            if (temp_path[-1] == current_url_Text):
                correct_path = temp_path
                print("key")
                print(k)
                break
            elif (temp_path[-1] == current_url):
                correct_path = temp_path
                print("key")
                print(k)
                break

        correct_unique_path = []
        for link_member in correct_path:
            if link_member not in correct_unique_path:
                correct_unique_path.append(link_member)
        print("Mention found in path {}".format(correct_unique_path))
        return correct_unique_path


    def get_LARCterms_found(self, flag_and_terms):
        terms_found_temp = []
        print("Terms found:")
        for n in range(len(flag_and_terms)):
            if (flag_and_terms[n][1]):
                print(flag_and_terms[n][1])
                if (flag_and_terms[n][2] == ""):
                    terms_found_temp.append(flag_and_terms[n][1])
            if (flag_and_terms[n][2]):
                print(flag_and_terms[n][2])
                term_found = flag_and_terms[n][1] + " " + flag_and_terms[n][2]
                terms_found_temp.append(term_found)

        for term in terms_found_temp:
            if term not in self.terms_found:
                self.terms_found.append(term)
        print("Terms found array:")
        print(self.terms_found)
        return self.terms_found


    def get_num_clicks_to_LARC(self):
        self.num_of_clicks = len(self.path_to_LARC) - 1
        if (len(self.path_to_LARC) - 1 == -1):
            self.num_of_clicks = "-"
        print("No of clicks: {}".format(self.num_of_clicks))
        return self.num_of_clicks
