import configparser

# 定义一个configparser对象
config = configparser.ConfigParser()

# 定义对象的段以及其内容（一个字典）
config["mysqld"] = {"port": "3306",
                    "socket": "/tmp/mysql.sock",
                    "basedir": "data/mysql/mysql.pid",
                    "user": "mysql",
                    "bind-address": "0.0.0.0",
                    "server-id": "1"}

config["client"] = {"port": "3306",
                    "socket": "/tmp/mysql.sock"}

config["mysqldump"] = {"max_allowed_packet": "16M"}

config["myisamchk"] = {"key_buffer_size": "8M",
                       "sort_buffer_size": "8M",
                       "read_buffer": "4M",
                       "write_buffer": "4M"}

# 打开一个文件句柄，将configparser对象写入
with open("my.cnf", "w") as cnf:
    config.write(cnf)

# 定义一个configparser对象用于读取
config_reader = configparser.ConfigParser()
# 读取配置文件
config_reader.read("my.cnf")
# 返回所有配置段
print(config_reader.sections())
# 返回指定段中的所有配置选项
print(config_reader.options("mysqld"))
# 以元组方式返回指定段中的所有配置项和值
print(config_reader.items("mysqld"))
# 取出指定配置项的值
print(config_reader["client"]["port"])
print(config_reader.get("client", "socket"))
# 遍历配置段内的字段和值
for key in config_reader["mysqld"]:
    print("%s : %s" % (key, config_reader["mysqld"][key]))

# 修改具体配置项
config_reader["client"]["port"] = "3307"
config_reader.set("client", "socket", "/var/run/mysql.sock")
# 删除配置段
config_reader.remove_section("mysqldump")
# 删除配置项
config_reader.remove_option("mysqld", "server-id")
# 插入段
if not config_reader.has_section("backup"):  # 判断段是否存在
    config_reader.add_section("backup")
# 插入配置项
if not config_reader.has_option("backup", "user"):  # 判断配置项是否存在
    config_reader.set("backup", "user", "backup_user")
# 重新写入文件
with open("my_new.cnf", "w") as new:
    config_reader.write(new)