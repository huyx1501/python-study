target = 80
count = 0
while count < 3:
    number = int(input("Input a number:"))
    if number < target:
        print("Too small")
    elif number > target:
        print("Too big")
    else:
        print("Bingo")
        break
    count += 1
else:
    print("Too many times..")