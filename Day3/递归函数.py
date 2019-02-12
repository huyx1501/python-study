
def calc(n):
    print(n)
    if int(n/2) > 0:
        return calc(int(n/2))
    return n


calc(12)