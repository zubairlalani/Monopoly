class Player:
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.properties = []
        self.position = 0
         
    def move(self, dice_roll):
        self.position += dice_roll
        self.position = self.position % 40
        
    def get_position(self):
        return self.position

    def get_money(self):
        return self.money

    def get_properties(self):
        return self.properties

    def get_name(self):
        return self.name
    