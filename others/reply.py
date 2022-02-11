from bin.receive import *
from bin.chat_mgt import *
while True:
    try:
        rev = rev_msg()
        print(rev)
        if rev == None:
            continue
    except:
        continue
    if rev["post_type"] == "message":
        #print(rev) #需要功能自己DIY
        if rev["message_type"] == "private": #私聊
            if rev['raw_message']=='在吗':
                qq = rev['sender']['user_id']
                send_msg({'msg_type':'private','number':qq,'msg':'我不在'})
                print(rev_msg())
        elif rev["message_type"] == "group": #群聊
            group = rev['group_id']
            if "[CQ:at,qq=" + str(bot_user_id) + "]" in rev["raw_message"]:
                if rev['raw_message'].split(' ')[1]=='测试':
                    qq=rev['sender']['user_id']
                    send_msg({'msg_type':'group','number':group,'msg':'[CQ:poke,qq={}]'.format(qq)})
                    
                else:
                    del_msg(rev["message_id"])#撤回消息
        else:
            continue
    else:  # rev["post_type"]=="meta_event":
        continue