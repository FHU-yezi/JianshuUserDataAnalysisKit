TOTAL_DATA_COUNT = 100000  # 总数据条数
if TOTAL_DATA_COUNT % 20 != 0:
    raise Exception("总数据量必须是 20 的整数倍")
DATABASE_NAME = "UserData.db"  # 数据库名称
SIMPLE_DATA_REQUESTS_COUNT = int(TOTAL_DATA_COUNT / 20)
SLEEP_TIME = 0