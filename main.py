from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *
import time

i=0
def parse(x):
    global i
    print("got em ",i*10+1)
    i+=1


def main():
    o=Options()
    #o.add_argument("--headless")
    d=webdriver.Chrome(options=o)
    d.implicitly_wait(5)
    d.get("https://minesweeper.online/best-players")
    time.sleep(1)
    d.find_element(By.ID,"show_all").click()
    
    while 1:
        try:
            s=d.find_element(By.ID,"stat_table_body").get_attribute("innerHTML")
            d.find_element(By.LINK_TEXT,">").click()
            parse(s)
        except StaleElementReferenceException:
            pass


if __name__=="__main__":
    main()