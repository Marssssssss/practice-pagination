import time
import random
import string
from elasticsearch import Elasticsearch


ES_HOST = 'http://localhost:9200'

# 分页参数
INDEX_NAME = "test"
PAGE_SIZE = 400  # 每页的文档数量
TOTAL_PAGES = 500  # 要查询的总页数


def create_index_with_docs(es_client, index_count):
    """ 创建 elasticsearch 索引，并生成指定数量的数据 """
    if es_client.indices.exists(index=INDEX_NAME):
        es_client.indices.delete(index=INDEX_NAME)
    es_client.indices.create(index=INDEX_NAME)
    
    settings = {
        "index": {
            "max_result_window": 1000000,
        }
    }

    es_client.indices.put_settings(body=settings, index=INDEX_NAME)

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
    start_time = time.time()
    for page in range(TOTAL_PAGES):
        page_start_time = time.time()
        from_param = page * PAGE_SIZE
        response = es_client.search(
            index=INDEX_NAME,  # 替换为你的索引名
            body={
                "query": {
                    "match_all": {}
                },
                "sort": {
                    "value": {
                        "order": "asc",
                    }
                },
                "from": from_param,
                "size": PAGE_SIZE
            }
        )
        print(f"Elasticsearch - Page {page + 1}: {len(response['hits']['hits'])} documents fetched in {time.time() - page_start_time:.4f} seconds.")
    print(f"all time: {time.time() - start_time}")


def test_elasticsearch_cursor_pull(es_client):
    print("start Elasticsearch cursor paging...")
    search_after = None
    start_time = time.time()
    while True:
        search_query = {
            "query": {
                "match_all": {}
            },
            "size": PAGE_SIZE,
            "sort": [
                {"value": "asc"},
                {"_id": "asc"}         # 作为二次排序，确保唯一性
            ],
            "search_after": search_after  # 使用上一次查询的最后一条文档的排序值
        }
        search_response = es.search(index=INDEX_NAME, body=search_query)
        hits = search_response['hits']['hits']
        if not hits:
            break
        search_after = hits[-1]['sort']
    print(f"all time: {time.time() - start_time}")


def test_elasticsearch_single_large_start_pull(es_client):
    """ 超大数据量大页码拉取 """
    
    start_time = time.time()
    from_param = (TOTAL_PAGES - 1) * PAGE_SIZE
    response = es_client.search(
        index=INDEX_NAME,  # 替换为你的索引名
        body={
            "query": {
                "match_all": {}
            },
            "sort": {
                "value": {
                    "order": "asc",
                }
            },
            "from": from_param,
            "size": PAGE_SIZE
        }
    )
    print(f"all time: {time.time() - start_time}")


if __name__ == "__main__":
    # 创建数据
    es_client = Elasticsearch(ES_HOST)
    # create_index_with_docs(es_client, PAGE_SIZE * TOTAL_PAGES)
    # 基本拉取
    # test_elasticsearch_base_pull(es_client)
    # 超大数据量大页码拉取
    test_elasticsearch_single_large_start_pull(es_client)
