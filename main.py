from bin.settings_print import *
from bin.settings_load import *
from bin.read_txt import *
from bin.chat_mgt import *
from bin.receive import *

from datetime import datetime
from random import randint
from time import *

import threading

# 主程序 #

next_report_time = None  # 初始化下次消息报告时间
time_difference = None  # 初始化时差校准变量
next_task_time = None  # 初始化重置任务队列时间
del_msg_queue = []  # 初始化消息撤回队列
report_queue = []  # 初始化消息报告队列
task_queue = []  # 初始化任务队列

curfew_state = 0  # 初始化当前宵禁状态
ads_record = 0  # 初始化广告记录变量
bad_record = 0  # 初始化脏话记录变量
rev = None  # 初始化原始消息内容


def Task_Processing():  # 任务处理
    global time_difference, report_queue, task_queue, next_report_time, next_task_time, ads_record, bad_record, curfew_state
    while 1:
        sleep(0.3) # 避免电脑卡卡卡卡
        # 执行宵禁（定时全员禁言）
        if len(curfew_time) == 2 and group_manage != [] and time_difference != None:  # 如果有有效的宵禁时间，且有有效的群管范围,且时差已校准
            # 如果设置的开始时间小于结束时间（如16:00-17:00），即禁言1小时
            if int(curfew_time[0]) <= int(curfew_time[1]):
                # 如果现在时间大于开始时间且小于结束时间
                if int(strftime('%H%M', localtime(int(time())+int(time_difference)))) >= int(curfew_time[0]) and int(strftime('%H%M', localtime(int(time())+int(time_difference)))) <= int(curfew_time[1]):
                    if curfew_state == 0:  # 如果处于未禁言状态，执行全员警言，设置为当前处于宵禁状态
                        curfew_state = 1
                        for TEMP0 in group_manage:
                            group_whole_ban(TEMP0, 'true')
                elif curfew_state == 1:  # 如果不在宵禁时间内，且当前处于宵禁状态，解除全员禁言，设置为当前处于非宵禁状态
                    curfew_state = 0
                    for TEMP0 in group_manage:
                        group_whole_ban(TEMP0, 'false')
            # 如果设置的开始时间大于结束时间（如17:00-16:00），即禁言23小时
            elif int(curfew_time[0]) >= int(curfew_time[1]):
                # 如果现在时间大于开始时间且小于结束时间
                if int(curfew_time[0]) <= int(strftime('%H%M', localtime(int(time())+int(time_difference)))) or int(strftime('%H%M', localtime(int(time())+int(time_difference)))) <= int(curfew_time[1]):
                    if curfew_state == 0:  # 如果处于未禁言状态，执行全员警言，设置为当前处于宵禁状态
                        curfew_state = 1
                        for TEMP0 in group_manage:
                            group_whole_ban(TEMP0, 'true')
                elif curfew_state == 1:  # 如果不在宵禁时间内，且当前处于宵禁状态，解除全员禁言，设置为当前处于非宵禁状态
                    curfew_state = 0
                    for TEMP0 in group_manage:
                        group_whole_ban(TEMP0, 'false')

        if del_msg_queue != []:  # 如果消息撤回队列不为空，则执行消息撤回队列
            # 如果达到了撤回消息的时间
            if int(del_msg_queue[0]['time']) <= int(time()) + int(time_difference):
                del_msg(del_msg_queue[0]['message_id'])  # 撤回消息
                del del_msg_queue[0]  # 删除对应的消息队列

        if report_queue != []:  # 如果消息报告队列不为空
            if next_report_time <= int(time()) + int(time_difference):  # 如果达到了处理报告的时间
                if len(report_cycle) == 2:  # 如果有有效的报告周期（启用了消息报告）
                    if admin_user_id != []:  # 如果有机器人管理员
                        # 向每个管理员发送处理好的报告
                        for TEMP0 in admin_user_id:
                            send_msg_private(TEMP0, '以下为本周期的异常聊天报告：')
                            sleep(0.2)  # 延时（怕发的太快）纯属无聊
                        for TEMP1 in report_queue:
                            for TEMP2 in admin_user_id:
                                send_msg_private(TEMP2, '群聊：\n'+str(TEMP1['group_id'])+'\n用户：\n'+str(TEMP1['user_id'])+'\n次数：\n'+str(TEMP1['num'])+'\n时间：\n'+str(
                                    datetime.fromtimestamp(int(TEMP1['time'])))+'\n最后异常消息内容：\n'+str(TEMP1['message'][:100])+'\n（只显示前100字）')
                        next_report_time = int(time()) + int(time_difference) + randint(
                            int(report_cycle[0]), int(report_cycle[1]))  # 设置下次报告处理时间
                else:
                    next_report_time = int(
                        time()) + int(time_difference) + 60  # 设置下次报告处理时间
                report_queue = []  # 清空报告队列

        if task_queue != []:  # 如果任务队列不为空
            if next_task_time <= int(time()) + int(time_difference):  # 如果达到了重置任务的时间
                task_queue = []  # 清空任务队列
                next_task_time = int(time()) + \
                    time_difference + int(task_cycle) * 60


def Message_Processing():  # 消息处理
    global time_difference, report_queue, task_queue, next_report_time, next_task_time, ads_record, bad_record, curfew_state
    while 1:
        try:
            rev = rev_msg()
            if rev == None:
                continue
        except:
            continue

        # 校准服务器与本地时差
        time_difference = int(rev['time']) - int(time())

        # 设置首次报告发送时间和任务队列时间
        if next_report_time == None:  # 如果下次报告发送时间为空
            if len(report_cycle) == 2:  # 如果有有效的报告周期
                next_report_time = rev['time'] + \
                    randint(int(report_cycle[0]), int(report_cycle[1]))
            if next_task_time == None:  # 如果下次任务重置时间为空
                next_task_time = rev['time'] + int(task_cycle) * 60

        # 消息处理
        if rev["post_type"] == "message":  # 如果接收到的内容为消息，开始判断消息类型

            if rev["message_type"] == "group":  # 如果为群聊消息
                bad_record = 0  # 默认消息不含脏话
                ads_record = 0  # 默认消息不含广告
                for TEMP1 in group_manage:  # 检查群聊是否属于管理范围
                    if TEMP1 == str(rev['group_id']):  # 如果属于管理范围
                        if rev['sender']['role'] == 'member':  # 如果是群聊普通成员则需要进行消息检查
                            if bad_word != []:  # 如果启用了脏话检查
                                for TEMP0 in bad_word:  # 逐一匹配脏话词库
                                    if TEMP0 in rev["message"]:  # 如果检测到了脏话
                                        bad_record = 1  # 加入脏话消息记录
                                        # 执行相关（未完工）
                                        print('【注意】群聊：'+str(datetime.fromtimestamp(int(rev['time']))), str(rev['group_id']), '中，用户：'+str(
                                            rev['group_id']), '发送了脏话：'+str(rev['message'][:100])+'（只显示前100字）')
                                        break
                            if ads_word != []:  # 如果启用了广告检查
                                for TEMP0 in ads_word:  # 逐一匹配广告词库
                                    if TEMP0 in rev["message"]:  # 如果检测到了广告
                                        ads_record = 1  # 加入广告消息记录
                                        # 执行相关（未完工）
                                        print('【注意】群聊：'+str(datetime.fromtimestamp(int(rev['time']))), str(rev['group_id']), '中，用户：'+str(
                                            rev['group_id']), '发送了广告：'+str(rev['message'][:100])+'（只显示前100字）')
                                        break
                        else:
                            # 对方身份为群聊管理员或群主，请自定义
                            pass
                        break

                if ("[CQ:at,qq=" + str(bot_user_id) + "]" in rev["raw_message"]) and ads_record == 0 and bad_record == 0:  # 如果为正常内容且机器人被艾特
                    if admin_user_id != []:  # 如果有机器人管理员
                        for TEMP0 in admin_user_id:  # 逐一匹配发言的用户是否为机器人管理员
                            if TEMP0 == str(rev["user_id"]):  # 如果是机器人管理员
                                # 执行相关命令（管理员指令）
                                print(str(datetime.fromtimestamp(
                                    int(rev['time'])))+'【提示】：当前暂不支持机器人指令[群聊]（管理员）')
                                break
                    else:
                        # 执行相关命令（普通指令）
                        print(str(datetime.fromtimestamp(
                            int(rev['time'])))+'【提示】：当前暂不支持机器人指令[群聊]（普通用户）')
                        pass

                # 群聊消息结算
                if ads_record == 1 or bad_record == 1:  # 如果为不良消息
                    if del_msg_time != None:  # 如果启用了撤回消息
                        del_msg_queue.append(
                            {'time': int(rev['time']) + int(del_msg_time), 'message_id': rev['message_id']})  # 将不良消息添加到撤回队列

                    # 脏话提醒与广告提醒
                    if ads_word_tips != [] or bad_word_tips != []:  # 如果启用了广告提醒或脏话提醒
                        ads_tips_msg = ''  # 设置消息为空
                        bad_tips_msg = ''
                        tips_msg_symbol = ''
                        if ads_record == 1 and bad_record == 1:
                            tips_msg_symbol = '\n'
                        if ads_record == 1:
                            ads_tips_msg = "[CQ:at,qq="+str(rev['user_id'])+"]" + \
                                ads_word_tips[randint(0, len(ads_word_tips)-1)]
                        if bad_record == 1:
                            bad_tips_msg = "[CQ:at,qq="+str(rev['user_id'])+"]" + \
                                bad_word_tips[randint(0, len(bad_word_tips)-1)]
                        send_msg_group(
                            rev['group_id'], ads_tips_msg + tips_msg_symbol + bad_tips_msg)

                    # 消息报告队列
                    cycles_num = 0  # 重置循环数
                    for TEMP0 in report_queue:  # 消息报告队列中匹配是否已有记录
                        if rev['group_id'] == TEMP0['group_id'] and rev['user_id'] == TEMP0['user_id']:  # 如果已有记录
                            if ads_record == 1:  # 如果发送了广告，记录一次犯错
                                report_queue[cycles_num]['num'] += 1
                            if bad_record == 1:  # 如果发送了脏话，记录一次犯错
                                report_queue[cycles_num]['num'] += 1
                            # 更新最后消息时间
                            report_queue[cycles_num]['time'] = rev['time']
                            # 更新最后消息内容
                            report_queue[cycles_num]['message'] = rev['message']
                            break
                        else:
                            cycles_num += 1
                    else:  # 如果没有记录
                        report_queue.append({'group_id': rev['group_id'], 'user_id': rev['user_id'],
                                            'num': 0, 'time': rev['time'], 'message': rev['message']})  # 在队列末尾添加记录
                        if ads_record == 1:  # 如果发送了广告，记录一次犯错
                            report_queue[-1]['num'] += 1
                        if bad_record == 1:  # 如果发送了脏话，记录一次犯错
                            report_queue[-1]['num'] += 1

                    # 任务处理队列
                    cycles_num = 0  # 重置循环数
                    for TEMP0 in task_queue:  # 任务处理队列中匹配是否已有记录
                        if rev['group_id'] == TEMP0['group_id'] and rev['user_id'] == TEMP0['user_id']:  # 如果已有记录
                            if ads_record == 1:  # 如果发送了广告，记录一次犯错
                                task_queue[cycles_num]['num'] += 1
                            if bad_record == 1:  # 如果发送了脏话，记录一次犯错
                                task_queue[cycles_num]['num'] += 1
                            if gag_num != None:  # 如果有有效的初次禁言触发禁言数
                                # 如果犯错次数达到了禁言标准
                                if task_queue[cycles_num]['num'] >= int(gag_num):
                                    # 如果禁言次数超过了预设的最大禁言次数
                                    if len(gag_time) - 1 <= task_queue[-1]['gag_num']:
                                        # 根据禁言设置规则中最后的时间禁言
                                        group_ban(rev['group_id'],
                                                  rev['user_id'], gag_time[-1])
                                    else:
                                        # 根据禁言设置规则禁言
                                        group_ban(
                                            rev['group_id'], rev['user_id'], gag_time[task_queue[cycles_num]['gag_num']])
                                    # 记录已禁言次数
                                    task_queue[cycles_num]['gag_num'] += 1
                            if fault_num != None:  # 如果有有效的最大过失数
                                # 如果犯错次数达到了移出群聊标准
                                if task_queue[cycles_num]['num'] >= int(fault_num):
                                    group_kick(rev['group_id'],
                                               rev['user_id'])  # 将其移出群聊
                            break
                        else:
                            cycles_num += 1
                    else:  # 如果没有记录
                        task_queue.append(
                            {'group_id': rev['group_id'], 'user_id': rev['user_id'], 'num': 0, 'gag_num': 0})  # 在队列末尾添加记录
                        if ads_record == 1:  # 如果发送了广告，记录一次犯错
                            task_queue[-1]['num'] += 1
                        if bad_record == 1:  # 如果发送了脏话，记录一次犯错
                            task_queue[-1]['num'] += 1
                        if gag_num != None and gag_num == 1:  # 如果有有效的初次禁言触发禁言数,且触发数为1
                            group_ban(rev['group_id'], rev['user_id'],
                                      gag_time[0])  # 根据禁言设置规则禁言
                            task_queue[-1]['gag_num'] = 1  # 记录已禁言次数
                        if fault_num != None and fault_num == 1:  # 如果有有效的最大过失数,且触发数为1
                            group_kick(rev['group_id'],
                                       rev['user_id'])  # 将其移出群聊

            elif rev["message_type"] == "private":  # 否则，如果为私聊消息
                if admin_user_id != []:  # 如果有机器人管理员
                    for TEMP0 in admin_user_id:  # 逐一匹配发言的用户是否为机器人管理员
                        if TEMP0 == str(rev["user_id"]):  # 如果是机器人管理员
                            # 执行相关命令（管理员指令）
                            print(str(datetime.fromtimestamp(
                                int(rev['time'])))+'【提示】：当前暂不支持机器人指令[私聊]（管理员）')
                            break
                else:
                    # 执行相关命令（普通指令）
                    print(str(datetime.fromtimestamp(
                        int(rev['time'])))+'【提示】：当前暂不支持机器人指令[私聊]（普通用户）')
                    pass


# 双线程运行
t1 = threading.Thread(target=Message_Processing)
t2 = threading.Thread(target=Task_Processing)
if __name__ == '__main__':
    t1.start()
    t2.start()
    t1.join()
    t2.join()


'''
# 消息完全匹配
if rev['raw_message'].split(' ')[1]=='[CQ:face,id=212]':
    send_msg_group(rev['group_id'],'[CQ:poke,qq={}]'.format(rev['sender']['user_id']))
                
'''
