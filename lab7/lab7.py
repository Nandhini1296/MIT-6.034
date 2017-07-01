# MIT 6.034 Lab 7: Support Vector Machines
# Written by Jessica Noss (jmn) and 6.034 staff

from svm_data import *

# Vector math
def dot_product(u, v):
    """Computes dot product of two vectors u and v, each represented as a tuple
    or list of coordinates.  Assume the two vectors are the same length."""
    return sum([i*j for (i,j) in zip(u,v)])

def norm(v):
    "Computes length of a vector v, represented as a tuple or list of coords."
    d=dot_product(v,v)
    length=d**0.5
    return length

# Equation 1
def positiveness(svm, point):
    "Computes the expression (w dot x + b) for the given point"
    w=svm.w
    b=svm.b
    return dot_product(w,point.coords)+b
    

def classify(svm, point):
    """Uses given SVM to classify a Point.  Assumes that point's true
    classification is unknown.  Returns +1 or -1, or 0 if point is on boundary"""
    d=positiveness(svm,point)
    if d>0:
        return 1
    elif d<0:
        return -1
    else:
        return 0

# Equation 2
def margin_width(svm):
    "Calculate margin width based on current boundary."
    return 2/norm(svm.w)

# Equation 3
def check_gutter_constraint(svm):
    """Returns the set of training points that violate one or both conditions:
        * gutter constraint (positiveness == classification for support vectors)
        * training points must not be between the gutters
    Assumes that the SVM has support vectors assigned."""
    result_points=[]
    w=margin_width(svm)

    for vector in svm.support_vectors:
        #print vector,positiveness(svm,vector),classify(svm,vector)
        if positiveness(svm,vector)!=vector.classification:
            result_points.append(vector)
        for point in svm.training_points:
            #print point,positiveness(svm,point),abs(positiveness(svm,vector))
            if abs(positiveness(svm,point))<1:
                result_points.append(point)

    return set(result_points)
        

# Equations 4, 5
def check_alpha_signs(svm):
    """Returns the set of training points that violate either condition:
        * all non-support-vector training points have alpha = 0
        * all support vectors have alpha > 0
    Assumes that the SVM has support vectors assigned, and that all training
    points have alpha values assigned."""
    result_points=[]
    for point in svm.training_points:
        if point in svm.support_vectors and not point.alpha>0:
            result_points.append(point)
        elif point not in svm.support_vectors and not point.alpha==0:
            result_points.append(point)
    return set(result_points)

def check_alpha_equations(svm):
    """Returns True if both Lagrange-multiplier equations are satisfied,
    otherwise False.  Assumes that the SVM has support vectors assigned, and
    that all training points have alpha values assigned."""
    flag1=False
    flag2=False
    prod1=0
    prod2=0
    l=[]
    for point in svm.training_points:
        prod1+=classify(svm,point)*point.alpha

    if prod1==0:
        flag1=True
    
    w=svm.w
    for point in svm.training_points:
            prod2=classify(svm,point)*point.alpha
            l.append([prod2*i for i in point.coords])
            
       
    temp=[sum(i) for i in zip(*l)]
    if temp==w:
        flag2=True
    
    if flag1==True and flag2==True:
        return True
    else:
        return False
    
# Classification accuracy
def misclassified_training_points(svm):
    """Returns the set of training points that are classified incorrectly
    using the current decision boundary."""
    result=[]
    for point in svm.training_points:
        if point.classification !=classify(svm,point):
            result.append(point)
    return set(result)

# Training
def update_svm_from_alphas(svm):
    """Given an SVM with training data and alpha values, use alpha values to
    update the SVM's support vectors, w, and b.  Return the updated SVM."""
    support_vectors=[]
    prod=0
    l=[]
    pos_b_values=[]
    neg_b_values=[]
    for point in svm.training_points:
        if point.alpha>0:
            support_vectors.append(point)
            
    svm.support_vectors=support_vectors

    for point in svm.training_points:
        prod=point.classification*point.alpha
        l.append([prod*i for i in point.coords])
                 
    temp=[sum(i) for i in zip(*l)]
    svm.w=temp

    for point in svm.support_vectors:
        if point.classification==1:
            pos_b_values.append(point.classification-(dot_product(svm.w,point)))
        elif point.classification==-1:
            neg_b_values.append(point.classification-(dot_product(svm.w,point)))

    svm.b=(min(neg_b_values)+max(pos_b_values))/2

    return svm

    
# Multiple choice
ANSWER_1 =11
ANSWER_2 =6
ANSWER_3 =3
ANSWER_4 =2

ANSWER_5 =['A','D']
ANSWER_6 =['A','B','D']
ANSWER_7 =['A','B','D']
ANSWER_8 =[]
ANSWER_9 =['A','B','D']
ANSWER_10 =['A','B','D']

ANSWER_11 =False
ANSWER_12 =True
ANSWER_13 =False
ANSWER_14 =False
ANSWER_15 =False
ANSWER_16 =True

ANSWER_17 =[1,3,6,8]
ANSWER_18 =[1,2,4,5,6,7,8]
ANSWER_19 =[1,2,4,5,6,7,8]

ANSWER_20 =6


#### SURVEY ####################################################################

NAME ='Nandhini Rengaraj'
COLLABORATORS ='None'
HOW_MANY_HOURS_THIS_LAB_TOOK =4
WHAT_I_FOUND_INTERESTING ='Training the SVM'
WHAT_I_FOUND_BORING ='None'
SUGGESTIONS ='None'
