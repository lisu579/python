# -*- coding: utf-8 -*-
import os
import math
import numpy
import time
import datetime


if __name__ == "__main__":
    dataDir = < data
    direction >
    dataDir_out = < output
    direction >
    dataDir_stations = rootDir + os.sep + r"NE_China\data\stations"

    sidArr = ["53463", "53478", "53480", "53487"]
    fields = ["TEM", "TMN", "TMX", "PRE", "RHU", "WIN", "PRS", "SSD"]

    START = "2000-01-01"
    END = "2018-12-31"

    period = [START.split('-')[0] + START.split('-')[1], END.split('-')[0] + END.split('-')[1]]
    period_days = GetDateArr_strdays(START, END)
    days = []

    # ## 逐站点提取数据
    for sid in sidArr:
        print(sid)

        # 计算起始搜索行数，提高提取速度
        sr = sidArr.index(sid) * 28

        c = ClimateData(dataDir, dataDir_out, int(sid), fields, period, days)
        c.ExtractData(sr=sr)
        c.SaveData(period_days, avg=False, d=False)