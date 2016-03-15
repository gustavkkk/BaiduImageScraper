'''
Created on Mar 12, 2016

@author: jchen
'''
import re
import urllib2
import json


class BaiduImage(object):
    '''
    classdocs
    usage: 
    
    
    '''
    
    search_url = lambda dummy,k,pn: "http://images.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=%s&pn=%d&gsm=0"%(k, pn*15)
    keywords = []
    image_urls = []

    def __init__(self, params=None):
        '''
        Constructor
        '''
        self.keywords = params
     
    def get_image_urls(self, html_content):
         
        exp = 'objURL":"([a-z.:/_A-Z0-9\-%]*)"'
        image_urls = re.findall(exp, html_content)
        print('%d images found in this page'%(len(image_urls)))
        return image_urls
    
    def get_search_url(self,keyword,n):
        encoded_kw = repr(keyword).replace('\\x', '%').upper()[1:-1]
        print "keyword: %s"%encoded_kw
        
        return self.search_url(encoded_kw,n)
    
    def get_image_urls_with_key(self,keyword,n):
        s_url = self.get_search_url(keyword, n)
        try:
            obj = urllib2.urlopen(s_url)
            s = str(obj.read())
            return self.get_image_urls(s)
        except Exception as e:
            print e
            pass
        print "failed to open baidu image search url for image urls"
    
    """
    Same as above function but return 
    """
    def get_jdata_with_key(self,keyword,n):
        s_url = self.get_search_url(keyword, n)
        try:
            obj = urllib2.urlopen(s_url)
            s = str(obj.read())
            return self.get_imgInfolist(s)
        except Exception as e:
            print e
            pass
        print "failed to open baidu image search url for jdata result"       
        
            
        
    def get_imgInfolist(self,src):
        start = src.index("ata('imgData'")
        start = src.index("[", start)
        newstr = src[start:]
        end = newstr.index("]", start)
        s = newstr[0:end + 1]
        data =  json.loads(s)
        refined = self.refine(data)
        return refined
    
    
    """
    remove useless items and return a list with smaller dictionaries
    """
    def refine(self,jdata):
        
        keys = ("fromPageTitle","objURL","type","width","height")
        refined_data = []
        for d in jdata:
            refined = {}
            if len(d) == 0:
                continue
            for key in keys:
                if key == "fromPageTitle":
                    d[key] = re.sub(r'<[^>]+>', r'', d[key])
                try:
                    refined[key] = d[key] 
                    #print "%s:%s"%(key,d[key])
                except Exception as e:
                    continue
            refined_data.append(refined)        
        return refined_data
    """
    download image into a file
    """ 
    def download(self,download_info):
        (url, file_name) = download_info
        print "trying downloading from%s"%url
        for i in range(2):
            try:
                response =  urllib2.urlopen(url, timeout=20)
                out_file  = open(file_name, 'wb')
                data = response.read() 
                out_file.write(data)
                print "OK for this one,written:%s"%file_name              
                return
            except Exception as e:
                print e
                pass
        print('Download failed: %s'%(url))                