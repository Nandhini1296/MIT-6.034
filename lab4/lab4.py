        # MIT 6.034 Lab 4: Constraint Satisfaction Problems
# Written by Dylan Holmes (dxh), Jessica Noss (jmn), and 6.034 staff

from constraint_api import *
from test_problems import get_pokemon_problem
import copy

#### PART 1: WRITE A DEPTH-FIRST SEARCH CONSTRAINT SOLVER

def has_empty_domains(csp) :
    "Returns True if the problem has one or more empty domains, otherwise False"
    var_list= csp.get_all_variables()
    for i in var_list:
        if len(csp.get_domain(i))==0:
            return True
    return False

def check_all_constraints(csp) :
    """Return False if the problem's assigned values violate some constraint,
    otherwise True"""
    val_list=csp.assigned_values
    for i in val_list:
        for j in val_list:
            con_list=csp.constraints_between(i,j)
            for k in con_list:
                if not k.check(val_list[i],val_list[j]):
                                return False
    return True
        

def solve_constraint_dfs(problem) :
    """Solves the problem using depth-first search.  Returns a tuple containing:
    1. the solution (a dictionary mapping variables to assigned values), and
    2. the number of extensions made (the number of problems popped off the agenda).
    If no solution was found, return None as the first element of the tuple."""
    count=0

    prob_list=[problem]


    

    while len(prob_list)>0:
        count+=1
        current_prob=prob_list.pop(0)
        if has_empty_domains(current_prob)or not check_all_constraints(current_prob):
                continue
        else:
                if len(current_prob.unassigned_vars)==0:
                    return (current_prob.assigned_values,count)
                else:
                    var=current_prob.pop_next_unassigned_var()
                    new_prob_list=[]
                    value_list=current_prob.get_domain(var)
                    for i in value_list:
                        new_prob=current_prob.copy()
                        new_prob.set_assigned_value(var,i)
                        new_prob_list.append(new_prob)
                    prob_list=new_prob_list+prob_list
            
    return (None,count)
                
                


#### PART 2: DOMAIN REDUCTION BEFORE SEARCH

def eliminate_from_neighbors(csp, var) :
    """Eliminates incompatible values from var's neighbors' domains, modifying
    the original csp.  Returns an alphabetically sorted list of the neighboring
    variables whose domains were reduced, with each variable appearing at most
    once.  If no domains were reduced, returns empty list.
##    If a domain is reduced to size 0, quits immediately and returns None."""


    neighbors=csp.get_neighbors(var)
    results=[]
    csp_new=csp.copy()
    var_values=csp.get_domain(var)
    for n in neighbors:
        eliminator=False
        constraints=csp.constraints_between(var,n)
        neighbor_domain=csp_new.get_domain(n)
        for neigh_val in neighbor_domain:
            condition=False
            for var_val in var_values:
                check_flag=True
                for constraint in constraints:
                    if not constraint.check(var_val,neigh_val):
                        check_flag=False
                        break
                if check_flag:
                    condition=True
                    break
            if not condition:
                csp.eliminate(n,neigh_val)
                eliminator=True
        if eliminator:
            results.append(n)
            if len(csp.get_domain(n))==0:
                      return None
    
    return sorted(set(results))
          
def domain_reduction(csp, queue=None) :
    """Uses constraints to reduce domains, modifying the original csp.
    If queue is None, initializes propagation queue by adding all variables in
    their default order.  Returns a list of all variables that were dequeued,
    in the order they were removed from the queue.  Variables may appear in the
    list multiple times.
    If a domain is reduced to size 0, quits immediately and returns None."""

    
    result=[]
    k=0
    if queue==None:
        queue=csp.get_all_variables()[:]
    while(len(queue))>0:
        var=queue.pop(0)
        result.append(var)
        eliminate=eliminate_from_neighbors(csp,var)
        if eliminate==None:
            return None
        for v in eliminate:
            if v not in queue:
                queue.append(v)
    return result

# QUESTION 1: How many extensions does it take to solve the Pokemon problem
#    with dfs if you DON'T use domain reduction before solving it?

# Hint: Use get_pokemon_problem() to get a new copy of the Pokemon problem
#    each time you want to solve it with a different search method.

def search_with_dfs():
    ans=solve_constraint_dfs(get_pokemon_problem())
    #print ans
#search_with_dfs()
    
ANSWER_1 =20

# QUESTION 2: How many extensions does it take to solve the Pokemon problem
#    with dfs if you DO use domain reduction before solving it?

def domain_before_search():
    omain_reduction(get_pokemon_problem(),queue=None)
    #print ans

#domain_before_search() 

ANSWER_2 =6


#### PART 3: PROPAGATION THROUGH REDUCED DOMAINS

def solve_constraint_propagate_reduced_domains(problem) :
    """Solves the problem using depth-first search with forward checking and
    propagation through all reduced domains.  Same return type as
    solve_constraint_dfs."""
    count=0

    prob_list=[problem]


    

    while len(prob_list)>0:
        current_prob=prob_list.pop(0)
        count+=1
        if has_empty_domains(current_prob)or not check_all_constraints(current_prob):
                continue
        else:
                if len(current_prob.unassigned_vars)==0:
                    return (current_prob.assigned_values,count)
                else:
                    var=current_prob.pop_next_unassigned_var()
                    #print("var",var)
                    new_prob_list=[]
                    value_list=current_prob.get_domain(var)
                    for i in value_list:
                        new_prob=current_prob.copy()
                        new_prob.set_assigned_value(var,i)
                        domain_reduction(new_prob,[var])
                        new_prob_list.append(new_prob)
                    prob_list=new_prob_list+prob_list
                    #print("unassigned",current_prob.unassigned_vars)
            
    return (None,count)

# QUESTION 3: How many extensions does it take to solve the Pokemon problem
#    with propagation through reduced domains? (Don't use domain reduction
#    before solving it.)

ANSWER_3 =7


#### PART 4: PROPAGATION THROUGH SINGLETON DOMAINS

def domain_reduction_singleton_domains(csp, queue=None) :
    """Uses constraints to reduce domains, modifying the original csp.
    Only propagates through singleton domains.
    Same return type as domain_reduction."""
        
    result=[]
    k=0
    if queue==None:
        queue=csp.get_all_variables()[:]
    while(len(queue))>0:
        var=queue.pop(0)
        result.append(var)
        eliminate=eliminate_from_neighbors(csp,var)
        if eliminate==None:
            return None
        for v in eliminate:
            if v not in queue and len(csp.get_domain(v))==1:
                queue.append(v)
    return result
    
                               

def solve_constraint_propagate_singleton_domains(problem) :
    """Solves the problem using depth-first search with forward checking and
    propagation through singleton domains.  Same return type as
    solve_constraint_dfs."""
    count=0

    prob_list=[problem]
 

    while len(prob_list)>0:
        count+=1
        current_prob=prob_list.pop(0)
        if has_empty_domains(current_prob)or not check_all_constraints(current_prob):
                continue
        else:
                if len(current_prob.unassigned_vars)==0:
                    return (current_prob.assigned_values,count)
                else:
                    var=current_prob.pop_next_unassigned_var()
                    ##print("var",var)
                    new_prob_list=[]
                    value_list=current_prob.get_domain(var)
                    for i in value_list:
                        new_prob=current_prob.copy()
                        new_prob.set_assigned_value(var,i)
                        domain_reduction_singleton_domains(new_prob,[var])
                        new_prob_list.append(new_prob)
                    prob_list=new_prob_list+prob_list
                    ##print("unassigned",current_prob.unassigned_vars)
            
    return (None,count)

# QUESTION 4: How many extensions does it take to solve the Pokemon problem
#    with propagation through singleton domains? (Don't use domain reduction
#    before solving it.)

ANSWER_4 =8


#### PART 5: FORWARD CHECKING

def propagate(enqueue_condition_fn, csp, queue=None) :
    """Uses constraints to reduce domains, modifying the original csp.
    Uses enqueue_condition_fn to determine whether to enqueue a variable whose
    domain has been reduced.  Same return type as domain_reduction."""
        
    result=[]
    k=0
    if queue==None:
        queue=csp.get_all_variables()[:]
    while(len(queue))>0:
        var=queue.pop(0)
        result.append(var)
        eliminate=eliminate_from_neighbors(csp,var)
        if eliminate==None:
            return None
        for v in eliminate:
            if v not in queue and enqueue_condition_fn(csp,v):
                queue.append(v)
    return result
                              


def condition_domain_reduction(csp, var) :
    """Returns True if var should be enqueued under the all-reduced-domains
    condition, otherwise False"""
    if csp==None or len(csp.get_domain(var))>=0:
        return True
    else:
        return False
    

def condition_singleton(csp, var) :
    """Returns True if var should be enqueued under the singleton-domains
     condition, otherwise False"""
    if len(csp.get_domain(var))==1:
        return True
    else:
        return False
 
def condition_forward_checking(csp, var) :
    """Returns True if var should be enqueued under the forward-checking
    condition, otherwise False"""
    if csp==None or len(csp.get_domain(var))>=0:
        return False
    else:
        return True


#### PART 6: GENERIC CSP SOLVER

def solve_constraint_generic(problem, enqueue_condition=None) :
    """Solves the problem, calling propagate with the specified enqueue
    condition (a function).  If enqueue_condition is None, uses DFS only.
    Same return type as solve_constraint_dfs."""
    count=0

    prob_list=[problem]
 

    while len(prob_list)>0:
        count+=1
        current_prob=prob_list.pop(0)
        if has_empty_domains(current_prob)or not check_all_constraints(current_prob):
                continue
        else:
                if len(current_prob.unassigned_vars)==0:
                    return (current_prob.assigned_values,count)
                else:
                    var=current_prob.pop_next_unassigned_var()
                    ##print("var",var)
                    new_prob_list=[]
                    value_list=current_prob.get_domain(var)
                    for i in value_list:
                        new_prob=current_prob.copy()
                        new_prob.set_assigned_value(var,i)
                        if enqueue_condition!=None:
                            propagate(enqueue_condition,new_prob,[var])
                        new_prob_list.append(new_prob)
                    prob_list=new_prob_list+prob_list
                    ##print("unassigned",current_prob.unassigned_vars)
            
    return (None,count)

# QUESTION 5: How many extensions does it take to solve the Pokemon problem
#    with DFS and forward checking, but no propagation? (Don't use domain
#    reduction before solving it.)

ANSWER_5 =9


#### PART 7: DEFINING CUSTOM CONSTRAINTS

def constraint_adjacent(m, n) :
    """Returns True if m and n are adjacent, otherwise False.
    Assume m and n are ints."""
    if abs(m-n)==1:
        return True
    else:
        return False
    

def constraint_not_adjacent(m, n) :
    """Returns True if m and n are NOT adjacent, otherwise False.
    Assume m and n are ints."""
    if abs(m-n)==1:
        return False
    else:
        return True

def all_different(variables) :
    """Returns a list of constraints, with one difference constraint between
    each pair of variables."""
    constraints_list=[]
##    for var1 in variables:
##        for var2 in variables:
##            constraint=Constraint(var1,var2,constraint_different)
##            if var1!=var2:
##                constraints_list.append(constraint)
    from itertools import combinations
    
    variable_list=combinations(variables,2)
    for var1,var2 in variable_list:
            constraint=Constraint(var1,var2,constraint_different)
            constraints_list.append(constraint)
    return constraints_list


#### PART 8: MOOSE PROBLEM (OPTIONAL)

moose_problem = ConstraintSatisfactionProblem(["You", "Moose", "McCain",
                                               "Palin", "Obama", "Biden"])

# Add domains and constraints to your moose_problem here:


# To test your moose_problem AFTER implementing all the solve_constraint
# methods above, change TEST_MOOSE_PROBLEM to True:
TEST_MOOSE_PROBLEM = False


#### SURVEY ###################################################

NAME ='Nandhini Rengaraj'
COLLABORATORS ='None'
HOW_MANY_HOURS_THIS_LAB_TOOK ='14'
WHAT_I_FOUND_INTERESTING ='Pokemon Problems'
WHAT_I_FOUND_BORING ='The long length of the lab questions'
SUGGESTIONS ='None'


###########################################################
### Ignore everything below this line; for testing only ###
###########################################################

if TEST_MOOSE_PROBLEM:
    # These lines are used in the local tester iff TEST_MOOSE_PROBLEM is True
    moose_answer_dfs = solve_constraint_dfs(moose_problem.copy())
    moose_answer_propany = solve_constraint_propagate_reduced_domains(moose_problem.copy())
    moose_answer_prop1 = solve_constraint_propagate_singleton_domains(moose_problem.copy())
    moose_answer_generic_dfs = solve_constraint_generic(moose_problem.copy(), None)
    moose_answer_generic_propany = solve_constraint_generic(moose_problem.copy(), condition_domain_reduction)
    moose_answer_generic_prop1 = solve_constraint_generic(moose_problem.copy(), condition_singleton)
    moose_answer_generic_fc = solve_constraint_generic(moose_problem.copy(), condition_forward_checking)
    moose_instance_for_domain_reduction = moose_problem.copy()
    moose_answer_domain_reduction = domain_reduction(moose_instance_for_domain_reduction)
    moose_instance_for_domain_reduction_singleton = moose_problem.copy()
    moose_answer_domain_reduction_singleton = domain_reduction_singleton_domains(moose_instance_for_domain_reduction_singleton)
