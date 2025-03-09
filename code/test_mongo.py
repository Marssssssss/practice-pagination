import time
import random
import string
from pymongo import MongoClient


ES_HOST = 'http://localhost:9200'

# 分页参数
INDEX_NAME = "test"
PAGE_SIZE = 10  # 每页的文档数量
TOTAL_PAGES = 500  # 要查询的总页数

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
        insert_result = collection.insert_one(doc)
        print(f"文档 {insert_result.inserted_id} 插入成功: {doc}")


def test_mongo_base_pull(mongo_collection):
    """ mongo 基本拉取分页 """
    print("开始 MongoDB 分页查询...")
    for page in range(TOTAL_PAGES):
        start_time = time.time()
        cursor = mongo_collection.find().skip(page * PAGE_SIZE).limit(PAGE_SIZE)
        results = list(cursor)
        end_time = time.time()
        print(f"MongoDB - Page {page + 1}: {len(results)} documents fetched in {end_time - start_time:.4f} seconds.")


if __name__ == "__main__":
    # 创建数据
    mongo_client = MongoClient(MONGO_URI)
    mongo_db = mongo_client['test']
    mongo_collection = mongo_db['test']
    create_docs(mongo_collection, PAGE_SIZE * TOTAL_PAGES)
    # 基本拉取
    test_mongo_base_pull(mongo_collection)
