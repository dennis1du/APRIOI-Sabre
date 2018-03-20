# -*- coding: utf-8 -*-
'''
i: crew member
j: pairing CP
d: day of the month[1:31]
l: layover ID
i--m
j--n
d--dn
l--ln
'''

import pyomo.environ as pe
import pyomo.opt
from Matrix_Data import * 

model= pe.ConcreteModel()

'''Define parameters, sets & indices, and variables'''
# Global Parameters
model.bh = BH_j
model.lh = LH_j
model.do = DO_jd
model.lo = LO_jl
model.ln = LN_j
model.ld = LD_j
model.ol = O_gh
model.lj = L_j

# Preference Parameters


# Sets and indices
model.i = pe.Set(initialize = set(range(1,m+1)))
model.j = pe.Set(initialize = set(range(1,n+1)))
model.l = pe.Set(initialize = set(range(1,ln+1)))
model.d = pe.Set(initialize = set(range(1,dn+1)))

store = [[]]
for g in range(1,n):
    for h in range(g+1,n+1):
        if O_gh[g][h] == 1:
            store.append([g,h])
model.s = pe.Set(initialize = set(range(1,len(store))))

# Variables
model.x = pe.Var(model.i, model.j, within = pe.Binary)
model.s1 = pe.Var(model.i, within = pe.NonNegativeReals)
model.s2 = pe.Var(model.i, within = pe.NonNegativeReals)

'''Objective function'''
def obj_rule(model):
    total_cost = 0
    for i in model.i:
        for j in model.j:
            pairingdays_assigned = model.ld[j] * model.x[i,j]
            blockhours_assigned = model.bh[j] * model.x[i,j]
            cost =  pairingdays_assigned + blockhours_assigned
            total_cost += cost
        total_cost = total_cost - 100*(model.s1[i]+model.s2[i])
    obj = total_cost
    return obj  
model.obj = pe.Objective(rule = obj_rule, sense = pe.maximize)

''' Global Constraints'''

### for all i (m)
# block hour - hard
def block_hard_rule(model, i):
    return sum ((model.bh[j] * model.x[i,j]) for j in range(1,n+1)) <= 100
model.block_hard_rule = pe.Constraint(model.i, rule = block_hard_rule)

# block hour - soft

def block_soft_upper(model, i):
    return sum ((model.bh[j] * model.x[i,j]) for j in range(1,n+1)) <= 95 + model.s2[i]
model.block_soft_upper = pe.Constraint(model.i, rule = block_soft_upper)

def block_soft_lower(model, i):
    return sum ((model.bh[j] * model.x[i,j]) for j in range(1,n+1)) >= 85 - model.s1[i]
model.block_soft_lower = pe.Constraint(model.i, rule = block_soft_lower)

# Min Days off in a planning period (Max Work)
def mindayoff_rule(model, i):
    return sum((sum ((model.do[j][d] * model.x[i,j]) for j in range(1,n+1))) for d in range(1,dn+1)) <= 23
model.mindayoff_rule = pe.Constraint(model.i, rule = mindayoff_rule)

# Max pairings with layover in a planning period
def maxlayoverpairing_rule(model, i):
    return sum ((model.lj[j] * model.x[i,j]) for j in range(1,n+1)) <= 4
model.maxlayoverpairing_rule = pe.Constraint(model.i, rule = maxlayoverpairing_rule)

### for all j (n)
# we assume now that one pairing can only assigned to one crewmember
def onetoone_rule(model, j):
    return sum((model.x[i,j]) for i in range(1,m+1)) <= 1
model.onetoone_rule = pe.Constraint(model.j, rule = onetoone_rule)

# overlap constraint
def overlap_rule(model, i, s):
    return (model.x[i,store[s][0]] + model.x[i,store[s][1]])  <= 1
model.overlap_rule = pe.Constraint(model.i, model.s, rule = overlap_rule)

'''Solve'''
'''
if __name__ == '__main__':
    opt= pyomo.opt.SolverFactory("cplex")
    #optimality_gap = 0.05
    #opt.options["mip_tolerances_mipgap"] = optimality_gap
    #opt.options["mip_strategy_probe"] = 3
    #opt.options["mip_strategy_search"] = 2
    #opt.options["mip_cuts_gomory"] = 2
    #opt.options["timelimit"] = 1800
    results=opt.solve(model, tee=True, keepfiles=True)
    results.write()'''
