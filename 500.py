import requests
from lxml import etree
import time
import gzip
import csv
import re
import json

nowtime=time.strftime('%Y-%m-%d',time.localtime(time.time()))
with open('D://500/%s.csv'%(nowtime), 'w', newline='') as csv_file:#存放位置
    csv_writer = csv.writer(csv_file,dialect='excel')
    L1=['','','','初盘欧赔','','','即时赔率','','返还率','','即时凯利']
    L2=['球队','公司','胜','平','负','胜','平','负','值','胜','平','负']
    csv_writer.writerow(L1)
    csv_writer.writerow(L2)
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate"
    }

    L=[]
    r = requests.get('https://trade.500.com/jczq/',headers=headers).text
    html = etree.HTML(r)
    html_data = html.xpath('//*[@class="td td-data"]/a/@href')
    for i in html_data:
        if "ouzhi" in i:
            L.append(i)
    for x in L:
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Host": "odds.500.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
        url1 = requests.get(x,headers=headers)
        url1.encoding=url1.apparent_encoding
        html = etree.HTML(url1.text)
        html_data = html.xpath('//ul[@class="odds_hd_list"]/li/a/text()') #双方球队队名
        name="主:%sVS客:%s" % (html_data[0],html_data[1])
        print(name)
        html_data1 = html.xpath('//*[@class="tb_plgs"]/@title')#足彩公司
        # print(html_data1)
        html_data2 = html.xpath('//*[@class="tr_bdb td_show_cp"]/td/text()')#赔率
        pattern = re.compile(r'ouzhi-(.+?).shtml')
        id = pattern.findall(x)
        url2 = requests.get('http://odds.500.com/fenxi1/json/ouzhi.php?&fid=%s&cid=1'%(id[0]),headers=headers)
        L3=url2.json()
        L4=[]
        L4.append(name)
        L4.append('竞彩官方')
        try:
            L4=L4+(L3[-1][0:5])
            L7=["","Bet365"]
            print(L4)
            csv_writer.writerow(L4)
            time1=L3[-1][4]
            timeArray1 = time.strptime(time1, "%Y-%m-%d %H:%M:%S")
            timeStamp1 = int(time.mktime(timeArray1)) 
            url3 = requests.get('http://odds.500.com/fenxi1/json/ouzhi.php?&fid=%s&cid=3'%(id[0]),headers=headers)
            L5=url3.json()
            timeStamp3 = 0
            for timex in L5:
                time2=timex[4]
                # print(time2)
                timeArray2 = time.strptime(time2, "%Y-%m-%d %H:%M:%S")
                timeStamp2 = int(time.mktime(timeArray2))
                if timeStamp2<timeStamp1 and timeStamp1-timeStamp3>timeStamp1-timeStamp2:
                    timeStamp3 = timeStamp2
                    L6 = timex
                    # print(L6)
                else:
                    continue
            L7=L7+L6[0:5]
            print(L7)
            csv_writer.writerow(L7)
        except:
            L4=L4+(['','未开售',''])
            csv_writer.writerow(L4)
            L7=["","Bet365",'','未开售','']
            csv_writer.writerow(L7)
        for y in range(0,5):
            x=10*y
            L=[]
            L.append('')
            L.append(html_data1[y])
            L=L+html_data2[x:x+10]
            print(L)
            csv_writer.writerow(L)