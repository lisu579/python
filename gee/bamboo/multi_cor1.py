import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import palettable
bamboo = pd.read_csv(r'D:\STUDY\data\test\Allometric2.csv')
graph = sns.pairplot(bamboo,
                     hue = "class",
                     palette=palettable.cartocolors.qualitative.Bold_9.mpl_colors,
                     kind='reg'  # 默认为scatter,reg加上趋势线
                     )
graph.fig.set_size_inches(12,12)

#sns.pairplot(data=bamboo, corner=True)
sns.set(style='whitegrid',font_scale=1.5)
#plt.tight_layout()
plt.show()