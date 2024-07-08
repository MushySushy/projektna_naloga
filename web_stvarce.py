from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *
import time, os, re, requests
from multiprocessing import Pool
import zapisovanje


seja=requests.Session()
format_strings=(
        "<h2>.*?alt=\"(.*?)\".*?",   #drzava
        "<h2>.*?<span>(.*?)</span>.*?",    #ime
        "(\d*?)<i class=\"fa fa-trophy score-icon.*?",   #pokali
        "time-icon  level1\"></i>(\d*?)</a>.*?",   #cas 1
        "time-icon  level2\"></i>(\d*?)</a>.*?",   #cas 2
        "time-icon  level3\"></i>(\d*?)</a>.*?",   #cas 3
        "eff-icon level1\"></i>(\d*?)%.*?",   #eff 1
        "eff-icon level2\"></i>(\d*?)%.*?",   #eff 1
        "eff-icon level3\"></i>(\d*?)%.*?",   #eff 1
        "([0-9 ]*?)<img src=\"/img/other/xp.svg\".*?",   #exp
        "mastery1\"></i>(\d*?)</a>.*?",   #eff 1
        "mastery2\"></i>(\d*?)</a>.*?",   #eff 2
        "mastery3\"></i>(\d*?)</a>.*?",   #eff 3
        "ws1\"></i>(\d*?)</a>.*?",   #win streak 1
        "ws2\"></i>(\d*?)</a>.*?",   #win streak 2
        "ws3\"></i>(\d*?)</a>.*?",   #win streak 3
        "end\d\"></i>(.*?)</a>.*?",   #endurance
        "wins-icon \"></i>([0-9 ]*?)</div>.*?",   #zmage
        )

def html2podatki(s):
    return tuple((lambda x:x.groups()[0] if x else None)(re.search(f,s,flags=re.DOTALL)) for f in format_strings)
        

def naberi_podatke_igralca(k):
    global seja, format_string

    print("\nenter ",k)
    
    for i in range(3):
        print("try ",i," on ",k)
        try:
            s=seja.get("https://minesweeper.online/player/"+str(k),timeout=1)
            print("got site on ",k)
            #print(s.text,s)
            if "Trophies" not in s.text:# or "    " in s.text:
                print("slb site")
                raise Exception()
            return html2podatki(s.text)
        except Exception:
            print("error on ",k)
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
    
    start=time.time()

    for i in range(1,n//10+1):
        while 1:
            try:
                s=d.find_element(By.ID,"stat_table_body").get_attribute("innerHTML")
                d.find_element(By.LINK_TEXT,">").click()
                for j in zapisovanje.izlusci_private_key(s):
                    f.write(j+"\n")
                    #print(naberi_podatke_igralca(j))
            
            except StaleElementReferenceException:
                continue
            break
        print("Nabral %d/%d igralcev (%.2f%%)"%(i*10,n,i/n*1000))
    
    print("Trajalo %.1f sekund"%(time.time()-start))

    f.close()

def main():
    #print(seja.get("https://minesweeper.online/player/"+str(9740766),timeout=1).text)
    #return
    #s=open("test.html",encoding="UTF-8").read()
    #print(s)
    #print(html2podatki(s))
    #return
    
    #naberi_kljuce(1000)
    #print(naberi_podatke_igralca(2620977))
    #return
    k=tuple(open("kljuci.txt").read().split("\n"))[:100]

    if 0:
        n=0
        for i in k:
            x=naberi_podatke_igralca(i)
            n+=x==None
            print(n,x)

    else:
        with Pool(processes=4) as pool:
            p=pool.map(naberi_podatke_igralca,k)
        print(p)
        print(len(p),p.count(None))

if __name__=="__main__":
    print("uwu")
    start=time.time()
    main()
    print("Trajalo %.1f sekund"%(time.time()-start))