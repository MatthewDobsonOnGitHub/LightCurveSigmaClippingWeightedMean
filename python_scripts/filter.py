import numpy as np

array_x=[5,1,7,4,3]
array_y=["nan",1,2,"nan",3]
n=0
for i in range(len(array_y)):
    if array_y[i]!=array_y[0]:
         n+=1
    else:
        continue
print(n)
x=np.zeros(n)
y=np.zeros(n)
s=0
for i in range (len(array_y)):
    if array_y[i]!=array_y[0]:
        x[s]=array_x[i]
        y[s]=array_y[i]
        s+=1
    else:
        continue
print(x,y)
