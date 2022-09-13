import requests


def setu():
    imgurl = insetu()
    imgstr = f'[CQ:image,type=show,file={imgurl}]'
    return imgstr


def insetu():
    url = "https://tuapi.eees.cc/api.php?"
    date = {
        'type': 'url',
        'category': 'dongman'
    }
    img = requests.get(url, params=date)
    return img.text
