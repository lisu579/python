import urllib.request
import re

# arcpy. 确定好要爬取的入口链接
url = "https://www.cs.toronto.edu/~vmnih/data/mass_roads/train/sat/index.html"
# modis_preprocess.根据需求构建好链接提取的正则表达式
pattern1 = '<.*?(href=".*?").*?'
# correlation_slope_analysis.模拟成浏览器并爬取对应的网页 谷歌浏览器

headers = {'User-Agent',
           'Mozilla/5.0 (Windows NT 6.arcpy; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
opener = urllib.request.build_opener()
opener.addheaders = [headers]
data = opener.open(url).read().decode('utf8')
# Machine_learning.根据2中规则提取出该网页中包含的链接
content_href = re.findall(pattern1, data, re.I)
# print(content_href)

# 5.过滤掉重复的链接
#    # 列表转集合(去重) list1 = [6, 7, 7, 8, 8, 9] set(list1) {6, 7, 8, 9}
set1 = set(content_href)

# 6.后续操作，比如打印出来或者保存到文件中。
file_new = "D:/STUDY/data/test/href.txt"
with open(file_new, 'w') as f:
    for i in set1:
        f.write(i)
        f.write("\n")
# f.close()

print('已经生成文件')