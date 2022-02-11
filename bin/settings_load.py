from bin.read_txt import *

try: bot_user_id = str(Read_Txt('settings/basic/bot_user_id.txt')[1])
except: bot_user_id = ''
try: group_manage = Read_Txt('settings/basic/group_manage.txt')[1:7]
except: group_manage = []
try: admin_user_id = Read_Txt('settings/basic/admin_user_id.txt')[1:4]
except: admin_user_id = []
try: curfew_time = Read_Txt('settings/basic/curfew_time.txt')[1:3]
except: curfew_time = []
try: task_cycle = int(Read_Txt('settings/basic/task_cycle.txt')[1])
except: task_cycle = 4320
try: report_cycle = Read_Txt('settings/basic/report_cycle.txt')[1:3]
except: report_cycle = []

try: server_send_port = int(Read_Txt('settings/server/server_send_port.txt')[1])
except: server_send_port = 5700
try: server_rec_port = int(Read_Txt('settings/server/server_rec_port.txt')[1])
except: server_rec_port = 5701
try: server_ip = str(Read_Txt('settings/server/server_ip.txt')[1])
except: server_ip = '127.0.0.1'

try: del_msg_time = int(Read_Txt('settings/member/del_msg_time.txt')[1])
except: del_msg_time = None
try: gag_num = int(Read_Txt('settings/member/gag_num.txt')[1])
except: gag_num = None
try: fault_num = int(Read_Txt('settings/member/fault_num.txt')[1])
except: fault_num = None
try: gag_time = Read_Txt('settings/member/gag_time.txt')[1:65]
except: gag_time = [10]

try: ads_word = Read_Txt('settings/word/ads_word.txt')[1:257]
except: ads_word = []
try: bad_word = Read_Txt('settings/word/bad_word.txt')[1:257]
except: bad_word = []
try: ads_word_tips = Read_Txt('settings/chat/ads_word_tips.txt')[1:65]
except: ads_word_tips = []
try: bad_word_tips = Read_Txt('settings/chat/bad_word_tips.txt')[1:65]
except: bad_word_tips = []