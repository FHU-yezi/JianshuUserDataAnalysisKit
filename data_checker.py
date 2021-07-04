from datetime import datetime

from db_config import UserData, db
from print_with_color import print_green, print_red, print_yellow
from JianshuResearchTools.assert_funcs import AssertUserUrl
from JianshuResearchTools.convert import UserSlugToUserUrl
from time import sleep
from JianshuResearchTools.exceptions import InputError
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

TOTAL_DATA_COUNT = len(UserData.select(UserData))  # 获取基础数据总数

if TOTAL_DATA_COUNT == 0:
    raise Exception("数据库为空，请检查")

def CheckData(data):
    if data["uid"] == None:
        print_red("第 {} 名用户的 uid 为空".format(data["ranking"]))
    # if data["uslug"] != None and data["user_url"] == None:
    #     print_red("第 {} 名用户的 Slug 不为空，但其个人主页 Url 为空".format(data["ranking"]))
    if data["uslug"] != None and data["user_url"] != None:
        correct_url = UserSlugToUserUrl(data["uslug"])
        if correct_url != data["user_url"]:
            print_red("第 {} 名用户的 Slug 与 Url 不对应".format(data["ranking"]))
    if data["user_url"] != None:
        try:
            AssertUserUrl(data["user_url"])
        except InputError:
            print_red("第 {} 名用户的个人主页 Url 异常".format(data["ranking"]))
    if data["likes_count"] and data["likes_count"] < 0:
        print_red("第 {} 名用户的点赞数为负".format(data["ranking"]))
    if data["followers_count"] and data["followers_count"] < 0:
        print_red("第 {} 名用户的关注数为负".format(data["ranking"]))
    if data["fans_count"] and data["fans_count"] < 0:
        print_red("第 {} 名用户的粉丝数为负".format(data["ranking"]))
    if data["FP_count"] and data["FP_count"] < 0:
        print_red("第 {} 名用户的简书钻为负".format(data["ranking"]))
    if data["FTN_count"] and data["FTN_count"] < 0:
        print_red("第 {} 名用户的简书贝为负".format(data["ranking"]))
    if data["assets_count"] and data["assets_count"] < 0:
        print_red("第 {} 名用户的资产为负".format(data["ranking"]))
    if data["articles_count"] and data["articles_count"] < 0:
        print_red("第 {} 名用户的文章数为负".format(data["ranking"]))
    if data["wordage"] and data["wordage"] < 0:
        print_red("第 {} 名用户的总字数为负".format(data["ranking"]))

print(f"请确认数据集信息：\n数据总量：{TOTAL_DATA_COUNT}")

if input("开始进行数据校验？(y/n)\n>>>") != "y":
    exit()

with tqdm(total=TOTAL_DATA_COUNT) as bar:
    for ranking, data in enumerate(UserData.select(UserData).order_by(UserData.ranking).execute()):
        ranking += 1
        data = data.__dict__["__data__"]
        CheckData(data)
        bar.update(1)

print_green("全部数据校验完成！")