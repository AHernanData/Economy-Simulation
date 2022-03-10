
import simpy
import random
import statistics
import names
import copy

env = simpy.Environment()
land = simpy.Resource(env, capacity=100)
def gen(n):
    for i in range(n):
        yield i
g = gen(1000)


#--------------------------------- People------------------------------------#


class citizen:
    population = 0
    total_happiness = 0
    avg_happiness = 0
    citizen_list = []
    
    def list_r():
        return citizen.citizen_list
    
    def __init__(self, money, happiness,config=1):
        self.name = names.get_full_name()
        self.money=money
        self.happiness=happiness
        self.r_happiness=happiness
        self.employed = False
        citizen.population += 1
        citizen.total_happiness += happiness
        citizen.avg_happiness = citizen.total_happiness / citizen.population
        citizen.citizen_list.append(self)
        if config == 1:
            pass
        
    def get_food(self):
        if self.money >= 10:
            self.money -= 10
            food_c.food_c_list[random.randrange(0,len(food_c.food_c_list))].get_money(10)
        else:
            self.happiness = 1
            print(self.name, "says, 'this sucks'")
    
    def make_company(self):
        if self.money >= 500:
            self.employed = True
            self.money -= 500
            global temp0
            temp0 = self
            exec("%s = company(temp0,500,1)" % ('B{}'.format(next(g))), globals())
            self.__class__ = business_owner
    
    def get_job(self):
        n=0
        for x in company.company_list:
            n += len(x)
        options = copy.deepcopy(company.company_list)
        for j in range(n):
            print(len(options[0]))
            if j == 5 or options == []:
                print(self.name, "has applied for all they can today")
                break
            product = random.choice(options)
            business = random.choice(product)
            if business.hire(self) == True:
                self.employed = True
                break
            else:
                product.remove(business)
                options = [ele for ele in options if ele != []]
                
    def get_money(self,amount):
        self.money += amount

class business_owner(citizen):
    def say_hi(self):
        print("yo")
        
#------------------------------- Businesses----------------------------------#
        
class company:
    company_list = []
    cost_mod = [10,0]

    def __init__(self,citizen,startup,product,cost=3):
        self.owner = citizen
        self.product = product
        self.worth = 0.6*startup
        self.recent_money = startup
        self.employees = []
        self.employee_names = [citizen.name]
        self.positions_available = startup/100
        if product == 1:
            self.__class__ = food_c
            food_c.food_costs[cost-1].append(self)
            self.cost = cost*company.cost_mod[product-1]
            food_c.food_c_list.append(self)
        
    def month_end(self):
        self.income = self.worth - self.recent_money
        self.worth = 0.3*self.income+self.worth
        self.labor = 0.7*self.income
        owner_bonus = 0.2*self.labor
        employee_income = 0.8*self.labor/(1+len(self.employees))
        owner_income = owner_bonus + employee_income  
        self.owner.get_money(owner_income)
        for i in range(len(self.employees)-1):
            self.employees[i+1].get_money(employee_income)
        
        
    def get_money(self,amount):
        self.worth += amount
        
    def hire(self,civilian):
        if int(self.positions_available) != 0:
            self.employees.append(civilian)
            self.employee_names.append(civilian.name)
            self.positions_available -= 1
            print("welcome aboard,", civilian.name, "we welcome you")
            return True
        else:
            print("Sorry", self, "isn't hiring now")
            return False
        
    def price_set(self,cost):
        company.food_costs[self]
        self.cost = 10*cost
            
class food_c(company):
    food_c_list = []
    company.company_list.append(food_c_list)
    food_costs = [[],[],[],[],[]]
    food_quality = [[],[],[],[],[]]
    
    def demand():
        print("demand is currently", citizen.pop())
    

        


#-------------------------------- Simulation Commands------------------------#

        
def start_simulation_env(population,wealthy=20,middle=60,poor=20):
    wealthy_pop = int((wealthy/100)*population)
    middle_pop = int((middle/100)*population)
    poor_pop = int((poor/100)*population)
    for i in range(wealthy_pop):
        exec("%s = citizen(random.randrange(1000,5000,100),random.randrange(3,5))" % ('P{}'.format(i)),globals())
    for i in range(middle_pop):
        exec("%s = citizen(random.randrange(100,1000,50),random.randrange(2,5))" % ('P{}'.format(i+wealthy_pop)),globals())
    for i in range(poor_pop):
        exec("%s = citizen(random.randrange(0,100,10),random.randrange(1,5))" % ('P{}'.format(i+middle_pop+wealthy_pop)),globals())
    for i in range(len(citizen.citizen_list)):
        citizen.citizen_list[i].make_company()

def first_day():
    for i in range(len(citizen.citizen_list)):
        citizen.citizen_list[i].get_food()
        if citizen.citizen_list[i].employed == False:
            citizen.citizen_list[i].get_job()
    for j in range(len(company.company_list)):
        for i in range(len(company.company_list[j])):
            company.company_list[j][i].month_end()
    
#--------------------------------Test Commands-------------------------------#

start_simulation_env(50,0,10,90)
first_day()