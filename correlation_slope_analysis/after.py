# -*- coding: utf-8 -*-
import os
# -*- coding: utf-8 -*-
import os
import math
import numpy
import time
import datetime


# DateTime
def GetDateArr_days(timeStart, timeEnd):
    TIME_Start = datetime.datetime.strptime(timeStart, "%Y-%m-%d")
    TIME_End = datetime.datetime.strptime(timeEnd, "%Y-%m-%d")
    dateArr = getDayByDay(TIME_Start, TIME_End)
    # print dateArr
    return dateArr


def GetDateArr_strdays(timeStart, timeEnd, fmt="%Y-%m-%d"):
    days = GetDateArr_days(timeStart, timeEnd)
    dateArr_str = []
    for d in days:
        dateArr_str.append(datetime.datetime.strftime(d, fmt))
    return dateArr_str


def getDayByDay(timeStart, timeEnd):
    oneday = datetime.timedelta(days=1)
    timeArr = [timeStart]
    while timeArr[len(timeArr) - 1] < timeEnd:
        tempday = timeArr[len(timeArr) - 1] + oneday
        timeArr.append(tempday)
    return timeArr


# Remove space(' ') and indent('\t') at the begin and end of the string
def StripStr(str):
    oldStr = ''
    newStr = str
    while oldStr != newStr:
        oldStr = newStr
        newStr = oldStr.strip('\t')
        newStr = newStr.strip(' ')
    return newStr


# Split string by spliter space(' ') and indent('\t') as default
def SplitStr(str, spliters=None):
    # spliters = [' ', '\t']
    # spliters = []
    # if spliter is not None:
    #     spliters.append(spliter)
    if spliters is None:
        spliters = [' ', '\t']
    destStrs = []
    srcStrs = [str]
    while True:
        oldDestStrs = srcStrs[:]
        for s in spliters:
            for srcS in srcStrs:
                tempStrs = srcS.split(s)
                for tempS in tempStrs:
                    tempS = StripStr(tempS)
                    if tempS != '':
                        destStrs.append(tempS)
            srcStrs = destStrs[:]
            destStrs = []
        if oldDestStrs == srcStrs:
            destStrs = srcStrs[:]
            break
    return destStrs


# Write file
def WriteLog(logfile, contentlist, MODE='replace'):
    if os.path.exists(logfile):
        if MODE == 'replace':
            os.remove(logfile)
            logStatus = open(logfile, 'w')
        else:
            logStatus = open(logfile, 'a')
    else:
        logStatus = open(logfile, 'w')
    if isinstance(contentlist, list) or isinstance(contentlist, tuple):
        for content in contentlist:
            logStatus.write("%s%s" % (content, '\r\n'))
    else:
        logStatus.write(contentlist)
    logStatus.flush()
    logStatus.close()


# Create forld
def createForld(forldPath):
    if not os.path.isdir(forldPath):
        os.makedirs(forldPath)


# Delete file
def DeleteFile(fp):
    if os.path.exists(fp):
        os.remove(fp)


# 创建类
class ClimateData:

    #  读取气象站点数据，格式化输出
    # （下载的原始逐日气象数据）

    def __init__(self, dir, dir_out, sid, fields, period, days):
        self.dataDir = dir
        self.dataDir_out = dir_out
        self.sid = sid
        self.period = period
        self.days = days
        self.fieldName = fields

        # code：数据类型，ind：数据索引号，frc：真值拉伸系数，ev:异常值阈值，详见气象数据说明文档
        self.fieldInfo = {
            "TEM": {"code": "12001", "ind": 7, "frc": 0.1, "ev": 30000},
            "TMX": {"code": "12001", "ind": 8, "frc": 0.1, "ev": 30000},
            "TMN": {"code": "12001", "ind": 9, "frc": 0.1, "ev": 30000},
            "PRE": {"code": "13011", "ind": 9, "frc": 0.1, "ev": 30000},  # 7:8-20 8:20-8 9:20-20
            "EVP": {"code": "13240", "ind": 7, "frc": 0.1, "ev": 1000},
            "RHU": {"code": "13003", "ind": 7, "frc": 1.0, "ev": 300},
            "WIN": {"code": "11002", "ind": 7, "frc": 0.1, "ev": 1000},
            "SSD": {"code": "14032", "ind": 7, "frc": 0.1, "ev": 99},
            "GST": {"code": "12030-0cm", "ind": 7, "frc": 0.1, "ev": 10000},
            "PRS": {"code": "10004", "ind": 7, "frc": 0.1, "ev": 20000}
        }
        # 全部数据
        self.data = {}
        # 数据日期
        self.data_date = {}
        # 存储逐年数据
        self.data_y = {}
        # 待提取日期数据
        self.data_d = {}

        # 获得日期数组
        self.GetDateArr()

        for i in self.fieldName:
            self.data[i] = []
            self.data_date[i] = []

        for t in self.years:
            self.data_y[t] = {}
            for i in self.fieldName:
                self.data_y[t][i] = []

        for d in self.days:
            self.data_d[d] = {}
            for i in self.fieldName:
                self.data_d[d][i] = 0

    def GetDateArr(self):
        '''
        # 根据起始日期，获得逐月日期
        #:return:
        '''
        self.date = []
        self.years = []
        startDT_y = int(self.period[0][0:4])
        startDT_m = int(self.period[0][4:6])
        endDT_y = int(self.period[1][0:4])
        endDT_m = int(self.period[1][4:6])

        if startDT_y == endDT_y:
            self.years.append(startDT_y)
            for j in range(startDT_m, endDT_m + 1):
                if j > 9:
                    self.date.append(str(startDT_y) + str(j))
                else:
                    self.date.append(str(startDT_y) + "0" + str(j))
        else:
            for i in range(startDT_y, endDT_y + 1):
                self.years.append(i)
                if i == startDT_y:
                    for j in range(startDT_m, 13):
                        if j > 9:
                            self.date.append(str(i) + str(j))
                        else:
                            self.date.append(str(i) + "0" + str(j))
                elif i < endDT_y:
                    for j in range(1, 13):
                        if j > 9:
                            self.date.append(str(i) + str(j))
                        else:
                            self.date.append(str(i) + "0" + str(j))
                else:
                    for j in range(1, endDT_m + 1):
                        if j > 9:
                            self.date.append(str(i) + str(j))
                        else:
                            self.date.append(str(i) + "0" + str(j))


########################分界线###################



if __name__ == "__main__":
    # 定义文件路径
    dataDir = r"D:\STUDY\data\meteology\00_20"
    dataDir_out = r"D:\STUDY\data\meteology\abstract"
    #dataDir_stations = rootDir + os.sep + r"D:\STUDY\data\meteology\00_20"


    sidArr = ["57947", "57957",	"59021", "59023", "59037", "59046", "59058", "59065",
              "59209", "59211", "59218", "59224", "59228", "59242", "59254", "59265", "59417",
              "59431", "59446", "59453", "59626", "59631", "59632", "59644", "59647", "57554",
              "57562", "57574", "57584", "57649", "57655", "57662", "57669", "57671", "57679",
              "57682", "57687", "57745", "57765", "57766", "57774", "57776", "57780", "57845",
              "57853", "57866", "57872", "57874", "57965", "57972", "57598", "57793", "57799",
              "57883", "57894", "57896", "57993", "58502", "58506", "58519", "58527", "58606",
              "58608", "58626", "58634", "58715", "58813", "59102"]  # 站号列表
    fields = ["TEM", "PRE", "EVP", "SSD"]  # 可选的提取变量列表
    START = "2000-01-01"  # 起始日期
    END = "2020-12-31"  # 终止日期

    period = [START.split('-')[0] + START.split('-')[1], END.split('-')[0] + END.split('-')[1]]
    period_days = GetDateArr_strdays(START, END)
    days = []

    '''逐站点提取数据
    for sid in sidArr:
        print(sid)

        # 计算起始搜索行数，提高提取速度
        sr = sidArr.index(sid) * 28

        c = ClimateData(dataDir, dataDir_out, int(sid), fields, period, days)
        c.ExtractData(sr=sr)
        c.SaveData(period_days, avg=False, d=False)
'''

# ## 合并多站点数据
stations_datadir = r"D:\STUDY\data\meteology\abstract"
outputfile = r"D:\STUDY\data\meteology\abstract1"

var_index = 0  # 变量索引号，对应数据提取结果中的变量位置

stations_data = {}
for sid in sidArr:
    stations_data[int(sid)] = []

for sid in sidArr:
    dataFile = stations_datadir + os.sep + str(int(sid)) + "_data_" + period[0] + "_" + period[1] + ".csv"
    print(dataFile)
    if (os.path.isfile(dataFile)):
        txtFile = open(dataFile, 'r')
        linesList = txtFile.read().split('\n')
        for k in range(1, len(linesList)):
            if len(linesList[k]) > 0:
                stationInfo = linesList[k].split(',')
                stations_data[int(sid)].append(float(stationInfo[var_index]))

print(stations_data[int(sidArr[0])])
stations_data_str = ""
stations_data_str += "date,"
for k in range(len(sidArr)):
    if k != len(sidArr) - 1:
        stations_data_str += "S%d," % int(sidArr[k])
    else:
        stations_data_str += "S%d\n" % int(sidArr[k])

for t in range(len(period_days)):
    stations_data_str += period_days[t] + ","
    for s in range(len(sidArr)):
        if s != len(sidArr) - 1:
            stations_data_str += "%.3f," % stations_data[int(sidArr[s])][t]
        else:
            stations_data_str += "%.3f\n" % stations_data[int(sidArr[s])][t]

print(stations_data_str)
def WriteLog(outputfile, stations_data_str):
    pass

WriteLog(outputfile, stations_data_str)
print("Finished!")