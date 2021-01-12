
"""[summary] Single player for a monopoly game
"""
class Player:
    def __init__(self, name, money, x, y):
        self.name = name
        self.money = money
        self.properties = []
        self.position = 0
        self.x = x
        self.y = y
         
    def move(self, dice_roll):
        self.position += dice_roll
        self.position = self.position % 40
        if self.position <= 10 :
            self.x += dice_roll * 70 * -1
        elif self.position > 10 and self.position <= 20 :
            self.y += dice_roll * 70 * -1
        elif self.position > 20 and self.position <= 30 :
            self.x += dice_roll * 70 
        elif self.position > 30 and self.position <= 40 :
            self.y += dice_roll * 70 
    
    def make_deposit(self, amount):
        self.money += amount
    
    def pay(self, amount):
        self.money -= amount
        
    def get_position(self):
        return self.position

    def get_money(self):
        return self.money

    def get_properties(self):
        return self.properties

    def get_name(self):
        return self.name
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    