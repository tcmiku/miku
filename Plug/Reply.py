import requests
url = "http://127.0.0.1:5700/send_group_msg?"
def Reply_group(groupid):
    message = {
        'group_id': groupid,
        'message': "测试成功"
    }
    requests.get(url, params=message)

def Menu(groupid):
    message ={
        'group_id':groupid,
        'message':"菜单:\n色图模块\n@模块\n预计:\n点歌\n模拟抽卡\nup主更新监听\n群事件监听\n......"
    }
    requests.get(url,params=message)