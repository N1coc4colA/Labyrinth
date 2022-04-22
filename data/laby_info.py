# -*- coding: utf-8 -*-
from random import randint
from PyQt5.QtGui import QPixmap

def isPlayable(rank):
	"""
	Know if the given rank on the labyrinth should be playable.

	Parameters
	----------
	rank: int
		The target rank.

	Returns
	-------
	bool
		If it is compatible.
	"""
	return rank%2 == 1

class BoardBackend:
	"""
	Main component of the labyrinth backend. Holds all  informations, handles operations and other miscellaneous things.
	"""
	def __init__(self, nb_players): #||||||||||||||||||||||||| mieux organiser la répartition des directions des chemins ||||||||||||||||||||||||||||||||||||
		self.height = 7
		self.width = 7

		self.card = Card()
		self.all_tile = []

		self.board = [[Tile(True, i+j*7, 'line') for i in range(self.width)] for j in range(self.height)]
		self.current = Tile(True, 49, 'line') #The actual tile

		for i in range(self.width):
			for j in range(self.height):
				if (i == 0 or i == self.width-1) and (j == 0 or j == self.height-1):
					self.board[i][j].setStat(False)
					self.board[i][j].setRoad("angle")
					self.board[i][j].setColor((j + i*2)//7+1)
					self.board[i][j].setOrientation((j + i*2)//7)
				elif i%2==0 and j%2==0:
					self.board[i][j].setStat(False)
					self.board[i][j].setRoad('triple')
				else:
					self.board[i][j].setStat(True)

		for x in range(7):
			for y in range(7):
				self.all_tile.append(self.board[x][y])

		self.card.random()
		self.player = []
		if nb_players == 1:
			pass
					#☺on verra plus tard pour le nombre de bots---------------------------------------------------------------------------------------------
		elif nb_players == 2:
			self.j1 = Persona(1, self.card.liste[:12])
			self.j2 = Persona(3, self.card.liste[12:])
			self.player.extend({self.j1, self.j2})

		elif nb_players == 3:
			self.j1 = Persona(1, self.card.liste[:5])
			self.j2 = Persona(2, self.card.liste[6:12])
			self.j3 = Persona(3, self.card.liste[12:18])
			self.player.extend({self.j1, self.j2, self.j3})

		elif nb_players == 4:
			self.j1 = Persona(1, self.card.liste[:6])
			self.j2 = Persona(2, self.card.liste[6:12])
			self.j3 = Persona(3, self.card.liste[12:18])
			self.j4 = Persona(4, self.card.liste[18:])
			self.player.extend({self.j1, self.j2, self.j3, self.j4})

	def move(self, rank, start):
		"""
		Submit the move requested.

		Parameters
		----------
		rank: int
			The column
		start: str
			The direction to move the tiles.
		"""
		cpy = self.current
		if isPlayable(rank) == True:
			if start == 'up':
				#begin, end = self.board[0][rank], self.board[6][rank]
				for i in range(6):
					self.board[i][rank], self.board[i+1][rank] = self.board[i+1][rank], self.board[i][rank]
				self.board[6][rank], self.current = self.current, self.board[6][rank]
				for i in self.player:
					if i.location == (rank, 7):
						i.setlocation(rank, 0)
			elif start == 'down':
				for i in range(0, 6, -1):
					self.board[i][rank], self.board[i+1][rank] = self.board[i+1][rank], self.board[i][rank]
				self.board[0][rank], self.current = self.current, self.board[0][rank]
				for i in self.player:
					if i.location == (rank, 0):
						i.setlocation(rank, 7)
			elif start == 'left':
				for i in range(6):
					self.board[rank][i], self.board[rank][i+1] = self.board[rank][i+1], self.board[rank][i]
				self.board[rank][6], self.current = self.current, self.board[rank][6]
				for i in self.player:
					if i.location == (7, rank):
						i.setlocation(0, rank)
			elif start == 'right':
				for i in range(6, 0, -1):
					self.board[rank][i], self.board[rank][i-1] = self.board[rank][i-1], self.board[rank][i]
				self.board[rank][0], self.current = self.current, self.board[rank][0]
				for i in self.player:
					if i.location == (0, rank):
						i.setlocation(7, rank)
		else:
			print("Invalid pos:", rank)

	def graph(self):
		for x in range(7):
			for y in range(7):
				for i in self.board[x][y].openings:
					if x != 0:
						if i =='n' and  not self.board[x-1][y] in self.board[x][y].nearbies:
							for j in self.board[x-1][y].openings:
								if j == "s":
									self.board[x][y].nearbies.append(self.board[x-1][y])
					if x != 6:
						if i =='s' and  not self.board[x+1][y] in self.board[x][y].nearbies:
							for j in self.board[x+1][y].openings:
								if j == "n":
									self.board[x][y].nearbies.append(self.board[x+1][y])
					if y != 6:
						if i =='e' and  not self.board[x+1][y] in self.board[x][y].nearbies:
							for j in self.board[x+1][y].openings:
								if j == "o":
									self.board[x][y].nearbies.append(self.board[x][y+1])
					if y != 0:
						if i =='o' and  not self.board[x-1][y] in self.board[x][y].nearbies:
							for j in self.board[x-1][y].openings:
								if j == "e":
									self.board[x][y].nearbies.append(self.board[x][y-1])

	def __str__(self):
		out = " ____________________________________\n"
		for l in self.board:
			out += " |"
			for e in l:
				v = str(e.getId())
				if len(v)  < 2:
					v = " " + v
				out += " " + v + " |"
			out += "\n"
		out += " ------------------------------------\n |"
		v = str(self.current.getId())
		if len(v)  < 2:
			v = " " + v
		out += " |\n ------\n"
		return out

class Tile:
	"""
	Backend object holding a tile's dataset.
	"""
	def __init__(self, fixed, ID, road, objet = None, color = 0):
		"""
		Parameters
		----------
		fixed: bool
			Make the tile fixed or not.

		ID: int
			The tile's UID.

		road: str
			Has to be 'line' ("|"), 'angle' ("L") or 'triple' ("T").

		objet: str, optional
			Name of the object located on the tile. The default is None.

		color: int, optional
			Has to be one of the followings: 0: no spawn (default), 1: white spawn, 2: turquoise spawn, 3: black spawn, 4: violet spawn
		"""
		self.pixmap = QPixmap("./images/tile_" + str(ID) + ".png")
		self.item = objet
		self.static = fixed
		self.spawn = color
		self._id = ID
		self.road = road
		self.orientation = 0	# orientation; 0: 0°, 1: 90°, 2: 180°, 3: 270°
		self.nearbies = []
		self.openings = []
		self.findOpenings()

	def isPlayable(self, rank):
		"""
		Know if the given rank on the labyrinth should be playable.

		Parameters
		----------
		rank: int
			The target rank.

		Returns
		-------
		bool
			If it is compatible.
		"""
		return rank%2 != 0

	def getId(self):
		"""
		Get the widget at a position.

		Returns
		-------
		int
			The tile's UID.
		"""
		return self._id

	def getItem(self):
		"""
		Get the tile's item.

		Returns
		-------
		str
		"""
		return self.item

	def isStatic(self):
		"""
		Get the tile's stat.

		Returns
		-------
		bool
		"""
		return self.static()

	def getSpawn(self):
		"""
		Get if the tile is a spawn.

		Returns
		-------
		spawn: int
			The spawn ID (or color)
		"""
		return self.spawn

	def getRoad(self):
		"""
		Get the tile's road.

		Returns
		-------
		str
		"""
		return self.road

	def getOrientation(self):
		"""
		Get the tile's orientation.

		Returns
		-------
		int
		"""
		return self.orientation

	def setItem(self, item):
		"""
		Change the item.

		Parameters
		----------
		item: str
			The new item.
		"""
		self.item = item

	def setStat(self, stat):
		"""
		Change the stat.

		Parameters
		----------
		stat: bool
			The new stat.
		"""
		self.static = stat

	def setColor(self, color):
		"""
		Change the color.

		Parameters
		----------
		color: int
			The new color ID.
		"""
		self.spawn = color

	def setRoad(self, road):
		"""
		Change the road.

		Parameters
		----------
		road: str
			The new road to use.
		"""
		self.road = road

	def setOrientation(self, orientation):
		"""
		Change the orientation.

		Parameters
		----------
		orientation: int
			The new orientation.
		"""
		self.orientation = orientation

	def findOpenings(self):
		"""
		Cette méthode permet de savoir sur une tuile (case) où sont les ouvertures.
		pour par la suite pouvoir faire la recherche de chemin
		"""
		if self.road == 'line':
			self.openings.extend(['n', 's'])
		else:
			self.openings.extend({"angle": [['s','e'], ['s','o'], ['n','o'], ['n','e']], "triple": [['e','s'],['o','e','s'],['n','o','s'],['n','o','e']]}[self.road][self.orientation])


class Persona:
	"""
	Backend object holding a player's dataset.
	"""
	def __init__(self, color, pile):
		self.goal = pile
		self.color = color
		self.location = [None, (0, 0), (7, 0), (7, 7), (0, 7)][self.color]

	def getLocation(self):
		"""
		Get the player's position.

		Returns
		-------
		location: tuple(int, int).
		"""
		return self.location

	def setLocation(self, x, y):
		"""
		Change the location

		Parameters
		----------
		x: int.
			x index.
		y: int.
			y index.
		"""
		self.location = (x, y)


class Card:
	"""
	Backend object holding a card's dataset.
	"""
	def __init__(self):
		self.liste = ["Pringles", "Dragon", "Passoire", "Langouste", "Bouteille", "Apple", "Ring", "LaserSaber", "PiderPig", "Covid", "Grale", "Meme", "Meme", "Kassos", "The Clap", "Batman", "Sun", "Homer", "Elon Musk", "Peery", "Pigeon", "Idefix", "Eye of Sauron", "oooooooooooo"]

	def random(self):
		"""
		Randomize the cards available.
		"""
		for i in range(0,24):
			a, b = randint(0,23), randint(0,23)
			self.liste[a], self.liste[b] = self.liste[b], self.liste[a]


class Pile:
	"""
	Pile structure.
	"""
	def __init__(self):
		self.pile = []

	def add(self, o):
		"""
		Add an item to the pile.

		Parameters
		----------
		o: Unknown.
			Object to add to the top of the pile.
		"""
		self.pile.append(o)

	def pop(self):
		"""
		Pop the last element of the pile.
		"""
		return self.pile.pop()

	def __len__(self):
		return len(self.pile)
