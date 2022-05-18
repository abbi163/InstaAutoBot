# Script for liking Story and Pictures 


# Necessary imports
import pandas as pd
import numpy as np
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import csv
import traceback
from datetime import date

# Class of operation !!

class InstagramBot:
    """
    Functions: 
        1. login
        2. profile
        3. accountPrivacy
        4. countPosts
        5. likePhotos
        6. likeStory
    
    """
    
    
    def __init__(self, user=None, pwd= None):
        self.username = user
        self.password = pwd
        self.bot = webdriver.Chrome(ChromeDriverManager(version="101.0.4951.41").install())
        
        
    def login(self):
        bot = self.bot
        bot.get('https://www.instagram.com/accounts/login/')
        time.sleep(3)
        email = bot.find_element_by_name('username').send_keys(self.username)
        password = bot.find_element_by_name('password').send_keys(self.password + Keys.RETURN)

        time.sleep(3)
      
    def profile(self, user):
        ''' '''
        time.sleep(3)
        bot = self.bot
        bot.get('https://www.instagram.com/{}'.format(user))
        time.sleep(3)
               
    def accountPrivacy(self):
        ''' Returns True if account is private, else False. '''
        bot = self.bot
        
        try:
            privacy_text = bot.find_element(By.XPATH,"//h2 [@class='rkEop']").text
            if privacy_text == "This account is private":
                return True
            else:
                return False
        except NoSuchElementException:
            return False

    def countPosts(self):
        '''returns the posts count in text form. '''
        bot = self.bot
        try:
            # suppose the username doesnot exits then try and exist will handle the case with non existant user return 0.
            posts = bot.find_element(By.XPATH,"//span[@class='g47SY ']").text
            return posts
        
        except NoSuchElementException:
            return '0'
        
    def likePhotos(self,amount = 3):
        ''' This program likes the picture'''
        bot = self.bot
        try:
            bot.find_element_by_class_name('v1Nh3').click()

            i = 1
            while i <= amount:
                time.sleep(4 + np.random.randint(1,6))
                
                # for liking picture
                bot.find_element_by_class_name('fr66n').click()
                time.sleep(1 + np.random.randint(2, 5))
                
                # for clicking next picture 
                bot.find_element(By.XPATH,"//button [@class='wpO6b  ']//*[@aria-label='Next']" ).click()
                time.sleep(1 + np.random.randint(3,5))
                i += 1
            return 0
        
        except NoSuchElementException:
            return print("Error Found ")
    
    def likeStory(self):
        """
        Open story, Likes Story and then close the story
        """

        bot = self.bot
        try:
            # Open Story !!
            bot.find_element_by_class_name("RR-M- ").click()
            
            time.sleep(2)

            # Like story !
            bot.find_element(By.XPATH,"//div [@class='EgD-3']").click()
            
            time.sleep(1)
            # Close Story !
            bot.find_element_by_class_name("aUIsh").click()

        except NoSuchElementException:
            pass



                            
                            
                            
# Running the whole program !!

# user name and password
user = "nisha.anand.180625"
pwd = "ayansh1611"

# dataframe reading
df =pd.read_csv("data/UserList.csv")

# running the program
insta = InstagramBot(user=user, pwd=pwd)
insta.login()

count = 0
for index in df.index:
    user = df.loc[index, "users"]
    interaction_status = df.loc[index, 'interaction_status']
    if interaction_status == 0:
        insta.profile(user)
        privacy = insta.accountPrivacy()
        df.loc[index, 'interaction_status'] = 1
        if privacy == False:
            post_count = insta.countPosts()
            if post_count not in ["0", "1", "2", "3"]:
                insta.likeStory()
                insta.likePhotos()
                df.loc[index, "pic_like_status"] = True
                df.loc[index, 'pic_like_date'] = date.today()
                # saving the data back to csv 
                df.to_csv("data/UserList.csv", index=None)
                count+=1
                print(count)
                if count>150:
                    break;