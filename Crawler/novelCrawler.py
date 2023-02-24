import re
import requests
import random
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time
url_start='https://w.linovelib.com/novel/3223/164671.html'
url_source="https://w.linovelib.com"
url_contentPage='https://w.linovelib.com/novel/3223/catalog'
ua=UserAgent()
file_output='d://_School//转史Web'
div_header='<div id="cp#">\n'
div_end='</div>\n'
content_header='<div class="acontent">'
content_end='</div>'
cur_url=url_start
def encodeutf8(s):
    return s.encode('utf-8',errors='replace')

with open(file_output,"wb") as fp:
    while cur_url!=url_contentPage:
        try:
            r=requests.get(cur_url,headers={'User-Agent':ua.random},timeout=8)
        except:
            print('Connection Timeout')
            time.sleep(3)
            continue
        print('Query: {url}\nResponse: {res}'.format(url=r.url,res=r.status_code))
        if not r.ok:
            print('Query unsuccessful:',r.status_code)
            time.sleep(15)
            continue
        html_txt=r.text
        url_nxt=url_source+re.compile("'/.*'").search(re.compile("url_next:'.*',url_index").search(html_txt).group(0)).group(0)[1:-1]
        soup=BeautifulSoup(html_txt,'lxml')
        id=re.compile('\d/\d+').search(cur_url).group(0)[2:]
        content=''.join(list(map(str,soup.select('.acontent p')))).replace('\r','')
        title=str(soup.select('.atitle')[0])
        fp.write(encodeutf8(div_header.replace('#',id)))
        fp.write(encodeutf8(title))
        fp.write(encodeutf8('\n'))
        fp.write(encodeutf8(content_header))
        fp.write(encodeutf8(content))
        fp.write(encodeutf8(content_end))
        fp.write(encodeutf8(div_end))
        cur_url=url_nxt
        time.sleep(random.randint(5,10))
print('Crawl Complete')