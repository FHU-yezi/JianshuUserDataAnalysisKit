# 全局设置
DATABASE_NAME = "UserData.db"

# 基础数据获取设置
BASIC_DATA_COUNT = 100000
BASIC_GETTER_SLEEP_TIME = 0.03
BASIC_DATA_FETCHES_BEFORE_SAVING = 30

# 完整数据获取设置
FULL_GETTER_SLEEP_TIME = 0.03
FULL_DATA_FETCHES_BEFORE_SAVING = 30
USER_PAGE_REQUEST_HEADER = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
}
USER_JSON_DATA_REQUEST_HEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57",
                          "X-INFINITESCROLL": "true",
                          "X-Requested-With": "XMLHttpRequest"}