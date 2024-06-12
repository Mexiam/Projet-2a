import random

class Entity:
    def __init__(self):
        self.id
        self.parent_male #contains the male parent entity 
        self.parent_female #contains the female parent entity
        self.sane #boolean : if false, entity loose speed and energy
        self.energy #dies if at 0. Entity has to eat to gain energy
        self.camouflage #determine with case camo if other entities can see it
        self.base_speed #basic speed of the entity. lower when entity is not sane
        self.base_energy_consumption #energy consumed at each round
        self.rationnality #probability to make a rationnal decision next round
        self.age = 0 #in number of rounds, updated each rounds
        self.maturity #minimum age for reproduction
        self.death_age #maximum age
        self.alive = True #boolean : if false, entity is dead
        self.risk_taking #probability to choose a dangerous move towards food or a partner
        self.position #a Case class entity


    def set_pos(self, position):
        self.position = position


    def kill(self):
        self.alive = False


    def end_round(self):
        if self.alive:
            if self.age >= self.death_age:
                self.alive = False
                return 0
            if self.energy <= 0:
                self.alive = False
                return 0
            self.energy = self.energy - self.base_energy_consumption
            self.age += 1
            
                
class Lapin(Entity):
    def __init__(self):
        return

        
class Loup(Entity):
    def __init__(self, ):
        return
 
      
class Case():
    def __init__(self, x, y, occupancy_rate = 0):
        self.type = round(random.uniform(0, 1), 0) #type of the case, it could be grass 0 , terrier 1 
        self.occupancy_rate = occupancy_rate # how mutch entities are at the same time on the case
        self.quantity_food = round(random.uniform(0, 1), 2) # quantity of food for rabbits
        self.camo = round(random.uniform(0, 1), 0) # if an entities can hide or not
        self.regen_food = round(random.uniform(0, 1), 2) # regen speed of food 
        self.x = x
        self.y = y
    
    def set_x(self, x):
        self.x = x

    def set_x(self, y):
        self.y = y
    
    def set_type(self, type):
        self.type = type

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_type(self):
        return self.type
    
    def get_quantity_food(self):
        return self.quantity_food
    
    def get_camo(self):
        return self.camo
    
    def get_regen_food(self):
        return self.regen_food
    
    def new_day(self):
        pass # grow grass here


class Map():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.map = list()
        for i in range(x):
            self.map.append(list())
            for j in range(y):
                self.map[i].append(Case(i,j))

    def new_day(self):
        for i in range(self.x):
            for j in range(self.y):
                self.map[i][j].new_day()



class Population():
    def __init__(self, entity_type, size):
        individuals = []
        for i in range(size):
            individuals.append(entity_type())



def print_plateau_terminal(size):
    plateau = Map(size, size)
    for i in range(0,size):
        for j in range(0,size):
            print(plateau.map[i][j].regen_food, end=" ")
        print()


print_plateau_terminal(5)