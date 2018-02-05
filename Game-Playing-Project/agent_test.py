"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent

from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    """
    def setUp(self):
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.game = isolation.Board(self.player1, self.player2)
        #print("fuck you!")
    """
    def test_game(self):
        from isolation import Board
        from game_agent import MinimaxPlayer
        #from game_agent import MinimaxPlayer2
        from game_agent import AlphaBetaPlayer
        #from sample_players import RandomPlayer
        from sample_players import GreedyPlayer
        #time_millis = lambda: 1000 * timeit.default_timer()
        
        
        
        # create an isolation board (by default 7x7)
        player1 = GreedyPlayer()
        #player2 = AlphaBetaPlayer()
        #player2 = MinimaxPlayer2()
        
        player2 = MinimaxPlayer()
        game = Board(player1, player2)
        
        # place player 1 on the board at row 2, column 3, then place player 2 on
        # the board at row 0, column 5; display the resulting board state.  Note
        # that the .apply_move() method changes the calling object in-place.
        #game.apply_move((2, 3))
        #print(time_millis)
        #print(game.get_legal_moves())
        
        #newmove1 = player3.get_move(game, lambda: 10)
        
        #print(newmove1)
        game.apply_move((2,3))
        
        #newmove = player2.get_move(game, lambda: 10)
        #print(newmove)
        
        #game.apply_move(newmove)
        #print(game.to_string())
        
        

        #game.apply_move((1,0))
        #print(game.to_string())
                
        newmove = player2.get_move(game, lambda: 10)
        game.apply_move(newmove)
        print(game.to_string())
        #print(newmove)
        
        
        
        #print(game.to_string())
        #game.apply_move((0,2))
        
        #newmove = player2.get_move(game, lambda: 10)
        #game.apply_move(newmove)
        #print(game.to_string())
        #print(newmove)
        
        print(game.to_string())
    
        # players take turns moving on the board, so player1 should be next to move
        assert(player1 == game.active_player)
    
        # get a list of the legal moves available to the active player
        new_game = game.forecast_move((1, 1))
        assert(new_game.to_string() != game.to_string())
        print("\nOld state:\n{}".format(game.to_string()))
        print("\nNew state:\n{}".format(new_game.to_string()))
    
        # play the remainder of the game automatically -- outcome can be "illegal
         #move", "timeout", or "forfeit"
        winner, history, outcome = game.play()
        print("\nWinner: {}\nOutcome: {}".format(winner, outcome))
        print(game.to_string())
        print("Move history:\n{!s}".format(history))
        
        

if __name__ == '__main__':
    unittest.main()
