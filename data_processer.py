from copy import copy
from datetime import datetime
from time import sleep

from JianshuResearchTools.assert_funcs import AssertUserUrl
from JianshuResearchTools.convert import UserSlugToUserUrl
from JianshuResearchTools.exceptions import InputError
from tqdm import tqdm

from db_config import UserData, db
from print_with_color import print_green, print_red, print_yellow

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

def CheckAndProcessData(raw_data):
    processed_data = copy(raw_data)
    if raw_data["uslug"] != None and raw_data["user_url"] == None:
        print_red("第 {} 名用户的 Slug 不为空，但其个人主页 Url 为空".format(raw_data["ranking"]))
    if raw_data["uslug"] != None and raw_data["user_url"] != None:
        correct_url = UserSlugToUserUrl(raw_data["uslug"])
        if correct_url != raw_data["user_url"]:
            print_red("第 {} 名用户的 Slug 与 Url 不对应".format(raw_data["ranking"]))
    if raw_data["user_url"] != None:
        try:
            AssertUserUrl(raw_data["user_url"])
        except InputError:
            print_red("第 {} 名用户的个人主页 Url 异常".format(raw_data["ranking"]))
    if raw_data["likes_count"] and raw_data["likes_count"] < 0:
        print_red("第 {} 名用户的点赞数为负，已设为空值".format(raw_data["ranking"]))
        processed_data["likes_count"] = None
    if raw_data["followers_count"] and raw_data["followers_count"] < 0:
        print_red("第 {} 名用户的关注数为负，已设为空值".format(raw_data["ranking"]))
        processed_data["followers_count"] = None
    if raw_data["fans_count"] and raw_data["fans_count"] < 0:
        print_red("第 {} 名用户的粉丝数为负，已设为空值".format(raw_data["ranking"]))
        processed_data["fans_count"] = None
    if raw_data["FP_count"] and raw_data["FP_count"] < 0:
        print_red("第 {} 名用户的简书钻为负，已设为空值".format(raw_data["ranking"]))
        processed_data["FP_count"] = None
    if raw_data["FTN_count"] and raw_data["FTN_count"] < 0:
        print_red("第 {} 名用户的简书贝为负，已设为空值".format(raw_data["ranking"]))
        processed_data["FTN_count"] = None
    if raw_data["assets_count"] and raw_data["assets_count"] < 0:
        print_red("第 {} 名用户的资产为负，已设为空值".format(raw_data["ranking"]))
        processed_data["assets_count"] = None
    if raw_data["articles_count"] and raw_data["articles_count"] < 0:
        print_red("第 {} 名用户的文章数为负，已设为空值".format(raw_data["ranking"]))
        processed_data["articles_count"] = None
    if raw_data["wordage"] and raw_data["wordage"] < 0:
        print_red("第 {} 名用户的总字数为负，已设为空值".format(raw_data["ranking"]))
        processed_data["wordage"] = None
    return processed_data

print(f"请确认数据集信息：\n数据总量：{TOTAL_DATA_COUNT}")

if input("开始进行数据预处理？(y/n)\n>>>") != "y":
    exit()

with tqdm(total=TOTAL_DATA_COUNT) as bar:
    for data_obj in UserData.select(UserData).order_by(UserData.ranking).execute():
        raw_data = data_obj.__dict__["__data__"]
        processed_data = CheckAndProcessData(raw_data)
        if processed_data != raw_data:
            UserData.update(**processed_data).where(UserData.uid==raw_data["uid"]).execute()
        bar.update(1)

print_green("全部数据处理完成！")
