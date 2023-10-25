import time
from playwright.sync_api import sync_playwright
import json, os, re
import search_tool.google_sheets as g
import sys
sys.path.append(r"")
import consts as c
import re



class Browser_start:
    def __init__(self):
        pass
        
    def parse(self,search):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            self.context = browser.new_context(locale='en-US',)
            self.page = self.context.new_page()
            self.check_cookies = os.path.exists("./search_tool/cookies.json")
            if self.check_cookies == True:
                Browser_start.load_cookies(self)
            try:
                self.page.goto("https://www.linkedin.com")
            except:
                print("On VPN for connect") 
            self.page.wait_for_load_state("load")
            time.sleep(1)
            self.page.reload()
            self.page.wait_for_load_state("load")
            if self.check_cookies == False:
                Browser_start.loger(self)
            g.connect_google_sheet()
            while c.NUM_SEARCH >= c.NUM_LINE:
                g.search_profile()
                Search_linkedIn.search(self)
                c.NUM_LINE+=1
            Browser_start.save_cookies(self)
            search = False
            return search
          
    def save_cookies(self):  
        with open("./search_tool/cookies.json", "w") as f:
            f.write(json.dumps(self.context.cookies()))

    def load_cookies(self):
        with open("./search_tool/cookies.json", "r") as f:
            try:
                cookies = json.loads(f.read())
                self.context.add_cookies(cookies)
            except:
                pass
            
    
    def loger(self):
        try:
            if self.page.query_selector("a[class='nav__button-secondary btn-md btn-secondary-emphasis']").text_content().strip() == "Sign in":
                time.sleep(2)
                self.page.query_selector("a[class='nav__button-secondary btn-md btn-secondary-emphasis']").click()
                self.page.get_by_label("Email or Phone").fill(c.USERNAME)
                self.page.get_by_label("Password").fill(c.PASSWORD)
                self.page.query_selector("div[class='login__form_action_container ']").click()
                self.page.wait_for_load_state("load")
                time.sleep(20)
        except:
            pass
        

class Search_linkedIn(Browser_start):
    def search(self):
        self.page.get_by_role("combobox").fill(c.FIRST_NAME +" "+ c.LAST_NAME)
        self.page.keyboard.press('Enter')
        self.page.wait_for_load_state("load")
        time.sleep(2)
        search_result_one = self.page.query_selector_all("ul[class='reusable-search__entity-result-list list-style-none']")
        for search_result in search_result_one:
            search_result_lst = search_result.query_selector_all("li[class='reusable-search__result-container']")
            try:
                if len(search_result_lst)!=0:
                    for member in search_result_lst:
                        info_member = member.text_content().lower()
                        c.COMPANY.lower()
                        if info_member.find(c.COMPANY) is True:
                            url = member.query_selector("a[class='app-aware-link  scale-down ']").get_attribute('href')
                            g.add_link(url)
                            break
                else:
                    url = search_result.query_selector("a[class='app-aware-link  scale-down ']").get_attribute('href')
                    g.add_link(url)
                    break
            except:
                pass
