from flask import Flask, request
import requests
from rebotmain import MYAPI
from Plug import Setu


def menu():
    data = request.get_json()
    message = data['message']
    message_id = data['message_id']
    message_type = data['message_type']
    uid = data['user_id']

    if "菜单" == message:
        a = "菜单:\n私聊(还没做)\n点歌\n色图(风控中无法发送)\n模拟抽卡(还没思路)\nup主更新监测(没思路)\n新番表(还没做)\n"
        MYAPI.send(a)
    elif "私聊" == message:
        a = '暂无'
        MYAPI.send(a)
    elif "点歌" == message:
        MYAPI.send("请输入歌曲名称:")
        song_name = MYAPI.reply(message_id)
        if song_name == '回复超时':
            MYAPI.send(f"[CQ:at,qq={uid}]"+"回复超时")
            return "OK"
        else:
            MYAPI.song(song_name)
    elif '来份色图' == message:
        img = Setu.setu()
        MYAPI.send(img)
    else:
        print('命令不正确')
    return "OK"
