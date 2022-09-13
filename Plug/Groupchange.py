import requests
url = "http://127.0.0.1:5700/send_group_msg?"
def recall(groupid):
    message = {
        'group_id': groupid,
        'message': "有人撤回消息了，不会是色图吧！！！"
    }
    requests.get(url, params=message)
