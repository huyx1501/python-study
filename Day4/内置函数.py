
def deco():
    def test():
        print("Hello")
    return  test

print(deco())
