import tempfile
import unittest

from .session import (
    RuntimeSession,
)

from .session_manager import (
    SessionManager,
)

from .session_store import (
    SessionStore,
)


class TestRuntimeSession(
    unittest.TestCase
):

    def test_lifecycle(self):

        session = RuntimeSession()

        self.assertEqual(
            session.status,
            "created",
        )

        session.start(
            "exp-001"
        )

        self.assertTrue(
            session.is_active()
        )

        session.pause()

        self.assertEqual(
            session.status,
            "paused",
        )

        session.resume()

        self.assertTrue(
            session.is_active()
        )

        session.close()

        self.assertTrue(
            session.is_closed()
        )


class TestSessionManager(
    unittest.TestCase
):

    def test_manager(self):

        manager = SessionManager()

        session = manager.create()

        manager.start(
            session.session_id,
            "exp-001",
        )

        self.assertEqual(
            len(manager.active()),
            1,
        )

        manager.close(
            session.session_id
        )

        self.assertEqual(
            len(manager.active()),
            0,
        )


class TestSessionStore(
    unittest.TestCase
):

    def test_store(self):

        with tempfile.TemporaryDirectory() as tmp:

            manager = SessionManager()

            manager.create(
                {
                    "source": "test"
                }
            )

            store = SessionStore(
                f"{tmp}/sessions.json"
            )

            store.save(
                manager.all()
            )

            data = store.load()

            self.assertEqual(
                len(data),
                1,
            )

            self.assertEqual(
                data[0]["metadata"]["source"],
                "test",
            )


if __name__ == "__main__":
    unittest.main()
