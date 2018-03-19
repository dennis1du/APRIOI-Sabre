# -*- coding: utf-8 -*-

import pyomo.environ as pe
import pyomo.opt
from Data import * 

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
model.l = L_j

# Preference Parameters


# Sets and indices
model.i = pe.Set(initialize = set(range(1,m+1)))
model.j = pe.Set(initialize = set(range(1,n+1)))
model.l = pe.Set(initialize = set(range(1,ln+1)))
model.d = pe.Set(initialize = set(range(1,dn+1)))

# Variables
model.x = pe.Var(model.i, model.j, within = pe.Binary)
model.s1 = pe.Var(model.i, within = pe.NonNegativeReals)
model.s2 = pe.Var(model.i, within = pe.NonNegativeReals)

'''Objective function'''
def obj_rule(model):
    total_cost = 0
    for i in model.i:
        for j in model.j:
            pairingdays_assigned = LD[j] * model.x[i,j]
            blockhours_assigned = BH[j] * model.x[i,j]
            score =  pairingdays_assigned + blockhours_assigned
            total_score += score
        total_score = total_score - 100*(model.s1[i] + model.s2[i])
    obj = total_score
    return obj  
model.obj = pe.Objective(rule = obj_rule, sense = pe.maximize)

i: crew member
j: pairing CP
d: day of the month[1:31]
l: layover ID
i--m
j--n
d--dn
l--ln
#### for all i (n)

''' Global Constraints'''
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
    return sum((sum ((model.do[i][j] * model.x[i,j]) for j in range(1,n+1))) for d in range(1,dn+1)) <= 23
model.mindayoff_rule = pe.Constraint(model.i, rule = mindayoff_rule)

# Max pairings with layover in a planning period
def maxlayoverpairing_rule(model, i):
    return sum ((model.l[j] * model.x[i,j]) for j in range(1,n+1)) <= 4
model.maxlayoverpairing_rule = pe.Constraint(model.i, rule = maxlayoverpairing_rule)

#### for all j (m)
#GC- we assume now that one pairing can only assigned to one crewmember
def onetoone_rule(model, j):
    return sum((model.x[i,j]) for i in range(1,m+1)) <= 1
model.onetoone_rule = pe.Constraint(model.j, rule = onetoone_rule)

#### overlap
def overlap_rule(model, j):
    for
    if    : 
    	return sum((model.x[i,j]) for i in range(1,n+1)) <= 1

model.overlap_rule = pe.Constraint(model.j, rule = overlap_rule)
