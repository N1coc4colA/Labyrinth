# -*- coding: utf-8 -*-

class plato :
    def __init__(self):
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
        

class parso :
    def __init__(self, color, liste, rank) :
        self.liste = liste
        self.goal = liste[rank]
        self.color = color
        
game = plato