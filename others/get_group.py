#获取群成员列表
import requests
def get_group(group_id):
    response = requests.post('http://127.0.0.1:5700/get_group_member_list?group_id='+str(group_id)).json()
    for i in response['data']:
        if(i['card']!=''):
            print(i['card']+str(i['user_id']))
        else:
            print(i['nickname']+str(i['user_id']))
