# Economy-Simulation
### An economy simulator to be run from the python console.
Latest version found in the Build 0.3 folder - [0.3.7](https://github.com/AHernanData/Economy-Simulation/blob/main/Build%200.3/Economy0.3.7.py)

Note: I created this project early on to see what I could do with Python. It is far from best practice, has a few unused elements, needs quite a bit of commentation, and serves mainly as a prototype. I may come back to revamp much of it in the future.

## Dependencies 

**names** and **termcolor** are required to run the script.

## Summary

The simulation script creates class objects for every citizen and company with randomly generated names. It is designed to mimic a simplified, modern economy with citizen agents and the companies they use, work for, or possibly own.

At the start of the simulation a population and wealth brackets (wealthy, middle, poor) designated with population percentages are assigned to start up the simulation. Wealthy enough citizens then create businesses.

The simulation runs, unemployed citizens apply for jobs and companies pay employees. Companies hire more individuals to make money, can become more "popular", and will lay off employees if they need to save or even file for bankrupcy when they hit wealth values that are too negative. Citizens buy food each month, take bank loans when needed, pay interest on loans, apply for jobs when unemployed, and occasionally take out business loans to create a new company.

At the end of the simulation, each object can be investigated to determine its attributes and the log_r method can be used to return a detailed log report of the events related to that citizen/company object.

## Simulation Parameters

The simulation parameters may be changed at the bottom of the script file under the "Test Commands" section in the "start_simulation_env()" method. Population is the number of citizen objects that will be present throughout the simulation, wealthy, middle, and poor are the percentages of the population in each wealth bracket at the start given as ints (exceeding 100 total is okay, they are weighted against their combined value). The value of the range function below that determines the number of simulated months the simulation will run for.


## Results Exploration

All objects have the log_r() method to print a log of events which occured to that particular object during the simulation.

Some useful global variables:
- richest - The citizen object with the highest wealth at the end of the simulation.
- richest_c - The company object with the highest wealth at the end of the simulation.
- richest_f, richest_m, richest_b - the richest food, manufacturing, and bank company objects respectively.
- oldest_f, oldest_m, oldest_b - the longest running (and not yet failed) food, manufacturing, and bank company objects respectively.

Useful citizen attributes:
- name - citizen's name
- money - the money held by the citizen
- employed - 0 means unemployed, 1 means employed
- credit - credit score of the citizen
- happiness - happiness value of the citizen (not too developed)

Useful company attributes:
- name - company's name (this can also be used to determine its business type; food companies have food names, banks have financial words in their names, manufacturing companies - are basically anything else)
- age - number of months the company has been running since its creation
- owner - the citizen object who created the company
- product - the product type of the business represented as an int. 0 : food company, 1 : manufacturing company, 2 : bank company
- worth - the value of the company which starts at 60% of the funds used to establish it and increases/decreases by 10% of the company's funds + 30% of the company's profits each month. (worth is used to determine popularity/influence and the maximum number of employees a company can have)
- funds - the actual cash a company has available
- employees -  a list of citizen objects who are the company's employees
- job_positions - the number of employees the company can hire
- influence - a value used to weigh the odds in this company's favor when citizens choose to interact with a company (apply for a job, buy food, take out a loan, ect)

Useful bank company specific attributes:
- members - a list of citizen objects who are the bank's current clients
- liabilities - total funds held in savings accounts by clients
- assets - total money loaned out to clients


## Example Images
### Simulation Start
![Run Start](https://github.com/AHernanData/Economy-Simulation/blob/main/images/hired.PNG?raw=true)

Here is the start of a simulation. "Month X" marks the current month of the simualtion and at the start all the newly founded companies are hiring new employees from the population. Citizens stating "this sucks" are those who are too poor to afford food during the current month.

### Mid Run
![Mid Run](https://github.com/AHernanData/Economy-Simulation/blob/main/images/during_run.PNG?raw=true)

This is an example of the simulation mid-run. Most logs are citizens being paid at their jobs and the business owners stating profits from their respective companies.

### Simulation End
![Run End](https://github.com/AHernanData/Economy-Simulation/blob/main/images/run_end.PNG?raw=true)

The end of a simulation starts by staing the number of unemployed individuals. Then it names off the richest citizen with their wealth and the richest company with its owner. Finally it states the number of active and failed businesses with a summary of each type of business that has failed.

### Citizen Log
![citizen log](https://github.com/AHernanData/Economy-Simulation/blob/main/images/r_citizen_log.PNG?raw=true)

Here is an example log from the richest citizen at the end of a run. Mr. Goodman started with a fair amount of wealth and created the company, Yummy Summer Squash which made them more money throughout the simulation.

### Company log
![company log](https://github.com/AHernanData/Economy-Simulation/blob/main/images/r_company_log.PNG?raw=true)

Here is an example company log of the company with the highest worth at the end of the simulation. Sauteed Vegetables company was started during month 3 by Willie Bonham and early on does not make much money as it starts taking on employees. 
By the end of month 13, however, the company is doing much better:

![company log end](https://github.com/AHernanData/Economy-Simulation/blob/main/images/r_company_log_end.PNG?raw=true)

Note that the company is making money from so many individuals that the log goes off the screen!


### Bank Failure
![Bank Fail](https://github.com/AHernanData/Economy-Simulation/blob/main/images/fed_reserve_failure.PNG)

During the simulation, banks must keep to a federal reserve limit of 20%. They will use their own funds to offset a failure to maintain the reserve at the end of a month, but if they fail to manage keeping to the reserve a total of 5 times, the bank will go bankrupt.











