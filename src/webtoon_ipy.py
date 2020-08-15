import clr
clr.AddReferenceToFileAndPath(r"D:\Lib\dll\NSoup.dll")
import NSoup

import System
from System.IO import *
from System.Net import *

debug = True
image_ext = None

def Download(url,filename,referer):
    wc = WebClient()
    wc.Headers.Add ("User-Agent", 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
    wc.Headers.Add ("Referer", referer)
    try:
        wc.DownloadFile(url, filename)
    except:
        print( url, "except" )
             
def DebugSave(filename,data):
    if debug:
        with open(filename, "w") as f:
            f.write(data.encode("utf-8"))
            
def DebugPrint(data):
    if debug:
        print(data);

def getWolfCom(comicsUrl,baseUrl,baseDir):
    doc = NSoup.NSoupClient.Connect(comicsUrl).Get()
    #DebugSave("a.html",doc.Html())
    elems = doc.Select("div.box > div.group.left-box > div.webtoon-bbs-list.bbs-list > ul > li");
    #DebugPrint(elems.Html());
        
    print(doc.Title)
    new_dir = Path.Combine(baseDir, doc.Title.replace(":","_"))
    if not Directory.Exists(new_dir): Directory.CreateDirectory(new_dir)
    print(new_dir)
   
    for e in elems:
        url = e.Select("a").First.Attr("href")
        if not url: continue
        url = baseUrl + url

        doc = NSoup.NSoupClient.Connect(url).Get()
        imgs = doc.Select("section.webtoon-body > div.group.image-view > img")
        print(doc.Title)

        sub_dir = Path.Combine(new_dir, doc.Title.replace(":","_"))
        if not Directory.Exists(sub_dir): Directory.CreateDirectory(sub_dir)

        k = 1;
        for img in imgs:
            img_url = img.Attr('src')
            if not img_url: continue
            if image_ext == None or img_url.endswith(image_ext):
                if( not img_url.startswith("http") ):
                    img_url = baseUrl + img_url
                file_name = "img_%04d.jpg" % k
                Download( img_url, Path.Combine(sub_dir, file_name), comicsUrl)
                print( img_url + " -> " + file_name )
                k = k + 1

def getFoxComics(comicsUrl,baseUrl,baseDir):
    getWolfCom(comicsUrl,baseUrl,baseDir)

def getWToon(comicsUrl,baseUrl,baseDir):
    doc = NSoup.NSoupClient.Connect(comicsUrl).Get()
    #DebugSave("a.html",doc.Html())
    elems = doc.Select("div.row > div.wvlist > div.left-box > div.wbody > ul > li");
    #DebugPrint(elems.Html());
        
    print(doc.Title)
    new_dir = Path.Combine(baseDir, doc.Title.replace(":","_"))
    if not Directory.Exists(new_dir): Directory.CreateDirectory(new_dir)
    print(new_dir)
   
    for e in elems:
        url = e.Select("a").First.Attr("href")
        if not url: continue
        url = baseUrl + url

        doc = NSoup.NSoupClient.Connect(url).Get()
        imgs = doc.Select("section.body > div.container > div.row > div.wview > div.wbody > img")
        print(doc.Title)
        #DebugSave("b.html",doc.Html())
        
        sub_dir = Path.Combine(new_dir, doc.Title.replace(":","_"))
        if not Directory.Exists(sub_dir): Directory.CreateDirectory(sub_dir)

        k = 1;
        for img in imgs:
            img_url = img.Attr('src')
            if not img_url: continue
            if image_ext == None or img_url.endswith(image_ext):
                if( not img_url.startswith("http") ):
                    img_url = baseUrl + img_url
                file_name = "img_%04d.jpg" % k
                Download( img_url, Path.Combine(sub_dir, file_name), comicsUrl)
                print( img_url + " -> " + file_name )
                k = k + 1

if __name__ == "__main__":
    url = [ 
        "https://wtwt30.com/v1?toon=1079",
    ]
    baseDir = r"D:\Temp2"
    for u in url:
        pos = u.find("/",len('https://')) #"https://wfwf105.com",https://fxfx21.com
        baseUrl = u[:pos+1]
        #getFoxComics(u,baseUrl,baseDir)
        getWToon(u,baseUrl,baseDir)
    
    
    
    