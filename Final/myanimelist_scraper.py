import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys   
import requests
import pandas as pd
import numpy as np
import time

pd.set_option('display.max_columns', None)

def get_selenium():                           
    options = webdriver.ChromeOptions()                      
    driver = webdriver.Chrome(options=options)
    return (driver)

anime_dict = {}

def get_summaries(url):

    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    summary = soup.find_all("div", {"class" : "synopsis js-synopsis"})
    anime_id = soup.find_all("div", {"class" : "genres js-genre"}, id=True)
    
    for i, j in zip(anime_id, summary):
        anime_dict[i["id"]] = j.get_text().strip().replace('\n',' ').replace('\r', ' ')

base_url = "https://myanimelist.net/anime/genre/"
more_pages = True
for a in range(83):
    if a+1 in [9,49,12]: # not family friendly
        continue
    driver = get_selenium()
    genre_url = base_url + str(a+1)
    get_summaries(genre_url)
    time.sleep(2)
    page_index = 2
    screen_height = driver.execute_script("return window.screen.height;")
    driver.execute_script(f"window.scrollTo(0, {screen_height / 2});")
    while more_pages:
        try:
            driver.find_element(By.CSS_SELECTOR, "p.message")
            more_pages = False
        except:
            full_url = genre_url + "?page=" + str(page_index)
            get_summaries(full_url)
            page_index += 1
            full_url = genre_url
            time.sleep(2)
            screen_height = driver.execute_script("return window.screen.height;")
            driver.execute_script(f"window.scrollTo(0, {screen_height / 2});")
    full_url = base_url
    
anime_dataframe = pd.DataFrame.from_dict(anime_dict, orient='index')
anime_dataframe.to_csv("anime_summaries.csv",sep =';',index=True)


    
driver.quit()
