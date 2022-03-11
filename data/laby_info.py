# -*- coding: utf-8 -*-
from random import randint

class Plato :
    def __init__(self, nb_joueur):
        self.hight = 7
        self.width = 7
        self.board = [[Tile(True, i+j*7, 'line') for j in range(self.width)]for i in range(self.hight)]
        for i in range(self.hight) :
            for j in range(self.widht) :
                if i == 0 and j == 0 :                  # initialisation of spwan 1 
                    self.board[i][j].modif_stat(False)
                    self.board[i][j].modif_color(1)
                    self.board[i][j].modif_raod('angle')
                    
                elif i == 0 and j == 7 :                  # initialisation of spwan 2
                    self.board[i][j].modif_stat(False)
                    self.board[i][j].modif_color(2)
                    self.board[i][j].modif_raod('angle')
                    
                elif i == 7 and j == 0 :                  # initialisation of spwan 3
                    self.board[i][j].modif_stat(False)
                    self.board[i][j].modif_color(3)
                    self.board[i][j].modif_raod('angle')
                    
                elif i == 7 and j == 7 :                  # initialisation of spwan 4
                    self.board[i][j].modif_stat(False)
                    self.board[i][j].modif_color(4)
                    self.board[i][j].modif_raod('angle')
                    
                elif self.board[i][j].get_id()%2 == 1 :  # initialisation des cases inpaires
                    self.board[i][j].modif_stat(False)
                    self.board[i][j].modif_raod('triple')
        if nb_joueur == 1 :
            pass
                    #☺on verra plus tard pour le nombre de bot
        elif nb_jouer == 2 :
            j1 = Perso(1, -è-------------------------------------------------------------------------)
                

class Tile :
    def __init__(self, fix, ID, road, objet = None, color = 0) : 
        """
        Cette class initialise des tuile carré qui vont fassoné le labyrinte.
        Cette class associe les toutes les valeurs (information) nécessaire pour les différencié et les utilisé

        Parameters
        ----------
        fix : BOOLEAN
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
        self.spwan = color
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
        self.color = color
        
    def mofi_road(self, road) :
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
            a, b = randint(0,24), randint(0,24)
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
    

        
game = Plato