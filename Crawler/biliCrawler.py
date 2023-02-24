from fake_useragent import UserAgent
import requests
import time
ua = UserAgent()
cookie = "buvid3=A0571362-097A-CA06-1A0C-E6AF74A198BD46682infoc; nostalgia_conf=-1; _uuid=2CAED6D4-DD52-105E6-7182-A6F6592CD3A545842infoc; CURRENT_FNVAL=4048; b_nut=100; rpdid=|(umuummY)Rm0J'uY~uY~km|u; fingerprint=12fde9658e75a53be3af10d415e4fd05; buvid_fp_plain=undefined; buvid_fp=12fde9658e75a53be3af10d415e4fd05; DedeUserID=1772432247; DedeUserID__ckMd5=19aa5571ac9f2a1e; share_source_origin=QQ; bsource=search_baidu; i-wanna-go-back=-1; b_ut=5; hit-new-style-dyn=0; hit-dyn-v2=1; CURRENT_QUALITY=112; buvid4=4CAFD8D7-A9D7-62C5-BFA3-30E06558C39C49828-022012513-l1%2BOsuGKNV2OpRt%2FJ%2FxYrQ%3D%3D; bili_jct=15250960d4a9a6d088f1c6944832f8bc; innersign=1; sid=8q2eqh7i; PVID=1; bp_video_offset_1772432247=752375290021281800; b_lsid=3C2FD1081_185C3B48DF5"
header = {
    "User-Agent": ua.random,
    "Cookie": cookie,
    "Host": "www.bilibili.com"
}
requestURL = "https://t.bilibili.com/?spm_id_from=333.1007.0.0"
lastModified = ""
updatetime=time.time()
while True:
    if time.time()-updatetime>=600:
        updatetime=time.time()
        header["User-Agent"]=ua.random
    response = requests.get(requestURL,headers=header)
    if not response.status_code==requests.codes.ok:
        print('Request Failure:{$1}'.format(response.status_code))
    else:
        print('Request ok')
        current=response.headers.get('Last-Modified',default='')
        if current!=lastModified:
            print('Updates on {_date}'.format(_date=current))
            lastModified=current
    time.sleep(40)

    