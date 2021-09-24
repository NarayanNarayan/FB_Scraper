import argparse
import time
import json
import csv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

with open('facebook_credentials.txt') as file:
    EMAIL = file.readline().split('"')[1]
    PASSWORD = file.readline().split('"')[1]





def _login(browser, email, password):
    browser.get("http://facebook.com")
    browser.maximize_window()
    browser.find_element_by_name("email").send_keys(email)
    browser.find_element_by_name("pass").send_keys(password)
    browser.find_element_by_name('login').click()
    time.sleep(5)

def _scroll(browser, infinite_scroll, lenOfPage):
    lastCount = -1
    match = False

    while not match:
        if infinite_scroll:
            lastCount = lenOfPage
        else:
            lastCount += 1

        # wait for the browser to load, this time can be changed slightly ~3 seconds with no difference, but 5 seems
        # to be stable enough
        time.sleep(5)

        if infinite_scroll:
            lenOfPage = browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return "
                "lenOfPage;")
        else:
            browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return "
                "lenOfPage;")

        if lastCount == lenOfPage:
            match = True


option = Options()
browser = webdriver.Chrome(executable_path="./chromedriver", options=option)


_login(browser, EMAIL, PASSWORD)

browser.get("https://www.facebook.com/DonaldTrump")
time.sleep(3)


_scroll(browser, False,10)

xpath='//span[@class="j83agx80 fv0vnmcu hpfvmrgz"]/span'
expand=browser.find_elements_by_xpath(xpath)




for expp in expand:
    action = webdriver.common.action_chains.ActionChains(browser)
    try:
        action.move_to_element_with_offset(expp, 2, 2)
        action.perform()
        expp.click()
        
    except:
        pass

time.sleep(10)

source_data = browser.page_source
bs_data = bs(source_data, 'html.parser')


scrollableTimeline = bs_data.find(class_="pwa15fzy",)
postss=scrollableTimeline.select("div.du4w35lb.k4urcfbm.sbcfpzgs")



postsjson=[]
def findcomments(xmls):
    comments = []
    comments_xmls = xmls.select("div.rj1gh0hx.buofh1pr.ni8dbmo4.stjgntxs.hv4rvrfc")
    for comment in comments_xmls:
        comments.append(comment.text)
    return comments
for post in postss:
    try:
        date=post.select("a.gmql0nx0.gpro0wi8.b1v8xokw")[0]['aria-label']
        post_text=post.find(attrs={"style":"text-align: start;"}).text
        comments=findcomments(post)
    except:
        break

    postsjson.append({"date":date,"text":post_text,"comments":comments})
print(len(postsjson))
with open('output.json', 'w') as file:
    json.dump(postsjson,file, indent=5)





