import random

class Entity:
    def __init__(self, case):
        #self.id
        #self.parent_male #contains the male parent entity 
        #self.parent_female #contains the female parent entity
        #self.sane #boolean : if false, entity loose speed and energy
        self.energy = round(random.uniform(0.3, 1), 2)#dies if at 0. Entity has to eat to gain energy
        #self.camouflage #determine with case camo if other entities can see it
        self.base_speed = round(random.uniform(0, 1), 2) #basic speed of the entity. lower when entity is not sane
        self.base_energy_consumption = round(random.uniform(0, 0.5), 2) #energy consumed at each round
        #self.rationnality #probability to make a rationnal decision next round
        self.age = 0 #in number of rounds, updated each rounds
        #self.maturity #minimum age for reproduction
        self.death_age = round(random.uniform(5, 20), 0)#maximum age
        self.alive = True #boolean : if false, entity is dead
        #self.risk_taking #probability to choose a dangerous move towards food or a partner
        self.position = case #a Case class entity


    def set_pos(self, position):
        self.position = position


    def kill(self):
        self.alive = False


    def new_day(self):
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
    pass

        
class Loup(Entity):
    pass
 
      
class Case():
    def __init__(self, x, y, type = 0, occupancy_rate = 0):
        self.type = type #type of the case, it could be grass 0 , terrier 1 
        self.occupancy_rate = occupancy_rate # how mutch entities are at the same time on the case
        self.quantity_food = round(random.uniform(0, 0.5), 2) # quantity of food for rabbits
        self.camo = round(random.uniform(0, 1), 0) # if an entities can hide or not
        self.regen_food = round(random.uniform(0, 0.2), 2) # regen speed of food 
        self.x = x
        self.y = y
    
    def set_x(self, x):
        self.x = x

    def set_x(self, y):
        self.y = y
    
    def set_rand_type(self, val):
        probability = round(random.uniform(0, 1), 2)
        if(probability > val):
            self.type = 1
        else:
            self.type = 0
        

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
        if self.type == 0 and self.quantity_food < 1:
            if((self.quantity_food + self.get_regen_food())>1):
                self.quantity_food = 1
            else:
                self.quantity_food += self.get_regen_food()
        else:
            if(self.type == 1):
                self.quantity_food = 0
            else:
                self.quantity_food = 1

#c = Case(0,1)
#c.type = 0
#for i in range(10):
#    print(c.quantity_food)
#    c.new_day()

class Map():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.map = list()
        for i in range(x):
            self.map.append(list())
            for j in range(y):
                new_case = Case(i, j)
                new_case.set_rand_type(0.9)
                self.map[i].append(new_case)

    def __getitem__(self, index):
        return self.map[index]            

    def new_day(self):
        for i in range(self.x):
            for j in range(self.y):
                self.map[i][j].new_day()

    def get_random_case(self):
        return self.map[int(round(random.uniform(0, self.x-1), 0))][int(round(random.uniform(0, self.y-1), 0))]  

    def get_food_quantity(self):
        sum = 0
        for i in range(self.x):
            for j in range(self.y):
                sum += self.map[i][j].quantity_food
        return sum        


class Population():
    def __init__(self, entity_type, size, map):
        self.individuals = []
        for i in range(size):
            random_case = map.get_random_case()
            self.individuals.append(entity_type(case=random_case))

    def __iter__(self):
        return iter(self.individuals)
    
    def __len__(self):
        return len(self.individuals)
    
    def x_list(self):
        return [individual.position.x for individual in self.individuals]
    
    def y_list(self):
        return [individual.position.y for individual in self.individuals]
    
    def new_day(self):
        for individual in self.individuals:
            individual.new_day()



def print_plateau_terminal(size):
    plateau = Map(size, size)
    for i in range(0,size):
        for j in range(0,size):
            print(plateau.map[i][j].regen_food, end=" ")
        print()


#print_plateau_terminal(5)