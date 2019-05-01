import unittest

from test.gameplay_test_case import GameplayTestCase
from test.load_game_test_case import LoadGameTestCase


def suite():
    suite1 = unittest.makeSuite(GameplayTestCase, 'test')
    suite2 = unittest.makeSuite(LoadGameTestCase, 'test')
    return unittest.TestSuite((suite1, suite2))


runner = unittest.TextTestRunner()
runner.run(suite())
