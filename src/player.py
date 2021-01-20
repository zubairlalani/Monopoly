class Player:
    """Single player for a monopoly game
    """
    
    def __init__(self, name, money, x, y):
        self.name = name
        self.money = money
        self.properties = set()
        self.color_frequency = {}
        self.position = 0
        self.x = x
        self.y = y
                 
    def move(self, dice_roll):
        temp_pos = self.position
        self.position += dice_roll
        self.position = self.position % 40
        while temp_pos != self.position:
            if temp_pos < 10:
                self.x += 56 * -1
                self.y = 670
            elif temp_pos >= 10 and temp_pos < 20:
                self.y += 56 * -1
                self.x = 70
            elif temp_pos >= 20 and temp_pos < 30:
                self.x += 56
                self.y = 90
            elif temp_pos >= 30 and temp_pos <= 40:
                self.y += 56
                self.x = 640
            temp_pos += 1
            temp_pos = temp_pos % 40
    
    def buy_property(self, property_id, property_color, price):
        if self.money - price >= 0 and property_id not in self.properties:
            self.properties.add(property_id)
            if property_color in self.color_frequency:
                self.color_frequency[property_color] += 1
            else:
                self.color_frequency[property_color] = 1
            
            self.money -= price
    
    def property_owned(self, property_id):
        return property_id in self.properties
    
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

    def get_color_frequency(self):
        return self.color_frequency
    
    def get_name(self):
        return self.name
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    