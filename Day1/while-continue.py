# -*- coding:utf-8 -*-
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
    if count == 3:
        choice = input("Do you want to continue? (y|n)")
        if choice == "y":
            count = 0
        else:
            print("exiting")