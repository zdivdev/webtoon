# -*- coding: utf-8 -*-

import os
import codecs
import base64

def imgFileToBase64( base_dir, image_file ):
    image_path = os.path.join(base_dir,image_file)
    print(image_path)
    with open( image_path, "rb" ) as f:
        data = base64.b64encode(f.read())
        print(type(data))
        return ('<img src="data:image/jpg;base64,' + data.decode('utf-8') )

def imgToHtml( base_dir, html_file ):
    with open( html_file, "r", encoding="utf-8" ) as f:
        begin = 0
        html = f.read()
        while True:
            begin = html.find("<img src=\"", begin)
            if begin >= 0:
                end = html.find('"',begin+12)
                img = imgFileToBase64(base_dir, html[begin+12:end])
                html = html[:begin] + img + html[end:]
                begin = end
            else:
                break
        with open( html_file + '.html', "w", encoding="utf-8" ) as wf:
            wf.write(html)

if __name__ == "__main__":
    base_dir = r"d:\Ebook\요리전체"
    files = os.listdir(base_dir)
    for f in files:
        html_path = os.path.join(base_dir,f)
        if os.path.isfile( html_path ):
            imgToHtml( base_dir, html_path )
