coffee = 0

coffee = int(input("어떤 커피 드릴까요?(1:보통,2:설탕,3:블랙)"))

print()
print("#1. 뜨거운 물을 준비한다.")
print("#2. 종이컵을 준비한다.")

if coffee == 1 :
    print("#2. 보통 커피를 탄다.")
elif coffee == 2 :
    print("#2. 설탕 커피를 탄다.")
elif coffee == 3 :
    print("#2. 블랙 커피를 탄다.")
else :
    print("#2. 아무 커피를 탄다.\n")