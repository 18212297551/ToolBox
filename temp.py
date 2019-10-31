import json
import re

import requests

a= """type
含义
ng
单曲
ly
歌词
comments评论
detail
歌曲详情
artist
歌手
album
专辑
playlist
歌单
my
MV
dj
radio
主播电台
dj
主播电台单曲id
detail_di主播电台歌曲详情
search
搜索"""
#type含义ng单曲ly歌词comments评论detail歌曲详情artist歌手album专辑playlist歌单myMVdjradio主播电台dj主播电台单曲iddetail_di主播电台歌曲详情search搜索
#https://music.163.com/#/playlist?id=2945719972
#https://music.163.com/#/song?id=1399533630
# https://music.163.com/#/song?id=238555

'''            mc_source = {
                '网易云': 'netease',
                'QQ音乐': 'qq',
                '酷狗': 'kugou',
                '酷我': 'kuwo',
                '虾米': 'xiami',
                '百度': 'baidu',
                '一听': '1ting',
                '咪咕': 'migu',
                '荔枝': 'lizhi',
                '蜻蜓': 'qingting',
                '喜马拉雅': 'ximalaya',
                '全名K歌': 'kg',
                '5Sing原创': '5singyc',
                '5Sing翻唱': '5singfc'
            }
            url = 'http://hd215.api.yesapi.cn/?s=App.Music.Search' #http://hn216.api.yesapi.cn/  http://hd215.api.yesapi.cn/
            _filter = 'name'
            mc_key = self.cmBox_2_mcsource.currentText()
            _website = mc_source[mc_key]
            # print(_website)

            data = {
                'app_key': '5E8512AAB713A041C41E076C754E3305',# C4486C64E77292F94BC56307B64C92AE  5E8512AAB713A041C41E076C754E3305
                'input': inputg,
                'filter': _filter,
                'website': _website,
                'page': page,
            }

            res = requests.get(url, data)
'''
# API　url = 'https://api.imjad.cn/cloudmusic/?type=?&id=?'
url = 'https://api.imjad.cn/cloudmusic/?type=playlist&id=2945719972'
data = {
    'app_key': '5E8512AAB713A041C41E076C754E3305',  # C4486C64E77292F94BC56307B64C92AE  5E8512AAB713A041C41E076C754E3305
    'input': '你',
    'filter': 'name',
    'website': 'netease',
    'page': 1,
}

url2 = 'http://hd215.api.yesapi.cn/?s=App.Music.Search'
res = requests.get(url)
req = res.content
reqq = json.loads(req)
print(reqq)
