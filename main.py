from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging
from time import sleep
from datetime import datetime
import csv
import random

logging.getLogger().setLevel(logging.INFO)

logging.info('started')
web_driver = "/Users/nicolasfornasari/OneDrive/19_ALPHALABS/webdriver/chromedriver_mac"

username = 'user'
password = 'password'


class InstaUnfollowers:

    def __init__(self, username, password):

        self.chrome_options = Options()
        self.chrome_options.add_argument("--window-position=500,0")

        self.driver = webdriver.Chrome(web_driver, chrome_options=self.chrome_options)
        self.driver.get('https://instagram.com/')

        self.driver.maximize_window()
        sleep(2)

        username_type = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
        username_type.send_keys(username)

        password_type = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
        password_type.send_keys(password)

        submit = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]')
        submit.click()

        sleep(3)

        not_save_data = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button')
        not_save_data.click()

        sleep(3)

        not_turn_notifications = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]')
        not_turn_notifications.click()
        
        sleep(3)

    def get_unfollowers(self):

        self.driver.get('https://www.instagram.com/n_fornasari/')
        sleep(3)

        Followers = self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")
        Followers.click()
        followers = self.get_people()

        Following = self.driver.find_element_by_xpath("//a[contains(@href,'/following')]")
        Following.click()
        following = self.get_people()

        not_following_back = [user for user in following if user not in followers]

        with open(f'./not_following_back_{datetime.now().date()}.csv', 'w', newline='') as file:
            wr = csv.writer(file, quoting=csv.QUOTE_ALL)
            wr.writerow(not_following_back)

        print(not_following_back)

    def get_people(self):
        sleep(2)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")
        prev_height, height = 0, 1
        while prev_height != height:
            prev_height = height

            start = random.uniform(2, 5)
            stop = random.uniform(start, 8)
            sleep(random.uniform(start, stop))

            height = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight;
                """, scroll_box)

        print('loop ended')
        links = scroll_box.find_elements_by_tag_name('a')
        print('links loaded started with names')

        names = [name.text for name in links if name.text != '']

        print('finished with names')

        close = self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/div[2]/button')
        close.click()
        return names

    def find_user(self, user):
        search_bar = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
        search_bar.send_keys(user)

    def enter_user(self, user):
        # user_profile = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[4]/div/a[1]/div/div[1]')
        # user_profile.click()
        self.driver.get('https://www.instagram.com/' + user + '/')
        
    def follow_user(self):
        follow = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/div/div/button')
        follow.click()

    def unfollow_user(self):
        unfollow = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/div[2]/div/div[2]/div/span/span[1]/button')
        unfollow.click()
        confirm_unfollow = self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[1]')
        confirm_unfollow.click()

my_bot = InstaUnfollowers(username=username, password=password)