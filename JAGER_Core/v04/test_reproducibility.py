import unittest

from .reproducibility import (
    ReproducibilityManifest,
)


class TestReproducibility(unittest.TestCase):

    def make_manifest(self):
        return ReproducibilityManifest(
            run_id="run-test",
            seed=42,
            budget=10,
            target="blackbox",
        )

    def test_manifest_contains_core_parameters(self):

        manifest = (
            self.make_manifest()
            .generate()
        )

        self.assertEqual(
            manifest["seed"],
            42,
        )

        self.assertEqual(
            manifest["budget"],
            10,
        )

        self.assertEqual(
            manifest["target"],
            "blackbox",
        )

    def test_fingerprint_exists(self):

        fingerprint = (
            self.make_manifest()
            .fingerprint()
        )

        self.assertEqual(
            len(fingerprint),
            64,
        )

    def test_same_configuration_is_reproducible(self):

        first = (
            self.make_manifest()
            .fingerprint()
        )

        second = (
            self.make_manifest()
            .fingerprint()
        )

        self.assertEqual(
            first,
            second,
        )


if __name__ == "__main__":
    unittest.main()
