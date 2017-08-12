#coding=utf-8
#================ 简介 ===================
#     脚本：          p站爬虫     
#     作者：          王子饼干   Q529324416 
#     时间：          2017年8月12日 03:37:18
#     描述:          由于王子开发自己的首要爬虫项目历时一周半,难以完成,推翻了好多次重写
#                    无数行代码付之东流，为了树立信心，决定跑来写一个简单的p站爬虫脚本，
#                    我想有一些人可能会需要把。就当是练练手。
#================ 简介 ===================

#================ synopsis ==================
#      Script:         Pixiv Spider
#      Developer:      PrinceBiscuit QQ529324416 Wechat 18262569939 
#      Time:           2017/8/12 03:37:18
#      Description     Because Little Prince carsh some trouble in temp project,it's difficult to complate,
#                      i rewrite it for a few times,which make me some tired,so i determine to develop a Pixiv Spider 
#                      Maybe someone need it,just for exercise
#================ synopsis ==================


import re
import time
import socket
import requests
import bs4
import urllib
import os
import sys
import io
import configparser
import threading

#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
#sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
class Final:
    '''save final for pixiv spider
    保存和p站爬虫相关的常量'''

    Headers={
        'host':'www.pixiv.net',
        'referer':"https://www.pixiv.net/",
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0',
        'accept-language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'accept-encoding':'gzip, deflate, br',
        'connection':'keep-alive',
        'upgrade-insecure-requests':'1',
        'cache-control':'max-age=0',
        'cookie':'p_ab_id=4; p_ab_id_2=8; device_token=91c3112fe5a33aa8c9d02d8b37403500; module_orders_mypage=%5B%7B%22name%22%3A%22recommended_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22fanbox%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; login_ever=yes; __utma=235335808.562646940.1501219988.1501781881.1501791377.12; __utmz=235335808.1501329291.5.3.utmcsr=accounts.pixiv.net|utmccn=(referral)|utmcmd=referral|utmcct=/login; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=female=1^6=user_id=26394916=1^9=p_ab_id=4=1^10=p_ab_id_2=8=1^11=lang=zh=1; _ga=GA1.2.562646940.1501219988; auto_view_enabled=1; PHPSESSID=26394916_4b100233c217b05721b53059aa2d27ec; is_sensei_service_user=1'
    }

    recommend_url=["https://www.pixiv.net/recommended.php","综合推荐"]                               #daily recommend 日推
    international_rank=['https://www.pixiv.net/ranking_area.php?type=detail&no=6',"国际排行榜"]       #International Ranking 国际排行榜 
    daily_rank=['https://www.pixiv.net/ranking.php?mode=daily',"每日排行榜"]                           #TodayRank 今日排行榜
    #mainly download picture from these url
    #主要通过这三个url下载图片

    @staticmethod
    def DownloadSource(image_url,filepath):
             '''a simple download function bind with Final class
             一个简单的下载函数，和Final绑定在一起'''

             res=requests.get(image_url,headers=Final.Headers)
             if res.status_code!=200:
                 #print('download failed...')
                 return None
             else:
                 with open(filepath,'wb') as f:
                    f.write(res.content)
                    f.close()
                 return True

    @staticmethod
    def DownloadPageS(url,headers,charset='utf-8'):
        
        res=requests.get(url,headers=headers)
        res.encoding='utf-8'
        #print(res.status_code)
        return res.text

    @staticmethod
    def DownloadPage(url,headers,charset='utf-8'):
        '''like download source,just for src code
        和downloadsource差不多，只不过是用于下载网页源代码的'''

        req=urllib.request.Request(url,headers=headers)
        return urllib.request.urlopen(req).read().decode(charset,'ignore')


class PixivSpider(threading.Thread):
    '''main program
    主程序'''

    IMG_MODEL=r'src="https://i\.pximg\.net/c/[0-9]*x[0-9]*/img-master/img/[0-9]*/[0-9]*/[0-9]*/[0-9]*/[0-9]*/[0-9]*/[0-9]*_p0_master1200\.jpg"'
    #the match model of picture,图片的匹配模型

    WORKING=[]

    class Log:
        '''save the log Information about download source
        记录爬取信息的日志'''
        LOGINFO='log_info'

        def __init__(self):
            
            self.dir_name="Resource\\"+self.__get_defalut_name()
            self.today_filepath=self.dir_name+"\\"+"log.ini"     #日志文件路径 filepath of log file
            if self.__file_exist(self.today_filepath):
                self.config=self.__get_config(self.today_filepath)
            else:
                try:
                    os.makedirs(self.dir_name)
                    self.__create_file(self.today_filepath)
                except:
                    pass
                self.config=self.__get_config(self.today_filepath)

        def __create_file(self,filepath):
            '''create a new file'''

            f=open(filepath,'w')
            f.close()     
            

        def __get_config(self,filepath):
            '''返回一个config对象
            return a config object'''    
            
            config=configparser.ConfigParser()
            config.readfp(open(filepath))
            if not config.has_section(PixivSpider.Log.LOGINFO):
                #why do this???,you won't understand
                config.add_section(PixivSpider.Log.LOGINFO)
            return config

        def __file_exist(self,filepath):
            '''判断文件是否存在
            check if file exist'''

            try:
                f=open(filepath,'r')
                f.close()
                return True
            except:
                return False

        def __get_defalut_name(self):
            '''根据时间取得文件名
            get floder name accroding to time
            '''

            time_tuple=time.localtime()
            year=str(time_tuple[0])+"-"
            month=str(time_tuple[1])+"-"
            day=str(time_tuple[2])

            return year+month+day

        def TakeNote(self,your_note,option):
            '''记录日志
            save the log message'''

            self.config.set(self.LOGINFO,option,your_note)
            self.config.write(open(self.today_filepath,'w'))

    def __init__(self,output,value,listbox):
        '''初始化p站爬虫的基本组件
        initialize the complement of pixiv spider'''

        threading.Thread.__init__(self)
        self.LOG=PixivSpider.Log()
        self.output=output
        self.value=value
        self.listbox=listbox

    def run(self):
             
        self.Main(Final.recommend_url)
        self.Main(Final.daily_rank)
        self.Main(Final.international_rank)
        self.output('下载完毕')
        
    def Main(self,which_url):
        
        title=which_url[1]
        which_url=which_url[0]
        if self.LOG.config.has_option(PixivSpider.Log.LOGINFO,'total_number'):
            self.total_number=int(self.LOG.config.get(PixivSpider.Log.LOGINFO,'total_number'))
        else:
            self.total_number=0
        self.output(title+'初始化完毕..')
        
        self.value.set('0')
        content=self.__download_content(which_url)
        #print(content)
        image_list=self.__get_image_list(content)
        max_number=len(image_list)
        temp_number=0
        self.output('正在下载'+title+'美图')
        
        for img in image_list:
                 
            filename=str(self.total_number+1)+".jpg"
            filepath=self.LOG.dir_name+"\\"+filename

            if not Final.DownloadSource(img,filepath):
                img=img.replace('jpg','png')
                filepath=filepath.replace('jpg','png')
                try:
                    f=open(filepath,'rb')
                    f.close()
                    self.listbox.insert(self.total_number,filepath)
                except:
                    self.listbox.insert(self.total_number,"下载失败")
            else:
                self.listbox.insert(self.total_number,filepath)

            self.total_number+=1
            temp_number+=1
            value=str(int(float(temp_number/max_number)*100))
            self.value.set(value)
            
        self.LOG.TakeNote(str(self.total_number),'total_number')

    def __download_content(self,url):
        '''download the web source code'''

        return Final.DownloadPageS(url,Final.Headers)

    def __get_image_list(self,content):
        '''return the raw image list from content'''

        raw_list=re.findall(PixivSpider.IMG_MODEL,content)
        image_list=[]
        for temp in raw_list:
            new=temp.split("=")[1].split('\"')[1]
            replace_str=re.findall(r'c/[0-9]*x[0-9]*/img-master',new)[0]
            first=new.replace(replace_str,'img-original')
            second=first.replace('_master1200',"")
            image_list.append(second)
        
        return image_list

    


if __name__=='__main__':

    #x=PixivSpider()
    #x.Main(Final.daily_rank)
    x.Main(Final.international_rank)
