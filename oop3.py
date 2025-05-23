class Car :
    name = ""
    speed = 0
    count = 0

    def __init__(self, name, speed) :
        self.name = name
        self.speed = speed
        Car.count += 1

    def getName(self) :
        return self.name
    def getSpeed(self) :
        return self.speed

car1, car2 = None, None

car1 = Car("아우디", 0)
print("%s의 현재 속도는 %d, 생산된 자동차는 총 %d대입니다." % (car1.getName(),car1.getSpeed(),Car.count))
car2 = Car("벤츠", 30)
print("%s의 현재 속도는 %d, 생산된 자동차는 총 %d대입니다." % (car2.getName(),car2.getSpeed(),car2.count))
car3 = Car("테스트용", 0)
print("car2.count는 %d입니다." % (car2.count))