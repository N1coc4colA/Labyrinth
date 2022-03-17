# -*- coding: utf-8 -*-
from random import randint

class Plato :
    def __init__(self, nb_joueur) : #||||||||||||||||||||||||| mieux organiser la répartition des directions des chemin |||||||||||||||||||||||||||||||||||| 
        self.height = 7
        self.width = 7
        
        self.card = Card()
        self.all_tile = []
        
        self.out_tile = Tile(True, 49, 'line')  #road et objet vont changer
        self.board = [[Tile(True, i+j*7, 'line') for i in range(self.width)]for j in range(self.height)]
        for i in range(self.height) :
            for j in range(self.width) :
                if i == 0 and j == 0 :                  # initialisation of spwan 1 
                    self.board[i][j].modif_stat(False)
                    self.board[i][j].modif_color(1)
                    self.board[i][j].modif_road('angle')
                    
                elif i == 0 and j == 7 :                  # initialisation of spwan 2
                    self.board[i][j].modif_stat(False)
                    self.board[i][j].modif_color(2)
                    self.board[i][j].modif_road('angle')
                    
                elif i == 7 and j == 0 :                  # initialisation of spwan 3
                    self.board[i][j].modif_stat(False)
                    self.board[i][j].modif_color(3)
                    self.board[i][j].modif_road('angle')
                    
                elif i == 7 and j == 7 :                  # initialisation of spwan 4
                    self.board[i][j].modif_stat(False)
                    self.board[i][j].modif_color(4)
                    self.board[i][j].modif_road('angle')
                    
                elif self.board[i][j].get_id()%2 == 1 :  # initialisation des cases inpaires
                    self.board[i][j].modif_stat(False)
                    self.board[i][j].modif_road('triple')
        
        for i in range(self.width):
            for j in range(self.height):
                if (i == 0 or i == self.width-1) and (j == 0 or j == self.height-1):
                    self.board[i][j].modif_stat(False)
                    self.board[i][j].modif_road("angle")
                elif i%2 == 0 and j%2==0:
                    self.board[i][j].modif_stat(False)
                else:
                    self.board[i][j].modif_stat(True)
        
        for x in range(7) :
            for y in range(7) :
                self.all_tile.append(self.board[x][y])
        self.all_tile.append(self.out_tile)
        
        self.card.random()
        if nb_joueur == 1 :
            pass
                    #☺on verra plus tard pour le nombre de bot---------------------------------------------------------------------------------------------
        elif nb_joueur == 2 :
            self.j1 = Perso(1, self.card.liste[:12])
            self.j2 = Perso(3, self.card.liste[12:])
            
        elif nb_joueur == 3 :
            self.j1 = Perso(1, self.card.liste[:5])
            self.j2 = Perso(2, self.card.liste[6:12])
            self.j3 = Perso(3, self.card.liste[12:18])
            
        elif nb_joueur == 4 :
            self.j1 = Perso(1, self.card.liste[:6])
            self.j2 = Perso(2, self.card.liste[6:12])
            self.j3 = Perso(3, self.card.liste[12:18])
            self.j4 = Perso(4, self.card.liste[18:])
            
        def jouable(self, rank) :
            return rank%2 != 0
        
        def move(self, rank, start, ID) :
            if self.jouable(rank) == True :
                if start == 'down' :
                    for i in range(6) :
                        self.board[i][rank], self.board[i+1][rank] = self.board[i+1][rank], self.board[i][rank]
                    self.board[7][rank], self.out_tile = self.out_tile, self.board[7][rank]
                elif start == 'up' :
                    for i in range(0, 6, -1) :
                        self.board[i][rank], self.board[i+1][rank] = self.board[i+1][rank], self.board[i][rank]
                    self.board[0][rank], self.out_tile = self.out_tile, self.board[0][rank]
                

class Tile :
    def __init__(self, fix, ID, road, objet = None, color = 0) : 
        """
        Cette class initialise des tuile carré qui vont fassoné le labyrinte.
        Cette class associe les toutes les valeurs (information) nécessaire pour les différencié et les utilisé
        Parameters
        ----------
        fix : BOOL
            | True = peut bouger | False = reste fix  |
            
        ID : INT
            DESCRIPTION.
            
        road : STR
            |  'line' = ligne droite  |  'angle' = virage  |  'triple' = triple sens  |
            
        objet : STR, optional
            nom de l'objet qui se situe sur la case, si il y en a un. The default is None.
            
        color : INT, optional
            | 0 = pas de spawn | 1 = spwan 'blanc' | 2 = spawn 'turquoise' | 3 = spwn 'noir' | 4 = spawn 'violet' |
            The default is 0.
            
        Returns
        -------
        None.
        """
        self.item = objet
        self.stat = fix
        self.spawn = color
        self._id = ID
        self.road = road
        self.orientation = 0       # orientation | 0 = 0° | 1 = 90° | 2 = 180° | 3 = 270° |
    
    def get_id(self) :
        return self._id
    
    def get_item(self) :
        return self.item
    
    def get_stat(self) :
        return self.stat()
    
    def get_spawn(self) :
        return self.spawn
    
    def get_road(self) :
        return self.road
    
    def get_orientation(self) :
        return self.orientation
    
    def modif_item(self, item) :
        self.item = item
    
    def modif_stat(self, stat) :
        self.stat = stat
    
    def modif_color(self, color) :
        self.spawn = color
        
    def modif_road(self, road) :
        self.road = road
        
    def modif_orientation(self, orientation) :
        self.orientation = orientation
        

class Perso :
    def __init__(self, color, pile) :
        self.goal = pile
        self.color = color
        if self.color == 1 : #tuple provisoir
            self.location = (0, 0)
        elif self.color == 2 :
            self.location = (7, 0)
        elif self.color == 3 :
            self.location = (7, 7)
        elif self.color == 4 :
            self.location = (0, 7)
        
    def get_location(self) :
        return self.location
    
    def modif_location(self, x, y) :
        self.location = (x, y)

class Card :
    def __init__(self) :
        self.liste = ["Pringles", "Dragon", "Passoire", "Langouste", "Bouteille", "Apple", "Ring", "LaserSaber", "PiderPig", "Covid", "Grale", "Meme", "Meme", "Kassos", "The Clap", "Batman", "Sun", "Homer", "Elon Musk", "Peery", "Pigeon", "Idefix", "Eye of Sauron", "oooooooooooo"]
         
    def random(self) :
        for i in range(0,24) :
            a, b = randint(0,23), randint(0,23)
            self.liste[a], self.liste[b] = self.liste[b], self.liste[a]
            

class Pile :
    def __init__(self) :
        self.pile = []
    
    def append(self, add) :
        self.pile.append(add)
    
    def pop(self):
        self.pile.pop(len(self.pile))
        
    def len_(self) :
        return len(self.pile)
    

        
game = Plato(4)