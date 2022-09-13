from flask import Flask, request
from Crypto.Cipher import AES
from base64 import b64encode
import random
import requests
import menu
import sqlite3
import time
import json

'''这是导入的另一个文件，下面会讲到'''

app = Flask(__name__)


class post163():
    @staticmethod
    def to_16(data):
        len1 = 16 - len(data) % 16
        data += chr(len1) * len1

        return data

    @staticmethod
    def encryption(data, key):
        iv = '0102030405060708'
        aes = AES.new(key=key.encode('utf-8'), IV=iv.encode('utf-8'), mode=AES.MODE_CBC)
        data1 = post163.to_16(data)
        bs = aes.encrypt(data1.encode('utf-8'))

        return str(b64encode(bs), 'utf-8')

    @staticmethod
    def get_enc(data):
        param4 = '0CoJUm6Qyw8W8jud'
        # enc='NA5SxhePf6dxIxX7'
        # enc='GLvjERPvSFUw6EVQ'
        enc = 'g4PXsCuqYE6icH3R'
        first = post163.encryption(data, param4)
        return post163.encryption(first, enc)

    @staticmethod
    def system(song):
        data = request.get_json()
        message_id = data['message_id']
        # 得到搜索歌曲的列表信息
        # MYAPI.send('请输入歌曲名称:')
        # song=input('请输入歌曲名称:')
        param1 = {"hlpretag": "<span class=\"s-fc7\">", "hlposttag": "</span>", "s": song, "type": "1", "offset": "0",
                  "total": "true", "limit": "30", "csrf_token": ""}
        data = json.dumps(param1)
        # 对请求参数的加密
        params = post163.get_enc(data)
        data = {
            'params': params,
            # 'encSecKey': 'c2bcf219b2d727ff351d8fc4e5cbb86b09c32055345c098b8a8faf9c1c8b2bc506623ffc2b45db3e72cf040c750848f4408147c881a494c99dc8596415ce27d7b8ff7128e41a2b987bc9b78b3f4d4e0f0f5925b9ae24d99d1923a0d0c5cae5a3ebaf83c1097cfc3fd876f77582f38b79bbd03718cc562c15877abe9628e89ff1'
            # 'encSecKey':'cd99d0f0c4210c9dfbd2fafec8640dae914f5d359e593338f699d98c0643dcc385a3889c89c98b3dcbe8f389aa91f47608ec236cd204adbd0236aae23125776c294f28d1753b685710e0173349e71715153e76c93a100ad682eab00033d3ebf3b5001a0046994800332cfc43445e59f28f5e874cb1dc04482d57da9cc67f6e8e'
            'encSecKey': 'bb20ee9409e57057e4d1b55e4d77c94bff4d8cbf181c467bbd3fa156e3419665c6c1e643621d5d82c128251fb85f0cb34d4f08c88407b4148924ffa818f59a64b3814784e7e3837bad4f6f9690cb2cf721d9ea1af12c16a32a9df00be710b70ee8ed32036cc6a465b28ef43f4382cbcb4595b3121be75ecba9171876b611b8fc'
        }
        url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='
        headerList = [  # user-agent列表，用于构造随机取值
            "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12",
            "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400'
        ]
        value = random.choice(headerList)
        headers = {'user-agent': value}
        response = requests.post(url=url, data=data, headers=headers)
        dict1 = json.loads(response.text)
        lists = dict1['result']['songs']
        # for i in range(len(lists)):
        #     MYAPI.send('[{}]-{}-->{}'.format(i + 1, lists[i]['name'], lists[i]['ar'][0]['name']))
        # # id = int(input('请输入想下载的歌曲序号:(从1开始)'))
        # MYAPI.send('请选择选择版本')
        # id = MYAPI.reply(message_id)
        id = 1
        song_id = lists[id - 1]['id']
        # song_name = lists[id - 1]['name'] + "_" + lists[id - 1]['ar'][0]['name']  # 歌曲名称

        url2 = 'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token='
        param2 = {"ids": "[{}]".format(song_id), "level": "standard", "encodeType": "aac",
                  "csrf_token": ""}  # post请求的参数
        data2 = json.dumps(param2)
        params = post163.get_enc(data2)
        data['params'] = params
        headers['user-agent'] = random.choice(headerList)
        response2 = requests.post(url=url2, data=data, headers=headers)
        dict2 = json.loads(response2.text)
        return dict2['data'][0]['id']


class MYAPI:
    @staticmethod
    def send(message):
        data = request.get_json()
        message_type = data['message_type']
        if 'group' == message_type:
            group_id = data['group_id']
            params = {
                "message_type": message_type,
                "group_id": str(group_id),
                "message": message
            }
        else:
            user_id = data['user_id']
            params = {
                "message_type": message_type,
                "user_id": user_id,
                "message": message
            }
        url = "http://127.0.0.1:5700/send_msg"

        requests.get(url, params=params)

    @staticmethod
    def save_message():
        data = request.get_json()
        uid = data['user_id']
        message = data['message']
        message_id = data['message_id']
        send_time = data['time']
        message_type = data['message_type']
        if message_type == 'group':
            group_id = data['group_id']
        else:
            group_id = "无"
        conn = sqlite3.connect("bot.db")
        c = conn.cursor()
        c.execute(
            "insert into message(QQ, message, message_id, send_time, message_type, group_id) values (?, ?, ?, ?, ?, ?)",
            (uid, message, message_id, send_time, message_type, group_id))
        conn.commit()
        conn.close()

    @staticmethod
    def reply(message_id):
        conn = sqlite3.connect("bot.db")
        c = conn.cursor()
        c.execute("SELECT * FROM message WHERE message_id = ?", (message_id,))
        results = c.fetchone()
        QQ = results[1]
        ID = results[0]
        group_id = results[6]
        message_type = results[5]
        num = ID + 1
        n = 0
        for i in range(60):
            n += 1
            try:
                c.execute("SELECT * FROM message WHERE id = ?", (num,))
                results = c.fetchone()
                new_QQ = results[1]
                new_group_id = results[6]
                new_message_type = results[5]
                if message_type == new_message_type == 'group':
                    if int(new_QQ) == int(QQ):
                        if int(new_group_id) == int(group_id):
                            new_message = results[2]
                            conn.commit()
                            conn.close()
                            return new_message
                        else:
                            num += 1
                            if n == 58:
                                conn.commit()
                                conn.close()
                                return "回复超时"
                            else:
                                time.sleep(1)
                                continue
                    else:
                        num += 1
                        if n == 58:
                            conn.commit()
                            conn.close()
                            return "回复超时"
                        else:
                            time.sleep(1)
                            continue
                elif message_type == new_message_type == 'private':
                    if int(new_QQ) == int(QQ):
                        new_message = results[2]
                        conn.commit()
                        conn.close()
                        return new_message
                    else:
                        num += 1
                        if n == 58:
                            conn.commit()
                            conn.close()
                            return "回复超时"
                        else:
                            time.sleep(1)
                            continue
                else:
                    num += 1
                    if n == 58:
                        conn.commit()
                        conn.close()
                        return "回复超时"
                    else:
                        time.sleep(1)
                        continue
            except:
                if n == 58:
                    conn.commit()
                    conn.close()
                    return "回复超时"
                else:
                    time.sleep(1)
                    continue

    @staticmethod
    def song(name_song):
        name_id = post163.system(name_song)
        MYAPI.send("[CQ:music,type=163,id=" + str(name_id) + "]")


@app.route('/', methods=["POST"])
def post_data():
    """下面的request.get_json().get......是用来获取关键字的值用的，关键字参考上面代码段的数据格式"""
    data = request.get_json()
    print(data)
    if data['post_type'] == 'message':
        MYAPI.save_message()
        message = data['message']
        print(message)
        menu.menu()
    else:
        print("暂不处理")

    return "OK"


if __name__ == '__main__':
    # 此处的 host和 port对应上面 yml文件的设置
    app.run(host='127.0.0.1', port=5701)  # 保证和我们在配置里填的一致
