number = int(input("1. 입력한 수식 계산 2.두 수 사이의 합계 :"))

if number == 1 :
    number1 = str(input("수식을 입력하세요 :"))
    number1_1 = eval(number1)
    print(number1,"결과는", number1_1,"입니다")
elif number == 2 :
    number2_1 = int(input("첫 번째 숫자를 입력하세요 :"))
    number2_2 = int(input("두 번째 숫자를 입력하세요 :"))
    number2_3 = (number2_1 + number2_2)/2*(number2_2 - number2_1 +1)
    print(number2_1, "+...+", number2_2, "는",number2_3, "입니다")