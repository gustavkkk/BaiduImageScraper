# -*- coding: utf-8 -*-
from baiduimage import BaiduImage
import os
#from multiprocessing.dummy import Pool
import codecs
import properties
import sys


reload(sys)
sys.setdefaultencoding('utf-8')

words = properties.keywords
output =  properties.output

keywords = words.split(",")

bi = BaiduImage()



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
    count = 0
    for d in image_jdata:
        url = d["objURL"]
        fimg = os.path.basename(url)
        plainfimg = fimg.encode("utf-8")
        fn, ext =  os.path.splitext(plainfimg)
        plainfimg = "%d%s"%(count+1,ext)
        #print plainfimg
        
        ftxt = "%d.txt"%(count+1)
        #print ftxt
        download_info = (url, plainfimg)
        bi.download(download_info)
        f = codecs.open(ftxt,"w", "utf-8")
        f.write(w)
        f.write("\r\n")
        f.write(d["fromPageTitle"])
        f.write("\r\n")
        f.write(d["objURL"])
        f.close()
        count += 1
        print "++++count:%d"%count
        want_stop = False
#         if count == 3:
#             count = 0 #Need to reset
#             print "stop for %s"%w
#             break

