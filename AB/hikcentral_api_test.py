import requests
import urllib3
import base64
import hashlib
import hmac
import logging
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)

#hikcenter Roraima

#url_base = 'https://200.164.65.185/artemis/api/'
#app_key = '23010081'
#secret_key = 'E2zAlrq4Fkd9tblrEN0z'

#Server Santa Helena - PR

#url_base = 'https://hikcentral.santahelena.pr.gov.br/artemis/api/'
#app_key = '29139079'
#secret_key = 'nQwIuuASx2OxD68VffnI'


#Server Mambore

#url_base = 'https://177.93.188.169/artemis/api/'
#app_key = '25577817'
#secret_key = 'qYFgW1KDkS8y4TIVMBQB'


#servidor MS

#url_base = 'https://177.174.32.238/artemis/api/'
#app_key = '29057842'
#secret_key = 'gYwd5kh6O0zcp0dJmjZi'

#CÓDIGO PARA O servidor hik Jardim Alegre - PR
#Dados Hikcenter
#url_base = 'https://45.229.91.108:9091/artemis/api/'
#app_key = '27361577'
#secret_key = 'BeQmMVZE99y9sJ0wUX6b'

url_base = 'https://hikcentral-rs.prf.gov.br/artemis/api/'
#url_base = 'https://10.88.9.2/artemis/api/'
app_key = '28054293'
secret_key = 'tgQbsqMGcNdplBdlZXcU'

#novo servidor hik cidade gaucha - PR
#url_base = 'https://186.250.232.70/artemis/api/'
#app_key = '29454260'
#secret_key = 'nXeNg2x18tgZ7UKYLPc9'

#novo servidor RS
#url_base = 'https://10.9.120.54/artemis/api/'
#app_key = '23571408'
#secret_key = '2ZMjUlU1x2KOa7c6PcM0'

#novo servidor Santa Catarina 
#url_base = 'https://10.8.3.63/artemis/api/'
#app_key = '24467837'
#secret_key = 'vafgbRGnJpGsFBf88Pst'


def get_signature(message, key):
    # encode message and key
    byte_key = bytes(key, 'UTF-8')  # key.encode() would also work in this case
    enc_msg = message.encode()
    # use the hmac.new function and the digest method
    h = hmac.new(byte_key, enc_msg, hashlib.sha256).digest()
    # print(h)
    # encode with base64
    s = base64.b64encode(h)
    #print(s)
    return s


def get_cameras():
    message_cams = f'POST\napplication/json\napplication/json;charset=UTF-8\nx-ca-key:{app_key}\n/artemis/api/resource/v1/cameras'
    headers_cams = {
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=UTF-8',
        'x-ca-key': app_key,
        'x-ca-signature-headers': 'x-ca-key',
        'x-ca-signature': get_signature(message_cams, secret_key),
    }
    data_cams = {
        'pageNo': 1,
        'pageSize': 200,
        'siteIndexCode': '0'
    }
    url_cams = url_base + 'resource/v1/cameras'
    print(url_cams)
    res_cams = requests.post(url_cams, headers=headers_cams, data=json.dumps(data_cams), verify=False)
    print(res_cams)
    # print(res_cams.request.headers)
    # print(res_cams.text)
    res_cams = json.loads(res_cams.text)
    # print(json.dumps(res_cams, indent=4))
    return res_cams


def get_records(camera_index, dt_start, dt_end, num_max):
    message_rec = f'POST\napplication/json\napplication/json;charset=UTF-8\nx-ca-key:{app_key}\n/artemis/api/pms/v1/crossRecords/page'
    headers_rec = {
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=UTF-8',
        'x-ca-key': app_key,
        'x-ca-signature-headers': 'x-ca-key',
        'x-ca-signature': get_signature(message_rec, secret_key),
    }
    data_rec = {
        'cameraIndexCode': str(camera_index),
        'startTime': dt_start,
        'endTime': dt_end,
        'pageNo': 1,
        'pageSize': num_max
    }
    url_rec = url_base + 'pms/v1/crossRecords/page'
    print(url_rec)
    res_rec = requests.post(url_rec, headers=headers_rec, data=json.dumps(data_rec), verify=False)
    # print(res_rec)
    # print(res_rec.request.headers)
    print(res_rec.text)
    res_rec = json.loads(res_rec.text)
    # print(json.dumps(res_rec, indent=4))
    return res_rec


def get_pictures(pic_uri):
    message_img = f'POST\napplication/json\napplication/json;charset=UTF-8\nx-ca-key:{app_key}\n/artemis/api/pms/v1/image'
    headers_img = {
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=UTF-8',
        'x-ca-key': app_key,
        'x-ca-signature-headers': 'x-ca-key',
        'x-ca-signature': get_signature(message_img, secret_key),
    }
    data_img = {'picUri': pic_uri}
    url_img = url_base + 'pms/v1/image'
    print(url_img)
    res_img = requests.post(url_img, headers=headers_img, data=json.dumps(data_img), verify=False)
    # print(res_img)
    # print(res_img.request.headers)
    # print(res_img.text)
    img = base64.b64decode(res_img.text.replace('data:image/jpeg;base64,', ''))
    with open('some_image.jpg', 'wb') as f:
        f.write(img)
    return img

dt_start = "2025-04-30T08:00:00-03:00"
dt_end = "2025-04-30T09:15:30-03:00"
cameras = get_cameras()
print(json.dumps(cameras['data']['list'], indent=4))

#records = get_records(27, dt_start, dt_end, 10)
#registros = records['data']['list']
# Itera sobre a lista em ordem inversa
#for registro in reversed(registros):
#    print(json.dumps(registro, indent=4))

#print(json.dumps(records['data']['list'], indent=4))
#picture = get_pictures(records['data']['list'][0]['vehiclePicUri'])
#print(picture)

# primeiro descobrir o index do ponto atraves da função cameras
# Depois comentar cameras e descomentar records, trocando o index, consegue ver a ultima passagem detectada.