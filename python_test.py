order_detail = []

def make_oder(name, qty):
    order_detail.append({"이름": name, "수량": qty})

print(order_detail)
make_oder("아메리카노", 2)
make_oder("플랫 화이트", 1)
print(order_detail)