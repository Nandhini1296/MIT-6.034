# MIT 6.034 Lab 5: k-Nearest Neighbors and Identification Trees
# Written by Jessica Noss (jmn), Dylan Holmes (dxh), and Jake Barnwell (jb16)

from api import *
from data import *
import math
log2 = lambda x: math.log(x, 2)
INF = float('inf')

################################################################################
############################# IDENTIFICATION TREES #############################
################################################################################

def id_tree_classify_point(point, id_tree):
    """Uses the input ID tree (an IdentificationTreeNode) to classify the point.
    Returns the point's classification."""
    classifier= id_tree.get_node_classification()
    
    if id_tree.is_leaf():
        return classifier
    else:
        val=id_tree.apply_classifier(point)
        return id_tree_classify_point(point,val)

def split_on_classifier(data, classifier):
    """Given a set of data (as a list of points) and a Classifier object, uses
    the classifier to partition the data.  Returns a dict mapping each feature
    values to a list of points that have that value."""
    result={}
    points_list=[]
    a=[]
    for point in data:
        a.append(classifier.classify(point))
    for i in set(a):
            for point in data:
                if i==classifier.classify(point):
                    points_list.append(point)                            
            result.update({i:points_list})
            points_list=[]
    
    return result


#### CALCULATING DISORDER

def branch_disorder(data, target_classifier):
    """Given a list of points representing a single branch and a Classifier
    for determining the true classification of each point, computes and returns
    the disorder of the branch."""
    a=[]
    import math
    total=0
    for point in data:
        a.append(target_classifier.classify(point))
    if len(set(a))==1:
        return 0
    else:
        for i in set(a):
            nbc=float(a.count(i))
            nb=float(len(a))
            ratio=nbc/nb
            total+=-ratio*math.log(ratio,2)
        return total
    

def average_test_disorder(data, test_classifier, target_classifier):
    """Given a list of points, a feature-test Classifier, and a Classifier
    for determining the true classification of each point, computes and returns
    the disorder of the feature-test stump."""
    test=[]
    avg_disorder=0
    branch=[]
    target=[]
    new_data=[]
    for point in data:
        test.append(test_classifier.classify(point))
        target.append(target_classifier.classify(point))

    nt=float(len(data))

    for i in set(test):
        for j in range(len(test)):
            if test[j]==i:
                branch.append(target[j])
                new_data.append(data[j])
        nb=float(len(branch))
        branch=[]
        ratio=nb/nt
        avg_disorder+=ratio*branch_disorder(new_data,target_classifier)
        new_data=[]      

    return avg_disorder

    

 
        

## To use your functions to solve part A2 of the "Identification of Trees"
## problem from 2014 Q2, uncomment the lines below and run lab5.py:
#for classifier in tree_classifiers:
#    print classifier.name, average_test_disorder(tree_data, classifier, feature_test("tree_type"))


#### CONSTRUCTING AN ID TREE

def find_best_classifier(data, possible_classifiers, target_classifier):
    """Given a list of points, a list of possible Classifiers to use as tests,
    and a Classifier for determining the true classification of each point,
    finds and returns the classifier with the lowest disorder.  Breaks ties by
    preferring classifiers that appear earlier in the list.  If the best
    classifier has only one branch, raises NoGoodClassifiersError."""
    disorder_list=[]
    a=[]
    result=[]
    try:
        possible_classifiers=sorted(possible_classifiers)
        for classifier in possible_classifiers:
            disorder=average_test_disorder(data,classifier,target_classifier)
            disorder_list.append(disorder)        
        temp=zip(disorder_list,possible_classifiers)
        temp=sorted(temp, key=lambda x:x[0])
        result=[i for (j,i) in temp]
        if len(split_on_classifier(data,result[0]))==1:
            raise NoGoodClassifiersError("NoGoodClassifiersError")
        else:                          
            return result[0]
    except NoGoodClassifiersError:
         raise NoGoodClassifiersError("NoGoodClassifiersError")
    
    
   


## To find the best classifier from 2014 Q2, Part A, uncomment:
#print find_best_classifier(tree_data, tree_classifiers, feature_test("tree_type"))


def construct_greedy_id_tree(data, possible_classifiers, target_classifier, id_tree_node=None):
    """Given a list of points, a list of possible Classifiers to use as tests,
    a Classifier for determining the true classification of each point, and
    optionally a partially completed ID tree, returns a completed ID tree by
    adding classifiers and classifications until either perfect classification
    has been achieved, or there are no good classifiers left."""
    
    
    if id_tree_node==None:
        id_tree_node=IdentificationTreeNode(target_classifier)
        
    if len(split_on_classifier(data,target_classifier))==1:
            id_tree_node=id_tree_node.set_node_classification(target_classifier.classify(data[0]))
            return id_tree_node  
    try:
            classifier=find_best_classifier(data,possible_classifiers,target_classifier)
            features=split_on_classifier(data,classifier).keys()
            id_tree_node=id_tree_node.set_classifier_and_expand(classifier,features)
            branches=id_tree_node.get_branches()
            branch_nodes=branches.values()
            tree_data=split_on_classifier(data,classifier)

            for (feature,child) in branches.items():
                construct_greedy_id_tree(tree_data[feature],possible_classifiers,target_classifier,child)
                
    except NoGoodClassifiersError:
         return id_tree_node

    return id_tree_node

    
    
## To construct an ID tree for 2014 Q2, Part A:
#print construct_greedy_id_tree(tree_data, tree_classifiers, feature_test("tree_type"))

## To use your ID tree to identify a mystery tree (2014 Q2, Part A4):
#tree_tree = construct_greedy_id_tree(tree_data, tree_classifiers, feature_test("tree_type"))
#print id_tree_classify_point(tree_test_point, tree_tree)

## To construct an ID tree for 2012 Q2 (Angels) or 2013 Q3 (numeric ID trees):
#print construct_greedy_id_tree(angel_data, angel_classifiers, feature_test("Classification"))
#print construct_greedy_id_tree(numeric_data, numeric_classifiers, feature_test("class"))


#### MULTIPLE CHOICE

ANSWER_1 ='bark_texture'
ANSWER_2 ='leaf_shape'
ANSWER_3 ='orange_foliage'

ANSWER_4 =[2,3]
ANSWER_5 =[3]
ANSWER_6 =[2]
ANSWER_7 =2

ANSWER_8 ='No'
ANSWER_9 ='No'


################################################################################
############################# k-NEAREST NEIGHBORS ##############################
################################################################################

#### MULTIPLE CHOICE: DRAWING BOUNDARIES

BOUNDARY_ANS_1 =3
BOUNDARY_ANS_2 =4

BOUNDARY_ANS_3 =1
BOUNDARY_ANS_4 =2

BOUNDARY_ANS_5 =2
BOUNDARY_ANS_6 =4
BOUNDARY_ANS_7 =1
BOUNDARY_ANS_8 =4
BOUNDARY_ANS_9 =4

BOUNDARY_ANS_10 =4
BOUNDARY_ANS_11 =2
BOUNDARY_ANS_12 =1
BOUNDARY_ANS_13 =4
BOUNDARY_ANS_14 =4


#### WARM-UP: DISTANCE METRICS

def dot_product(u, v):
    """Computes dot product of two vectors u and v, each represented as a tuple
    or list of coordinates.  Assume the two vectors are the same length."""
    return sum([i*j for (i,j) in zip(u,v)])

def norm(v):
    "Computes length of a vector v, represented as a tuple or list of coords."
    d=dot_product(v,v)
    length=d**0.5
    return length

def euclidean_distance(point1, point2):
    "Given two Points, computes and returns the Euclidean distance between them."
    e_dist=0
    l1=point1.coords
    l2=point2.coords

    for i,j in zip(l1,l2):
        e_dist+=(i-j)**2
        
    return e_dist**0.5

def manhattan_distance(point1, point2):
    "Given two Points, computes and returns the Manhattan distance between them."
    m_dist=0
    l1=point1.coords
    l2=point2.coords

    for i,j in zip(l1,l2):
        m_dist+=abs(i-j)

    return m_dist

def hamming_distance(point1, point2):
    "Given two Points, computes and returns the Hamming distance between them."
    h_dist=0
    l1=point1.coords
    l2=point2.coords

    for i in range(len(l1)):
        if l1[i]!=l2[i]:
            h_dist+=1

    return h_dist

def cosine_distance(point1, point2):
    """Given two Points, computes and returns the cosine distance between them,
    where cosine distance is defined as 1-cos(angle_between(point1, point2))."""
    c_dist=0
    l1=point1.coords
    l2=point2.coords
    d=dot_product(l1,l2)
    nu=norm(l1)
    nv=norm(l2)
    c_dist=1-d/(nu*nv)
    return c_dist
                   


#### CLASSIFYING POINTS

def get_k_closest_points(point, data, k, distance_metric):
    """Given a test point, a list of points (the data), an int 0 < k <= len(data),
    and a distance metric (a function), returns a list containing the k points
    from the data that are closest to the test point, according to the distance
    metric.  Breaks ties lexicographically by coordinates."""
    import copy
    old_data=copy.copy(data)
    a=[]
    result=[]
    
    data=sorted(data, key=lambda x:x.coords)
    for point1 in data:
        metric=distance_metric(point,point1)
        a.append(metric)

    temp=zip(a,data)
    temp=sorted(temp, key=lambda x:x[1].coords)
    temp = sorted(temp, key=lambda x:x[0])
    result=[i for (j,i) in temp]

    
    return result[:k]

def knn_classify_point(point, data, k, distance_metric):
    """Given a test point, a list of points (the data), an int 0 < k <= len(data),
    and a distance metric (a function), returns the classification of the test
    point based on its k nearest neighbors, as determined by the distance metric.
    Assumes there are no ties."""
    neighbours=get_k_closest_points(point,data,k,distance_metric)
    val=0
    best_val=None
    class_val=[]
    for i in neighbours:
        class_val.append(i.classification)
        for j in class_val:
            count=class_val.count(j)
            if count>val:
                val=count
                best_val=j
    return best_val
            

## To run your classify function on the k-nearest neighbors problem from 2014 Q2
## part B2, uncomment the line below and try different values of k:
#print knn_classify_point(knn_tree_test_point, knn_tree_data, 5, euclidean_distance)


#### CHOOSING k

def cross_validate(data, k, distance_metric):
    """Given a list of points (the data), an int 0 < k <= len(data), and a
    distance metric (a function), performs leave-one-out cross-validation.
    Return the fraction of points classified correctly, as a float."""
    count=0
    correct=0.0
    wrong=0.0
    
    for count in range(len(data)):
        test_set=data[count]
        train_data=data[:count]+data[(count+1):]
        if knn_classify_point(test_set,train_data,k,distance_metric)==test_set.classification:
            correct=correct+1
        else:
            wrong+=1          
           
    return correct/(wrong+correct)
        
    

def find_best_k_and_metric(data):
    """Given a list of points (the data), uses leave-one-out cross-validation to
    determine the best value of k and distance_metric, choosing from among the
    four distance metrics defined above.  Returns a tuple (k, distance_metric),
    where k is an int and distance_metric is a function."""
    result=[]
    distance_metric=[cosine_distance, hamming_distance,euclidean_distance, manhattan_distance]
   
    for i in range(1,len(data)+1):
        for j in range(len(distance_metric)):
            val=[cross_validate(data,i,distance_metric[j])]
            val.append(i)
            val.append(distance_metric[j])
            result.append(val)
    
    result=sorted(result, key=lambda result:result[0])
    return (result[-1][1],result[-1][-1])
    

## To find the best k and distance metric for 2014 Q2, part B, uncomment:
#print find_best_k_and_metric(knn_tree_data)


#### MORE MULTIPLE CHOICE

kNN_ANSWER_1 ='Overfitting'
kNN_ANSWER_2 ='Underfitting'
kNN_ANSWER_3 =4

kNN_ANSWER_4 =4
kNN_ANSWER_5 =1
kNN_ANSWER_6 =3
kNN_ANSWER_7 =3

#### SURVEY ###################################################

NAME ='Nandhini Rengaraj'
COLLABORATORS ='None'
HOW_MANY_HOURS_THIS_LAB_TOOK ='14'
WHAT_I_FOUND_INTERESTING ='ID Trees'
WHAT_I_FOUND_BORING ='Multiple Choice Questions'
SUGGESTIONS ='None'
