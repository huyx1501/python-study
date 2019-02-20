from conf import config
import time

date = time.strftime("%Y-%m-%d", time.localtime())
datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def logger(uid="", level="INFO", scene="", msg=""):
    data = "[%s] [%s] [UID=%s] [%s] - %s" % (datetime, level, uid, scene, msg)
    path = "%s\%s%s%s" \
           % (config.log_conf["log_path"], config.log_conf["log_prefix"], date, config.log_conf["log_suffix"])
    with open(path, "a", encoding="utf-8") as log:
        log.write(data)
        log.write("\n")
