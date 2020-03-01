from lxml import etree #xpath
import requests
import re,time,json
import random


def getURL(url):
    myHeaders = ['User-Agent:Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',\
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',\
        'User-Agent:Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11']

    headers = {'User-Agent':myHeaders[random.randint(0,2)]}

    try:
        response = requests.get(url,headers=headers)
        print(response.status_code)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        return None
        

for i in range(5):
    offset = 20*i
    url = 'https://movie.douban.com/top250?start=' + str(offset) + '&filter='

    content = getURL(url)


    html = etree.HTML(content)

    items = html.xpath('//ol[@class="grid_view"]/li')
    with open("./movieResult.txt","a") as f:
        for item in items:
            name_ch = item.xpath('.//span[@class="title"]/text()')[0]
            # longname = item.xpath('.//span[@class="title"]/text()')[1]
            # name_nch = re.findall('\xa0/\xa0(.*)',longname)[0]
            longinfo = item.xpath('.//div[@class="bd"]/p/text()')
            a = longinfo[0].strip()
            director = re.findall('(.*?):(.*?)\xa0',a)[0][1]
            b = longinfo[1].strip()

            try:
                info = re.findall('([0-9]{4})\xa0/\xa0(.*?)\xa0/\xa0(.*)',b)[0]
                info = info[1]+'/ '+info[2]
            except:
                info = '暂无'

            
            ratingNum = item.xpath('.//div[@class="star"]/span/text()')[0]
            ratingPeople = item.xpath('.//div[@class="star"]/span/text()')[1]
            quote = item.xpath('.//p[@class="quote"]/span/text()')[0]
            s = '电影名称： ' + name_ch + '\n\t 导演：' + director + ' / 类型：' +\
                info[0]+'/ '+ info +  '\n\t 评分：' + ratingNum + ' / ' + ratingPeople + '\n\t 经典：' + quote +'\n'
            f.write(s)




