import os
import unittest
from datetime import datetime, timedelta

os.environ["TESTING"] = "true"

from app import TimelinePost, app, mydb


MODELS = [TimelinePost]


class TestTimelinePostApi(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

        if mydb.is_closed():
            mydb.connect()
        mydb.drop_tables(MODELS, safe=True)
        mydb.create_tables(MODELS)

    def tearDown(self):
        mydb.drop_tables(MODELS, safe=True)

    def test_timeline_page_loads(self):
        response = self.client.get("/timeline")

        self.assertEqual(response.status_code, 200)

    def test_create_timeline_post(self):
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "Ada Lovelace",
                "email": "ada@example.com",
                "content": "I love writing tests.",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "Ada Lovelace")
        self.assertEqual(response.json["email"], "ada@example.com")
        self.assertEqual(response.json["content"], "I love writing tests.")
        self.assertEqual(TimelinePost.select().count(), 1)

    def test_get_timeline_posts(self):
        older_post = TimelinePost.create(
            name="Older Post",
            email="older@example.com",
            content="First post.",
            created_at=datetime.now() - timedelta(days=1),
        )
        newer_post = TimelinePost.create(
            name="Newer Post",
            email="newer@example.com",
            content="Second post.",
            created_at=datetime.now(),
        )

        response = self.client.get("/api/timeline_post")

        self.assertEqual(response.status_code, 200)
        posts = response.json["timeline_posts"]
        self.assertEqual(len(posts), 2)
        self.assertEqual([post["id"] for post in posts], [newer_post.id, older_post.id])

    def test_delete_timeline_post(self):
        post = TimelinePost.create(
            name="Delete Me",
            email="delete@example.com",
            content="This post should be deleted.",
        )

        response = self.client.delete(f"/api/timeline_post/{post.id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["id"], post.id)
        self.assertIsNone(TimelinePost.get_or_none(TimelinePost.id == post.id))

    def test_create_timeline_post_requires_name(self):
        response = self.client.post(
            "/api/timeline_post",
            data={"email": "missing@example.com", "content": "Missing name."},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "Invalid timeline post")

    def test_create_timeline_post_rejects_blank_content(self):
        response = self.client.post(
            "/api/timeline_post",
            data={"name": "Blank", "email": "blank@example.com", "content": "   "},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "Invalid timeline post")

    def test_delete_missing_timeline_post_returns_404(self):
        response = self.client.delete("/api/timeline_post/999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["error"], "Timeline post not found")


if __name__ == "__main__":
    unittest.main()
