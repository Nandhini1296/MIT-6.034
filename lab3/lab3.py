# MIT 6.034 Lab 3: Games
# Written by Dylan Holmes (dxh), Jessica Noss (jmn), and 6.034 staff

from game_api import *
from boards import *
INF = float('inf')

def is_game_over_connectfour(board) :
    "Returns True if game is over, otherwise False."
    chain_list=board.get_all_chains()
    game_over=True
    for i in range(0,board.num_cols):
        if not board.is_column_full(i):
            game_over=False
    
    for j in range(0,len(chain_list)):
                if len(chain_list[j])>=4:
                    game_over=True
   
    return game_over
                

def next_boards_connectfour(board) :
    """Returns a list of ConnectFourBoard objects that could result from the
    next move, or an empty list if no moves can be made."""
    moves=[]
    if is_game_over_connectfour(board):
        return []
    else:
        for i in range(0,board.num_cols):
            if not board.is_column_full(i):
                moves=moves+[board.add_piece(i)]
    return moves

def endgame_score_connectfour(board, is_current_player_maximizer) :
    """Given an endgame board, returns 1000 if the maximizer has won,
    -1000 if the minimizer has won, or 0 in case of a tie."""
    if board.count_pieces(None)==42 and is_game_over_connectfour(board):
            final_score=0
    elif is_current_player_maximizer and is_game_over_connectfour(board):
            final_score=-1000
    else:
        if is_game_over_connectfour(board):
            final_score=1000
    
    return final_score

def endgame_score_connectfour_faster(board, is_current_player_maximizer) :
    """Given an endgame board, returns an endgame score with abs(score) >= 1000,
    returning larger absolute scores for winning sooner."""
    total_number=42
    if is_current_player_maximizer:
        score=-1000-(total_number-board.count_pieces())
    else:
        score=1000+(total_number-board.count_pieces())
    return score

    
def heuristic_connectfour(board, is_current_player_maximizer) :
    """Given a non-endgame board, returns a heuristic score with
    abs(score) < 1000, where higher numbers indicate that the board is better
    for the maximizer."""
    heuristic_value=heuristic_cal(board,is_current_player_maximizer)-heuristic_cal(board,not is_current_player_maximizer)
    return heuristic_value

def heuristic_cal(board,is_current_player_maximizer):
        score=0
        for chain in board.get_all_chains(is_current_player_maximizer):
            if len(chain)==1:
                score+=1
            elif len(chain)==2:
                score+=10
            elif len(chain)==3:
                score+=100
        return score

# Now we can create AbstractGameState objects for Connect Four, using some of
# the functions you implemented above.  You can use the following examples to
# test your dfs and minimax implementations in Part 2.

# This AbstractGameState represents a new ConnectFourBoard, before the game has started:
state_starting_connectfour = AbstractGameState(snapshot = ConnectFourBoard(),
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)

# This AbstractGameState represents the ConnectFourBoard "NEARLY_OVER" from boards.py:
state_NEARLY_OVER = AbstractGameState(snapshot = NEARLY_OVER,
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)

# This AbstractGameState represents the ConnectFourBoard "BOARD_UHOH" from boards.py:
state_UHOH = AbstractGameState(snapshot = BOARD_UHOH,
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)


#### PART 2 ###########################################
# Note: Functions in Part 2 use the AbstractGameState API, not ConnectFourBoard.

def dfs_maximizing(state) :
    """Performs depth-first search to find path with highest endgame score.
    Returns a tuple containing:
     0. the best path (a list of AbstractGameState objects),
     1. the score of the leaf node (a number), and
     2. the number of static evaluations performed (a number)"""
    
    paths=[]
    
    def dfs_expand(state,path):
        new_path=path[:]
        new_path.append(state)
        if state.is_game_over():
            paths.append(new_path)
            return True
        else:
            for move in state.generate_next_states():
                dfs_expand(move,new_path)
        return paths

    dfs_expand(state,[])

    num_eval=0
    path_scores=[]
    for i in paths:
        score=i[-1].get_endgame_score(is_current_player_maximizer=True)
        path_scores.append(score)
        num_eval+=1

    x=path_scores.index(max(path_scores))
    final_path=paths[x]
    final_score=max(path_scores)

    return [final_path, final_score,num_eval]


        

def minimax_endgame_search(state, maximize=True) :
    """Performs minimax search, searching all leaf nodes and statically
    evaluating all endgame scores.  Same return type as dfs_maximizing."""
    paths=[]
    scores=[]
    evals=[]

    if state.is_game_over():
        return([state],state.get_endgame_score(maximize),1)
    for move in state.generate_next_states():
        expand=minimax_endgame_search(move,not maximize)
        paths.append([state]+expand[0])
        scores.append(0+expand[1])
        evals.append(0+expand[2])
    if maximize:
        return [paths[scores.index(max(scores))],max(scores),sum(evals)]
    else:
        return[paths[scores.index(min(scores))],min(scores),sum(evals)]

    
# Uncomment the line below to try your minimax_endgame_search on an


# AbstractGameState representing the ConnectFourBoard "NEARLY_OVER" from boards.py:

#pretty_print_dfs_type(minimax_endgame_search(state_NEARLY_OVER))


def minimax_search(state, heuristic_fn=always_zero, depth_limit=INF, maximize=True) :
    "Performs standard minimax search.  Same return type as dfs_maximizing."
    paths=[]
    scores=[]
    evals=[]
    
    if state.is_game_over():
        return([state],state.get_endgame_score(maximize),1)
    elif depth_limit==0:
        return([state],heuristic_fn(state.get_snapshot(),maximize),1)
    else:
        for move in state.generate_next_states():
            expand=minimax_search(move,heuristic_fn,depth_limit-1,not maximize)
            paths.append([state]+expand[0])
            scores.append(0+expand[1])
            evals.append(0+expand[2])
        if maximize:
            return [paths[scores.index(max(scores))],max(scores),sum(evals)]
        else:
            return [paths[scores.index(min(scores))],min(scores),sum(evals)]  



            

# Uncomment the line below to try minimax_search with "BOARD_UHOH" and
# depth_limit=1.  Try increasing the value of depth_limit to see what happens:

#pretty_print_dfs_type(minimax_search(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=1))


def minimax_search_alphabeta(state, alpha=-INF, beta=INF, heuristic_fn=always_zero,
                             depth_limit=INF, maximize=True) :
    "Performs minimax with alpha-beta pruning.  Same return type as dfs_maximizing."
    paths=[]
    alpha_scores=[]
    beta_scores=[]
    evals=[]
    
    
    if state.is_game_over():        
        return ([state],state.get_endgame_score(maximize),1)
    elif depth_limit==0:
        return([state],heuristic_fn(state.get_snapshot(),maximize),1)
    else:
        for move in state.generate_next_states():
            expand=minimax_search_alphabeta(move,alpha,beta,heuristic_fn,depth_limit-1,not maximize)
            evals.append(expand[2])
            if maximize:
                if expand[1]>alpha:
                    alpha=expand[1]
                    alpha_scores.append(expand[1])
                    paths=([state]+expand[0])
            else:
                if expand[1]<beta:
                    beta=expand[1]
                    beta_scores.append(expand[1])
                    paths=([state]+expand[0])
               

                   
            if alpha>=beta:
                break
            
    if maximize:
            return [paths,alpha,sum(evals)]
    else:
            return [paths,beta,sum(evals)]
    

# Uncomment the line below to try minimax_search_alphabeta with "BOARD_UHOH" and
# depth_limit=4.  Compare with the number of evaluations from minimax_search for
# different values of depth_limit.

#pretty_print_dfs_type(minimax_search_alphabeta(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=4))


def progressive_deepening(state, heuristic_fn=always_zero, depth_limit=INF,
                          maximize=True) :
    """Runs minimax with alpha-beta pruning. At each level, updates anytime_value
    with the tuple returned from minimax_search_alphabeta. Returns anytime_value."""
    anytime_value = AnytimeValue()   # TA Note: Use this to store values.
    #for move in state.generate_next_states():
    for i in range(1, depth_limit+1):
        expand=minimax_search_alphabeta(state,-INF,INF,heuristic_fn,i,maximize)
        anytime_value.set_value(expand)
    return anytime_value

# Uncomment the line below to try progressive_deepening with "BOARD_UHOH" and
# depth_limit=4.  Compare the total number of evaluations with the number of
# evaluations from minimax_search or minimax_search_alphabeta.

#print progressive_deepening(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=4)


##### PART 3: Multiple Choice ##################################################

ANSWER_1 = '4'

ANSWER_2 = '1'

ANSWER_3 = '4'

ANSWER_4 = '5'


#### SURVEY ###################################################

NAME ='Nandhini Rengaraj'
COLLABORATORS ='None'
HOW_MANY_HOURS_THIS_LAB_TOOK ='12'
WHAT_I_FOUND_INTERESTING ='Minimax Search'
WHAT_I_FOUND_BORING ='Implementing the helper functions'
SUGGESTIONS ='None'
