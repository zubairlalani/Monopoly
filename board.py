class Board:
    def __init__(self):
        self.properties = []
        self.chance_cards = []
        self.community_chest_cards = []
    
    def init_locations(self):
        '''
        self.properties.append(Location(0, "Mediterranean Avenue", "Brown", 60, [10, 30, 90, 160, 250], , true))
        self.properties.append(Location(0, "Baltic Avenue", "Brown", 60, 4,[20, 60, 180, 320] true))
        self.properties.append(Location(0, "Mediterranean Avenue", "Brown", 60, 2, true))
        self.properties.append(Location(0, "Mediterranean Avenue", "Brown", 60, 2, true))
        self.properties.append(Location(0, "Mediterranean Avenue", "Brown", 60, 2, true))
        self.properties.append(Location(0, "Mediterranean Avenue", "Brown", 60, 2, true))
        self.properties.append(Location(0, "Mediterranean Avenue", "Brown", 60, 2, true))
        self.properties.append(Location(0, "Mediterranean Avenue", "Brown", 60, 2, true))
        self.properties.append(Location(0, "Mediterranean Avenue", "Brown", 60, 2, true))
        '''
        
    
class Location:
    
    def __init__(self, property_id, name, color, cost, rent, house_amnts, is_property) :
        self.id = property_id
        self.name = name
        self.color = color
        self.cost = cost
        self.rent = rent
        self.house_amnt = house_amnts
        self.is_property = is_property
        
    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
    
    def get_color(self):
        return self.color
    
    def get_cost(self):
        return self.cost
    
    def get_rent(self):
        return self.rent
    
    def is_property(self):
        return self.is_property
    def __str__(self):
        return self.name+" "+self.color+" $"+str(self.cost)+" $"+str(self.rent)
    