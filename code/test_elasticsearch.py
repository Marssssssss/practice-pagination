import time
import random
import string
from elasticsearch import Elasticsearch


ES_HOST = 'http://192.168.31.197:9200'

# 分页参数
INDEX_NAME = "test"
PAGE_SIZE = 10  # 每页的文档数量
TOTAL_PAGES = 5  # 要查询的总页数


def create_index_with_docs(es_client, index_count):
    """ 创建 elasticsearch 索引，并生成指定数量的数据 """
    if not es_client.indices.exists(index=INDEX_NAME):
        es_client.indices.create(index=INDEX_NAME)

    def random_string(length=10):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(length))

    for i in range(index_count):
        doc = {
            'id': i,
            'name': random_string(random.randint(5, 15)),
            'value': random.randint(1, 100),
            'description': random_string(30)
        }
        es_client.index(index=INDEX_NAME, id=i, body=doc)
    print(f"finished create docs!")


def test_elasticsearch_base_pull(es_client):
    """ elasticsearch 基本拉取分页 """
    print("start Elasticsearch paging...")

    for page in range(TOTAL_PAGES):
        page_start_time = time.time()
        from_param = page * PAGE_SIZE
        response = es_client.search(
            index=INDEX_NAME,  # 替换为你的索引名
            body={
                "query": {
                    "match_all": {}
                },
                "from": from_param,
                "size": PAGE_SIZE
            }
        )
        print(f"Elasticsearch - Page {page + 1}: {len(response['hits']['hits'])} documents fetched in {time.time() - page_start_time:.4f} seconds.")


if __name__ == "__main__":
    # 创建数据
    es_client = Elasticsearch(ES_HOST)
    create_index_with_docs(es_client, PAGE_SIZE * TOTAL_PAGES)
    # 基本拉取
    test_elasticsearch_base_pull(es_client)
