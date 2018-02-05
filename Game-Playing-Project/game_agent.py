"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import isolation


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    
    This should be the best heuristic function for your project submission.
    
    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    
    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    
    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    #improved improved
    #this adds a score onto improved for being closer to the center than your 
    #opponent.  So if two scores are equal, then one that puts the user closer to
    #the center would be preferred.  
    #being closer to the center should not add the equivalent of more than 1 or 
    #2 moves because at the end of the game, 1 or 2 moves may be all there is left.  
    #I think I will have the overall weight +,- .66 for a total difference of 1 move.  

    
    if game.is_winner(player):
        return float("inf")
    
    elif game.is_loser(player):
        return float("-inf")
        
    y = game.height/2.
    x = game.width/2.
    
    yp,xp = game.get_player_location(player)
    
    yo, xo = game.get_player_location(game.get_opponent(player))
        
    #my distance from center divided by approx max distance * 1.5
    centerscore =(((((x - xp)**2) + ((y-yp)**2))**.5) / (15)) -.5
    
    #opponent distance from center
    opcenterscore =(((((x - xo)**2) + ((y-yo)**2))**.5) / (15)) -.5
    
    my_moves = len(game.get_legal_moves(player))
    op_moves = len(game.get_legal_moves(game.get_opponent(player)))
    
    #final score calculation
    return float((my_moves - op_moves) + centerscore - opcenterscore)
    
    
    
def custom_score_2(game, player):
    """
    Calculate the heuristic value of a game state from the point of view
    of the given player.
    
    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    
    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    
    #this heuristic prioritizes positions where if the players are closer,
    #then our player should be closer to the center
    #1/distance between players * (our distance from the center) - (opponent distance from cen
    if game.is_winner(player):
        return float("inf")
    
    elif game.is_loser(player):
        return float("-inf")
    
    
    my_pos = game.get_player_location(player)
    op_pos = game.get_player_location(game.get_opponent(player))
    
    y = game.width / 2.
    x = game.height / 2.
    
    #distance between players
    dplayers = (((my_pos[0] - op_pos[0])**2 + (my_pos[1] - op_pos[1])**2)**.5)
    
    #my distance to center
    mydcenter = (((my_pos[0] - x)**2 + (my_pos[1] - y)**2)**.5)
    
    #opponents distance to center
    oppdcenter = (((op_pos[0] - x)**2 + (op_pos[1] - y)**2)**.5)
    
    #final calculation 
    return ((1/dplayers) * (mydcenter - oppdcenter))
    #return custom_score(game, player)
    # TODO: finish this function!
    #raise NotImplementedError
    
    


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
       
     
    #This heuristic places emphasis on staying on the 9 center squares.  
    #in which case abs of any dim would be within 1.5 of the center.  

    
    if game.is_winner(player):
        return float("inf")
    
    elif game.is_loser(player):
        return float("-inf")
        
    y = game.height/2.
    x = game.width/2.
    
    yp,xp = game.get_player_location(player)
        
    #if the position is in the 9 center squares, return 10    
    if ((x - xp)**2 <= 2.25) and ((y-yp)**2 <= 2.25):
        return 10.
    else:
        return float(len(game.get_legal_moves(player)))
         
            
            
    
    
    


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move
        
   
    #return move with maximum score
    #okay, so first of all we need a way of associating scores with all of these moves
    #basically we keep calling max or min value, until the desired depth is reached. 
    def minimax(self, game, depth):
        
        #for all moves in get all legal moves, 
        #and then send to min value.  
        #min value returns a tuple score, move
        #I think we can actually directly take the max here, the max returns the tuple with largest
        #score, and then we take the second argument (the move) and only return that
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
            
        if len(game.get_legal_moves()) == 0:
            return (-1,-1)
           
        return max([self.min_value((game.forecast_move(move)), 0, depth), move] for move in game.get_legal_moves())[1]
        
    def max_value(self, game, currentdepth, depth):
        #GET RID OF THIS WHEN INCORPORATING INTO CHESS PROGRAM
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        currentdepth += 1

        #if we have reached the critical depth, then we should return 
        #the custom_score
        if currentdepth == depth or len(game.get_legal_moves()) == 0:
            return self.score(game, game.active_player)
        
        #for all in possible moves
        #take the  max of the returned scores
        #if we are not at a root node, then we need to continue the recursion
        return max(self.min_value(game.forecast_move(move1), currentdepth, depth) for move1 in game.get_legal_moves())
        
	

    def min_value(self, game,currentdepth, depth):
        #GET RID OF THIS WHEN INCORPORATING INTO CHESS PROGRAM
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        currentdepth += 1
        
        #if we have reached the critical depth, then we should return 
        #the custom_score
        if depth == currentdepth or len(game.get_legal_moves()) == 0:
            return self.score(game, game._inactive_player)

        #for all in possible moves
        #take the  max of the returned scores
        #if we are not at a root node, then we need to continue the recursion
        return min(self.max_value(game.forecast_move(move), currentdepth, depth) for move in game.get_legal_moves())
        


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left
        best_move = (-1, -1)
        
        #while the time has not expired
        try:
            depth = 1
            while 1:
                best_move = self.alphabeta(game, depth)
                depth += 1
                if depth > 25:
                    break

        except SearchTimeout:
            return best_move
            
        return best_move
        
        
        

    #Lessons learned here: after implementing minimaxplayer2 which got lost 
    #somewhere in version control, I realized that the reason this 
    #one returns different values is because it essentially implements a 
    #local maximum function, that is it takes the first score, move tuple
    #with the highest score.  The maximum function in minimax always returns the
    #same move because after score it starts comparing the move tuple within the score
    #move tuple.  Since all moves are unique, there will be one with a greatest score.
    #the get all possible moves function returns the moves in a different order every time.  
    #in my unit test.  If I just compared the entire tuples instead of the 
    #scores I could change this to the same max in minimax and the results would be the same
    #but this doesn't really matter.  
    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        #return move with maximum score
        #okay, so first of all we need a way of associating scores with all of these moves
        #basically we keep calling max or min value, until the desired depth is reached. 
        
        #so this is a bit different than the previous version, max and min do the pruning, so it doesnt make sense to
        #add a layer of pruning into minimax function, so this time, the top layer max evaluation is done in max_value itself
        #we can just return a tuple of a move and its score so that we dont need to actually search through to find the move later.  
        #also I think we can just increment current depth when we call min val from max val and max val from min val, or I could just start it at -1
        #ill try -1 for now
        return self.max_value(game, alpha, beta, -1, depth)[1]#max([self.min_value((game.forecast_move(move)), 0, depth), move] for move in game.get_legal_moves())[1]
		
    def max_value(self, game, alpha, beta, currentdepth, depth):
        #GET RID OF THIS WHEN INCORPORATING INTO CHESS PROGRAM
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        currentdepth += 1

        #if we have reached the critical depth, then we should return 
        #the custom_score
        if currentdepth == depth or len(game.get_legal_moves()) == 0:
            #The inactive player is always the one that has just moved, thus
            #that is the position we want.  We implemented the move when
            #we called this function in min_value.
            return self.score(game, game.active_player), game.get_player_location(game.inactive_player)
        
        #for all n, move in legal moves
        #get scorein, the score of the score, move tuple 
        for n,move in enumerate(game.get_legal_moves()):
            scorein = self.min_value(game.forecast_move(move), alpha, beta, currentdepth, depth)[0]
           
            #movescore is the maximum score, move tuple
            #we set this if n is 0 or if scorein is greater than the current movescore
            if n == 0 or scorein > movescore[0]:
                movescore = scorein, move
            
            #pruning statement
            #if this branch cannot be used, then we return
            #hence pruning the branch
            if movescore[0] >= beta:
                return movescore
            
            #set alpha, this will be sent to following branches to ensure
            #that they can possibly be greater than the current max
            #if not, we prune them
            alpha = max(alpha, movescore[0])
        return movescore
     
	

    def min_value(self, game, alpha, beta, currentdepth, depth):
        #GET RID OF THIS WHEN INCORPORATING INTO CHESS PROGRAM
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        currentdepth += 1
        
        #if we have reached the critical depth, then we should return 
        #the custom_score
        if depth == currentdepth or len(game.get_legal_moves()) == 0:
            #The inactive player is always the one that has just moved, thus
            #that is the position we want.  We implemented the move when
            #we called this function in min_value.
            return self.score(game, game._inactive_player), game.get_player_location(game.inactive_player)
        
        #for all n, move in legal moves
        #get scorein, the score of the score, move tuple 
        for n,move in enumerate(game.get_legal_moves()):
            scorein = self.max_value(game.forecast_move(move), alpha, beta, currentdepth, depth)[0]
            
            #movescore is the minimum score, move tuple
            #we set this if n is 0 or if scorein is less than than the current movescore
            if n == 0 or scorein < movescore[0]:
                movescore = scorein, move
            
            #pruning statement
            #if this branch cannot be used, then we return
            #hence pruning the branch
            if movescore[0] <= alpha:
                return movescore
            
            #set beta, this will be sent to following branches to ensure
            #that they can possibly be greater than the current max
            #if not, we prune them
            beta = min(beta, movescore[0])
        
        return movescore


