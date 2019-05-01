import unittest
import os

from game import Game, GameException, error_message


class LoadGameTestCase(unittest.TestCase):
    def loadGame(self, board_str):
        tmp_filename = 'tmp.in'
        with open(tmp_filename, 'w') as f:
            f.write(board_str)
        self.game = Game(tmp_filename)
        os.remove(tmp_filename)

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.game = None

    def testValidLoad(self):
        board_str = '''2 0
0 7
1 1 1 1 0 1 0 0
1 1 1 0 0 0 0 1
0 0 0 0 1 0 1 1
1 1 0 0 1 0 0 0
'''
        self.loadGame(board_str)
        expected_board = [
            [1, 1, 1, 1, 0, 1, 0, 0],
            [1, 1, 1, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 0, 1, 1],
            [1, 1, 0, 0, 1, 0, 0, 0]
        ]
        self.assertListEqual(self.game.board, expected_board)
        self.assertIs(self.game.moves, 0)
        self.assertEqual(self.game.start_pos, (2, 0))
        self.assertEqual(self.game.current_pos, self.game.start_pos)
        self.assertEqual(self.game.end_pos, (0, 7))
        self.assertIs(self.game.rows, 4)
        self.assertIs(self.game.cols, 8)

    def testInvalidStartPos(self):
        board_str = '''1 0
0 7
1 1 1 1 0 1 0 0
1 1 1 0 0 0 0 1
0 0 0 0 1 0 1 1
1 1 0 0 1 0 0 0
'''
        self.assertRaisesRegex(GameException, error_message['INVALID_START_END_WALL'], self.loadGame, board_str)

    def test(self):
        board_str = '''2 0
0 7
1 1 1 1 0 1 0 0
1 1 1 0 0 0 0 1
0 1 0 0 1 0 1 1
1 1 0 0 1 0 0 0
'''
        self.assertRaisesRegex(GameException, error_message['INVALID_BOARD_PATH'], self.loadGame, board_str)
