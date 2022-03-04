# -*- coding: utf-8 -*-

class plato :
    def __init__(self):
        self.hight = 7
        self.width = 7
        self.board = [[Tile(True, i+j*7, None, 0) for j in range(self.width)]for i in range(self.hight)]
        for i in range(self.hight) :
            for j in range(self.widht) :
                if i == 0 and j == 0 :
                    self.board[i][j].modif_stat(False)
                    self.board[i][j].modif_color(1)
                elif i == 0 and j == 7 :
                    self.board[i][j].modif_stat(False)
                    self.board[i][j].modif_color(2)
                elif i == 7 and j == 0 :
                    self.board[i][j].modif_stat(False)
                    self.board[i][j].modif_color(3)
                elif i == 7 and j == 7 :
                    self.board[i][j].modif_stat(False)
                    self.board[i][j].modif_color(4)
                elif self.board[i][j].get_id()%2 == 1 :
                    self.board[i][j].modif_stat(False)
                    
                    
                

class Tile :
    def __init__(self, fix, ID, objet, color) : #tourner et road
        self.item = objet
        self.stat = fix #True = peut bouger et False = reste fix
        self.spwan = color
        self._id = ID
    
    def get_id(self) :
        return self._id
    
    def get_item(self) :
        return self.item
    
    def get_stat(self) :
        return self.stat()
    
    def get_spawn(self) :
        return self.spawn
    
    def modif_item(self, item) :
        self.item = item
    
    def modif_stat(self, stat) :
        self.stat = stat
    
    def modif_color(self, color) :
        self.color = color