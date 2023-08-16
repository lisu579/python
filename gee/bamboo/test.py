import pandas as pd
import matplotlib.pyplot as plt


# create data
data = pd.read_csv(r'D:\STUDY\data\test\Allometric2.csv')
x=data['Allometric2'].values.ravel()
y=data['AGB_Avi'].values.ravel()

# Big bins
plt.hist2d(x, y, bins=(50, 50), cmap=plt.cm.jet)
plt.show()

# Small bins
plt.hist2d(x, y, bins=(300, 300), cmap=plt.cm.jet)
plt.show()

# If you do not set the same values for X and Y, the bins won't be a square!
plt.hist2d(x, y, bins=(300, 30), cmap=plt.cm.jet)
plt.show()