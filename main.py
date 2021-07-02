from time import sleep

import colorama
import requests
from JianshuResearchTools.objects import User
from JianshuResearchTools.rank import GetAssetsRankData
from lxml import etree

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
    for item in data_list:
        item["FP_count"] = item["FP"]
        del item["FP"]
    UserData.insert_many(data_list).execute()

def BasicDataGetter(start_id):
    data = GetAssetsRankData(start_id)
    return data

def FullDataGetter(basic_data):
    result = basic_data
    result["url"] = "".join(["https://www.jianshu.com/u/"), basic_data["uslug"]])
    


def BasicDataGettingProcess():
    print_green("开始获取基础数据")
    print("共需请求", SIMPLE_DATA_REQUESTS_COUNT, "次")
    if SLEEP_TIME == 0:
        print_yellow("请注意，不设置请求间隔可能被封禁")
    data_list = []
    requests_after_save = 0
    start_id_when_save = 1
    for requests_count in range(SIMPLE_DATA_REQUESTS_COUNT):
        start_id = requests_count * 20 + 1  # JRT 是给人用的所以对起始值做了处理，但是这是程序
        request_data_list = BasicDataGetter(start_id)
        print(f"{start_id - 1} 至 {start_id + 20 - 1} 的数据获取成功")
        requests_after_save += 1
        data_list = data_list + request_data_list
        if requests_after_save == REQUESTS_BEFORE_SAVE:
            StoreDataListToDatabase(db, data_list)
            print_green(f"{start_id_when_save - 1} 至 {start_id_when_save + len(data_list) - 1} 的数据已成功保存")
            data_list = []
            start_id_when_save = start_id + 20
            requests_after_save = 0
        sleep(SLEEP_TIME)
    print_green("全部任务完成！")
    db.close()
    print_green("数据库已正常关闭！")
    
    
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
