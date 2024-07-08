from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *
import time, os, re, requests
import zapisovanje


seja=requests.Session()
format_strings=(
        "<h2>.*?<span>(.*?)</span>.*?",    #ime
        "<h2>.*?alt=\"(.*?)\".*?",   #drzava
        "(\d*?)<i class=\"fa fa-trophy score-icon.*?",   #pokali
        "wins-icon \"></i>([0-9 ]*?)</div>.*?",   #zmage
        "end\d\"></i>(.*?)</a>.*?",   #endurance
        "([0-9 ]*?)<img src=\"/img/other/xp.svg\".*?",   #exp
        "time-icon  level1\"></i>(\d*?)</a>.*?",   #cas 1
        "time-icon  level2\"></i>(\d*?)</a>.*?",   #cas 2
        "time-icon  level3\"></i>(\d*?)</a>.*?",   #cas 3
        "eff-icon level1\"></i>(\d*?)%.*?",   #eff 1
        "eff-icon level2\"></i>(\d*?)%.*?",   #eff 1
        "eff-icon level3\"></i>(\d*?)%.*?",   #eff 1
        "mastery1\"></i>(\d*?)</a>.*?",   #mastery 1
        "mastery2\"></i>(\d*?)</a>.*?",   #mastery 2
        "mastery3\"></i>(\d*?)</a>.*?",   #mastery 3
        "ws1\"></i>(\d*?)</a>.*?",   #win streak 1
        "ws2\"></i>(\d*?)</a>.*?",   #win streak 2
        "ws3\"></i>(\d*?)</a>.*?",   #win streak 3
        )

def html2podatki(s):
    t=[(lambda x:x.groups()[0] if x else None)(re.search(f,s,flags=re.DOTALL)) for f in format_strings]
    t[3]=t[3].replace(" ","")
    t[5]=t[5].replace(" ","")
    t[4]=(lambda x:int(x[0])*60+int(x[1]))(re.match("(\d+)h (\d+)m",t[4]).groups())
    for i in range(2,len(t)):
        t[i]=int(t[i])

    return tuple(t)

        

def naberi_podatke_igralca(k):
    for i in range(3):
        try:
            s=seja.get("https://minesweeper.online/player/"+str(k),timeout=1)
            #print(s.text,s)
            if "Trophies" not in s.text:# or "    " in s.text:
                raise Exception()
            return (int(k),)+html2podatki(s.text)
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
    k=tuple(open("kljuci.txt").read().split("\n"))[:200]

    for i in k:
        print(naberi_podatke_igralca(i))


if __name__=="__main__":
    start=time.time()
    main()
    print("Trajalo %.1f sekund"%(time.time()-start))