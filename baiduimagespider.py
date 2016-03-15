# -*- coding: utf-8 -*-
import urllib2
from baiduimage import BaiduImage
import os
import sys
#from multiprocessing.dummy import Pool
import codecs
import properties


words = properties.keywords
output =  properties.output

keywords = words.split(",")

bi = BaiduImage()

count = 0

pn = 0

for w in keywords:
    dest_folder = output + "\\" + w
    dest_folder=unicode(dest_folder,'utf8')
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    os.chdir(dest_folder)
    #Now, we are in a directory by a keyword
    image_jdata = bi.get_jdata_with_key(w,pn) 
     
    #for url in image_urls:
    for d in image_jdata:
        url = d["objURL"]
        fimg = os.path.basename(url)
        try:
            ftxt = fimg[0:fimg.index(".")] + ".txt"
        except:
            ftxt = fimg + ".txt"
        print ftxt
        download_info = (url, fimg)
        bi.download(download_info)
        
        f = codecs.open(ftxt,"w", "utf-8")
        f.write(d["fromPageTitle"])
        f.close()
        
        count += 1
        print "++++count:%d"%count
        want_stop = False
#         if count == 3:
#             count = 0 #Need to reset
#             print "stop for %s"%w
#             break

