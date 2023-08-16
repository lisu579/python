# 导入sympy库
from sympy import symbols,sin,plot
# 定义幂函数
def func(x,y):
   return x**y
# 定义数学符号x,y
x=symbols('x')
y=symbols('y')
# 生成y=x函数公式
f1=func(x,5.555)
# 绘制图形
plot(f1,(x,-10,10))
