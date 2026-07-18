import os
import unittest
from datetime import datetime, timedelta

from peewee import SqliteDatabase

os.environ["TESTING"] = "true"

from app import TimelinePost, mydb


MODELS = [TimelinePost]


class TestTimelinePostDatabase(unittest.TestCase):
    def setUp(self):
        self.test_db = SqliteDatabase(":memory:")
        self.test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        self.test_db.connect()
        self.test_db.create_tables(MODELS)

    def tearDown(self):
        self.test_db.drop_tables(MODELS)
        self.test_db.close()
        mydb.bind(MODELS, bind_refs=False, bind_backrefs=False)

    def test_create_and_retrieve_timeline_post(self):
        created_at = datetime.now()
        post = TimelinePost.create(
            name="Grace Hopper",
            email="grace@example.com",
            content="Testing database writes and reads.",
            created_at=created_at,
        )

        fetched_post = TimelinePost.get_by_id(post.id)

        self.assertEqual(fetched_post.name, "Grace Hopper")
        self.assertEqual(fetched_post.email, "grace@example.com")
        self.assertEqual(fetched_post.content, "Testing database writes and reads.")
        self.assertEqual(fetched_post.created_at, created_at)

    def test_retrieve_timeline_posts_in_reverse_chronological_order(self):
        older_post = TimelinePost.create(
            name="Older Post",
            email="older@example.com",
            content="This was created first.",
            created_at=datetime.now() - timedelta(days=1),
        )
        newer_post = TimelinePost.create(
            name="Newer Post",
            email="newer@example.com",
            content="This was created second.",
            created_at=datetime.now(),
        )

        posts = list(TimelinePost.select().order_by(TimelinePost.created_at.desc()))

        self.assertEqual([post.id for post in posts], [newer_post.id, older_post.id])


if __name__ == "__main__":
    unittest.main()
