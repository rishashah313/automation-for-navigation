
from selenium import webdriver
from bs4 import BeautifulSoup

"""
Queue of urls for the bfs approach to find the shortest path to LARC
"""

class Queue_of_Links:

    def __init__(self):
        self.current_queue = []
        self.current_queue_text = []

    def add_to_queue(self, link, link_text):
        self.current_queue.append(link)
        self.current_queue_text.append(link_text)

    def pop_from_queue(self):
        current_url = self.current_queue.pop(0)
        current_url_Text = self.current_queue_text.pop(0)
        return current_url, current_url_Text




