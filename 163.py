from Crypto.Cipher import AES
from base64 import b64encode
import requests
import random
import json
import os


def to_16(data):
    len1=16-len(data)%16
    data+=chr(len1)*len1

    return data

def encryption(data,key):
    iv = '0102030405060708'
    aes = AES.new(key=key.encode('utf-8'),IV=iv.encode('utf-8'),mode=AES.MODE_CBC)
    data1 = to_16(data)
    bs=aes.encrypt(data1.encode('utf-8'))

    return str(b64encode(bs),'utf-8')

def get_enc(data):
    param4 = '0CoJUm6Qyw8W8jud'
    #enc='NA5SxhePf6dxIxX7'
    #enc='GLvjERPvSFUw6EVQ'
    enc='g4PXsCuqYE6icH3R'
    first=encryption(data,param4)
    return encryption(first,enc)

if __name__ == '__main__':
    # 得到搜索歌曲的列表信息
    song=input('请输入歌曲名称:')
    param1 = {"hlpretag": "<span class=\"s-fc7\">", "hlposttag": "</span>", "s": song, "type": "1", "offset": "0",
              "total": "true", "limit": "30", "csrf_token": ""}
    data=json.dumps(param1)
    # 对请求参数的加密
    params=get_enc(data)
    data={
        'params': params,
        #'encSecKey': 'c2bcf219b2d727ff351d8fc4e5cbb86b09c32055345c098b8a8faf9c1c8b2bc506623ffc2b45db3e72cf040c750848f4408147c881a494c99dc8596415ce27d7b8ff7128e41a2b987bc9b78b3f4d4e0f0f5925b9ae24d99d1923a0d0c5cae5a3ebaf83c1097cfc3fd876f77582f38b79bbd03718cc562c15877abe9628e89ff1'
        #'encSecKey':'cd99d0f0c4210c9dfbd2fafec8640dae914f5d359e593338f699d98c0643dcc385a3889c89c98b3dcbe8f389aa91f47608ec236cd204adbd0236aae23125776c294f28d1753b685710e0173349e71715153e76c93a100ad682eab00033d3ebf3b5001a0046994800332cfc43445e59f28f5e874cb1dc04482d57da9cc67f6e8e'
        'encSecKey':'bb20ee9409e57057e4d1b55e4d77c94bff4d8cbf181c467bbd3fa156e3419665c6c1e643621d5d82c128251fb85f0cb34d4f08c88407b4148924ffa818f59a64b3814784e7e3837bad4f6f9690cb2cf721d9ea1af12c16a32a9df00be710b70ee8ed32036cc6a465b28ef43f4382cbcb4595b3121be75ecba9171876b611b8fc'
    }
    url='https://music.163.com/weapi/cloudsearch/get/web?csrf_token='
    headerList=[   # user-agent列表，用于构造随机取值
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400'
    ]
    value=random.choice(headerList)
    headers={'user-agent':value}
    response=requests.post(url=url,data=data,headers=headers)
    dict1=json.loads(response.text)
    lists=dict1['result']['songs']
    for i in range(len(lists)):
        print('[{}]-{}-->{}'.format(i+1,lists[i]['name'],lists[i]['ar'][0]['name']))
    id=int(input('请输入想下载的歌曲序号:(从1开始)'))
    song_id=lists[id-1]['id']
    song_name=lists[id-1]['name']+"_"+lists[id-1]['ar'][0]['name']   # 歌曲名称

    # 下面代码为下载歌曲的代码

    url2='https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token='
    param2= {"ids": "[{}]".format(song_id), "level": "standard", "encodeType": "aac", "csrf_token": ""}  # post请求的参数
    data2=json.dumps(param2)
    params=get_enc(data2)
    data['params']=params
    headers['user-agent']=random.choice(headerList)
    response2=requests.post(url=url2,data=data,headers=headers)
    dict2=json.loads(response2.text)
    print(dict2['data'][0]['id'])
    downloadUrl=dict2['data'][0]['url']
    downloadDir='./网易云音乐'
    # try:   # 自动创建文件夹
    #     os.mkdir(downloadDir)
    # except Exception as e:
    #     print(e)
    #
    # # 下载歌曲代码
    # response3=requests.get(url=downloadUrl,headers=headers)
    # # 以二进制的形式写入到文件中
    # with open(file='{}/{}.mp3'.format(downloadDir,song_name),mode='wb') as f:
    #     f.write(response3.content)