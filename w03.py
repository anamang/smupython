print("입력 진수 결정(16/10/8/2) : ")
alpha=int(input())

print("값입력 : ")
num=input()

num1=False

if alpha==16:
    num1 = int(num,16)
elif alpha==10:
    num1 = int(num,10)
elif alpha==8:
    num1 = int(num,8)
elif alpha==2:
    num1 = int(num,2)
else:
    print("(16/10/8/2)진수만 가능합니다".format(alpha,num,num1)) #진수 확인

if type(num1) is int:
    print("16진수   ==>", hex(int(num1)))
    print("10진수   ==>", num1)
    print("8진수    ==>", oct(int(num1)))
    print("2진수    ==>", bin(int(num1)).format(alpha,num,num1))