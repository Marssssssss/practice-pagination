import time
import random
import string
from pymongo import MongoClient, ASCENDING,DESCENDING


ES_HOST = 'http://localhost:9200'

# 分页参数
INDEX_NAME = "test"
PAGE_SIZE = 10  # 每页的文档数量
TOTAL_PAGES = 1000  # 要查询的总页数

# MongoDB 配置
MONGO_URI = 'mongodb://localhost:27017'


def create_docs(mongo_collection, num_docs):
    """ 创建 mongo 文档 """
    def random_string(length=10):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(length))

    for i in range(num_docs):
        doc = {
            'id': i,
            'name': random_string(random.randint(5, 15)),
            'value': random.randint(1, 100),
            'description': random_string(30)
        }
        insert_result = mongo_collection.insert_one(doc)


def test_mongo_base_pull(mongo_collection):
    """ mongo 基本拉取分页 """
    print("开始 MongoDB 分页查询...")
    start = time.time()
    for page in range(TOTAL_PAGES):
        start_time = time.time()
        cursor = mongo_collection.find().sort({"value": 1}).skip(page * PAGE_SIZE).limit(PAGE_SIZE)
        results = list(cursor)
        end_time = time.time()
    print(f"all_time: {time.time() - start}")


def test_mongo_cursor_pull(mongo_collection):
    """ 游标动态分页拉取 """
    print("开始动态分页查询")
    last_value = None
    last_id = None
    start = time.time()
    while True:
        if last_value:
            query = {
                "$or": [
                    {"value": {"$gt": last_value}}, 
                    {"value": last_value, "id": {"$gt": last_id}}
                ]
            }
        else:
            query = {}
        results = list(mongo_collection.find(query).sort({"value": 1, "id": 1}).limit(PAGE_SIZE))
        if not results:
            break
        last_value = results[-1]["value"]
        last_id = results[-1]["id"]
    print(f"all_time: {time.time() - start}")


def test_mongo_single_large_start_pull(mongo_collection):
    start = time.time()
    cursor = mongo_collection.find().sort({"_id": 1}).skip((TOTAL_PAGES - 1) * PAGE_SIZE).limit(PAGE_SIZE)
    results = list(cursor)
    print(f"all_time: {time.time() - start}")


if __name__ == "__main__":
    # 创建数据
    mongo_client = MongoClient(MONGO_URI)
    mongo_db = mongo_client[INDEX_NAME]
    if INDEX_NAME in mongo_db.list_collection_names():
        mongo_db.drop_collection(INDEX_NAME)
    mongo_collection = mongo_db[INDEX_NAME]
    create_docs(mongo_collection, PAGE_SIZE * TOTAL_PAGES)
    # 基本拉取
    # mongo_collection.create_index([("value", ASCENDING), ("id", DESCENDING)])
    mongo_collection.create_index([("value", ASCENDING)])
    mongo_collection.create_index([("id", ASCENDING)])
    test_mongo_base_pull(mongo_collection)
    # 超大数据量大页码单次拉取
    # test_mongo_single_large_start_pull(mongo_collection)
    test_mongo_cursor_pull(mongo_collection)

    
    indexes = mongo_collection.index_information()
    for index_name, index_info in indexes.items():
        print(f"Index Name: {index_name}")
        print(f"Index Info: {index_info}")
        print("--------")
