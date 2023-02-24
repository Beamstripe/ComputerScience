import re
import requests
import random
import os
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time
url_start='https://w.linovelib.com/novel/2321/121884.html'
url_source="https://w.linovelib.com"
url_contentPage='https://w.linovelib.com/novel/2321/catalog'
url_coverimage='https://w.linovelib.com/files/article/image/2/2321/2321s.jpg'
ua=UserAgent(browsers=["chrome", "edge", "firefox", "safari", "opera"])
file_output='novel/*.html'
content_page='index.html'
book_title='转生成蜘蛛又怎样！'
cur_url=url_start
columntitle=''

content_page_head=r"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"> <meta http-equiv="X-UA-Compatible" content="IE=edge"> <meta name="viewport" content="initial-scale=1.0,minimum-scale=1.0,user-scalable=yes,width=device-width"> <title>Content</title> <script type="text/javascript"> function gotolink(chapterurl) { window.location.href = chapterurl; } </script> <style> .booktitle { position: relative; text-align: center; font: 700 3rem/5rem 'Microsoft yahei'; height: auto; } .content { display: flex; flex-flow: column nowrap; background-color: #333; } section { display: flex; flex-flow: column nowrap; } .cltitle { position: relative; height: auto; font: 900 2rem/3rem 'SimSun'; background-color: #999; text-indent: 0.5rem; color: #eee; } .cptitle { position: relative; height: auto; text-indent: 1rem; font: 500 1.5rem/3rem 'SimSun'; background-color: #ddd; cursor: pointer; } </style></head><body> <div class="content"> """

content_page_end=r"""</div></body></html>"""

novel_page_head=r"""<!DOCTYPE html><html><head><meta charset="UTF-8"> <meta http-equiv="X-UA-Compatible" content="IE=edge"> <meta name="viewport" content="initial-scale=1.0,minimum-scale=1.0,user-scalable=yes,width=device-width"> <title>$ttl</title> <script src="https://cdn.staticfile.org/jquery/1.8.3/jquery.min.js"></script> <script type="text/javascript"> var readparams = { url_next: '$nxt', url_prev: '$prv', url_contentpage: '$ctt' }; var nightmode = false; $(document).ready(function () { $("body,.atitle,p").toggleClass("day"); $(".viewmode").click(function () { $("body,.atitle,p").toggleClass("night"); $("body,.atitle,p").toggleClass("day"); if ($("button").html() == 'day') { $("button").html('night'); } else { $("button").html('day'); } nightmode = !nightmode; if (nightmode) $("hr").css('border', 'solid #999'); else $("hr").css('border', 'solid #555'); }); $(window).dblclick(function () { let obj = $('body'); obj.scrollTop(obj.prop("scrollHeight")); }); $(window).scroll(function () { $(".viewmode").css('top', $(window).scrollTop()); }); $("body").keydown(function (event) { if (event.keyCode == 37) location = readparams.url_prev; if (event.keyCode == 39) location = readparams.url_next; }) }); </script> <style> .imagecontent { display: block; width: 100%; position: relative; } .apage { display: flex; flex-direction: column; } .night { color: #fcfcfc; background-color: #242424; } .day { color: #303030; background-color: rgb(255, 242, 226); } .atitle { font-family: 'HarmonyOS Sans SC Bold', 'Microsoft YaHei'; text-align: center; } p { text-indent: 2rem; padding-left: 3%; padding-right: 3%; } .viewmode { height: 3rem; width: 3.5em; cursor: pointer; } button { width: 3.5rem; height: 3rem; text-align: center; border: medium solid violet; font: 700 1rem/2rem 'times new roman' } .footnote span { border: medium solid gray; background-color: #fcfcfc; text-decoration: none; margin: 1rem; padding: 0.33rem; } .footnote span:link { color: gray; } .footnote span:hover { color: red; } .footnote span:visited { color: gray; } .footnote { display: flex; justify-content: center; cursor: pointer; } hr { border: solid #888; } img { height: auto; max-width: 100%; } </style></head><body> <div class="viewmode"> <button>night</button> </div>"""

novel_page_end=r"""<div class="footnote"> <span for="prvpage" onclick="window.location.href = readparams.url_prev;">上一页</span> <span for="cttpage" onclick="window.location.href = readparams.url_contentpage;">目录</span> <span for="nxtpage" onclick="window.location.href = readparams.url_next;">下一页</span> </div></body></html>"""

def encodeutf8(s):
    return s.encode('utf-8',errors='replace')

def tryConnection(url):
    response = requests.Response()
    success = False
    counter = 10
    while not success:
        try:
            response=requests.get(url,headers={'User-Agent':ua.random},timeout=8)
            print('Query: {url}\nResponse: {res}'.format(url=response.url,res=response.status_code))
            assert response.ok
            success=True
        except:
            if response.status_code != None and response.status_code == 404 and counter<=0:
                raise ValueError('URL:{f} does not exist.'.format(f=response.url))
            print('Restart in 20 sec')
            counter-=1
            time.sleep(20)
            success=False
    return response

def downloadPic(url):
    pic=tryConnection(url).content
    picorder=url[26:].replace('/','-');
    with open('novel/image/pic-'+picorder,'wb') as fp:
        fp.write(pic)
    print('Picture downloaded:'+url)
    localurl='image/pic-'+picorder
    print('Save in /novel/'+localurl)
    time.sleep(1)
    return localurl


# Check if directories are created

if not os.path.exists('novel/image'):
    os.makedirs('novel/image')

# Download cover image

index_img=tryConnection(url_coverimage).content
coverimgfmt=re.compile('\.[a-z]*$').search(url_coverimage).group(0)
with open('novel/image/cover'+coverimgfmt,'wb') as fp:
    fp.write(index_img)

with open('novel/'+content_page,'wb') as ctfp:

    # Contents page head

    ctfp.write(encodeutf8(content_page_head+'\n'))
    ctfp.write(encodeutf8('<div class="booktitle" style="background-color: #ddd;"> $ </div> <section> '.replace('$',book_title)))
    
    while cur_url!=url_contentPage:
        file_output='w'+re.compile('\d.*').search(cur_url).group(0).replace('/','_')
        with open('novel/'+file_output,"wb") as fp:

            # connect and retrieve the data

            r=tryConnection(cur_url)
            html_txt=r.text

            # initialize the url needed

            url_nxt=url_source+re.compile("'/.*'").search(re.compile("url_next:'.*',url_index").search(html_txt).group(0)).group(0)[1:-1]
            url_prv=url_source+re.compile("'/.*'").search(re.compile("url_previous:'.*',url_next").search(html_txt).group(0)).group(0)[1:-1]
            bookmark_prv='w'+re.compile('\d.*').search(url_prv).group(0).replace('/','_')
            bookmark_nxt='w'+re.compile('\d.*').search(url_nxt).group(0).replace('/','_')
            chapterid=re.compile('\d_.*\.html').search(file_output).group(0)[2:-5]
            if bookmark_nxt.find('catalog')!=-1:
                bookmark_nxt=content_page
            if bookmark_prv.find('catalog')!=-1:
                bookmark_prv=content_page

            # content filter and selection
            
            soup=BeautifulSoup(html_txt,'lxml')
            content=''.join(list(map(str,soup.select('.apage')))).replace('\r','')
            content=re.compile('<div class="cgo">.*</div>').sub('',content)
            title=str(soup.select('.atitle>h1')[0]).replace('<h1 id="atitle">','').replace('</h1>','')
            cur_columntitle=str(soup.select('.atitle>h3')[0]).replace('<h3>','').replace('</h3>','')

            # download the retrieved images
            for img in soup.find_all('img'):
                imgurl=img.attrs['src']
                localimage=downloadPic(imgurl)
                content=content.replace(imgurl,localimage)
            
            # write in the title in contents page

            if cur_columntitle!=columntitle:
                if columntitle!='':
                    ctfp.write(encodeutf8(r"""</section><section>"""))
                ctfp.write(encodeutf8(r"""<div class="cltitle">{cltitle}</div>""".format(cltitle=cur_columntitle)))
                columntitle=cur_columntitle
            ctfp.write(encodeutf8(r"""<div class="cptitle" id="cp{cpid}" onclick="gotolink('{link}');">{cptitle}</div>""".format(cpid=chapterid,link=file_output,cptitle=title)))

            # write in the novel content in novel page
            cur_novel_page_head=novel_page_head
            cur_novel_page_head=cur_novel_page_head.replace('$nxt',bookmark_nxt)
            cur_novel_page_head=cur_novel_page_head.replace('$prv',bookmark_prv)
            cur_novel_page_head=cur_novel_page_head.replace('$ctt',content_page+'#cp'+chapterid)
            cur_novel_page_head=cur_novel_page_head.replace('$ttl',title)
            fp.write(encodeutf8(cur_novel_page_head+'\n'))
            fp.write(encodeutf8(content+'\n'))
            fp.write(encodeutf8(novel_page_end))
            cur_url=url_nxt
            time.sleep(random.random()*7+3)
    # Content page end
    ctfp.write(encodeutf8(r"""</section></div></body></html>"""))
print('Crawl Complete')

