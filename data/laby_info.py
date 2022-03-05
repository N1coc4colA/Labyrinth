# -*- coding: utf-8 -*-

class plato :
    def __init__(self):
        self.hight = 7
        self.width = 7
        self.board = [[Tile(True, i+j*7, 'line', None, 0) for j in range(self.width)]for i in range(self.hight)]
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
    def __init__(self, fix, ID, road, objet, color) : #|||||||||||||||||||tourner||||||||||||||||||||||
        self.item = objet
        self.stat = fix # | True = peut bouger | False = reste fix  |
        self.spwan = color
        self._id = ID
        self.road = road #  |  'line' = ligne droite  |  'angle' = virage  |  'triple' = triple sens  |
    
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
    
    def modif_item(self, item) :
        self.item = item
    
    def modif_stat(self, stat) :
        self.stat = stat
    
    def modif_color(self, color) :
        self.color = color
        
    def mofi_road(self, road) :
        self.road = road
        
        
game = plato
