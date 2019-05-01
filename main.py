from game import *
import msvcrt
import sys

game = Game("data/board1.in")

game.printBoard()

status = False
while not status:
	key = msvcrt.getch()
	try:
		key = key.decode("utf-8")
		if key.lower() == "w":
			status = game.move(Direction.UP)
			print("=============UP=============")
		elif key.lower()  == "a":
			status = game.move(Direction.LEFT)
			print("============LEFT============")
		elif key.lower()== "s":
			status = game.move(Direction.DOWN)
			print("============DOWN============")
		elif key.lower() == "d":
			status = game.move(Direction.RIGHT)
			print("============RIGHT===========")
		elif key.lower() == "q":
			sys.exit(0)
		else:
			print("Invalid key!")
	except GameException as ex:
		print(ex)
	finally:
		game.printBoard()

print()
print("🎉  💰   CONGRATULATIONS!   💰  🎉")
print(f"Number of moves: {game.get_moves_no()}")