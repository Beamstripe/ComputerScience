import requests
import jieba
import imageio
from wordcloud import WordCloud
def frequencyStats(text:str,textmode:str):
    dic = {}
    words=[]
    if textmode == '0':
        text_cleaned = text.lower()
        for ch in '`!@#$%^&*()_+-=[]\\{}|;":,./<>?':
            text_cleaned=text_cleaned.replace(ch,' ')
        words = text_cleaned.split()
        for word in words:
            dic[word]=dic.get(word,0)+1
    else:
        text=text.encode('gbk','ignore').decode('gbk','ignore')
        words=jieba.lcut(text)
        for word in words:
            dic[word]=dic.get(word,0)+1
    wordlist = list(dic.items())
    wordlist.sort(key=lambda x:x[1],reverse=True)
    return (wordlist,words)
      
mode = input('Please define the language of the text:\n0:English\n1:Chinese\n')
textInputSource = input('Enter URL or a text starting with $\n')
if textInputSource[0] != '$':
    textInputSource = requests.get(textInputSource).text
else:
    textInputSource.removeprefix('$')
statlist,wordlist = frequencyStats(text=textInputSource,textmode=mode)
for e in statlist:
    print('%s:%d'%(e[0],e[1]))
wordCloudRes=''
for word in wordlist:
    wordCloudRes+=word+' '
bgImage = imageio.imread('d://sample.jpg')
cloud = WordCloud(background_color='white',width=800,height=800,font_path='D://HarmonyOS_Sans_Bold.ttf',mask=bgImage).generate(wordCloudRes)
cloud.to_file('d://wordcloud.png')
print('word cloud generated in d://wordcloud.png')