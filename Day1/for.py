target = 80
count = 0
for i in range(3):
    number = int(input("Input a number:"))
    if number < target:
        print("Too small")
    elif number > target:
        print("Too big")
    else:
        print("Bingo")
        break
else:
    print("Too many times..")
