import json
from datetime import datetime
from time import sleep, time

import colorama
import requests
from JianshuResearchTools.objects import User
from JianshuResearchTools.rank import GetAssetsRankData
from lxml import etree

from config import *
from db_config import *

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

def UpdateDataInDatabase(db, basic_data, full_data):
    UserData.update(**full_data).where(UserData.uid==basic_data["uid"]).execute()

def BasicDataGetter(start_id):
    data = GetAssetsRankData(start_id)
    return data

def FullDataGetter(basic_data):
    result = basic_data
    result["url"] = "".join(["https://www.jianshu.com/u/", basic_data["uslug"]])
    
    user_page_html_obj = etree.HTML(requests.get(result["url"], headers=USER_PAGE_REQUEST_HEADER).content)
    if "您要找的页面不存在" in user_page_html_obj.xpath("//*/text()"):  # 用户账号状态异常
        print_yellow("用户账号状态异常，已跳过")
        return result
    try:
        result["FTN_count"] = float(user_page_html_obj.xpath("//div[@class='info']/ul/li[6]/div[@class='meta-block']/p")[0].text
                                    .replace(".", "").replace("w", "000"))
        result["assets_count"] = round(abs(result["FP_count"] + result["FTN_count"]), 3)
    except IndexError:
        print_yellow("获取用户资产失败，已跳过")
        
    result["badges"] = user_page_html_obj.xpath("//li[@class='badge-icon']/a/text()")
    result["badges"] = [item.replace(" ", "").replace("\n", "") for item in result["badges"]]  # 移除空格和换行符
    result["badges"] = [item for item in result["badges"] if item != ""]  # 去除空值
    result["articles_count"] = int(user_page_html_obj.xpath("//div[@class='info']/ul/li[3]/div[@class='meta-block']/a/p")[0].text)
    user_data_json_obj = json.loads(requests.get(result["url"].replace("https://www.jianshu.com/u/", 
                                                                       "https://www.jianshu.com/asimov/users/slug/"), 
                                                 headers=USER_DATA_JSON_REQUEST_HEADER).content)
    result["gender"] = {
        0: "未知（0）", 
        1: "男", 
        2: "女", 
        3: "未知（3）"
    }[user_data_json_obj["gender"]]
    result["followers_count"] = user_data_json_obj["following_users_count"]
    result["fans_count"] = user_data_json_obj["followers_count"]
    result["wordage"] = user_data_json_obj["total_wordage"]
    result["likes_count"] = user_data_json_obj["total_likes_count"]
    result["last_update_time"] = datetime.fromtimestamp(user_data_json_obj["last_updated_at"])
    try:
        result["vip_type"] = {
                                "bronze": "铜牌",
                                "silver": "银牌" , 
                                "gold": "黄金", 
                                "platina": "白金"
                            }[user_data_json_obj["member"]["type"]]
        result["vip_expire_date"] = datetime.fromtimestamp(user_data_json_obj["member"]["expires_at"])
    except KeyError:
        pass
    try:
        result["introduction_text"] = "\n".join(etree.HTML(user_data_json_obj["intro"]).xpath("//*/text()"))
    except AttributeError:
        print("用户没有简介，已跳过")
    return result


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
    print("共需请求", TOTAL_DATA_COUNT, "次")
    if SLEEP_TIME == 0:
        print_yellow("请注意，不设置请求间隔可能被封禁")
    for ranking, basic_data in enumerate(UserData.select(UserData).order_by(UserData.ranking).execute()):
        ranking += 1
        basic_data = basic_data.__dict__["__data__"]
        full_data = FullDataGetter(basic_data)
        print(f"成功获取第 {ranking} 位用户的完整信息")
        UpdateDataInDatabase(db, basic_data, full_data)
        print_green(f"第 {ranking} 位用户的完整信息已成功保存")
    print_green("全部任务完成！")
    db.close()
    print_green("数据库已正常关闭！")


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
