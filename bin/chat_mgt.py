import socket
from urllib import parse

from bin.settings_load import *


def send_msg_private(user_id, msg):  # 发送消息【对方QQ号），消息内容】
    server_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_client.connect((server_ip, server_send_port))
    # 将字符中的特殊字符进行url编码
    # msg = msg.replace(" ", "%20") #已弃用
    # msg = msg.replace("\n", "%0a") #已弃用
    msg = parse.quote(msg, safe='')
    payload = "GET /send_private_msg?user_id=" + str(user_id) + "&message=" + msg + " HTTP/1.1\r\nHost:" + str(
        server_ip) + ":" + str(server_send_port) + "\r\nConnection: close\r\n\r\n"
    server_client.send(payload.encode("utf-8"))
    print("【私聊】" + str(user_id), "发送：\n" + parse.unquote(msg))
    server_client.close()
    return 0


def send_msg_group(group_id, msg):  # 发送消息【对方群号，消息内容】
    server_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_client.connect((server_ip, server_send_port))
    # 将字符中的特殊字符进行url编码
    # msg = msg.replace(" ", "%20") #已弃用
    # msg = msg.replace("\n", "%0a") #已弃用
    msg = parse.quote(msg, safe='')
    payload = "GET /send_group_msg?group_id=" + str(group_id) + "&message=" + msg + " HTTP/1.1\r\nHost:" + str(
        server_ip) + ":" + str(server_send_port) + "\r\nConnection: close\r\n\r\n"
    server_client.send(payload.encode("utf-8"))
    print("【群聊】" + str(group_id), "发送：\n" + parse.unquote(msg))
    server_client.close()
    return 0


def del_msg(msg_id):  # 撤回消息【消息ID】
    server_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_client.connect((server_ip, server_send_port))
    payload = "GET /delete_msg?message_id=" + str(msg_id) + " HTTP/1.1\r\nHost:" + str(
        server_ip) + ":" + str(server_send_port) + "\r\nConnection: close\r\n\r\n"
    server_client.send(payload.encode("utf-8"))
    print("【撤回】" + str(msg_id))
    server_client.close()
    return 0


def group_kick(group_id, user_id, reject_add_request='false'):  # 踢出成员【群号，QQ号，屏蔽加群申请】
    server_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_client.connect((server_ip, server_send_port))
    payload = "GET /set_group_kick?group_id=" + str(group_id) + "&user_id=" + str(user_id) + "&reject_add_request=" + str(
        reject_add_request) + " HTTP/1.1\r\nHost:" + str(server_ip) + ":" + str(server_send_port) + "\r\nConnection: close\r\n\r\n"
    server_client.send(payload.encode("utf-8"))
    print("【提示】群聊：" + str(group_id) + " 中，已踢出",
          str(user_id) + "，屏蔽加群申请：" + reject_add_request)
    server_client.close()
    return 0


def group_ban(group_id, user_id, duration=1):  # 禁言成员【群号，QQ号，禁言时长，单位：分】
    server_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_client.connect((server_ip, server_send_port))
    payload = "GET /set_group_ban?group_id=" + str(group_id) + "&user_id=" + str(user_id) + "&duration=" + str(
        int(duration)*60) + " HTTP/1.1\r\nHost:" + str(server_ip) + ":" + str(server_send_port) + "\r\nConnection: close\r\n\r\n"
    server_client.send(payload.encode("utf-8"))
    print("【提示】群聊：" + str(group_id) + " 中，已禁言 " + str(user_id), duration, "分钟")
    server_client.close()
    return 0


def group_whole_ban(group_id, enable='false'):  # 全体禁言【群号，是否启用(true/false】
    server_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_client.connect((server_ip, server_send_port))
    payload = "GET /set_group_whole_ban?group_id=" + str(group_id) + "&enable=" + str(
        enable) + " HTTP/1.1\r\nHost:" + str(server_ip) + ":" + str(server_send_port) + "\r\nConnection: close\r\n\r\n"
    server_client.send(payload.encode("utf-8"))
    print("【提示】群聊：" + str(group_id) + " 中，全体禁言已设为 " + str(enable))
    server_client.close()
    return 0


'''示例
send_msg('private', user_id,'你好') # 私聊消息
send_msg('group', group_id, '大家好') # 群聊消息
send_msg('group', group_id, '[CQ:face,id=174]') # #表情
4酷 5哭 12调皮 13呲牙 14微笑 15难过 20偷笑 27尴尬？ 31骂 32疑问 33嘘 
39再见 97擦汗 174摊手 176皱眉 178斜眼笑 212托腮
https://github.com/kyubotics/coolq-http-api/wiki/%E8%A1%A8%E6%83%85-CQ-%E7%A0%81-ID-%E8%A1%A8
语音[CQ:record,file=http://xxxx.com/1.mp3]艾特[CQ:at,qq=user_id]踢了踢[CQ:poke,qq={}]
链接分享[CQ:share,url=http://baidu.com,title=百度]
del_msg(msg_id) # 撤回消息【消息ID】
group_kick(group_id, user_id, false)  # 踢出成员【群号，QQ号，屏蔽加群申请】
group_ban(group_id, user_id, 1)  # 禁言成员【群号，QQ号，禁言时长，单位：分】
'''
