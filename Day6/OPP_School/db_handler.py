import pickle
import os


def save_info(obj):
    path = os.path.join("db", "%s.data" % obj.name)
    with open(path, "w") as f:
        return pickle.dumps(f)


def load_info():
    files = os.listdir("db")
    for item in files:
        path = os.path.join("db", item)
        with open(path, "r") as f:
            pass


def school_list():
    pass
