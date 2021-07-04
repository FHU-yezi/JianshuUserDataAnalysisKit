import json
from datetime import datetime
from time import sleep

import requests
from lxml import etree

from db_config import UserData, db
from getter_config import (DATABASE_NAME, FULL_DATA_FETCHES_BEFORE_SAVING,
                           FULL_GETTER_SLEEP_TIME,
                           USER_JSON_DATA_REQUEST_HEADER,
                           USER_PAGE_REQUEST_HEADER)
from print_with_color import print_green, print_red, print_yellow

print("正在连接数据库")
try:
    db.connect()
    db.create_tables([UserData])  # 如果表已存在则不会创建
except Exception as e:
    print_red("连接数据库失败")
    print(e)
    exit()
else:
    print_green("连接数据库成功")

def StoneDataListToDatabase(basic_data_list, full_data_list):
    for basic_data, full_data in zip(basic_data_list, full_data_list):
        UserData.update(**full_data).where(UserData.uid==basic_data["uid"]).execute()

def DataGetter(basic_data):
    result = basic_data
    if result["uslug"] == None:
        print_yellow("用户账号状态异常，已跳过")
        return result
    result["user_url"] = "".join(["https://www.jianshu.com/u/", basic_data["uslug"]])
    
    user_page_html_obj = etree.HTML(requests.get(result["user_url"], headers=USER_PAGE_REQUEST_HEADER).content)
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
    user_data_json_obj = json.loads(requests.get(result["user_url"].replace("https://www.jianshu.com/u/", 
                                                                       "https://www.jianshu.com/asimov/users/slug/"), 
                                                 headers=USER_JSON_DATA_REQUEST_HEADER).content)
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
        pass  # 没有开通会员
    try:
        result["introduction_text"] = "\n".join(etree.HTML(user_data_json_obj["intro"]).xpath("//*/text()"))
    except AttributeError:
        pass  # 没有设置简介
    return result

def ProcessDataList(data_list):
    # 目前这个函数什么都不做
    return data_list

FULL_DATA_COUNT = len(UserData)  # 获取基础数据总数
print(f"请确认数据获取配置：\n数据库文件名为 {DATABASE_NAME} \n共获取 {FULL_DATA_COUNT} 条数据\n\
等待时间为 {FULL_GETTER_SLEEP_TIME} 秒\n每 {FULL_DATA_FETCHES_BEFORE_SAVING} 条数据保存一次")

if input("开始获取完整数据？(y/n)\n>>>") != "y":
    exit()

print_green("开始获取完整数据")


# 初始化变量
unsaved_basic_data_list = []
unsaved_full_data_list = []

for ranking, basic_data in enumerate(UserData.select(UserData).order_by(UserData.ranking).execute()):
    ranking += 1  # range 从 0 开始
    basic_data = basic_data.__dict__["__data__"]
    
    full_data = DataGetter(basic_data)
    full_data = ProcessDataList(full_data)
    unsaved_basic_data_list.append(basic_data)
    unsaved_full_data_list.append(full_data)
    print(f"获取第 {ranking} 位用户的数据成功")
    
    if len(unsaved_full_data_list) == FULL_DATA_FETCHES_BEFORE_SAVING:
        StoneDataListToDatabase(unsaved_basic_data_list, unsaved_full_data_list)
        print_green("{} 条数据已成功保存".format(len(unsaved_full_data_list)))
        
        # 重置未保存数据列表
        unsaved_basic_data_list = []
        unsaved_full_data_list = []
    
    sleep(FULL_GETTER_SLEEP_TIME)

print_green("任务全部完成！")
db.close()
print_green("数据库已正常关闭！")
