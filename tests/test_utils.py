import unittest

from app import create_app, db
from app.utils import get_or_create
from app.models import User


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_ctx.pop()

    def test_get_or_create(self):
        user1, created1 = get_or_create(User, name="foo", social_id="bar")
        db.session.add(user1)
        db.session.commit()
        user2, created2 = get_or_create(User, name="foo", social_id="bar")
        self.assertTrue(created1)
        self.assertFalse(created2)
        self.assertEquals(user1, user2)