# MIT 6.034 Lab 9: Boosting (Adaboost)
# Written by Jessica Noss (jmn), Dylan Holmes (dxh), and 6.034 staff

from math import log as ln
from utils import *



#### BOOSTING (ADABOOST) #######################################################

def initialize_weights(training_points):
    """Assigns every training point a weight equal to 1/N, where N is the number
    of training points.  Returns a dictionary mapping points to weights."""
    result={}
    weight=make_fraction(1,len(training_points))
    for point in training_points:
        result[point]=weight
        
    return result

def calculate_error_rates(point_to_weight, classifier_to_misclassified):
    """Given a dictionary mapping training points to their weights, and another
    dictionary mapping classifiers to the training points they misclassify,
    returns a dictionary mapping classifiers to their error rates."""
    error_rate={}
    result={}
    for classifier in classifier_to_misclassified:
        points_list=classifier_to_misclassified[classifier]
        error=0
        for point in points_list:
            error+=point_to_weight[point]
        result[classifier]=error

    return result

        

def pick_best_classifier(classifier_to_error_rate, use_smallest_error=True):
    """Given a dictionary mapping classifiers to their error rates, returns the
    best* classifier, or raises NoGoodClassifiersError if best* classifier has
    error rate 1/2.  best* means 'smallest error rate' if use_smallest_error
    is True, otherwise 'error rate furthest from 1/2'."""
    results=classifier_to_error_rate.copy()
    try:
        if use_smallest_error:
            val=min(sorted(results),key=results.get)
            if results.get(val)==make_fraction(1,2):
                raise NoGoodClassifiersError("NoGoodClassifiersError")
            else:
                return val
        else:
            for classifier in results:
                    val=make_fraction(abs(results[classifier]-make_fraction(1,2)))
                    results[classifier]=val
            best_classifier=max(sorted(results),key=results.get)
            if results.get(best_classifier)==0:
                raise NoGoodClassifiersError("NoGoodClassifiersError")
            else:
                return best_classifier

    except NoGoodClassifiersError:
            raise NoGoodClassifiersError("NoGoodClassifiersError")

def calculate_voting_power(error_rate):
    """Given a classifier's error rate (a number), returns the voting power
    (aka alpha, or coefficient) for that classifier."""
    if error_rate==0:
        return INF
    elif error_rate==1:
        return -INF
    else:
        return 1/2.0*ln((1-error_rate)/error_rate)

def get_overall_misclassifications(H, training_points, classifier_to_misclassified):
    """Given an overall classifier H, a list of all training points, and a
    dictionary mapping classifiers to the training points they misclassify,
    returns a set containing the training points that H misclassifies.
    H is represented as a list of (classifier, voting_power) tuples."""
    misclassified_points=[]
    for point in training_points:
        inc=0
        for voting_power in H:
            if point in classifier_to_misclassified[voting_power[0]]:
                inc-=voting_power[1]
            else:
                inc+=voting_power[1]
        if inc<=0:
            misclassified_points.append(point)
            
    return set(misclassified_points)

def is_good_enough(H, training_points, classifier_to_misclassified, mistake_tolerance=0):
    """Given an overall classifier H, a list of all training points, a
    dictionary mapping classifiers to the training points they misclassify, and
    a mistake tolerance (the maximum number of allowed misclassifications),
    returns False if H misclassifies more points than the tolerance allows,
    otherwise True.  H is represented as a list of (classifier, voting_power)
    tuples."""
    misclassified_points=get_overall_misclassifications(H,training_points,classifier_to_misclassified)
    if len(misclassified_points)>mistake_tolerance:
        return False
    else:
        return True

def update_weights(point_to_weight, misclassified_points, error_rate):
    """Given a dictionary mapping training points to their old weights, a list
    of training points misclassified by the current weak classifier, and the
    error rate of the current weak classifier, returns a dictionary mapping
    training points to their new weights.  This function is allowed (but not
    required) to modify the input dictionary point_to_weight."""
    for point in point_to_weight:
        if point in misclassified_points:
            point_to_weight[point]=make_fraction(1,2)*make_fraction(1,error_rate)*point_to_weight[point]
        else:
            point_to_weight[point]=make_fraction(1,2)*make_fraction(1,(1.0-error_rate))*point_to_weight[point]

    return point_to_weight        

def adaboost(training_points, classifier_to_misclassified,
             use_smallest_error=True, mistake_tolerance=0, max_rounds=INF):
    """Performs the Adaboost algorithm for up to max_rounds rounds.
    Returns the resulting overall classifier H, represented as a list of
    (classifier, voting_power) tuples."""
    results={}
    H=[]
    count=0
    for point in training_points:
        results[point]=1.0/len(training_points)
    while count<max_rounds:
        try:
            classifier_error_rates=calculate_error_rates(results,classifier_to_misclassified)
            best_classifier=pick_best_classifier(classifier_error_rates,use_smallest_error)
            classifiers_vpowers=calculate_voting_power(classifier_error_rates[best_classifier])
            count+=1
            if is_good_enough(H,training_points,classifier_to_misclassified,mistake_tolerance) or make_fraction(classifier_error_rates[best_classifier]) == make_fraction(1,2):
                break
            H.append((best_classifier,classifiers_vpowers))
            results=update_weights(results,classifier_to_misclassified[best_classifier],classifier_error_rates[best_classifier])
        except NoGoodClassifiersError:
            break

    return H     


#### SURVEY ####################################################################

NAME ='Nandhini Rengaraj'
COLLABORATORS ='None'
HOW_MANY_HOURS_THIS_LAB_TOOK =4
WHAT_I_FOUND_INTERESTING ='Adaboost'
WHAT_I_FOUND_BORING ='The long names of lists and dicts'
SUGGESTIONS ='None'
