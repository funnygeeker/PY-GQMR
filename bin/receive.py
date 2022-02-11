# 接收上报的事件，感谢"皮小孩ls"的文章：https://blog.csdn.net/qq_44809707/article/details/119959864
# 但是，这不是最优解！！！！
import socket,json
from bin.settings_load import *
ListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ListenSocket.bind((server_ip, server_rec_port))
ListenSocket.listen(100)
HttpResponseHeader = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"

def request_to_json(msg):
    for i in range(len(msg)):
        if msg[i]=="{" and msg[-1]=="\n":
            return json.loads(msg[i:])
    return None
#需要循环执行，返回值为json格式
def rev_msg():# json or None
    Client, Address = ListenSocket.accept()
    Request = Client.recv(4096).decode(encoding='utf-8') # 我的能力有限，1.0.1的bug只能修到这了（1024=>4096）
    rev_json = request_to_json(Request)
    Client.sendall((HttpResponseHeader).encode(encoding='utf-8'))
    Client.close()
    #print(rev_json)
    return rev_json