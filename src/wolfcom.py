import bs4, codecs
import requests
import os
import io

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
image_ext = 'jpg'
request_headers = {
    'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 '
                   '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'),
    'Referer' : ("https://wfwf105.com/list?toon=381&title=%B8%BE%C4%AB%C6%E4")
}

def getFile(url):
    with codecs.open(url,'r', encoding='utf8') as f:
        html = f.read()
    return bs4.BeautifulSoup(html, 'html.parser')

def getUrl(url, headers={}, params=()):
    resp = requests.get(url, verify=False, headers=headers, params=params)
    #resp.headers
    #html = resp.content.decode('utf8')
    html = resp.text
    return bs4.BeautifulSoup(html, 'html.parser')

def urlToFile(url, file_name):
    resp = requests.get(url, verify=False, headers=request_headers, params=())
    with open(file_name, "wb") as f:
        f.write(resp.content)

def extractTag(bs,tag):
    [s.extract() for s in bs(tag)]

def getWolfCom( comicsUrl, baseUrl, baseDir):
    doc = getUrl(comicsUrl)
    title = doc.find("title").text
    elist = doc.select("div.box > div.group.left-box > div.webtoon-bbs-list.bbs-list > ul > li")
    
    new_dir = os.path.join(baseDir, title.replace(":","_"))
    if not os.path.isdir(new_dir): os.mkdir(new_dir)

    for e in elist:
        a = e.find('a',"view_open",href=True)
        if not a: continue
        url = baseUrl + a['href']

        doc = getUrl(url, request_headers)
        title = doc.find("title").text
        imgs = doc.select("section.webtoon-body div.group.image-view img")

        sub_dir = os.path.join(new_dir, title.replace(":","_"))
        if not os.path.isdir(sub_dir): os.mkdir(sub_dir)

        k = 1;
        for img in imgs:
            img_url = img.get('src')
            if not img_url: continue
            if image_ext == None or img_url.endswith(image_ext):
                if( not img_url.startswith("http") ):
                    img_url = baseUrl + img_url
                file_name = "img_%04d.jpg" % k
                urlToFile( img_url, os.path.join( sub_dir, file_name) )
                print( img_url + " -> " + file_name )
                k = k + 1

if __name__ == "__main__":
        url = "https://wfwf105.com/list?toon=381&title=%B8%BE%C4%AB%C6%E4"
        iurl = "https://wfwf105.com"
        bdir = "D:/Temp2/"
        getWolfCom(url, iurl, bdir)

