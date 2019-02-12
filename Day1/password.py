import getpass

username = input("Username:")
password = getpass.getpass("Password:")

_username = "Bob"
_password = "123456"

if _username == username and _password == password :
    print("Welcome")
else:
    print("ERROR")


