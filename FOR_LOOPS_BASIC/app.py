for i in range(151):
    print(i)
    
for i in range(5,1000):
    print (i)
    
for i in range(1, 101):
    if i % 10 == 0:
        print("Coding Dojo")
    elif i % 5 == 0:
        print("Coding")
    else:
        print(i)
num =  0
for i in range(1,500000,2):
    num += i
    print(num)
    num = 2018
while num > 0:
    print(num)
    num -= 4

lowNum = 2
highNum = 9
mult = 3

for i in range(lowNum, highNum + 1):
    if i % mult == 0:
        print(i)