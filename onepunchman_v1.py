import requests
import re
import os
import cv2
import numpy as np
import matplotlib.pylab as plt

#get url for episode 1 to 121
def getSeries1(start,end):
    try:
        basic=13932016480028985383
        base=r'https://tonarinoyj.jp/episode/'
        series=[]
        episodenums=[]
        for i in range(start,end+1):
            num=basic-i+1
            url=base+str(num)
            series.append(url)
            episodenums.append(i)
        return (series,episodenums)
    except:
        return"Url generating error"

#get HTML text
def getHTMLText(url):
    try:
        headers = {
    "User-Agent":'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10'
}
        r=requests.get(url,timeout=30,headers=headers)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return"Getting HTML text error"

#getting urls for pics for each episode
def parsePage(html):
    try:
        urllist=[]
        pattern = re.findall('data-src=".*',html)
        for i in pattern:
            t=i.split(r'//')
            urllist.append(t[1][:-1])
        return urllist
    except:
        return"Parsing error"

#download the pics
def getPic(urllist,title):
    root="D://pics//"
    count=1
    for suffix in urllist:
        episodepath=root+"episode"+str(title)+'//'
        path=episodepath+str(count)+'.jpg'
        address=r'https://'+suffix
        print(address)
        try:
            if not os.path.exists(episodepath):
                os.makedirs(episodepath)
            if not os.path.exists(path):
                r=requests.get(address)
                with open(path,'wb') as f:
                    f.write(r.content)
                    f.close()
                print("文件{}保存成功".format(count))
                count+=1
            else:
                print("文件已存在")
        except Exception as e:
            print(e)
            print("爬取失败")
    return count-1

#rearrange the pics for reading
def RearrangePic(root,count):
    try:
        print(root,count)
        for num in range(1,count+1):
            filename=root+str(num)+'.jpg'
            src_img=cv2.imread(filename)
            h,w,c=src_img.shape
            w1=round(w/4)
            h1=280
            a=[]
            b=[]
            for i in range(4):
                for j in range(4):
                    a.append(src_img[(i*h1):((i+1)*h1-1),(j*w1):((j+1)*w1-1),:])
            for k in range(4):
                b.append(src_img[h1*4:h,(k*w1):((k+1)*w1-1),:])
            res1=np.hstack((a[0],a[4],a[8],a[12]))
            res2=np.hstack((a[1],a[5],a[9],a[13]))
            res3=np.hstack((a[2],a[6],a[10],a[14]))
            res4=np.hstack((a[3],a[7],a[11],a[15]))
            left=np.hstack((b[0],b[1],b[2],b[3]))
            res=np.vstack((res1,res2,res3,res4,left))
            cv2.imwrite(filename,res)
    except Exception as e:
        print("Rearranging error",e)


#main program
def main():
    startpoint=int(input("Start from?(Endpoint included.)\n"))
    endpoint=int(input("End by?(Endpoint included.)\n"))
    series,episodenums=getSeries1(startpoint,endpoint)
    items=list(zip(series,episodenums))
    for i in items:
        html=getHTMLText(i[0])
        urllist=parsePage(html)
        countpage=getPic(urllist,str(i[1]))
        root="D://pics//"+"episode"+str(i[1])+'//'
        if countpage!=26:
            RearrangePic(root,countpage)
        else:
            pass
    if startpoint == endpoint:
        print("Episode{} download complete!".format(startpoint))
    else:
        print("Episode{} to episode{} download complete!".format(startpoint,endpoint))

main()
