from time import sleep

from JianshuResearchTools.rank import GetAssetsRankData

from db_config import UserData, db
from getter_config import (BASIC_DATA_COUNT, BASIC_DATA_FETCHES_BEFORE_SAVING,
                           BASIC_GETTER_SLEEP_TIME, DATABASE_NAME)
from print_with_color import print_green, print_red

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

if BASIC_DATA_COUNT % 20 != 0:
    raise Exception("数据量必须是 20 的整数倍，请检查配置文件")

def StoneDataListToDatabase(data_list):
    UserData.insert_many(data_list).execute()

def DataGetter(start_id):
    data = GetAssetsRankData(start_id)
    return data

def ProcessDataList(data_list):
    for data in data_list:
        # JRT 问题，暂时避开
        data["assets_count"] = data["FP"]
        del data["FP"]
    return data_list

print(f"请确认数据获取配置：\n数据库文件名为 {DATABASE_NAME} \n共获取 {BASIC_DATA_COUNT} 条数据\n\
等待时间为 {BASIC_GETTER_SLEEP_TIME} 秒\n每 {BASIC_DATA_FETCHES_BEFORE_SAVING} 条数据保存一次")

if input("开始获取基础数据？(y/n)\n>>>") != "y":
    exit()

print_green("开始获取基础数据")


# 初始化变量
unsaved_data_list = []

for count in range(int(BASIC_DATA_COUNT / 20)):
    count += 1  # range 从 0 开始
    start_id = count * 20 - 20 + 1
    
    data_list = DataGetter(start_id)
    data_list = ProcessDataList(data_list)
    unsaved_data_list.append(data_list)
    print(f"第 {count} 次({start_id} - {start_id + 20 -1})数据获取成功")
    
    if len(unsaved_data_list) == BASIC_DATA_FETCHES_BEFORE_SAVING:
        data_list_to_save = sum(unsaved_data_list, [])  # 合并列表
        StoneDataListToDatabase(data_list_to_save)
        print_green("{} 条数据已成功保存".format(len(data_list_to_save)))
        del data_list_to_save  # 释放内存
        unsaved_data_list = []  # 重置未保存数据列表
    
    sleep(BASIC_GETTER_SLEEP_TIME)

print_green("任务全部完成！")
db.close()
print_green("数据库已正常关闭！")
