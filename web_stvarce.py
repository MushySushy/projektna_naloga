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

    if t[3]!=None:
        t[3]=t[3].replace(" ","")
    if t[4]!=None:
        t[4]=sum(int(i[:-1])*{"s":1,"m":60,"h":60*60,"d":24*60*60}[i[-1]] for i in t[4].split(" "))
    if t[5]!=None:
        t[5]=t[5].replace(" ","")
    
    for i in range(2,len(t)):
        if t[i]!=None:
            t[i]=int(t[i])

    return tuple(t)


def naberi_podatke_igralca(k):
    for i in range(3):
        try:
            s=seja.get("https://minesweeper.online/player/"+str(k),timeout=1)
            #print(s.text,s)
            if "Trophies" not in s.text:
                raise Exception()
            return (int(k),)+html2podatki(s.text)
        except Exception:
            pass


def naberi_kljuce(n,file):
    o=Options()
    #o.add_argument("--headless")
    d=webdriver.Chrome(options=o)
    d.implicitly_wait(5)
    d.get("https://minesweeper.online/best-players")
    time.sleep(1)

    if os.path.exists(file):
        os.remove(file)
    f=open(file,"a",encoding="UTF-8")
    f.write("kljuc,ime,drzava,pokali,zmage,endurance,exp,cas1,cas2,cas3,eff1,eff2,eff3,mastery1,mastery2,mastery3,ws1,ws2,ws3\n")

    start_time=time.time()

    for i in range(1,n//10+1):
        while 1:
            try:
                s=d.find_element(By.ID,"stat_table_body").get_attribute("innerHTML")
                d.find_element(By.LINK_TEXT,">").click()
                for j in zapisovanje.izlusci_private_key(s):
                    try:
                        p=",".join(str(k) for k in naberi_podatke_igralca(j))+"\n"
                        f.write(p)
                        print(p,end="")
                    except Exception:
                        print("Zgubil igralca ",j)
            except StaleElementReferenceException:
                print("Error pri ",i)
                continue
            break
        print("\nNabral %d/%d igralcev (%.2f%%) v %.1f sekundah\n"%(i*10,n,i/n*1000,time.time()-start_time))

    f.close()

def main():
    naberi_kljuce(1000,"bepis.csv")
    #print(naberi_podatke_igralca(6596922))
    #print(html2podatki(open("test.html",encoding="UTF-8").read()))


if __name__=="__main__":
    main()