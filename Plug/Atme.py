import requests
def atme(groupid,uid=None):
    url = "http://127.0.0.1:5700/send_group_msg?"
    message = {
        'group_id': groupid,
        'message': "哎呀，你干嘛~~~~\n输入tcmiku可查看菜单"
    }
    requests.get(url, params=message)