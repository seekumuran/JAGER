import unittest

from .novelty import NoveltyDetector


class TestNoveltyDetector(unittest.TestCase):

    def setUp(self):
        self.detector = NoveltyDetector()

    def sample(self):
        return {
            "cpu_load": 50,
            "memory_load": 50,
            "num_processes": 50,
            "num_threads": 100,
            "ipc_intensity": 50,
        }

    def test_empty_history_is_novel(self):
        score = self.detector.score(
            self.sample(),
            [],
        )

        self.assertEqual(score, 1.0)

    def test_identical_input_low_novelty(self):
        score = self.detector.score(
            self.sample(),
            [self.sample()],
        )

        self.assertEqual(score, 0.0)

    def test_different_input_has_novelty(self):
        other = self.sample()
        other["cpu_load"] = 90

        score = self.detector.score(
            self.sample(),
            [other],
        )

        self.assertGreater(score, 0.0)


if __name__ == "__main__":
    unittest.main()
