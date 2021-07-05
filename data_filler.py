from copy import copy
from JianshuResearchTools.user import GetUserArticlesInfo, GetUserFansInfo, GetUserFollowersInfo
from print_with_color import print_green, print_red, print_yellow

from db_config import UserData, db
from tqdm import tqdm

print("正在连接数据库")
try:
    db.connect()
except Exception as e:
    print_red("连接数据库失败")
    print(e)
    exit()
else:
    print_green("连接数据库成功")

TOTAL_DATA_COUNT = len(UserData)  # 获取基础数据总数

if TOTAL_DATA_COUNT == 0:
    raise Exception("数据库为空，请检查")

def GetUserRealArticlesCount(user_url):
    page = 1
    result = 0
    while True:
        data = GetUserArticlesInfo(user_url, page, 500)
        if data == []:
            break
        else:
            result += len(data)
            page += 1
    return result

def GetUserRealFollowersCount(user_url):
    page = 1
    result = 0
    while True:
        data = GetUserFollowersInfo(user_url, page)
        if data == []:
            break
        else:
            result += len(data)
            page += 1
    return result

def GetUserRealFansCount(user_url):
    page = 1
    result = 0
    while True:
        data = GetUserFansInfo(user_url, page)
        if data == []:
            break
        else:
            result += len(data)
            page += 1
    return result

def FillUserData(raw_data):
    if raw_data["FTN_count"] == None:
        return raw_data  # 用户账号状态异常，跳过获取过程
    filled_data = copy(raw_data)
    if raw_data["user_url"] != None and raw_data["articles_count"] == None:
        filled_data["articles_count"] = GetUserRealArticlesCount(raw_data["user_url"])
        print("第 {} 位用户的文章数填充成功".format(raw_data["ranking"]))
    if raw_data["user_url"] != None and raw_data["followers_count"] == None:
        filled_data["followers_count"] = GetUserRealFollowersCount(raw_data["user_url"])
        print("第 {} 位用户的关注数填充成功".format(raw_data["ranking"]))
    if raw_data["user_url"] != None and raw_data["fans_count"] == None:
        filled_data["fans_count"] = GetUserRealFansCount(raw_data["user_url"])
        print("第 {} 位用户的粉丝数填充成功".format(raw_data["ranking"]))
        
    return filled_data

print(f"请确认数据集信息：\n数据总量：{TOTAL_DATA_COUNT}")

if input("开始进行数据填充？(y/n)\n>>>") != "y":
    exit()
    
with tqdm(total=TOTAL_DATA_COUNT) as bar:
    for data_obj in UserData.select(UserData).order_by(UserData.ranking).execute():
        raw_data = data_obj.__dict__["__data__"]
        filled_data = FillUserData(raw_data)
        if filled_data != raw_data:
            UserData.update(**filled_data).where(UserData.uid==raw_data["uid"]).execute()
            print_green("第 {} 名用户的数据已更新".format(raw_data["ranking"]))
            print("更新后的数据：文章 {} 篇，关注 {} 人，粉丝 {} 人".format(
                filled_data["articles_count"], filled_data["followers_count"], filled_data["fans_count"]))
        bar.update(1)

print_green("全部数据填充完成！")
db.close()
print_green("数据库已正常关闭！")