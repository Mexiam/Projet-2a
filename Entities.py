from numpy import random

class Entity:
    def __init__(self, case, population, id, avg_lifespan=20):
        self.id = id
        self.parent_male = '' #contains the male parent entity 
        self.parent_female = '' #contains the female parent entity
        #self.sane #boolean : if false, entity loose speed and energy
        self.energy = round(random.uniform(1, 5), 2)#dies if at 0. Entity has to eat to gain energy
        #self.camouflage #determine with case camo if other entities can see it
        self.base_speed = round(random.uniform(0, 1), 2) #basic speed of the entity. lower when entity is not sane
        self.base_energy_consumption = round(random.uniform(0, 0.5), 2) #energy consumed at each round
        #self.rationnality #probability to make a rationnal decision next round
        self.age = 0 #in number of rounds, updated each rounds
        self.maturity = 6 #minimum age for reproduction
        self.death_age = round(random.normal(loc=avg_lifespan, scale=avg_lifespan/2), 0)#maximum age
        self.alive = True #boolean : if false, entity is dead
        #self.risk_taking #probability to choose a dangerous move towards food or a partner
        self.position = case #a Case class entity
        case.add_entity(self)
        self.population = population

    def reproduce(self, entity):
        print('Reproduction of ' + type(self).__name__ + ' ' + str(self.id) + ' with ' + type(entity).__name__ + ' ' + str(entity.id) + ' at pos ' + str(self.position))
        if entity.age >= entity.maturity and self.age >= self.maturity:
            baby = type(entity)(case=self.position, population=self.population)
            self.population.add(baby)
            baby.parent_male = self
            baby.parent_female = entity

    def kill(self, reason=""):
        self.alive = False
        print('Death : ' + type(self).__name__ + ' ' + str(self.id) + ' reason : ' + reason + ' at pos ' + str(self.position))

    def moove_to(self, case):
        self.position = case
        case.add_entity(self)

    def end_day(self):
        if self.alive:
            if self.age >= self.death_age:
                self.kill("natural death")
                return 0
            if self.energy <= 0:
                self.kill("starved to death")
                return 0
            self.energy = self.energy - self.base_energy_consumption
            self.age += 1

    def random_move(self):        
        val = random.uniform(0, 3)
        if(val < 0.75):
            self.moove_to(self.position.up())
        if(val > 0.75 and val < 1.5):
            self.moove_to(self.position.right())
        if(val > 1.5 and val < 2.25):
            self.moove_to(self.position.down())
        if(val > 2.25 and val < 3):
            self.moove_to(self.position.left())


class Lapin(Entity):
    def __init__(self, case, population, id=0):
        super().__init__(case, population, id, avg_lifespan=30)

    def meet(self, entity):
        if isinstance(entity, Lapin):
            self.reproduce(entity)
        if isinstance(entity, Loup):
            print("lapin "+ str(self.id) + " meet loup on case type " + str(self.position.type))
            entity.eat(self)

    def new_day(self):
        self.energy += self.position.quantity_food
        self.position.quantity_food = 0
        self.random_move()
        self.end_day()        

        
class Loup(Entity):
    def __init__(self, case, population, id=0):
        super().__init__(case, population, id, avg_lifespan=60)

    def meet(self, entity):
        if isinstance(entity, Loup):
            self.reproduce(entity)
        elif isinstance(entity, Lapin):
            self.eat(entity)

    def eat(self, entity):
        if self.position.type == 0:
            self.energy += entity.energy
            entity.kill("eaten by Loup " + str(self.id))

    def new_day(self):
        self.random_move()
        self.end_day()
 
      
class Case():
    def __init__(self, x, y, map, type = 0, occupancy_rate = 0):
        self.type = type #type of the case, it could be grass 0 , terrier 1 
        self.occupancy_rate = occupancy_rate # how mutch entities are at the same time on the case
        self.quantity_food = round(random.uniform(0, 0.5), 2) # quantity of food for rabbits
        self.camo = round(random.uniform(0, 1), 0) # if an entities can hide or not
        self.regen_food = round(random.uniform(0, 0.2), 2) # regen speed of food 
        self.x = x
        self.y = y
        self.entity_list = []
        self.map = map
    
    def set_rand_type(self, val):
        probability = round(random.uniform(0, 1), 2)
        if(probability > val):
            self.type = 1
        else:
            self.type = 0
    
    def get_type(self):
        return self.type
    
    def get_quantity_food(self):
        return self.quantity_food
    
    def get_camo(self):
        return self.camo
    
    def get_regen_food(self):
        return self.regen_food
    
    def add_entity(self, entity):
        self.entity_list.append(entity)

    def up(self, n=1):
        return self.map.get_case(self.x, self.y-n)
    
    def left(self, n=1):
        return self.map.get_case(self.x-n, self.y)

    def right(self, n=1):
        return self.map.get_case(self.x+n, self.y)

    def down(self, n=1):
        return self.map.get_case(self.x, self.y+n)

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
        if len(self.entity_list) >= 2:
            for i in range(0, len(self.entity_list)-1):
                for j in range(i+1, len(self.entity_list)):
                    self.entity_list[i].meet(self.entity_list[j])
        self.entity_list = []

    def __str__(self):
        return '(x: ' + str(self.x) + ',y: ' + str(self.y) + ')'   
     
#c = Case(0,1)
#c.type = 0
#for i in range(10):
#    print(c.quantity_food)
#    c.new_day()

class Map():
    def __init__(self, x, y):
        self.max_x = x
        self.max_y = y
        self.map = list()
        for i in range(x):
            self.map.append(list())
            for j in range(y):
                new_case = Case(i, j, self)
                new_case.set_rand_type(0.9)
                self.map[i].append(new_case)

    def __getitem__(self, index):
        return self.map[index]            

    def new_day(self):
        for i in range(self.max_x):
            for j in range(self.max_y):
                self.map[i][j].new_day()

    def get_random_case(self):
        return self.map[int(round(random.uniform(0, self.max_x-1), 0))][int(round(random.uniform(0, self.max_y-1), 0))]  

    def get_food_quantity(self):
        sum = 0
        for i in range(self.max_x):
            for j in range(self.max_y):
                sum += self.map[i][j].quantity_food
        return sum
    
    def get_food_map(self):
        result = []
        for i in range(self.max_x):
            result.append([])
            for j in range(self.max_y):
                result[i].append(self.map[i][j].quantity_food)
        return result

    def protected_pos(self):
        x_list = []
        y_list = []
        for i in range(self.max_x):
            for j in range(self.max_y):
                if self.map[i][j].type == 1:
                    x_list.append(i)
                    y_list.append(j)
        return (x_list, y_list)  

    def get_case(self, x, y):
        if x < 0:
            x = 0
        if x >= len(self.map):
            x = len(self.map) - 1
        if y < 0:
            y = 0 
        if y >= len(self.map[x]):
            y = len(self.map[x]) - 1 
        return self.map[x][y]


class Population():
    def __init__(self, entity_type, size, map):
        self.individuals = []
        for _ in range(size):
            random_case = map.get_random_case()
            self.individuals.append(entity_type(case=random_case, population=self, id=len(self.individuals)))

    def __iter__(self):
        return filter(lambda i: i.alive, self.individuals)
    
    def __len__(self):
        return len(list(filter(lambda i: i.alive, self.individuals)))
    
    def x_list(self):
        return [individual.position.x for individual in filter(lambda i: i.alive, self.individuals)]
    
    def y_list(self):
        return [individual.position.y for individual in filter(lambda i: i.alive, self.individuals)]
    
    def new_day(self):
        for individual in filter(lambda i: i.alive, self.individuals):
            individual.new_day()

    def add(self, entity):
        self.individuals.append(entity)
        entity.id = len(self.individuals)


def print_plateau_terminal(size):
    plateau = Map(size, size)
    for i in range(0,size):
        for j in range(0,size):
            print(plateau.map[i][j].regen_food, end=" ")
        print()


#print_plateau_terminal(5)