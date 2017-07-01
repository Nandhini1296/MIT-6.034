# MIT 6.034 Lab 1: Rule-Based Systems
# Written by 6.034 staff

from production import IF, AND, OR, NOT, THEN, DELETE, forward_chain
from data import *

#### Part 1: Multiple Choice #########################################

ANSWER_1 = '2'

ANSWER_2 = '4'

ANSWER_3 = '2'

ANSWER_4 = '0'

ANSWER_5 = '3'

ANSWER_6 = '1'

ANSWER_7 = '0'

#### Part 2: Transitive Rule #########################################

transitive_rule = IF( AND('(?x) beats (?y)','(?y) beats (?z)'),
                      THEN('(?x) beats (?z)'))

# You can test your rule by uncommenting these print statements:
print forward_chain([transitive_rule], abc_data)
print forward_chain([transitive_rule], poker_data)
print forward_chain([transitive_rule], minecraft_data)


#### Part 3: Family Relations #########################################

# Define your rules here:
rule1=IF(('person (?x)'),
         THEN ('self (?x) (?x)'))
rule2=IF( AND( 'parent (?x) (?y)','parent (?x) (?z)',NOT ('self (?y) (?z)')),
        THEN ('sibling (?y) (?z)'))
rule3=IF( AND('parent (?x) (?y)'),
        THEN ('child (?y) (?x)'))
rule4=IF( AND( 'parent (?x) (?y)','parent (?z) (?w)', 'sibling (?x) (?z)',NOT ('self (?y) (?w)')),
        THEN ('cousin (?y) (?w)'),('cousin (?w) (?y)'))
rule5=IF( AND( 'parent (?x) (?y)','parent (?y) (?z)'),
        THEN('grandparent (?x) (?z)'))
rule6=IF( AND( 'parent (?x) (?y)','parent (?y) (?z)'),
        THEN('grandchild (?z) (?x)'))
# Add your rules to this list:
family_rules = [rule1,rule2,rule3,rule4,rule5,rule6]


# Uncomment this to test your data on the Simpsons family:
print forward_chain(family_rules, simpsons_data, verbose=False)

# These smaller datasets might be helpful for debugging:
#print forward_chain(family_rules, sibling_test_data, verbose=True)
#print forward_chain(family_rules, grandparent_test_data, verbose=True)

# The following should generate 14 cousin relationships, representing 7 pairs
# of people who are cousins:
black_family_cousins = [
    relation for relation in
    forward_chain(family_rules, black_data, verbose=False)
    if "cousin" in relation ]

# To see if you found them all, uncomment this line:
print black_family_cousins


#### Part 4: Backward Chaining #########################################

# Import additional methods for backchaining
from production import PASS, FAIL, match, populate, simplify, variables

def backchain_to_goal_tree(rules, hypothesis):
    """
    Takes a hypothesis (string) and a list of rules (list
    of IF objects), returning an AND/OR tree representing the
    backchain of possible statements we may need to test
    to determine if this hypothesis is reachable or not.

    This method should return an AND/OR tree, that is, an
    AND or OR object, whose constituents are the subgoals that
    need to be tested. The leaves of this tree should be strings
    (possibly with unbound variables), *not* AND or OR objects.
    Make sure to use simplify(...) to flatten trees where appropriate.
    """
    results=[hypothesis]
    for rule in rules:
        consequent=rule.consequent()
        for expr in consequent:
           bindings=match(expr,hypothesis)
           if bindings or expr == hypothesis:
                antecedent=rule.antecedent()
                if isinstance(antecedent,str):
                   new_hypothesis=populate(antecedent,bindings)
                   results.append(backchain_to_goal_tree(rules,new_hypothesis))
                   results.append(new_hypothesis)
                else:
                    statements=[populate(new_antecedent,bindings) for new_antecedent in antecedent]
                    new_results=[]
                    for statement in statements:
                        new_results.append(backchain_to_goal_tree(rules,statement))
                    if isinstance (antecedent, AND):
                        results.append(AND(new_results))
                    elif isinstance(antecedent,OR):
                        results.append(OR(new_results))
    return simplify(OR(results))

                    
                                         
# Uncomment this to run your backward chainer:
print backchain_to_goal_tree(zookeeper_rules, 'opus is a penguin')


#### Survey #########################################

NAME ='Nandhini Rengaraj'
COLLABORATORS ='None'
HOW_MANY_HOURS_THIS_LAB_TOOK =8
WHAT_I_FOUND_INTERESTING ='Family based rule systems'
WHAT_I_FOUND_BORING ='Multiple choice questions'
SUGGESTIONS ='None'


###########################################################
### Ignore everything below this line; for testing only ###
###########################################################

# The following lines are used in the tester. DO NOT CHANGE!
transitive_rule_poker = forward_chain([transitive_rule], poker_data)
transitive_rule_abc = forward_chain([transitive_rule], abc_data)
transitive_rule_minecraft = forward_chain([transitive_rule], minecraft_data)
family_rules_simpsons = forward_chain(family_rules, simpsons_data)
family_rules_black = forward_chain(family_rules, black_data)
family_rules_sibling = forward_chain(family_rules, sibling_test_data)
family_rules_grandparent = forward_chain(family_rules, grandparent_test_data)
family_rules_anonymous_family = forward_chain(family_rules, anonymous_family_test_data)
