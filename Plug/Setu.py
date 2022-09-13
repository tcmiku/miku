import requests

def setu(groupid):
    imgurl=insetu()
    url = "http://127.0.0.1:5700/send_group_msg?"
    imgstr = f'[CQ:image,type=show,file={imgurl}]'
    message = {
        'group_id': groupid,
        'message':imgstr
    }
    requests.get(url, params=message)

def insetu():
    url = "https://tuapi.eees.cc/api.php?"
    date = {
        'type':'url',
        'category':'dongman'
    }
    img=requests.get(url,params=date)
    return img.text

def fish(groupid):
    url_up = "http://127.0.0.1:5700/send_group_msg?"
    url ="https://api.vvhan.com/api/moyu?type=json"
    reurl = requests.get(url).json()
    imgstr = f'[CQ:image,type=show,file={reurl["url"]}]'
    message = {
        'group_id': groupid,
        'message': imgstr
    }
    requests.get(url_up, params=message)

def img(message,groupid):
    print(message)
    if message == '来份色图':
        setu(groupid)
    else:
        fish(groupid)
