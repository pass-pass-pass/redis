import redis

redis.Redis(host = 'localhost', port = 2222, db = 0)
import time
class RedisManager:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    def save_article(self, article_id, content):
        self.r.set(f"article:{article_id}", content)

    # def get_all_article_ids(self):
    #     """Retrieve all article IDs"""
    #     return self.r.smembers('article_ids')

    def get_article(self, article_id):
        return self.r.get(f"article:{article_id}")

    def add_comment_to_article(self, article_id, comment):
        self.r.lpush(f"comments:{article_id}", comment)

    def get_comments_for_article(self, article_id):
        return self.r.lrange(f"comments:{article_id}", 0, -1)

    def add_tag_to_article(self, article_id, tag):
        self.r.sadd(f"tags:{article_id}", tag)

    def get_tags_for_article(self):
        return self.r.smembers('article_ids')

    def increase_article_views(self, article_id):
        self.r.zincrby("article_views", 1, article_id)

    def get_most_viewed_articles(self):
        return self.r.zrevrange("article_views", 0, 4) 

    def save_article_details(self, article_id, details):
        self.r.hmset(f"article_details:{article_id}", details)

    def get_article_details(self, article_id):
        return self.r.hgetall(f"article_details:{article_id}")

    def increase_views_with_timestamp(self, article_id):
        pipeline = self.r.pipeline()
        pipeline.zincrby("article_views", 1, article_id)
        pipeline.set(f"last_viewed:{article_id}", time.time())
        pipeline.execute()

    def save_article_details(self, article_id, details):
        self.r.hmset(f"article_details:{article_id}", details)
    def get_article_details(self, article_id):
        return self.r.hgetall(f"article_details:{article_id}")
