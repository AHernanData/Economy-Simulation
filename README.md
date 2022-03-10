# Economy-Simulation
### An economy simulator to be run from the console.

Note: I created this project early on to see what I could do with Python. It is far from best practice, has a few unused elements, needs quite a bit of commentation, and serves mainly as a prototype. I may come back to revamp much of it in the future.

Needed dependancies: names, simpy, termcolor

## Summary

The simulation script creates class objects for every citizen and company with randomly generated names.

At the start of the simualtion a population and wealth brackets (wealthy, middle, poor) designated with population percentages are assigned to start up the simulation. Wealthy enough citizen then create businesses.

The simulation runs, unemployed citizens apply for jobs and companies pay employees. Companies hire more individuals to make money, can become more "popular", and will lay off employees if they need to save or even file for bankrupcy when they hit low wealth values that are too negative. Citizens buy food each month, take bank loans when needed, pay interest on loans, apply for jobs when unemployed, and occaisionally take out business loans to create a new company.

At the end of the simulation, each object can be investigated to determine its stats and the log_r method can be used to return a datailed log report of the events related to that citizen/business object.

## Simulation Parameters

The simulation parameters may be changed at the bottom of the script file under the "Test Commands" section in the "start_simulation_env()" method. Population is the number of citizen objects that will be present throughout the simulation, wealthy, middle, and poor are the percentages of the population in each wealth bracket at the start. The value of the range function below that dtermines the number of simulated months the simulation will run for.


## Results Exploration

All objects have the log_r() method to print a log of events which occured to that particular object during the simulation.

Some useful global variables:
richest - The citizen object with the highest wealth at the end of the simulation.
richest_c - The company object with the highest wealth at the end of the simulation.
richest_f, richest_m, richest_b - the richest food, manufacturing, and bank company objects respectively.
oldest_f, oldest_m, oldest_b - the longest running (and not yet failed) food, manufacturing, and bank company objects respectively.

Useful citizen attributes:
name - citizen's name
money - the money held by the citizen
employed - 0 means unemployed, 1 means employed
credit - credit score of the citizen
happiness - happiness value of the citizen (not too developed)

Useful company attributes:
name - company's name (this can also be used to determine its business type; food companies have food names, banks have financial words in their names, manufacturing companies are basically anything else)
age - number of months the company has been running since its creation
owner - the citizen object who created the company
product - the product type of the business represented as an int. 0 : food company, 1 : manufacturing company, 2 : bank company
worth - the value of the company which starts at 60% funds used to establish it and increases/decreases by 10% of the company's funds + 30% of the company's profits each month. (worth is used to determine popularity/influence and the maximum number of employees a company can have)
funds - the actual cash a company has available
employees -  a list of citizen objects who are the company's employees
job_positions - the number of employees the company can hire
influence - a value used to weigh the odds in this companies favor when citizens choose to interact with a company (apply for a job, buy food, take out a loan, ect)

Useful bank company specific attributes:
members - a list of citizen objects who are the bank's current clients
liabilities - total funds held in savings accounts by clients
assets - total money loaned out to clients




