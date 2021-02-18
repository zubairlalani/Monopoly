class GameEngine:
    """Handles game logic such as jail, taxes, rolling doubles, turns, rent, etc
    """
    def __init__(self, amount_of_players):
        """Initilaize essential logic to the game such as players, starting turn, whether someone has rolled
        
        Args:
            amount_of_players (int): Amount of players that will participate in the game
        """
        self.amount_of_players = amount_of_players
        self.turn = 0 # Starts on first players turn
        self.rollled = False # Determines which phase of a players turn (rolling, trading, etc)
        self.doubles = 0 # Determines amount doubles rolled
        self.dice_roll = 0 # Dice roll for a single turn
    
    def change_turn(self):
        self.turn += 1
        self.turn = self.turn % self.amount_of_players # Make sure that the turn loops based on amount of players
        self.rollled = False
        self.doubles = 0
        
    def get_turn(self):
        return self.turn
    
    def check_player_pos(self, player, players):
        if player.is_player_turn(self.turn):
            if player.get_position() == 30: # Jail
                player.go_to_jail()
        
            elif player.get_position() == 4: # Tax $200
                print("TAX 200!")
                player.pay(200)
            elif player.get_position() == 38: # Tax $100
                print("TAX 100!")
                player.pay(100)
            elif player.get_position() == 2 or player.get_position() == 17 or player.get_position() == 33: # Community Chest spots
                pass
            elif player.get_position() == 7 or player.get_position() == 22 or player.get_position() == 36: # Chance spots
                pass
            
            for other_player in players:
                if other_player is not player and other_player.property_owned(player.get_position()):
                    # WHen both electric community and water works is owned, 
                    # the rent is 10 times the dice roll, otherwise it is 4 times the roll
                    if player.get_position() == 12: # electric community
                        if other_player.property_owned(28): # Water works
                            rent = 10 * self.dice_roll 
                        else:
                            rent = 4 * self.dice_roll
                    elif player.get_position() == 28:
                        if other_player.property_owned(12):
                            rent = 10 * self.dice_roll
                        else:
                            rent = 4 * self.dice_roll
                    elif player.get_position() == 5 or player.get_position() == 15 or player.get_position() == 25 or player.get_position() == 35: # railroads
                        number_of_railroads = other_player.get_number_of_group_owned("RR")
                        if number_of_railroads == 1:
                            rent = property_dict["locations"][player.get_position()]["rent"]
                        elif number_of_railroads == 2:
                            rent = property_dict["locations"][player.get_position()]["rent1"]
                        elif number_of_railroads == 3:
                            rent = property_dict["locations"][player.get_position()]["rent2"]
                        elif number_of_railroads == 4:
                            rent = property_dict["locations"][player.get_position()]["rent3"]
                            
                        
                    else:
                        rent = property_dict["locations"][player.get_position()]["rent"]
                        if other_player.has_color_group(property_dict["locations"][player.get_position()]["color"]):
                            number_of_houses = other_player.get_property_house_amount(player.get_position())
                            # Determine rent based on number of nhouses
                            if number_of_houses == 0:
                                rent = 2 * rent # When a player owns a color group the regular rent is doubled
                            elif number_of_houses == 1:
                                rent = property_dict["locations"][player.get_position()]["rent1"]
                            elif number_of_houses == 2:
                                rent = property_dict["locations"][player.get_position()]["rent2"]
                            elif number_of_houses == 3:
                                rent = property_dict["locations"][player.get_position()]["rent3"]
                            elif number_of_houses == 4:
                                rent = property_dict["locations"][player.get_position()]["rent4"]
                            elif number_of_houses == 5:
                                rent = property_dict["locations"][player.get_position()]["rent5"]
                    other_player.make_deposit(rent)
                    player.pay(rent)
                    

    
    def set_dice_roll(self, dice_roll, double):
        self.dice_roll = dice_roll
        for player in players:
            if player.is_player_turn(self.turn):
                player.move(dice_roll) # Move the player the sum of the roll
                break
        
        if double:
            self.doubles += 1
            if self.doubles == 3: # When three doubles are rolled, player goes to jail
                for player in players:
                    if player.is_player_turn(self.turn):
                        player.go_to_jail()
                        break
                self.doubles == 0
                self.rollled = True
        else:
            self.rollled = True
        
        self.check_player_pos()
        
    def roll_complete(self):
        return self.rollled
    
    def process_trade(self):
        pass
    
    def is_player_in_jail(self):
        for player in players:
            if player.is_player_turn(game.turn):
                player.increment_jail()
                if player.get_jail_count() > 3:
                    player.leave_jail()
                return player.is_in_jail()