# -*- coding: utf-8 -*-
import os

import numpy
import time
import datetime


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

    def ExtractData(self, sr=0):

        # Extract data
        #:param sr: start row numbers, default is 0
        #:return:

        print("Data extracting...")
        # Get date arr把time.clock()换掉了
        s_time = time.process_time()

        # 遍历每个数据类型
        for fn in self.fieldName:
            # 遍历逐月日期
            for dt in self.date:
                print(fn, dt)
                yr = int(dt[0:4])
                # 拼接字符串，组成数据文件路径
                field = fn
                if fn == "TMN" or fn == "TMX":
                    field = "TEM"

                fileName = self.dataDir + os.sep + "SURF_CLI_CHN_MUL_DAY-" + \
                           field + "-" + self.fieldInfo[fn]['code'] + "-" + dt + ".TXT"
                if not os.path.isfile(fileName):
                    raise Exception("Can not find %s" % fileName)
                else:
                    txtFile = open(fileName, 'r')
                    linesList = txtFile.read().split('\n')
                    iffind = False
                    hasdata = True
                    # 逐行遍历数据
                    for i in range(sr, len(linesList)):
                        if len(linesList[i]) > 0:
                            # 将每行数据拆成数组，按照索引提取数据
                            lineArr = SplitStr(linesList[i], spliters=' ')
                            if int(lineArr[0]) == self.sid:
                                iffind = True
                                # 将数据存储至数组
                                od = float(lineArr[self.fieldInfo[fn]['ind']])
                                # PRS 数值处理
                                if fn == "PRS":
                                    if od >= self.fieldInfo[fn]['ev']:
                                        od = -100
                                # PRE 数值处理
                                elif fn == "PRE":
                                    if od == 32766:
                                        od = -100
                                    elif od == 32700:
                                        od = 0
                                    elif od > 99999:
                                        od = 0
                                    else:
                                        od = od - int(od / 1000) * 1000
                                else:
                                    # 异常值处理,异常值用-100代替
                                    if od >= float(self.fieldInfo[fn]['ev']) / float(self.fieldInfo[fn]['frc']):
                                        # od = float(lineArr[int(self.fieldInfo[fn]['ind']) - arcpy])
                                        od = -100.

                                # 将处理结果添加至数据字典
                                if od != -100:
                                    self.data[fn].append(od * float(self.fieldInfo[fn]['frc']))
                                    self.data_y[yr][fn].append(od * float(self.fieldInfo[fn]['frc']))
                                else:
                                    self.data[fn].append(od)
                                    self.data_y[yr][fn].append(od)

                                # 保存对应的日期
                                data_date_str = lineArr[4] + "-" + lineArr[5] + "-" + lineArr[6]
                                data_date_date = datetime.datetime.strptime(data_date_str, "%Y-%m-%d")
                                data_date_fmt = datetime.datetime.strftime(data_date_date, "%Y-%m-%d")
                                self.data_date[fn].append(data_date_fmt)

                            # 遍历完所设置站点的日期后结束循环
                            if int(lineArr[0]) != self.sid and iffind:
                                break

                        # 如果未匹配到数据，做标记
                        if i == len(linesList) - 27 and not iffind:
                            hasdata = False
                            break

                    # 如果未匹配数据，用-9999填充
                    if not hasdata:
                        firstrow = SplitStr(linesList[0], spliters=' ')
                        s0 = firstrow[0]
                        for k in range(len(linesList)):
                            lineArr_s0 = SplitStr(linesList[k], spliters=' ')
                            if int(lineArr_s0[0]) == int(s0):
                                # 将-9999添加至数据字典
                                self.data[fn].append(-9999)
                                self.data_y[yr][fn].append(-9999)
                                # 保存对应的日期
                                data_date_str = lineArr_s0[4] + "-" + lineArr_s0[5] + "-" + lineArr_s0[6]
                                data_date_date = datetime.datetime.strptime(data_date_str, "%Y-%m-%d")
                                data_date_fmt = datetime.datetime.strftime(data_date_date, "%Y-%m-%d")
                                self.data_date[fn].append(data_date_fmt)
                            else:
                                break

        e_time = time.process_time()
        print("\t<Run time: %.3f s>" % (e_time - s_time))

    def SaveData(self, period_days, avg=True, d=True):
        '''
        #将提取的数据存储到文件
        #:param avg: 输出逐年平均数据
        #:return:
        '''
        print("Save as file...", end='')
        outStr = ""
        outStr += "date,"
        # 添加字段
        for s in range(len(self.fieldName)):
            if s != len(self.fieldName) - 1:
                outStr += self.fieldName[s] + ","
            else:
                outStr += self.fieldName[s] + "\n"
        # 先遍历天数，再遍历类型，逐日添加数据
        for k in range(len(self.data[self.fieldName[0]])):
            # outStr += period_days[k] + ","
            for s in range(len(self.fieldName)):
                if s == 0:
                    outStr += str(self.data_date[self.fieldName[s]][k]) + ","

                if s != len(self.fieldName) - 1:
                    outStr += str(self.data[self.fieldName[s]][k]) + ","
                else:
                    outStr += str(self.data[self.fieldName[s]][k]) + "\n"

        # Save
        createForld(self.dataDir_out)
        outputFile = self.dataDir_out + os.sep + str(self.sid) + "_data_" + self.period[0] + "_" + self.period[
            1] + ".csv"
        DeleteFile(outputFile)
        WriteLog(outputFile, outStr, MODE='append')

        # 输出逐年平均
        if avg:
            outStr = ""
            # 添加字段
            outStr += "DATE,"
            for s in range(len(self.fieldName)):
                if s != len(self.fieldName) - 1:
                    outStr += self.fieldName[s] + ","
                else:
                    outStr += self.fieldName[s] + "\n"

            # 先遍历年份，再遍历类型，逐日添加数据
            for yr in self.years:
                outStr += str(yr) + ","
                for s in range(len(self.fieldName)):
                    # 获取平均值
                    if self.fieldName[s] == "PRE":
                        # 降水求累加值
                        data_avg = numpy.sum(self.data_y[yr][self.fieldName[s]])
                    else:
                        data_avg = numpy.average(self.data_y[yr][self.fieldName[s]])

                    if s != len(self.fieldName) - 1:
                        outStr += str(data_avg) + ","
                    else:
                        outStr += str(data_avg) + "\n"

            outputFile_avg = self.dataDir_out + os.sep + str(self.sid) + "_data_" + self.period[0] + "_" + self.period[
                1] + "_avg.csv"
            DeleteFile(outputFile_avg)
            WriteLog(outputFile_avg, outStr, MODE='append')

        # 输出日数据
        if d:
            outStr = ""
            # 添加字段
            outStr += "DATE,"
            for s in range(len(self.fieldName)):
                if s != len(self.fieldName) - 1:
                    outStr += self.fieldName[s] + ","
                else:
                    outStr += self.fieldName[s] + "\n"

            # 先遍历年份，再遍历类型，逐日添加数据
            for d in self.days:
                outStr += str(d) + ","
                for s in range(len(self.fieldName)):
                    data_d = self.data_d[d][self.fieldName[s]]

                    if s != len(self.fieldName) - 1:
                        outStr += str(data_d) + ","
                    else:
                        outStr += str(data_d) + "\n"

            outputFile_d = self.dataDir_out + os.sep + "data_" + self.period[0] + "_" + self.period[1] + "_days.csv"
            DeleteFile(outputFile_d)
            WriteLog(outputFile_d, outStr, MODE='append')

        print("Completed!")


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


########################分界线###################


if __name__ == "__main__":
    # 定义文件路径
    dataDir = r"D:\STUDY\data\meteology\00_20"
    dataDir_out = r"D:\STUDY\data\meteology\after"
    dataDir_stations = r"D:\STUDY\data\meteology\after" + os.sep + r"D:\STUDY\data\meteology\待用\stations"

    sidArr = ["57947", "57957",	"59021"]  # 站号列表
    fields = ["TEM"]  # 可选的提取变量列表

    START = "2000-01-01"  # 起始日期
    END = "2000-12-31"  # 终止日期

    period = [START.split('-')[0] + START.split('-')[1], END.split('-')[0] + END.split('-')[1]]
    period_days = GetDateArr_strdays(START, END)
    days = []
'''
    # 逐站点提取数据
    for sid in sidArr:
        print(sid)

        # 计算起始搜索行数，提高提取速度
        sr = sidArr.index(sid) * 28

        c = ClimateData(dataDir, dataDir_out, int(sid), fields, period, days)
        c.ExtractData(sr=sr)
        c.SaveData(period_days, avg=False, d=False)
'''


# ## 合并多站点数据
stations_datadir =r"D:\STUDY\data\meteology\00_20"
outputfile = r"D:\STUDY\data\meteology\after1"
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
                stations_data[int(sid)].append(str(stationInfo[var_index]))

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
WriteLog(outputfile, stations_data_str)
print("Finished!")
