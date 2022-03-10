import sys, simpy, random, statistics, names
import Food_names
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
            choice = random.choices(food_c.food_c_list,weights=wants.company_influence[0])
            food_c.food_c_list[choice].get_money(10,self)
            self.log.append(["bought food from {}.".format(food_c.food_c_list[choice].name)])
            
        else:
            self.happiness = 1
            self.log.append(["couldn't afford food"])
            print(self.name, "says, 'this sucks'")
            
    
    def make_company(self):
        if self.money >= 500:
            if company.company_list[1] == []:
                self.employed = True
                self.money -= 500
                global temp0
                temp0 = self
                exec("%s = company(temp0,500,1)" % ('B{}'.format(next(g))), globals())
                self.__class__ = business_owner
            else:
                self.employed = True
                self.money -= 500
                temp0 = self
                exec("%s = company(temp0,500,random.randrange(len(company.company_list)))" % ('B{}'.format(next(g))), globals())
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
        x = [i for i, e in enumerate(businesses) if e == []]
        for j in x:
            products.remove(j)
        businesses = [ele for ele in businesses if ele != []]
        for i in range(n):
            if i == 5 or products == []:
                self.log.append([self.name, 'has applied for all they can tody'])
                return 1
                break
            product_choice = random.choice(products)
            business_choice = random.choices(businesses[product_choice],wants.company_influence[product_choice])
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
    company_product = ['food_c', 'manufacturing_c']
    cost_mod = [10,0]

    def __init__(self,citizen,startup,product,cost=3):
        self.owner = citizen
        self.name = colored('{}'.format(Food_names.foodname()), 'green')
        self.product = product
        self.expense_level = cost
        self.worth = 0.6*startup
        self.funds = 0.2*startup
        self.recent_funds = self.funds
        self.employees = []
        self.employee_names = [citizen.name]
        self.positions_available = int(self.worth/100)
        self.owner.log.append([self.owner.name, 'Started the business {}!'.format(self.name)])
        self.product_alignment(product,cost,startup)
        self.log = [['DAY {}'.format(simulation.Day)],[self.name, 'started by {}, is a {}, has ${} funds, and is worth {}'.format(self.owner.name,company.company_product[product],self.funds,self.worth)]]

    def product_alignment(self,product,cost,startup):
        exec('self.__class__ = %s' % (company.company_product[product]),globals(),locals())
        self.alignment[0].append(self)
        self.alignment[1][cost].append(self)
        self.cost = cost*company.cost_mod[product]
        self.wage = self.start_wage
        if product!= 1:
            choice = random.randrange(0,len(manufacturing_c.manufacturing_c_list))
            manufacturing_c.manufacturing_c_list[choice].get_money(0.2*startup,self)

    def month_end(self):
        self.income = round(self.funds - self.recent_funds,2)
        self.worth = round((0.3*self.income)+self.worth,2)       #Lots of fixed numbers here subject to be variables later
        self.profit = 0.5*self.income
        industrial_cost = round(0.2*self.income,2)
        owner_bonus = 0.2*self.profit
        employee_income = self.wage
        owner_income = round(owner_bonus + self.wage,2)
        self.owner.get_money(owner_income)
        print(self.owner.name,'says, My company', self.name,'got me ${}'.format(owner_income))
        self.owner.log.append([self.name, 'brought in {}'.format(owner_income)])
        for i in range(len(self.employees)):
            self.employees[i].get_money(employee_income)
            print(self.employees[i].name, 'says, "I got paid ${}"'.format(employee_income))
            self.employees[i].log.append(['Paid ${}.'.format(employee_income)])
        if self.product != 1:
            try:
                choice = random.randrange(0,len(manufacturing_c.manufacturing_c_list))
                manufacturing_c.manufacturing_c_list[choice].get_money(industrial_cost,self)
            except: manufacturing_c.sad_fund += industrial_cost
        self.funds -= round(employee_income*len(self.employees) + owner_income + industrial_cost,2)
        self.recent_funds = self.funds
        self.worth += round(0.1*self.funds,2)
        self.positions_available = max(int(self.worth/100),0)
        self.log.append(['Income was ${}, paid owner ${}, paid employees total of ${}, funds are now ${}, worth is ${}'.format(self.income,owner_income,len(self.employees)*employee_income,self.funds,self.worth)])
        if self.positions_available < len(self.employees) or self.employees == []:
            self.lay_off()
       
    def get_money(self,amount,payer):
        self.funds += amount
        self.log.append(['got paid ${} by {}'.format(amount,payer.name)])
        
    def hire(self,civilian):
        if int(self.positions_available-len(self.employees)) != 0:
            self.employees.append(civilian)
            self.employee_names.append(civilian.name)
            self.positions_available -= 1
            print("Hired!,", civilian.name, self.name, "welcomes you \n")
            self.log.append(['Hired, {}!'.format(civilian.name)])
            return True
        else:
            return False
    
    def lay_off(self):
        if self.employees == []:
            self.bankruptcy()
        n = len(self.employees)-self.positions_available
        for i in range(n):
            victim = random.choice(self.employees)
            victim.employed = False
            victim.log.append(['{} got fired by {} (lay off)! :('.format(victim.name,self.name)])
            self.log.append(['Had to lay off {}'.format(victim.name)])
            self.employees.remove(victim)

    def bankruptcy(self):
        print(self.name, "has gone bankrupt!")
        company.company_list[self.product].remove(self)
        self.alignment[1][self.expense_level].remove(self)
        self.owner.__class__ = citizen
        self.owner.employed = False
        self.__class__ = failed_c
        self.failed_c_list.append(self)
        self.log.append([self.name, "could not continue running. We are shutting down, indefinitely"])
        self.owner.log.append([self.owner.name, "couldn't keep {} running. Had to file for bankruptcy".format(self.name)])
        simulation.environment_update()
            
    def price_set(self,cost):
        company.food_costs[self]
        self.cost = 10*cost
            
    def log_r(self):
        for x in range(len(self.log)):
            print(*self.log[x])

class food_c(company):
    food_c_list = []
    company.company_list.append(food_c_list)
    food_costs = [[],[],[],[],[]]
    food_quality = [[],[],[],[],[]]
    alignment = [food_c_list, food_costs, food_quality]
    start_wage=10
    
    def demand():
        print("demand is currently", citizen.pop())
    
class manufacturing_c(company):
    sad_fund = 0
    manufacturing_c_list=[]
    company.company_list.append(manufacturing_c_list)
    manufacturing_costs = [[],[],[],[],[]]
    manufacturing_quality = [[],[],[],[],[]]
    alignment = [manufacturing_c_list, manufacturing_costs, manufacturing_quality]
    start_wage=15

class failed_c(company):
    failed_c_list = []

#--------------------------------AI------------------------------------------#

class wants:
    company_influence = []
    overall_weight = 0
    
    def set_weights():                                                          #sets up a list containing the "influence" weight each company has due to their worth. indices in list line up with the indicies in the overall company list
        for i in range(len(company.company_list)):
            wants.company_influence.append([])
            for j in range(len(company.company_list[i])):
                wants.overall_weight += company.company_list[i][j].worth                         #need to sum through all companies
            for j in range(len(company.company_list[i][j])):                                     #now that overall weight is set, individual weights can be done
                wants.company_influence[i].append(company.company_list[i][j].worth/wants.overall_weight)




















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
        wants.set_weights()

    def one_day():
        unemployment=0
        simulation.Day += 1
        print('DAY {}'.format(simulation.Day))
        for i in range(len(citizen.citizen_list)):
            citizen.citizen_list[i].log.append(['DAY {}'.format(simulation.Day)])
            citizen.citizen_list[i].get_food()
            if citizen.citizen_list[i].employed == False:
                unemployment += citizen.citizen_list[i].get_job()
        for j in range(len(company.company_list)):
            for i in company.company_list[j]:
                i.month_end()
        for i in range(len(citizen.citizen_list)):
            citizen.citizen_list[i].log.append(['\n'])
        print(unemployment,"are unemployed \n")
        
    def environment_update():
        wants.set_weights()
#--------------------------------Test Commands-------------------------------#

simulation.start_simulation_env(50,10,30,60)
for x in range(100):
    simulation.one_day()
    
