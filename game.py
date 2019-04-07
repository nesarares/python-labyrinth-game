from constants import *
from enum import Enum

class Direction(Enum):
	UP = 1
	RIGHT = 2
	DOWN = 3
	LEFT = 4

class GameException(Exception):
	def __init__(self, message):
		super().__init__(message)

class Game:
	def __init__(self, filename):
		self.board = []
		self.rows = -1
		self.cols = -1
		self.current_pos = (-1, -1)
		self.start_pos = (-1, -1)
		self.end_pos = (-1, -1)
		self.moves = 0
		self.load_game(filename)

	def set_start(self, start):
		try:
			self.start_pos = (int(start[0]), int(start[1]))
		except ValueError:
			raise GameException(error_message["INVALID_START_NUMBER"])

	def set_end(self, end):
		try:
			self.end_pos = (int(end[0]), int(end[1]))
		except ValueError:
			raise GameException(error_message["INVALID_END_NUMBER"])

	def set_board(self, lines):
		self.board = []
		try:
			for line in lines:
				line = list(map(lambda x: int(x), line.strip().split(" ")))
				non_valid_items = len(list(filter(lambda x: x != 1 and x != 0, line)))
			
				if non_valid_items != 0:
					raise GameException(error_message["INVALID_BOARD_ITEMS"])
				self.board.append(line)
			
			self.rows = len(self.board)
			self.cols = len(self.board[0])
			
			non_valid_lines = len(list(filter(lambda x: len(x) != self.cols, self.board)))
			if non_valid_lines != 0:
					raise GameException(error_message["INVALID_BOARD_ROWS"])

		except ValueError:
			raise GameException(error_message["INVALID_BOARD_NUMBER"])

	def is_pos_on_edge(self, pos):
		# Position is outside of board
		if pos[0] < 0 or pos[0] >= self.rows \
			or pos[1] < 0 or pos[1] >= self.cols:
			return False

		# Position is inside board (not on edge)
		if (pos[0] > 0 and pos[0] <= self.rows-2) and \
			(pos[1] > 0 and pos[1] <= self.cols-2):
			return False
		
		return True

	def check_start_end(self):
		if not self.is_pos_on_edge(self.start_pos):
			raise GameException(error_message["INVALID_START_EDGE"])
		if not self.is_pos_on_edge(self.end_pos):
			raise GameException(error_message["INVALID_END_EDGE"])
		if self.start_pos == self.end_pos:
			raise GameException(error_message["INVALID_START_END_OVERLAP"])
		if self.board[self.start_pos[0]][self.start_pos[1]] != 0 \
			or self.board[self.end_pos[0]][self.end_pos[1]] != 0:
			raise GameException(error_message["INVALID_START_END_WALL"])

	def set_current_pos(self, pos):
		self.current_pos = (pos[0], pos[1])

	def load_game(self, filename):
		with open(filename, "r") as file:
			start = file.readline().strip().split(" ")
			end = file.readline().strip().split(" ")
			lines = file.readlines()
			self.set_board(lines)
			self.set_start(start)
			self.set_end(end)
			self.check_start_end()
			self.set_current_pos(self.start_pos)
			if not self.exists_path():
				raise GameException(error_message["INVALID_BOARD_PATH"])

	def is_wall(self, pos):
		return self.board[pos[0]][pos[1]] == 1
	
	def get_valid_next(self, pos):
		next = []
		
		next_pos = (pos[0] - 1, pos[1]) # UP
		if pos[0] != 0 and not self.is_wall(next_pos):
				next.append(next_pos)

		next_pos = (pos[0] + 1, pos[1]) # DOWN
		if pos[0] != self.rows - 1 and not self.is_wall(next_pos):
				next.append(next_pos)
		
		next_pos = (pos[0], pos[1] - 1) # LEFT
		if pos[1] != 0 and not self.is_wall(next_pos):
				next.append(next_pos)
		
		next_pos = (pos[0], pos[1] + 1) # RIGHT
		if pos[1] != self.cols - 1 and not self.is_wall(next_pos):
				next.append(next_pos)
		
		return next

	def exists_path(self):
		visited = []
		to_visit =  [(self.start_pos[0], self.start_pos[1])]

		pos = (-1, -1)
		
		while pos != self.end_pos and len(to_visit) > 0:
			pos = to_visit[0]
			to_visit = to_visit[1:]

			visited.append(pos)
			next_list = self.get_valid_next(pos)
			for next_pos in next_list:
				if next_pos in visited:
					continue
				to_visit.append(next_pos)

		return pos == self.end_pos

	def move(self, direction):
		next_pos = (-1, -1)
		if direction == Direction.UP:
			next_pos = (self.current_pos[0] - 1, self.current_pos[1])
			if self.current_pos[0] == 0 or self.is_wall(next_pos):
				raise GameException(error_message["INVALID_MOVE"])
			self.current_pos = next_pos

		elif direction == Direction.DOWN:
			next_pos = (self.current_pos[0] + 1, self.current_pos[1])
			if self.current_pos[0] == self.rows - 1 or self.is_wall(next_pos):
				raise GameException(error_message["INVALID_MOVE"])
			self.current_pos = next_pos
		
		elif direction == Direction.LEFT:
			next_pos = (self.current_pos[0], self.current_pos[1] - 1)
			if self.current_pos[1] == 0 or self.is_wall(next_pos):
				raise GameException(error_message["INVALID_MOVE"])
			self.current_pos = next_pos
		
		elif direction == Direction.RIGHT:
			next_pos = (self.current_pos[0], self.current_pos[1] + 1)
			if self.current_pos[1] == self.cols - 1 or self.is_wall(next_pos):
				raise GameException(error_message["INVALID_MOVE"])
			self.current_pos = next_pos

		else:
			raise GameException(error_message["INVALID_DIRECTION"])

		self.moves += 1

		if next_pos == self.end_pos:
			return True
		return False
	
	def printBoard(self):
		for (i, line) in enumerate(self.board):
			for (j, elem) in enumerate(line):
				if elem == 0:
					if self.current_pos == (i, j):
						print('✖ ', end = '')
					elif self.start_pos == (i, j):
						print('◎ ', end = '')
					elif self.end_pos == (i, j):
						print('◉ ', end = '')
					else:
						print('▢ ', end = '')
				else:
					print('▩ ', end = '')
			print()

	def get_moves_no(self):
		return self.moves
