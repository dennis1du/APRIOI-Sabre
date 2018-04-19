# -*- coding: utf-8 -*-

'''
i--m: crew member
j--n: pairing
d--dn: date
'''

import pyomo.environ as pe
import pyomo.opt
from Data_V3 import * 

model= pe.ConcreteModel()

'''Define parameters, sets & indices, and variables'''
optimality_gap = 0.1
# Model Parameters
c1=0
c2=1
c3=0
upper_hard = 100
upper_soft = 95
lower_soft = 85
upper_dayoff = 24
upper_layover = 4

# Global Parameters
model.bh = BH_j
model.do = DO_jd
model.ld = LD_j
model.lj = L_j
model.lnmax = LNMax_j
model.lnmin = LNMin_j

store_ol = [[]]
for g in range(1,n):
    for h in range(g+1,n+1):
        if O_gh[g][h] == 1:
            store_ol.append([g,h])
model.ol = pe.Set(initialize = set(range(1,len(store_ol))))

# Preference Parameters
store_cp1 = [[]]
for i in range(1,m):
    if CP1_i[i] != -1:
        store_cp1.append([i, CP1_i[i]])
model.cp1 = pe.Set(initialize = set(range(1,len(store_cp1))))

store_cp2j = [[]]
for i in range(1,m):
    row = [[]]
    for j in range(1,n):
        if PL_j[j] == CP2_i[i]:
            row.append(j)
    store_cp2j.append(row)

store_cp2i = [[]]
for i in range(1,m):
    if CP2_i[i] != -1:
        store_cp2i.append(i)
model.cp2 = pe.Set(initialize = set(range(1,len(store_cp2i))))

store_cp3max = [[]]
for i in range(1,m):
    if CP3Max_i[i] != -1:
        store_cp3max.append([i, CP3Max_i[i]])
model.cp3max = pe.Set(initialize = set(range(1,len(store_cp3max))))

store_cp3min = [[]]
for i in range(1,m):
    if CP3Min_i[i] != -1:
        store_cp3min.append([i, CP3Min_i[i]])
model.cp3min = pe.Set(initialize = set(range(1,len(store_cp3min))))

# Sets and indices
model.i = pe.Set(initialize = set(range(1,m+1)))
model.j = pe.Set(initialize = set(range(1,n+1)))
model.d = pe.Set(initialize = set(range(1,dn+1)))
model.dd = pe.Set(initialize = set(range(1,dn+1-6)))

# Variables
model.x = pe.Var(model.i, model.j, within = pe.Binary)
model.y = pe.Var(model.i, model.d, within = pe.Binary)
model.s1 = pe.Var(model.i, within = pe.NonNegativeReals)
model.s2 = pe.Var(model.i, within = pe.NonNegativeReals)

'''Objective Function'''
def obj_rule(model):
    total_cost = 0
    for i in model.i:
        for j in model.j:
            pairingdays_assigned = model.ld[j] * model.x[i,j]
            blockhours_assigned = model.bh[j] * model.x[i,j]
            cost =  c1*pairingdays_assigned + c2*blockhours_assigned
            total_cost += cost
        total_cost = total_cost - c3*(model.s1[i]+model.s2[i])
    obj = total_cost
    return obj  
model.obj = pe.Objective(rule = obj_rule, sense = pe.maximize)

'''Variable Constraints'''
def y_rule1(model, i, d):
    return sum ((model.do[j][d] * model.x[i,j]) for j in range(1,n+1)) <= 5*model.y[i,d]
model.y_rule1 = pe.Constraint(model.i, model.d, rule = y_rule1)

def y_rule2(model, i, d):
    return sum ((model.do[j][d] * model.x[i,j]) for j in range(1,n+1)) >= model.y[i,d]
model.y_rule2 = pe.Constraint(model.i, model.d, rule = y_rule2)

''' Global Constraints'''
### for all i (m)
# block hour - hard
def block_hard_rule(model, i):
    return sum ((model.bh[j] * model.x[i,j]) for j in range(1,n+1)) <= upper_hard
model.block_hard_rule = pe.Constraint(model.i, rule = block_hard_rule)

# block hour - soft
def block_soft_upper(model, i):
    return sum ((model.bh[j] * model.x[i,j]) for j in range(1,n+1)) <= upper_soft + model.s2[i]
model.block_soft_upper = pe.Constraint(model.i, rule = block_soft_upper)

def block_soft_lower(model, i):
    return sum ((model.bh[j] * model.x[i,j]) for j in range(1,n+1)) >= lower_soft - model.s1[i]
model.block_soft_lower = pe.Constraint(model.i, rule = block_soft_lower)

# Min Days off in a planning period (Max Work)
def mindayoff_rule(model, i):
    return sum( model.y[i,d] for d in range(1,dn+1)) <= upper_dayoff
model.mindayoff_rule = pe.Constraint(model.i, rule = mindayoff_rule)

# Max pairings with layover in a planning period
def maxlayoverpairing_rule(model, i):
    return sum ((model.lj[j] * model.x[i,j]) for j in range(1,n+1)) <= upper_layover
model.maxlayoverpairing_rule = pe.Constraint(model.i, rule = maxlayoverpairing_rule)

# overlap constraint
def overlap_rule(model, i, ol):
    return (model.x[i,store_ol[ol][0]] + model.x[i,store_ol[ol][1]])  <= 1
model.overlap_rule = pe.Constraint(model.i, model.ol, rule = overlap_rule)

### for all j (n)
# we assume now that one pairing can only assigned to one crewmember
def onetoone_rule(model, j):
    return sum((model.x[i,j]) for i in range(1,m+1)) <= 1
model.onetoone_rule = pe.Constraint(model.j, rule = onetoone_rule)

# at least 1 day off in consecutive 7 days
def one_off_day(model, i, d):
    return sum(model.y[i,d] for d in range(d,d+7)) <= 6
model.one_off_day = pe.Constraint(model.i, model.dd, rule = one_off_day)

''' Preference Constraints'''
# CP1
def CP1(model, cp1):
    return model.y[store_cp1[cp1][0], store_cp1[cp1][1]] == 0
model.CP1 = pe.Constraint(model.cp1, rule = CP1)

def CP2(model, cp2):
    return sum(model.x[store_cp2i[cp2],store_cp2j[store_cp2i[cp2]][j]] for j in range(1,len(store_cp2j[store_cp2i[cp2]]))) >= 1
model.CP2 = pe.Constraint(model.cp2, rule = CP2)

def CP3Max(model, cp3max, j):
    return model.x[store_cp3max[cp3max][0],j]*model.lnmax[j] <= store_cp3max[cp3max][1]
model.CP3Max = pe.Constraint(model.cp3max, model.j, rule = CP3Max)
'''
def CP3Min(model, cp3min, j):
    return model.x[store_cp3min[cp3min][0],j]*model.lnmin[j] >= store_cp3min[cp3min][1]
model.CP3Min = pe.Constraint(model.cp3min, model.j, rule = CP3Min)'''

'''Solve'''
opt = pyomo.opt.SolverFactory('cplex')
opt.options["mip_tolerances_mipgap"] = optimality_gap
#opt.options["mip_strategy_probe"] = 3
#opt.options["mip_strategy_search"] = 2
#opt.options["mip_cuts_gomory"] = 2
#opt.options["timelimit"] = 1800
results=opt.solve(model, tee=True, keepfiles=True)
x = model.x.get_values()
x_nonzero = [ key for (key, value) in x.items() if value >.5]
y = model.y.get_values()
y_nonzero = [ key for (key, value) in y.items() if value >.5]
if __name__ == '__main__':
    results.write()
    print(x_nonzero)
