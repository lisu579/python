
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

    # 逐站点提取数据
    for sid in sidArr:
        print(sid)

        # 计算起始搜索行数，提高提取速度
        sr = sidArr.index(sid) * 28

        c = ClimateData(dataDir, dataDir_out, int(sid), fields, period, days)
        c.ExtractData(sr=sr)
        c.SaveData(period_days, avg=False, d=False)
