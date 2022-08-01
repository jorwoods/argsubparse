import argparse
import unittest

import argsubparse

class TestArgSubParse(unittest.TestCase):
    def setUp(self) -> None:

        parser = argparse.ArgumentParser()
        self.parser = parser

        return super().setUp()

    def test_store_true(self):
        def sample_func(a: bool = False) -> None:
            pass

        parser = argsubparse.create_subparser(self.parser, sample_func)
        parsed = parser.parse_args(["--a"])
        
        self.assertTrue(parsed.a)
