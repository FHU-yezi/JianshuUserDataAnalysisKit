from time import sleep

import colorama
from JianshuResearchTools.objects import User
from JianshuResearchTools.rank import GetAssetsRankData

from config import *
from db_config import *
from db_config import UserData

colorama.init(autoreset = True)

def print_green(text):
    print(colorama.Fore.GREEN + text)

def print_yellow(text):
    print(colorama.Fore.YELLOW + text)

def print_red(text):
    print(colorama.Fore.RED + text)


print("正在链接数据库")
db.connect()
print_green("连接数据库成功")
print("数据库名称：", DATABASE_NAME)

db.create_tables([UserData])
print_green("创建表成功")

def StoreDataListToDatabase(db, data_list):
    for item in data_list:  # 临时处理
        item["avatar_url"] = item["name"]
        item["FP_count"] = item["FP"]
        del item["name"]
        del item["FP"]
    UserData.insert_many(data_list).execute()

def BasicDataGetter(start_id):
    data = GetAssetsRankData(start_id)
    return data


def BasicDataGettingProcess():
    print_green("开始获取基础数据")
    print("共需请求", SIMPLE_DATA_REQUESTS_COUNT, "次")
    if SLEEP_TIME == 0:
        print_yellow("请注意，不设置请求间隔可能被封禁")
    for requests_count in range(SIMPLE_DATA_REQUESTS_COUNT):
        start_id = requests_count * 20 + 1  # JRT 是给人用的所以对起始值做了处理，但是这是程序
        data_list = BasicDataGetter(start_id)
        StoreDataListToDatabase(db, data_list)
        print_green(f"{start_id} 至 {start_id + 20} 的数据已成功保存到数据库")
        sleep(SLEEP_TIME)
    
    
def FullDataGettingProcess():
    print_green("开始获取完整数据")
    print_red("功能未实现")


def ChoiceBasicDataInfo():
    print("获取基础数据：")
    print("当前设置的数据数量：", TOTAL_DATA_COUNT)
    if input("您确认要开始获取吗？（输入 y 确认）\n>>>") == "y":
        BasicDataGettingProcess()
    else:
        exit()

def ChoiceFullDataInfo():
    print("获取完整数据：")
    print("当前设置的数据数量：", TOTAL_DATA_COUNT)
    if input("您确认要开始获取吗？（输入 y 确认）\n>>>") == "y":
        FullDataGettingProcess()
    else:
        exit()


while True:
    choice = input("请选择操作：\n1. 获取基础数据\n2. 获取完整数据\n>>>") 
    if choice == "1":
        ChoiceBasicDataInfo()
        break
    elif choice == "2":
        ChoiceFullDataInfo()
        break
    else:
        print_red("输入错误，请重新输入！")
