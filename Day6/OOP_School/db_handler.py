import pickle
import os


def save_info(obj, obj_name):
    """
    使用pickle保存对象到文件
    :param obj: 要保存的对象
    :param obj_name:  对象名，用于确定存储时的文件名
    :return: None
    """
    path = os.path.join("db", "%s.data" % obj_name)  # 根据对象名组织文件路径
    with open(path, "wb") as f:
        pickle.dump(obj, f)  # 使用pickle模块讲对象存入文件
        f.flush()  # 强制刷新文件到硬盘


def load_info(obj_name):
    """
    根据对象名读取文件
    :param obj_name:  要读取的对象名称
    :return:  返回读取到的对象
    """
    path = os.path.join("db", "%s.data" % obj_name)
    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:  # 如果指定的对象存储文件不存在在返回None
        return None
    except Exception as e:
        print("打开文件失败", e)
        return None
