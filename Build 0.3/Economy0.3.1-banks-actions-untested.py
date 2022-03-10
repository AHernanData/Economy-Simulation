import sys, simpy, random, statistics, names
import CompNames
from termcolor import colored, cprint


env = simpy.Environment()
land = simpy.Resource(env, capacity=100)
def gen(n):
    for i in range(n):
        yield i
g = gen(1000)
B=[]

#--------------------------------- People------------------------------------#


class citizen:
    population = 0
    total_happiness = 0
    avg_happiness = 0
    citizen_list = []
    non_business = []

    
    def __init__(self, money, happiness,config=1):
        self.name = colored('{}'.format(names.get_full_name()), 'cyan')
        self.money=money
        self.happiness=happiness
        self.r_happiness=happiness
        self.employed = 0
        self.bank_id = 0
        self.bank_choice = 0
        self.credit = 700
        self.bank_account = [0,0,0]
        self.log = [['DAY {}'.format(simulation.Day)],[self.name, 'started with ${} and {} happiness'.format(self.money, self.happiness)]]
        citizen.population += 1
        citizen.total_happiness += happiness
        citizen.avg_happiness = citizen.total_happiness / citizen.population
        citizen.citizen_list.append(self)
        citizen.non_business.append(self)
        if config == 1:
            pass
        
    def get_food(self):
        try:
            if self.money >= 10:
                self.money -= 10
                choice = random.choices(food_c.food_c_list,weights=wants.company_influence[0])[0]
                choice.get_money(10,self)
                self.log.append(["bought food from {}.".format(choice.name)])
            else:
                if self.bank_account[0]>=10:
                    self.withdraw_money(10)
                    self.get_food()
                else:
                    self.happiness = 1
                    self.log.append(["couldn't afford food"])
                    print(self.name, "says, 'this sucks'")    
        except:
            print('No one gets to eat anymore')
            

            
    
    def make_company(self,amount):
        if self.money >= amount and amount >= 500:
            if company.company_list[1] == []:
                simulation.log.append(["Pre non business list is {}".format(len(citizen.non_business))])
                self.employed = 1
                self.money -= amount
                exec("%s = company(self,amount,1)" % ('B{}'.format(next(g))), globals(),locals())
                self.__class__ = business_owner
                simulation.log.append(["Post non business list is {}".format(len(citizen.non_business))])
                citizen.non_business.remove(self)
                wants.set_weights()
                return 1
            else:
                
                simulation.log.append(["Pre non business list is {}".format(len(citizen.non_business))])
                self.employed = 1
                self.money -= amount
                exec("%s = company(self,amount,random.randrange(len(company.company_list)))" % ('B{}'.format(next(g))), globals(),locals())
                self.__class__ = business_owner
                simulation.log.append(["Post non business list is {}".format(len(citizen.non_business))])
                citizen.non_business.remove(self)
                wants.set_weights()
                return 1
        else:
            return False
    
    def get_job(self):
        n=1
        for x in company.company_list:
            n += len(x)
        options = company.company_list
        products = list(range(len(options)))
        businesses = []
        for x in products:
            businesses.append(list(range(len(options[x]))))
        x = [i for i, e in enumerate(businesses) if e != []]
        products = x
        businesses = [ele for ele in businesses if ele != []]
        for i in range(n):  
            if i == 5 or products == []:
                self.log.append([self.name, 'has applied for all they can tody'])
                wants.set_weights()
                return 
            product_choice = random.choice(products)
            business_choice = random.choices(businesses[product_choice],weights=wants.company_influence[product_choice])[0]
            if options[product_choice][business_choice].hire(self) == True:
                self.employed = 1
                self.log.append([self.name, 'got hired at {}!'.format(options[product_choice][business_choice].name)])
                wants.set_weights()
                return 
            else:
                self.log.append([self.name, 'Applied at {}'.format(options[product_choice][business_choice].name)])
                x = [i for i, e in enumerate(businesses[product_choice]) if e == business_choice]
                wants.company_influence[product_choice].pop(x[0])
                businesses[product_choice].remove(business_choice)
                x = [i for i, e in enumerate(businesses) if e != []]
                products = x
                
    def get_money(self,amount):
        self.money += amount
        
    def choose_bank(self):
        try:
            self.bank_choice = random.choices(company.company_list[2],weights=wants.company_influence[2])[0]
            self.bank_choice.create_account(self)
        except:
            print('No banks available, sorry!')
        
    def business_loan(self,loan,business_investment):
        if bank.bank_c_list != []:
            if self.bank_choice == 0:
                self.choose_bank()            
                self.bank_choice.business_loan(self,loan,business_investment)
        
    def save_money(self,amount):
        if bank.bank_c_list != []:
            if self.bank_choice == 0:
                self.choose_bank()
            self.bank_choice.save(self,amount)
            
    def withdraw_money(self,amount):
        if bank.bank_c_list != []:
            if self.bank_choice == 0:
                self.choose_bank()
            self.bank_choice.withdraw(self,amount)
        
        
        
    def month_end(self):
        simulation.Unemployment += 1 - self.employed
        self.log.append([])
        
    def log_r(self):
        for x in range(len(self.log)):
            print(*self.log[x])




class business_owner(citizen):
    def say_hi(self):
        print("yo")
        

        
        
        
        
#------------------------------- Businesses----------------------------------#
        
class company:
    company_list = []
    company_product = ['food_c', 'manufacturing_c', 'bank']
    cost_mod = [10,0]

    def __init__(self,citizen,startup,product,cost=3):
        self.owner = citizen
        self.product = product
        self.expense_level = cost
        self.expand_ticker = 0
        self.worth = 0.6*startup
        self.funds = 0.2*startup
        self.recent_funds = self.funds
        self.employees = []
        self.employee_names = [citizen.name]
        self.job_positions = int(self.worth/100)
        self.worth_used = 0.5
        self.product_alignment(product,cost,startup)
        

    def product_alignment(self,product,cost,startup):
        exec('self.__class__ = %s' % (company.company_product[product]),globals(),locals())
        self.alignment[0].append(self)
        self.unique()
        self.wage = self.start_wage
        if product!= 1:
            choice = random.randrange(0,len(manufacturing_c.manufacturing_c_list))
            manufacturing_c.manufacturing_c_list[choice].get_money(0.2*startup,self)
        if not product == 2:
            self.cost = cost*company.cost_mod[product]
            self.alignment[1][cost].append(self)
        self.owner.log.append([self.owner.name, 'Started the business {}!'.format(self.name)])
        self.log = [['DAY {}'.format(simulation.Day)],[self.name, 'started by {}, is a {}, has ${} funds, and is worth {}'.format(self.owner.name,company.company_product[product],self.funds,self.worth)]]

    def month_end(self):
        self.finances_start()
        wage_data=self.wages()
        self.pay_owner(wage_data[0])
        self.pay_employees(wage_data[1],wage_data[2])
        self.pay_manufacturer(wage_data[3])
        self.finances_end(wage_data)
        self.evaluate_financial_standing(wage_data)
        self.worth_used = max(len(self.employees)/(self.positions_avaliable+1),0)

    def finances_start(self):
        self.income = round(self.funds - self.recent_funds,2)
        self.worth = round((0.3*self.income)+self.worth,2)       
        self.profit = 0.5*self.income
        self.log.append(["Today's income is ${}.".format(self.income)])
                                                                #Lots of fixed numbers here subject to be variables later
    def wages(self):
        owner_bonus = 0.2*self.profit
        owner_income = round(owner_bonus + self.wage,2)
        employee_income = self.wage
        employee_income_total = self.wage*len(self.employees)
        industrial_cost = round(0.5*self.income,2)
        wage_data = [owner_income,employee_income,employee_income_total,industrial_cost]
        return wage_data

    def pay_owner(self,owner_income):
        self.owner.get_money(owner_income)
        print(self.owner.name,'says, My company', self.name,'got me ${}'.format(owner_income))
        self.log.append(["{} got ${} from {}.".format(self.owner.name, owner_income, self.name)])
        self.owner.log.append([self.name, 'brought in {}'.format(owner_income)])
    
    def pay_employees(self,employee_income,employee_income_total): 
        for i in range(len(self.employees)):
            self.employees[i].get_money(employee_income)
            print(self.employees[i].name, 'says, "I got paid ${}"'.format(employee_income))
            self.employees[i].log.append(['Paid ${}.'.format(employee_income)])
        self.log.append(['paid employees total of ${}.'.format(employee_income_total)])

    def pay_manufacturer(self,industrial_cost):
        if self.product != 1:
            try:
                choice = random.choices(manufacturing_c.manufacturing_c_list,weights=wants.company_influence[1])[0]
                choice.get_money(industrial_cost,self)
                self.log.append(['Paid manufacturer, {}, ${}'.format(choice.name,industrial_cost)])
            except: 
                manufacturing_c.sad_fund += industrial_cost
                self.log.append(['The industry is gone, just paid some poor saps from out of town ${}'.format(industrial_cost)])

    
    def finances_end(self,wage_data):
        self.funds -= round(wage_data[0]+wage_data[2]+wage_data[3],2)
        self.recent_funds = round(self.funds,2)
        self.worth += round(0.1*self.funds,2)
        self.log.append(['Worth is now {} and funds are at ${}'.format(self.worth,self.funds)])
        
    def evaluate_financial_standing(self,wage_data):
        self.positions_avaliable = self.job_positions - len(self.employees)
        employee_potential = self.worth/100
        if self.expand_ticker >= 5:
            self.expand_ticker = 0
            self.job_positions += 1
        if self.job_positions < employee_potential:
            self.expand_ticker += 1
        if employee_potential < len(self.employees):
            self.expand_ticker = 0
            self.job_positions = max(int(employee_potential),0)
            self.lay_off()


       
    def get_money(self,amount,payer):
        self.funds += amount
        self.log.append(['got paid ${} by {}'.format(amount,payer.name)])
        
    def hire(self,civilian):
        if int(self.job_positions-len(self.employees)) > 0:
            self.employees.append(civilian)
            self.employee_names.append(civilian.name)
            print("Hired!,", civilian.name, self.name, "welcomes you \n")
            self.log.append(['Hired, {}!'.format(civilian.name)])
            return True
        else:
            return False
    
    def lay_off(self):
        if self.employees == [] and self.worth < -100:
            self.bankruptcy()
            return
        n = len(self.employees)-self.job_positions
        for i in range(n):
            victim = random.choice(self.employees)
            victim.employed = 0
            victim.log.append(['{} got fired by {} (lay off)! :('.format(victim.name,self.name)])
            self.log.append(['Had to lay off {}'.format(victim.name)])
            self.employees.remove(victim)

    def bankruptcy(self):
        print(self.name, "has gone bankrupt!")
        company.company_list[self.product].remove(self)
        if self.product == 2:
            if self.bank_end != 1:
                self.bank_failure()
        if not self.product == 2:
            self.alignment[1][self.expense_level].remove(self)
        self.owner.__class__ = citizen
        self.owner.employed = 0
        citizen.non_business.append(self.owner)
        self.__class__ = failed_c
        self.failed_c_list.append(self)
        self.log.append([self.name, "could not continue running. We are shutting down, indefinitely."])
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
    start_wage=15
    
    def unique(self):
        self.name = colored('{}'.format(CompNames.foodname()), 'green')

    
class manufacturing_c(company):
    sad_fund = 0
    manufacturing_c_list=[]
    company.company_list.append(manufacturing_c_list)
    manufacturing_costs = [[],[],[],[],[]]
    manufacturing_quality = [[],[],[],[],[]]
    alignment = [manufacturing_c_list, manufacturing_costs, manufacturing_quality]
    start_wage=15
    
    def unique(self):
        self.name = colored('{}'.format(CompNames.manufacturername()), 'green')

class failed_c(company):
    failed_c_list = []

#---------------------------Banking-------------------------------------------#

class bank(company):
    bank_c_list = []
    company.company_list.append(bank_c_list)
    minimum_reserve = 0.20
    loan_interest = 0.05
    saving_interest = 0.01
    alignment=[bank_c_list]
    start_wage = 15
    
    def unique(self):
        self.name = colored('{}'.format(CompNames.bankname()), 'green')
        self.members = []
        self.account_index = []
        self.savings = 0
        self.loans = 1
        self.business_loans = 2
        self.assets = 0
        self.liabilities = 0
        self.min_credit = 700
        self.warnings = 0
        self.bank_end = 0

    def create_account(self,citizen):
        self.members.append(citizen)
        self.account_index.append([0,0,0])
        citizen.bank_id = len(self.members)-1
        citizen.bank_choice = self
        
    def save(self,citizen,amount):
        self.account_index[citizen.bank_id][0]+= amount
        citizen.bank_account[0] = self.account_index[citizen.bank_id][0]
        self.liabilities += amount
        citizen.money -= amount

    def withdraw(self,citizen,amount):
        if self.account_index[citizen.bank_id][0] >= amount:
            self.account_index[citizen.bank_id][0]-= amount
            citizen.bank_account[0] = self.account_index[citizen.bank_id][0]
            self.liabilities -= amount
            citizen.money += amount
        else:
            return False            

    def business_loan(self,citizen,amount,target):
        if amount >= 500:
            if citizen.credit < 700:
                return False
            self.account_index[citizen.bank_id][2]+= amount
            self.assets += amount
            citizen.money += amount
            citizen.make_company(target)
            self.log.append(["Our client, {} was approved for a business loan of ${}!".format(citizen.name,amount)])
    
    def bank_month_end(self):
        for n in self.account_index:
            self.liabilities += n[0]*0.01
            n[0] = n[0]*1.01
            self.assets += n[1]*0.05
            n[1] = n[1]*0.05
            self.assets += n[2]*0.05
            n[1] = n[2]*0.05
        for n in self.members:
            n.bank_account[0]=self.account_index[n.bank_id][0]
            if self.account_index[n.bank_id][2] > 0:
                owed = 0.1*self.account_index[n.bank_id][2] + 36
                if n.money >= owed:
                    n.money -= owed
                    self.account_index[n.bank_id][2] -= owed
                    n.bank_account[2] = self.account_index[n.bank_id][2]
                    self.assets -= 0.8*owed
                    self.funds += 0.2*owed
                    n.credit += 5
                    self.log.append(["Recieved ${} off of {}'s interest payment of ${}".format(0.2*owed,n.name,owed)])
                    n.log.append('Made loan payment of ${} to {}'.format(owed,self.name))
                elif n.money < owed:
                    n.bank_account[2] = self.account_index[n.bank_id][2]
                    n.credit -= 5
                    self.log.append(["{} couldn't afford their interest payment of {}".format(n.name,owed)])
                    n.log.append('Missed loan payment of ${} to {}'.format(owed,self.name))
        self.log.append(["Assets aer {} Liabilities are at {} with {} clients".format(self.assets,self.liabilities,len(self.members))])
                    
        if (self.liabilities+1)/(self.assets+1) < bank.minimum_reserve:
            self.warnings += 1
            if self.warnings == 5:
                print(self.name, 'has broken the Federal Reserve Requirement too many times! They are being shut down')
                self.bankruptcy()
                
    def bank_failure(self):
        for n in self.members:
            n.bank_choice = 0
        self.bank_end = 1














#--------------------------------AI------------------------------------------#

class wants:
    company_influence = []
    overall_weight = 0
    
    def set_weights(): 
        wants.company_influence = []
        wants.overall_weight = 1                                                         #sets up a list containing the "influence" weight each company has due to their worth. indices in list line up with the indicies in the overall company list
        for i in range(len(company.company_list)):
            wants.company_influence.append([])
            for j in range(len(company.company_list[i])):
                wants.overall_weight += company.company_list[i][j].worth_used                         #need to sum through all companies
            for j in range(len(company.company_list[i])):                                     #now that overall weight is set, individual weights can be done
                wants.company_influence[i].append(company.company_list[i][j].worth/wants.overall_weight)











#-------------------------------- Simulation --------------------------------#

class simulation:
    Day = 0
    Unemployment = 0
    log = []
    
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
            citizen.citizen_list[i].make_company(500)
            citizen.citizen_list[i].log.append(['\n'])


    def one_day():
        simulation.Unemployment=0
        simulation.Day += 1
        print('DAY {}'.format(simulation.Day))
        i=0
        for n in citizen.non_business:
            i+=1
            if i % 5 == 0:
                choice = random.choice(citizen.non_business)
                simulation.log.append(["initially,",choice in citizen.non_business,choice.money])
                if choice.money >= 500:
                    print('wait!')
                    pass
                if not choice.make_company(500):
                    amount = random.randrange(500,1000,100)
                    simulation.log.append(["after,",choice in citizen.non_business])
                    choice.business_loan(amount,amount)
                else:
                    simulation.log.append(["made company with own money"])
        for j in range(len(company.company_list)):
            for i in company.company_list[j]:
                i.log.append(['DAY {}'.format(simulation.Day)])
        for i in citizen.citizen_list:
            i.log.append(['DAY {}'.format(simulation.Day)])
            i.get_food()
            if i.employed == 0:
                i.get_job()
        for j in range(len(company.company_list)):
            for i in company.company_list[j]:
                i.month_end()
        for i in bank.bank_c_list:
            i.bank_month_end()
        for i in citizen.citizen_list:
            i.month_end()
        print(simulation.Unemployment,"are unemployed \n")
        for j in range(len(company.company_list)):
            for i in company.company_list[j]:
                i.log.append('\n')
                
    def environment_update():
        wants.set_weights()
        
    def end_simulation():
        y=0
        for i in citizen.citizen_list:
            if i.money > y:
                y = i.money  
                richest_guy = i
        print(richest_guy.name, "is the richest with ${}.".format(y))
        global richest
        richest = richest_guy
        y = 0
        global c
        c= []
        for i in company.company_list:
            if i != []:
                for j in i:
                    c.append(j)
                    if j.worth > y:
                        y = j.worth
                        richest_company = j
        failed_c_results = []
        for i in company.company_list:
            failed_c_results.append(0)
        for i in failed_c.failed_c_list:
            failed_c_results[i.product] += 1
        print(richest_company.name, 'is the biggest company, owned by', richest_company.owner.name)
        print('There are {} businesses active and {} businessed that have failed'.format(len(c),len(failed_c.failed_c_list)))
        print("{} food companies failed, {} manufacturing companies failed, and {} banks failed".format(failed_c_results[0],failed_c_results[1],failed_c_results[2]))
        global richest_c
        richest_c = richest_company
        
    def log_r():
        for x in range(len(simulation.log)):
            print(*simulation.log[x])
                
#--------------------------------Test Commands-------------------------------#

simulation.start_simulation_env(100,10,30,60)
for x in range():
    simulation.one_day()
simulation.end_simulation()


