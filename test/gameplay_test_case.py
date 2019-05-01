import unittest
import os

from game import Game, Direction, GameException, error_message


class GameplayTestCase(unittest.TestCase):
    def loadGame(self):
        tmp_filename = 'tmp.in'
        board_str = '''2 0
0 7
1 1 1 1 0 1 0 0
1 1 1 0 0 0 0 1
0 0 0 0 1 0 1 1
1 1 0 0 1 0 0 0
'''
        with open(tmp_filename, 'w') as f:
            f.write(board_str)
        self.game = Game(tmp_filename)
        os.remove(tmp_filename)

    def setUp(self):
        super().setUp()
        self.loadGame()

    def tearDown(self):
        super().tearDown()
        self.game = None

    def testValidMove(self):
        finished = self.game.move(Direction.RIGHT)
        self.assertFalse(finished)
        self.assertEqual(self.game.current_pos, (2, 1))
        self.assertIs(self.game.moves, 1)

    def testHitWall(self):
        self.assertRaisesRegex(GameException, error_message['INVALID_MOVE'], self.game.move, Direction.UP)
        self.assertEqual(self.game.current_pos, (2, 0))
        self.assertIs(self.game.moves, 0)

    def testFinished(self):
        self.game.move(Direction.RIGHT)
        self.game.move(Direction.RIGHT)
        self.game.move(Direction.RIGHT)
        self.game.move(Direction.UP)
        self.game.move(Direction.RIGHT)
        self.game.move(Direction.RIGHT)
        self.game.move(Direction.RIGHT)
        self.game.move(Direction.UP)
        finished = self.game.move(Direction.RIGHT)
        self.assertTrue(finished)
        self.assertEqual(self.game.current_pos, (0, 7))
        self.assertIs(self.game.moves, 9)
