# -*- coding: utf-8 -*-
"""[summary]
表情控制 rhubarb-lip-sync
初值 = 127,0,0,209,102,51,86,79,79,147,99,155
A = '127,0,0,209,102,51,86,79,79,147,99,155' # 闭嘴,拼音p,b,m.A和X基本相同
B = '127,0,0,209,102,110,86,79,79,147,99,155' # 嘴巴微微张开，咬紧牙关
C = '127,0,0,209,102,180,86,79,79,147,99,155' # 嘴巴张一半
D = '127,0,0,209,102,255,86,79,79,147,99,155' # 嘴巴张最大
E = '127,0,0,209,102,255,255,79,79,147,99,155' # 嘴巴o形
F = '127,109,0,209,102,160,168,79,79,147,99,155' # 撅起嘴

G = '127,0,0,209,102,90,86,79,79,147,99,155' # 不用f，v发音
H = '127,0,0,209,102,255,86,79,79,147,99,155' # 介于CD之间
X = '127,0,0,209,102,51,86,79,79,147,99,155' # 和A基本相同，但要比A放松
"""

import numpy as np
np.set_printoptions(threshold = 1e6) 
import time

# struct_time = time.strptime("30 Nov 00", "%d %b %y")
# print("返回的元组: "+str(struct_time))

st = "00:00:12"
et = "9:33:33"

# time to seconds


def t2s(t):
    h, m, s = t.strip().split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)


print(t2s(st))


# seconds to time
def s2t(seconds):
    s, ms = divmod(seconds, 30)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return ("%02d:%02d:%02d.%02d" % (h, m, s, ms))


# 获取output音频长度和行数
file = np.loadtxt('output.txt', dtype=np.str)
sound_lengh = file[len(file)-1][0]
rows = len(file)
print("sound_lengh:", sound_lengh)
print("lines:", rows)

# 读入文件内容
emotion_file = open("output.txt", "r")
emotion_file2 = open("output2.txt", "w")
data_list = []
for line in emotion_file.readlines():
    data_list.append(line.replace("\n", "").split("\t"))

for i in range(rows):
    print(data_list[i][0].split("."))
print(data_list)


# 机器人表情脚本时间序列
seconds = float(sound_lengh) * 100 + 1

time = np.empty(shape=[0, 2], dtype=str)
s = "127,0,0,209,102,51,86,79,79,147,99,155,"
# 初始化时间
for i in range(int(seconds)):
    time = np.append(time, [[s2t(i), s]], axis=0)
# 插入表情
for i in range(int(seconds)):
    for j in range(rows):
        if data_list[j][0] == time[i][0].split(":")[2]:
            time[i][1] = data_list[j][1]
    # print(s2t(i)+", 128,128,128,128,128,128,128,128,128,128,128,128")
print("结果")
print(time)

np.savetxt('test.out.txt', time, delimiter=', ', fmt='%s')



emotion_file.close()
