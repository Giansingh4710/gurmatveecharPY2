# C:/Python27/python.exe GurmatVecharToSD.py 
# C:/Python27/Scripts/pip2.exe install six bs4 requests datetime os re


# import urllib.request
from six.moves import urllib
from bs4 import BeautifulSoup as bs 
import requests
from datetime import datetime as dt
import os
import re
mb=re.compile(r"([0-9]{1,3}(\.[0-9]*)?\s((MB)|(KB)))")


totalFiles=0
def getAllLinks(url,folder="main"):
    res=requests.get(url)
    soup=bs(res.text, 'html.parser')
    khatas=soup.find_all("table",cellpadding=4)
    khatas=khatas[4:-2]
    folderWithLinks={folder:[]}
    count=0 
    for file in khatas:
        try:
            title=file.find("font",size="2",color="0069c6").text
        except AttributeError:
            print("No Good. But we caught it!!")
            continue
        newUrl="http://www.gurmatveechar.com/"+file.find("a").get("href")
        if "mp3" in newUrl.lower():
            global totalFiles
            totalFiles+=1
            count+=1
            length=file.find_all("td",align="right")
            for td in length:
                if "mb" in td.text.lower() or "kb" in td.text.lower():
                    theMB=td.text
            title=str(count).zfill(3)+" ) "+title+"???"+theMB
            folderWithLinks[folder].append(title)
            folderWithLinks[folder].append(newUrl)
        else:
            newFolder=title
            newFolderWithLinks=getAllLinks(newUrl,newFolder)
            if folder=="main":
                folderWithLinks.update(newFolderWithLinks)
            else:
                folderWithLinks[folder].append(newFolderWithLinks) 
    return folderWithLinks

def download(khatas,thePath):
    for khata in khatas:
        folderPath=thePath
        if khata!="main":
            folderPath=thePath+khata+"\\"
            os.mkdir(folderPath)
            if type(khatas[khata][0])==dict:
                listOfDict=khatas[khata]
                for dictt in listOfDict:
                    if type(dictt)==dict:
                        download(dictt,folderPath)
                continue
        titles=[khatas[khata][i] for i in range(len(khatas[khata])) if i%2==0]
        links=[khatas[khata][i] for i in range(len(khatas[khata])) if i%2!=0]
        for i in range(len(links)):
            title=titles[i].split("???")[0]+".mp3"
            noNo='\/:*?"<>|'
            for bad in noNo:
                if bad in title:
                    title=title.replace(bad,"#")
            urllib.request.urlretrieve(links[i],folderPath+title)
            print(title+' - '+links[i])

def EnterUrl(link,path):
    start=str(dt.now())

    if path[-1]!="/":
        path+="/"

    khatas=getAllLinks(link)
    download(khatas,path)

    end=str(dt.now())

    print("In total: "+str(totalFiles)+" total files\n")
    
    print("Start: "+start)
    print("End: "+end+"\n\n")
    startSeconds=(int(start[11:13])*60*60)+(int(start[14:16])*60)+int(start[17:19])
    endSeconds=(int(end[11:13])*60*60)+(int(end[14:16])*60)+int(end[17:19])
    totalSeconds=endSeconds-startSeconds
    print("Seconds: "+str(totalSeconds))
    print("Minutes: "+str(totalSeconds/60))
    print("Hours: "+str(totalSeconds/(60*60)))
    
url="https://www.gurmatveechar.com/audio.php?q=f&f=%2FKatha%2F02_Present_Day_Katha%2FGiani_Harbhajan_Singh_Dhudikey_%28Vidyarthi_Sampardai_Bhindra%29%2FSri_Dasam_Guru_Granth_Sahib_Ji_Katha%2F16_Charitropakhyan_Katha"
path="C:/users/jsdosanj/Downloads/Katha/"
EnterUrl(url,path)
