import sys, simpy, random, statistics, names, Food_names
from termcolor import colored, cprint


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
        self.name = colored('{}'.format(names.get_full_name()), 'cyan')
        self.money=money
        self.happiness=happiness
        self.r_happiness=happiness
        self.employed = False
        self.log = [['DAY {}'.format(simulation.Day)],[self.name, 'started with ${} and {} happiness'.format(self.money, self.happiness)]]
        citizen.population += 1
        citizen.total_happiness += happiness
        citizen.avg_happiness = citizen.total_happiness / citizen.population
        citizen.citizen_list.append(self)
        if config == 1:
            pass
        
    def get_food(self):
        if self.money >= 10:
            self.money -= 10
            choice = random.randrange(0,len(food_c.food_c_list))
            food_c.food_c_list[choice].get_money(10)
            self.log.append(["bought food from {}.".format(food_c.food_c_list[choice].name)])
            
        else:
            self.happiness = 1
            self.log.append(["couldn't afford food"])
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
        n=1
        for x in company.company_list:
            n += len(x)
        options = company.company_list
        products = list(range(len(options)))
        businesses = []
        for x in products:
            businesses.append(list(range(len(options[x]))))
        for i in range(n):
            if i == 5 or products == []:
                self.log.append([self.name, 'has applied for all they can tody'])
                return 1
                break
            product_choice = random.choice(products)
            business_choice = random.choice(businesses[product_choice])
            if options[product_choice][business_choice].hire(self) == True:
                self.employed = True
                self.log.append([self.name, 'got hired at {}!'.format(options[product_choice][business_choice].name)])
                return 0
                break
            else:
                self.log.append([self.name, 'Applied at {}'.format(options[product_choice][business_choice].name)])
                businesses[product_choice].remove(business_choice)
                x = [i for i, e in enumerate(businesses) if e == []]
                for j in x:
                    products.remove(j)
                businesses = [ele for ele in businesses if ele != []]
                
    def get_money(self,amount):
        self.money += amount
        
    def log_r(self):
        for x in range(len(self.log)):
            print(*self.log[x])

class business_owner(citizen):
    def say_hi(self):
        print("yo")
        
#------------------------------- Businesses----------------------------------#
        
class company:
    company_list = []
    cost_mod = [10,0]

    def __init__(self,citizen,startup,product,cost=3):
        self.owner = citizen
        self.name = colored('{}'.format(Food_names.foodname()), 'green')
        self.product = product
        self.worth = 0.6*startup
        self.recent_money = self.worth
        self.employees = []
        self.employee_names = [citizen.name]
        self.positions_available = startup/100
        self.owner.log.append([self.owner.name, 'Started the business {}!'.format(self.name)])
        if product == 1:
            self.__class__ = food_c
            food_c.food_costs[cost-1].append(self)
            self.cost = cost*company.cost_mod[product-1]
            food_c.food_c_list.append(self)
        
    def month_end(self):
        self.income = self.worth - self.recent_money
        self.worth = 0.3*self.income+self.worth
        self.recent_money = self.worth
        self.labor = 0.7*self.income
        owner_bonus = 0.2*self.labor
        employee_income = 0.8*self.labor/(1+len(self.employees))
        owner_income = owner_bonus + employee_income  
        self.owner.get_money(owner_income)
        print(self.owner.name,'says, My company', self.name,'got me ${}'.format(owner_income))
        self.owner.log.append([self.name, 'brought in {}'.format(owner_income)])
        for i in range(len(self.employees)):
            self.employees[i].get_money(employee_income)
            print(self.employees[i].name, 'says, "I got paid {}"'.format(employee_income))
            self.employees[i].log.append(['Paid ${}.'.format(employee_income)])
        
    def get_money(self,amount):
        self.worth += amount
        
    def hire(self,civilian):
        if int(self.positions_available) != 0:
            self.employees.append(civilian)
            self.employee_names.append(civilian.name)
            self.positions_available -= 1
            print("Hired!,", civilian.name, self.name, "welcomes you")
            print()
            return True
        else:
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
    

        


#-------------------------------- Simulation --------------------------------#
class simulation:
    Day = 0
        
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
            citizen.citizen_list[i].log.append(['\n'])

    def one_day():
        unemployment=0
        simulation.Day += 1
        for i in range(len(citizen.citizen_list)):
            citizen.citizen_list[i].log.append(['DAY {}'.format(simulation.Day)])
            citizen.citizen_list[i].get_food()
            if citizen.citizen_list[i].employed == False:
                unemployment += citizen.citizen_list[i].get_job()
        for j in range(len(company.company_list)):
            for i in range(len(company.company_list[j])):
                company.company_list[j][i].month_end()
        for i in range(len(citizen.citizen_list)):
            citizen.citizen_list[i].log.append(['\n'])
        print(unemployment,"are unemployed")
#--------------------------------Test Commands-------------------------------#

simulation.start_simulation_env(50,10,30,60)
for x in range(10):
    simulation.one_day()