# coding:utf-8
# author:xiaofeng
# 通过公开的uid下载该用户的所有歌曲


import requests
import json
from bs4 import BeautifulSoup
import urllib.request
import time


uid = '639d94862d2b308337'  #通过点击任意全民K歌歌曲获得
# root_url = 'https://node.kg.qq.com/personal?uid='   #全民K歌主页
music_page_dict = {}
music_save_path = 'C:/DDD/music/全民K歌'

def test():
    get_music_page(uid)


def get_music_page(uid):
    start = '1'

    t_url = 'https://node.kg.qq.com/cgi/fcgi-bin/kg_ugc_get_homepage?jsonpCallback=callback_1&g_tk=5381&outCharset=utf-8&format=jsonp&type=get_ugc&start='+start+'&num=8&touin=&share_uid='+uid+'&g_tk_openkey=5381&_=1517154835629'
    music_page_lists=[]
    r = requests.get(t_url)
    song_object = json.loads(r.content.decode('utf-8')[11:-1])
    page = song_object['data']['has_more']
    for start in range(1, page+2):
        t_url = 'https://node.kg.qq.com/cgi/fcgi-bin/kg_ugc_get_homepage?jsonpCallback=callback_1&g_tk=5381&outCharset=utf-8&format=jsonp&type=get_ugc&start=' + str(start) + '&num=8&touin=&share_uid=' + uid + '&g_tk_openkey=5381&_=1517154835629'
        r = requests.get(t_url)
        song_object = json.loads(r.content.decode('utf-8')[11:-1])
        ugclist_dict = song_object['data']['ugclist']
        for music_info_dict in ugclist_dict:
            music_page_dict[music_info_dict['title']] = music_info_dict['shareid']
    # return music_page_dict


def get_music_url(page):
    t_url = 'https://node.kg.qq.com/play?s='+page+'&g_f=personal'
    r = requests.get(t_url)
    soup = BeautifulSoup(r.content, 'lxml')
    json_content = soup.find_all('script', {'type': 'text/javascript'})[2].get_text()[len('window.__DATA__ = '):-2]
    music_info = json.loads(json_content)
    # print(music_info['detail']['playurl'])
    playurl = music_info['detail']['playurl']
    return playurl


def dow_music(music_title, music_url):
    urllib.request.urlretrieve(music_url, music_save_path + '/全民k歌' + uid + '_' + music_title + '.mp3')
    return


if __name__ == '__main__':
    # music_page_lists = get_music_page(uid)
    # print(music_page_lists)
    # print(len(music_page_lists))
    # print(get_music_url('t1kTJKtqdMHNEtqM'))
    # test()
    get_music_page(uid)
    # print(music_page_dict)
    # print(len(music_page_dict))
    for m_title in music_page_dict.keys():
        time.sleep(2)
        dow_music(m_title, get_music_url(music_page_dict[m_title]))
