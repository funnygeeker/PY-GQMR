import time
from bin.settings_load import *
print('--------------------正在初始化--------------------')
print('--【欢迎使用：极客街社群-Q群协管-V1.0.3_120222】--')
print('作者Github：https://www.github.com/funnygeeker')
print('作者B站个人主页：https://b23.tv/b39RG2r')
print('作者技术社区官网：https://geekjie.com')
print('作者联系邮箱：yangcmd@qq.com')
print('Python小白早期作品，不喜勿喷')
time.sleep(2)
print('---------------------基本设置---------------------')
print('机器人QQ号:', bot_user_id)
print('需要管理的QQ群:', group_manage)
print('机器人管理员QQ号:', admin_user_id)
print('群聊宵禁时间范围:', curfew_time)
print('撤回禁言等任务执行周期:', task_cycle, '分')
print('异常场聊天报告发送周期:', report_cycle, '秒')
time.sleep(2)
print('---------------------服务设置---------------------')
print('GO-CQHTTP发送端口:', server_send_port)
print('GO-CQHTTP接收端口:', server_rec_port)
print('GO-CQHTTP服务所在IP:', server_ip)
time.sleep(2)
print('---------------------成员设置---------------------')
print('成员消息撤回间隔:', del_msg_time, '秒')
print('成员首次禁言次数:', gag_num, '次')
print('成员最大犯错次数:', fault_num, '次')
print('成员禁言规则列表:', gag_time)
time.sleep(2)
print('---------------------群管词库---------------------')
print('广告词库:', ads_word)
print('脏话词库:', bad_word)
print('广告消息提示:', ads_word_tips)
print('脏话消息提示:', bad_word_tips)
print('-----------------配置文件加载完毕-----------------')
time.sleep(1)
print('【信息】群聊协管机器人启动完成......')