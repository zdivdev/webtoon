import clr
clr.AddReferenceToFileAndPath(r"D:\Lib\dll\NSoup.dll")
import NSoup

import System
from System.IO import *
from System.Net import *

debug = False
image_ext = None

def Download(url,filename,referer):
    wc = WebClient()
    wc.Headers.Add ("User-Agent", 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
    wc.Headers.Add ("Referer", referer)
    try:
        wc.DownloadFile(url, filename)
    except:
        print( url, "except" )
                
def getWolfCom(comicsUrl,baseUrl,baseDir):
    doc = NSoup.NSoupClient.Connect(comicsUrl).Get()
    '''
    with open("a.html", "w") as f:
        f.write(document.Html())
    '''
    elems = doc.Select("div.box > div.group.left-box > div.webtoon-bbs-list.bbs-list > ul > li");
    if debug:
        print(elems.Html());
        
    print(doc.Title)
    new_dir = Path.Combine(baseDir, doc.Title.replace(":","_"))
    if not Directory.Exists(new_dir): Directory.CreateDirectory(new_dir)
    print(new_dir)
    
    for e in elems:
        url = e.Select("a").First.Attr("href")
        if not url: continue
        url = baseUrl + url

        doc = NSoup.NSoupClient.Connect(url).Get()
        imgs = doc.Select("section.webtoon-body > div.group.image-view > img");
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

if __name__ == "__main__":
    url = "https://wfwf105.com/list?toon=4526"
    baseUrl = "https://wfwf105.com"
    baseDir = r"D:\Temp3"
    getWolfCom(url,baseUrl,baseDir)
    
    
    
    