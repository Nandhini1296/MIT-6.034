# MIT 6.034 Lab 8: Bayesian Inference
# Written by Dylan Holmes (dxh), Jessica Noss (jmn), and 6.034 staff

from nets import *


#### ANCESTORS, DESCENDANTS, AND NON-DESCENDANTS ###############################

def get_ancestors(net, var):
    "Return a set containing the ancestors of var"
    ancestors=list(net.get_parents(var))
    for val in net.get_parents(var):
        ancestors.extend(get_ancestors(net,val))
    return set(ancestors)

def get_descendants(net, var):
    "Returns a set containing the descendants of var"
    descendants=list(net.get_children(var))
    for val in net.get_children(var):
        descendants.extend(get_descendants(net,val))
    return set(descendants)

def get_nondescendants(net, var):
    "Returns a set containing the non-descendants of var"
    variables=net.get_variables()
    descendants=list(get_descendants(net,var))
    non_descendants=[]
    for val in variables:
        if val not in descendants:
            non_descendants.append(val)
    non_descendants.remove(var)
    return set(non_descendants)

def simplify_givens(net, var, givens):
    """If givens include every parent of var and no descendants, returns a
    simplified list of givens, keeping only parents.  Does not modify original
    givens.  Otherwise, if not all parents are given, or if a descendant is
    given, returns original givens."""
    parents=net.get_parents(var)
    

    for parent in parents:
        if parent not in givens:
            return givens

    descendants=get_descendants(net,var)

    for d in descendants:
        if d in givens:
            return givens

    my_dict={}
    for val in givens.keys():
        if val in parents:
            my_dict[val]=givens.get(val)
    return my_dict


#### PROBABILITY ###############################################################

def probability_lookup(net, hypothesis, givens=None):
    "Looks up a probability in the Bayes net, or raises LookupError"
    try:
        new_givens=simplify_givens(net,hypothesis.keys()[-1],givens)
        probability=net.get_probability(hypothesis,new_givens,True)
        return probability
    except TypeError:
        probability=net.get_probability(hypothesis,givens,True)
        return probability
    except ValueError:
        raise LookupError("LookupError")
    except LookupError:
        raise LookupError("LookupError")

def probability_joint(net, hypothesis):
    "Uses the chain rule to compute a joint probability"
    variables=net.topological_sort()
    variables.reverse()
    prob=1.0
    givens={}
    for var in variables:
            prob=prob*probability_lookup(net,{var:hypothesis.pop(var)},simplify_givens(net,var,hypothesis))    
    return prob

def probability_marginal(net, hypothesis):
    "Computes a marginal probability as a sum of joint probabilities"
    p_marginal=0
    combinations=net.combinations(net.get_variables(),hypothesis)
    for dictionary in combinations:
        p_marginal=p_marginal+probability_joint(net,dictionary)
    return p_marginal

def probability_conditional(net, hypothesis, givens=None):
    "Computes a conditional probability as a ratio of marginal probabilities"
    if givens==None:
        givens={}
    for key in hypothesis:
        if key in givens:
            if givens.get(key)!= hypothesis.get(key):
                return 0.0
    all_hypothesis=dict(hypothesis,**givens)
    return probability_marginal(net,all_hypothesis)/probability_marginal(net,givens)
    

def probability(net, hypothesis, givens=None):
    "Calls previous functions to compute any probability"
    if givens=={}:
        return probability_marginal(net,hypothesis)
    else:
        return probability_conditional(net,hypothesis,givens)


#### PARAMETER-COUNTING AND INDEPENDENCE #######################################

def number_of_parameters(net):
    "Computes minimum number of parameters required for net"
    num=0
    pairings=[]
    for var in net.get_variables():
        parents=list(net.get_parents(var))
        for combo in net.combinations(parents,None):
            pairings.append(combo)
        num+=(len(net.get_domain(var))-1)*len(pairings)
        pairings=[]
    return num


def is_independent(net, var1, var2, givens=None):
    """Return True if var1, var2 are conditionally independent given givens,
    otherwise False.  Uses numerical independence."""
    flag=True
    if givens==None:
        givens={}
    next_givens=givens.copy()
    for val1 in net.get_domain(var1):
        for val2 in net.get_domain(var2):
            givens.update({var2:val2})
            if approx_equal(probability_conditional(net,{var1:val1},givens),probability_conditional(net,{var1:val1},next_givens),0.00001):
                pass
            else:
                flag=False
    return flag
                
    

   
    
                                    
def is_structurally_independent(net, var1, var2, givens=None):
    """Return True if var1, var2 are conditionally independent given givens,
    based on the structure of the Bayes net, otherwise False.
    Uses structural independence only (not numerical independence)."""
    ancestors1=get_ancestors(net,var1)
    ancestors1.add(var1)
    ancestors2=get_ancestors(net,var2)
    ancestors2.add(var2)
    ancestors=ancestors1.union(ancestors2)
    
    if givens!=None:
        ancestors=ancestors.union(givens)
        for each in givens.keys():
            p=set(get_ancestors(net,each))
            ancestors=ancestors.union(p)
    my_net=net.subnet(ancestors)
    for var in ancestors:
        parents=net.get_parents(var)
        if parents=={}:
            pass
        else:
            for parent1 in list(parents)[:-1]:
                
                 for parent2 in list(parents)[1:]:
                     
                     my_net=my_net.link(parent1,parent2)
                     my_net=my_net.link(parent2,parent1)
             
    my_net=my_net.make_bidirectional()
    
    if givens!={} and givens!=None:
        for each in givens.keys():
            if each in my_net.get_variables():
                my_net=my_net.remove_variable(each)
    
    if var1 not in my_net.get_variables() or var2 not in my_net.get_variables():
        flag=True
    else:    
        if my_net.find_path(var1,var2)==None:
            flag=True
        else:
            flag=False

    return flag
                     


#### SURVEY ####################################################################

NAME ='Nandhini Rengaraj'
COLLABORATORS ='None'
HOW_MANY_HOURS_THIS_LAB_TOOK =6
WHAT_I_FOUND_INTERESTING ='Probability calculations'
WHAT_I_FOUND_BORING ='None'
SUGGESTIONS ='None'
