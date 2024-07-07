from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *
import time, os, re, requests
import zapisovanje


seja=requests.Session()
format_string=(".*?"
        "<h2>.*?alt=\"(.*?)\".*?"   #drzava
        "<span>(.*?)</span>.*?"    #ime
        "(\d*?)<i class=\"fa fa-trophy score-icon.*?"   #pokali
        "time-icon  level1\"></i>(\d*?)</a>.*?"   #cas 1
        "time-icon  level2\"></i>(\d*?)</a>.*?"   #cas 2
        "time-icon  level3\"></i>(\d*?)</a>.*?"   #cas 3
        "eff-icon level1\"></i>(\d*?)%.*?"   #eff 1
        "eff-icon level2\"></i>(\d*?)%.*?"   #eff 1
        "eff-icon level3\"></i>(\d*?)%.*?"   #eff 1
        "([0-9 ]*?)<img src=\"/img/other/xp.svg\".*?"   #exp
        "mastery1\"></i>(\d*?)</a>.*?"   #eff 1
        "mastery2\"></i>(\d*?)</a>.*?"   #eff 2
        "mastery3\"></i>(\d*?)</a>.*?"   #eff 3
        "ws1\"></i>(\d*?)</a>.*?"   #win streak 1
        "ws2\"></i>(\d*?)</a>.*?"   #win streak 2
        "ws3\"></i>(\d*?)</a>.*?"   #win streak 3
        "end\d\"></i>(.*?)</a>.*?"   #endurance
        "wins-icon \"></i>([0-9 ]*?)</div>.*?"   #zmage
        )

def naberi_podatke_igralca(k):
    global seja, format_string
    
    for i in range(3):
        try:
            return re.search(format_string,seja.get("https://minesweeper.online/player/"+str(k),timeout=1).text).groups()
        except Exception:
            pass


def naberi_kljuce(n):
    o=Options()
    #o.add_argument("--headless")
    d=webdriver.Chrome(options=o)
    d.implicitly_wait(5)
    d.get("https://minesweeper.online/best-players")
    time.sleep(1)
    #d.find_element(By.ID,"show_all").click()

    if os.path.exists("kljuci.txt"):
        os.remove("kljuci.txt")
    f=open("kljuci.txt","a")
    
    s=time.time()

    for i in range(1,n//10+1):
        while 1:
            try:
                s=d.find_element(By.ID,"stat_table_body").get_attribute("innerHTML")
                d.find_element(By.LINK_TEXT,">").click()
                for j in zapisovanje.izlusci_private_key(s):
                    #f.write(j+"\n")
                    print(naberi_podatke_igralca(j))
            
            except StaleElementReferenceException:
                continue
            break
        print("Nabral %d/%d igralcev (%.2f%%)"%(i*10,n,i/n*1000))
    
    print("Trajalo %.1f sekund"%(time.time()-s))

    f.close()

def main():
    naberi_kljuce(1000)
    #print(naberi_podatke_igralca(4043148))
    return
    n=0
    for i in open("kljuci.txt").read().split("\n")[:40]:
        print(naberi_podatke_igralca(i),n)
        n+=1

if __name__=="__main__":
    main()