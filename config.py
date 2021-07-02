TOTAL_DATA_COUNT = 100000  # 总数据条数
if TOTAL_DATA_COUNT % 20 != 0:
    raise Exception("总数据量必须是 20 的整数倍")
DATABASE_NAME = "UserData.db"  # 数据库名称
SIMPLE_DATA_REQUESTS_COUNT = int(TOTAL_DATA_COUNT / 20)
SLEEP_TIME = 0.03
REQUESTS_BEFORE_SAVE = 10  # 多少次数据获取保存一次

USER_PAGE_REQUEST_HEADER = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
}
USER_DATA_JSON_REQUEST_HEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57",
                          "X-INFINITESCROLL": "true",
                          "X-Requested-With": "XMLHttpRequest"}