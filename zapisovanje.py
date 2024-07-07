import re


def filtriraj(s):
    f=("<tr class=\"\">.*?"
        #"<td>(.*?)</td>.*?"    #rank
        "<td><nobr><img src=\"/img/flags/(.*?).png\".*?"    #drzava
        "<a id=\"player_link_.*?\" href=\"/player/(.*?)\">(.*?)</a>.*?"    #private key, ime
        ""
        )
    return re.findall(f,s)

def izlusci_private_key(s):
    return re.findall(r"href=\"/player/(\d+)\"",s)


def main():
    print(filtriraj(open("bepis.txt",encoding="UTF-8").read()))

if __name__=="__main__":
    main()