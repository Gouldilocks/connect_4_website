import copy
import math
import numpy as np
import matplotlib as plt
import random
from scipy.signal import convolve2d

class Gouldilocks:
  def __init__(self) -> None:
    self.player = None
    self.board = None
    self.stall_actions = []
    self.turns_taken = 1

  def center_only_played(self, overrideBoard):
    # If the opponent has not played in any column other than the middle, play in the middle
    HasntPLayedMiddle = True
    for i in range(len(overrideBoard[0])):
        if i != 3:
            for x in range(len(overrideBoard)):
                if overrideBoard[x][i] != 0:
                    HasntPLayedMiddle = False
    if HasntPLayedMiddle and 3 in self.actions(overrideBoard):
        return True, 3

  def first_move(self, board):
    firstMove = True
    for row in board:
      for col in row:
        if col != 0:
          firstMove = False
    return firstMove

  def get_move(self, board, player):
    self.player = player
    firstMove = True
    for row in board:
      for col in row:
        if col == self.player:
          firstMove = False
    # first move should always be center
    if firstMove:
        return 3

    # Check if only the center has been played
    if self.center_only_played(board):
        return 3

    self.board = board
    move = self.calc_move(self.board)
    return move

  def result(self, b, action, player):
    new_board = copy.deepcopy(b)
    for i in range(len(new_board)-1, -1, -1):
        if new_board[i][action] == 0:
            new_board[i][action] = player
            return new_board
    return new_board

  def pruned_actions(self, board):
      action_replay = [i for i in range(len(board[0])) if board[0][i] == 0]

      # Remove any actions that we are boycotting
      for act in self.stall_actions:
        if act in action_replay:
          action_replay.remove(act)

      return action_replay

  def actions(self, board):
        return [i for i in range(len(board[0])) if board[0][i] == 0]

  # Function that checks for terminal states
  # Returns true if the game is over, false otherwise
  def terminal(self, board):
      # Check for horizontal wins
      for i in range(len(board)):
          for j in range(len(board[0]) - 3):
              if board[i][j] != 0 and board[i][j] == board[i][j+1] == board[i][j+2] == board[i][j+3]:
                  return True

      # Check for vertical wins
      for i in range(len(board) - 3):
          for j in range(len(board[0])):
              if board[i][j] != 0 and board[i][j] == board[i+1][j] == board[i+2][j] == board[i+3][j]:
                  return True

      # Check for positive diagonal wins
      for i in range(len(board) - 3):
          for j in range(len(board[0]) - 3):
              if board[i][j] != 0 and board[i][j] == board[i+1][j+1] == board[i+2][j+2] == board[i+3][j+3]:
                  return True

      # Check for negative diagonal wins
      for i in range(3, len(board)):
          for j in range(len(board[0]) - 3):
              if board[i][j] != 0 and board[i][j] == board[i-1][j+1] == board[i-2][j+2] == board[i-3][j+3]:
                  return True

      # Check for draw
      if len(self.actions(board)) == 0:
          return True

      return False

  def utility(self, board, player):
    # Check for horizontal wins
    for i in range(len(board)):
        for j in range(len(board[0]) - 3):
            if board[i][j] != 0 and board[i][j] == board[i][j+1] == board[i][j+2] == board[i][j+3]:
                if board[i][j] == player:
                    return 1
                else:
                    return -1

    # Check for vertical wins
    for i in range(len(board) - 3):
        for j in range(len(board[0])):
            if board[i][j] != 0 and board[i][j] == board[i+1][j] == board[i+2][j] == board[i+3][j]:
                if board[i][j] == player:
                    return 1
                else:
                    return -1

    # Check for positive diagonal wins
    for i in range(len(board) - 3):
        for j in range(len(board[0]) - 3):
            if board[i][j] != 0 and board[i][j] == board[i+1][j+1] == board[i+2][j+2] == board[i+3][j+3]:
                if board[i][j] == player:
                    return 1
                else:
                    return -1

    # Check for negative diagonal wins
    for i in range(3, len(board)):
        for j in range(len(board[0]) - 3):
            if board[i][j] != 0 and board[i][j] == board[i-1][j+1] == board[i-2][j+2] == board[i-3][j+3]:
                if board[i][j] == player:
                    return 1
                else:
                    return -1

    # Check for draw
    if len(self.actions(board)) == 0:
        return 0
    return None  

  # Returns the column in which opponent has a winning move. -1 if there is none
  def check_override_move(self, board):
    for i in self.actions(board):
        if self.terminal(self.result(board, i, -self.player)):
            util = self.utility(self.result(board, i, -self.player), self.player)
            if util == 1:
                return i
            elif util == -1:
                return i
        elif self.terminal(self.result(board, i, self.player)):
            util = self.utility(self.result(board, i, self.player), self.player)
            if util == 1:
                return i
            elif util == -1:
                return i
    return None

  # This function should return an array of actions that are one win away for us,
    # and one loss away for the opponent, so we want to stall them
  def get_new_stall_actions(self, board):
    self.stall_actions = []
    for act in self.actions(board):
        oppResult = self.result(board, act, self.player)
        oppResult = self.result(oppResult, act, -self.player)
        if self.utility(oppResult, self.player) == -1:
            self.stall_actions.append(act)

        myResult = self.result(board, act, -self.player)
        myResult = self.result(myResult, act, self.player)
        if self.utility(myResult, self.player) == 1:
            self.stall_actions.append(act)
    

  # Returns a percent of the center control that a board has for the given player, as a percentage. 1 if the middle column(s) are controlled by player 1, -1 otherwise
  # You can bias it left or right by 1, to get the middle left and middle right
  def center_control(self, board, player=1):
      middle_column = (len(board[0])//2)
      middle_right_column = middle_column + 1
      middle_left_column = middle_column - 1
      # Loop through the middle column and see who owns it
      num_p1 = 0
      num_p2 = 0
      for i in range(len(board)):
          if board[i][middle_column] == player:
              num_p1 += 1.5
          elif board[i][middle_column] == -player:
              num_p2 += 1.5
          if board[i][middle_right_column] == player:
              num_p1 += 1
          elif board[i][middle_right_column] == -player:
              num_p2 += 1
          if board[i][middle_left_column] == player:
              num_p1 += 1
          elif board[i][middle_left_column] == -player:
              num_p2 += 1

      if num_p2 != 0:
          return num_p1 / (num_p1 + num_p2)
      else:
          return 1

  def check_3x3(self, board, trap_set, x, y, player):
      matches = 0
      for i in range(3):
          for j in range(3):
            if trap_set[i][j] == 1:
              if board[y + i][x + j] == player:
                  matches += 1
              elif board[y + i][x + j] == -player:
                  return 0
      return matches

  def check_zig_trap(self, board, player):
    max_matches = 0
    trap_set = [
        [0, 0, 1],
        [0, 1, 1],
        [1, 1, 0]
    ]

    # Don't look at the first row
    # Don't look at the last 3 columns
    for y in range(1, len(board) - 2):
        for x in range(len(board[0]) - 3):
            if board[y][x] == player:
                matches = self.check_3x3(board, trap_set, x, y, player)
                if matches > max_matches:
                    max_matches = matches    
    
    trap_set = [
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 1]
    ]
    # Don't look at the first row
    # Don't look at the first column or the last 2 columns
    for y in range(1, len(board) - 2):
        for x in range(1, len(board[0]) - 2):
            if board[y][x] == player:
                matches = self.check_3x3(board, trap_set, x, y, player)
                if matches > max_matches:
                    max_matches = matches

    return max_matches


  def check_L_trap(self, board, player):
    max_matches = 0
    trap_set = [
        [1, 1, 1],
        [1, 0, 1],
        [1, 0, 1]
    ]
    # Don't look at the first row
    # Don't look at the last 3 columns
    for y in range(1, len(board) - 2):
        for x in range(len(board[0]) - 3):
            if board[y][x] == player:
                matches = self.check_3x3(board, trap_set, x, y, player)
                if matches > max_matches:
                    max_matches = matches

    return max_matches

  # Returns the number of 7 traps that a player has
  def check_7_trap(self, board, player):
      max_matches = 0
      trap_set = [
        [1, 1, 1],
        [0, 1, 0],
        [1, 0, 0]
      ]
      # Don't look at the first row
      # Don't look at the last 3 columns
      for y in range(1, len(board) - 2):
          for x in range(len(board[0]) - 3):
            if board[y][x] == player:
              matches = self.check_3x3(board, trap_set, x, y, player)
              if matches > max_matches:
                max_matches = matches
            
                  

      # Check for a mirror image of the trap
      trap_set = [    
        [1, 1, 1],
        [0, 1, 0],
        [0, 0, 1]
      ]
      for y in range(1, len(board) - 2):
          for x in range(1, len(board[0]) - 2):
            if board[y][x] == player:
              matches = self.check_3x3(board, trap_set, x, y, player)
              if matches > max_matches:
                max_matches = matches

      return max_matches

  def num_possible_wins(self, board, player):
    num_in_wins_for_player = []
    num_in_wins_for_opp = []
    # Check for horizontal wins
    for i in range(len(board)):
        for j in range(len(board[0]) - 3):
            num_in_wins_for_player.append(0)
            num_in_wins_for_opp.append(0)
            for k in range(4):
                if board[i][j+k] == player:
                    num_in_wins_for_player[-1] += 1
                elif board[i][j+k] == -player:
                    num_in_wins_for_opp[-1] += 1

    # Check for vertical wins
    for i in range(len(board) - 3):
        for j in range(len(board[0])):
            num_in_wins_for_player.append(0)
            num_in_wins_for_opp.append(0)
            for k in range(4):
                if board[i+k][j] == player:
                    num_in_wins_for_player[-1] += 1
                elif board[i+k][j] == -player:
                    num_in_wins_for_opp[-1] += 1

    # Check for positive diagonal wins
    for i in range(len(board) - 3):
        for j in range(len(board[0]) - 3):
            num_in_wins_for_player.append(0)
            num_in_wins_for_opp.append(0)
            for k in range(4):
                if board[i+k][j+k] == player:
                    num_in_wins_for_player[-1] += 1
                elif board[i+k][j+k] == -player:
                    num_in_wins_for_opp[-1] += 1

    # Check for negative diagonal wins
    for i in range(3, len(board)):
        for j in range(len(board[0]) - 3):
            num_in_wins_for_player.append(0)
            num_in_wins_for_opp.append(0)
            for k in range(4):
                if board[i-k][j+k] == player:
                    num_in_wins_for_player[-1] += 1
                elif board[i-k][j+k] == -player:
                    num_in_wins_for_opp[-1] += 1

    # Cancel any of them that have been filled
    for i in range(len(num_in_wins_for_player)):
        if num_in_wins_for_player[i] + num_in_wins_for_opp[i] == 4:
            num_in_wins_for_player[i] = 0
            num_in_wins_for_opp[i] = 0

    playerTotal = 0
    oppTotal = 0

    # Check for ruined wins
    for i in range(len(num_in_wins_for_player)):
        if num_in_wins_for_player[i] == 0 and num_in_wins_for_opp[i] == 0:
            pass
        elif num_in_wins_for_player[i] == 0:
            oppTotal += 1
        elif num_in_wins_for_opp[i] == 0:
            playerTotal += 1

    return playerTotal, oppTotal

  def evaluation(self, evalBoard, player):
    # First check for terminal state on any of the possible moves. return super high num if it is a win.
    ut = self.utility(evalBoard, player)
    if ut == -1:
        return -9_999_999
    if ut == 1:
        return 9_999_999

    seven_traps = self.check_7_trap(evalBoard, player)
    if seven_traps:
        return 9_999_999

    seven_traps_opp = self.check_7_trap(evalBoard, -player)
    if seven_traps_opp:
        return -9_999_999

    num_wins_p1, num_wins_p2 = self.num_possible_wins(evalBoard, player)
    return (-num_wins_p2) 

  def minimax_new(self, evaluation_func, myb, depth, alpha, beta, maximizingPlayer=True, player=1):
    if depth == 0 or self.terminal(myb):
        return evaluation_func(myb, player), None

    if maximizingPlayer:
        act = None
        maxEval = -math.inf

        # Check the middle actions first
        theActions = self.pruned_actions(myb)
        if len(theActions) == 0:
            theActions = self.actions(myb)
        if 4 in theActions:
            theActions.remove(4)
            theActions.insert(0, 4)
        if 2 in theActions:
            theActions.remove(2)
            theActions.insert(0, 2)
        if 3 in theActions:
            theActions.remove(3)
            theActions.insert(0, 3)

        for action in theActions:
            eval = self.minimax_new(evaluation_func, self.result(myb, action, player), depth - 1, alpha, beta, False, player)
            if eval[0] > maxEval:
                maxEval = eval[0]
                act = action
            alpha = max(alpha, eval[0])
            if beta <= alpha:
                break
        return maxEval, act
    else:
        act = None
        minEval = math.inf

        # Get the pruned actions first
        theActions = self.pruned_actions(myb)
        if len(theActions) == 0:
            theActions = self.actions(myb)
        if 4 in theActions:
            theActions.remove(4)
            theActions.insert(0, 4)
        if 2 in theActions:
            theActions.remove(2)
            theActions.insert(0, 2)
        if 3 in theActions:
            theActions.remove(3)
            theActions.insert(0, 3)

        for action in theActions:
            eval = self.minimax_new(evaluation_func, self.result(myb, action, -player), depth - 1, alpha, beta, True, player)
            if eval[0] < minEval:
                minEval = eval[0]
                act = action
            beta = min(beta, eval[0])
            if beta <= alpha:
                break
        return minEval, act


  def earlyEval(self, evalBoard, player):
    # First check for terminal state
    ut = self.utility(evalBoard, player)
    if ut == -1:
        return -9_999_999
    if ut == 1:
        return 9_999_999

    seven_traps_opp = self.check_7_trap(evalBoard, -player)
    if seven_traps_opp > 3:
        return -seven_traps_opp * 1_000_000

    seven_traps = self.check_7_trap(evalBoard, player)
    if seven_traps > 3:
        return seven_traps * 1_000_000

    threat_heights_yellow, threat_heights_red = self.check_control(evalBoard)
    if min(threat_heights_yellow) < min(threat_heights_red):
        tot = 0
        for x in threat_heights_yellow:
            if x != 9:
                tot += 6 - x
        return -player * tot

    elif min(threat_heights_red) < min(threat_heights_yellow):
        tot = 0
        for x in threat_heights_red:
            if x != 9:
                tot += 6 - x
        return player * tot
    return 0

  def get_heights(self, board):
    heights = [6, 6, 6, 6, 6, 6, 6]
    for i in range(0, 7):
        for j in range(0, 6):
            if board[j][i] == 0:
                heights[i] -= 1
            else:
                break
    return heights

  def who_has_control(self, board):
    threat_heights_yellow, threat_heights_red = self.check_control(board)
    if min(threat_heights_yellow) < min(threat_heights_red):
        return -1
    elif min(threat_heights_red) < min(threat_heights_yellow):
        return 1
    return 0

  def check_control(self, board):
    odd_rows = [1, 3, 5]
    even_rows = [0, 2, 4]

    # Check for horizontal odd threats for yellow
    threat_heights_yellow = [9, 9, 9, 9, 9, 9, 9]
    threat_heights_red = [9, 9, 9, 9, 9, 9, 9]

    for y in range(0, 6):
        for x in range(0, 4):
            if board[y][x] == 0 and board[y][x+1] == board[y][x+2] == board[y][x+3]:
                if y in even_rows and board[y][x+1] == -1:
                    threat_heights_yellow[x] = 5 - y
                elif y in odd_rows and board[y][x+1] == 1:
                    threat_heights_red[x] = 5 - y

            elif board[y][x+1] == 0 and board[y][x] == board[y][x+2] == board[y][x+3]:
                if y in even_rows and board[y][x] == -1:
                    threat_heights_yellow[x+1] = 5 - y
                elif y in odd_rows and board[y][x] == 1:
                    threat_heights_red[x+1] = 5 - y

            elif board[y][x+2] == 0 and board[y][x] == board[y][x+1] == board[y][x+3]:
                if y in even_rows and board[y][x] == -1:
                    threat_heights_yellow[x+2] = 5 - y
                elif y in odd_rows and board[y][x] == 1:
                    threat_heights_red[x+2] = 5 - y

            elif board[y][x] == board[y][x+1] == board[y][x+2] and board[y][x+3] == 0:
                if y in even_rows and board[y][x] == -1:
                    threat_heights_yellow[x+3] = 5 - y
                elif y in odd_rows and board[y][x] == 1:
                    threat_heights_red[x+3] = 5 - y

    # Check for diagonal down odd threats for yellow
    for y in range(0, 3):
        for x in range(0, 4):
            if board[y][x] == 0 and board[y+1][x+1] == board[y+2][x+2] == board[y+3][x+3]:
                if y in even_rows and threat_heights_yellow[x] > y and board[y+1][x+1] == -1:
                    threat_heights_yellow[x] = 5 - y
                elif y in odd_rows and threat_heights_red[x] > y and board[y+1][x+1] == 1:
                    threat_heights_red[x] = 5 - y

            elif board[y+1][x+1] == 0 and board[y][x] == board[y+2][x+2] == board[y+3][x+3]:
                if y+1 in even_rows and threat_heights_yellow[x+1] > y+1 and board[y][x] == -1:
                    threat_heights_yellow[x+1] = 5 - (y+1)
                elif y+1 in odd_rows and threat_heights_red[x+1] > y+1 and board[y][x] == 1:
                    threat_heights_red[x+1] = 5 - (y+1)

            elif board[y+2][x+2] == 0 and board[y][x] == board[y+1][x+1] == board[y+3][x+3]:
                if y+2 in even_rows and threat_heights_yellow[x+2] > y+2 and board[y][x] == -1:
                    threat_heights_yellow[x+2] = 5 - (y+2)
                elif y+2 in odd_rows and threat_heights_red[x+2] > y+2 and board[y][x] == 1:
                    threat_heights_red[x+2] = 5 - (y+2)

            elif board[y][x] == board[y+1][x+1] == board[y+2][x+2] and board[y+3][x+3] == 0:
                if y+3 in even_rows and threat_heights_yellow[x+3] > y+3 and board[y][x] == -1:
                    threat_heights_yellow[x+3] = 5 - (y+3)
                elif y+3 in odd_rows and threat_heights_red[x+3] > y+3 and board[y][x] == 1:
                    threat_heights_red[x+3] = 5 - (y+3)

    # Check for diagonal up odd threats for yellow
    for y in range(3, 6):
        for x in range(0, 4):
            # y == 4, x == 1
            if board[y][x] == 0 and board[y-1][x+1] == board[y-2][x+2] == board[y-3][x+3]:
                if y in even_rows and threat_heights_yellow[x] > y and board[y-1][x+1] == -1:
                    threat_heights_yellow[x] = 5 - y
                elif y in odd_rows and threat_heights_red[x] > y and board[y-1][x+1]:
                    threat_heights_red[x] = 5 - y

            elif board[y-1][x+1] == 0 and board[y][x] == board[y-2][x+2] == board[y-3][x+3]:
                if y-1 in even_rows and threat_heights_yellow[x+1] > y-1 and board[y][x] == -1:
                    threat_heights_yellow[x+1] = 5 - (y-1)
                elif y-1 in odd_rows and threat_heights_red[x+1] > y-1 and board[y][x] == 1:
                    threat_heights_red[x+1] = 5 - (y-1)

            elif board[y-2][x+2] == 0 and board[y][x] == board[y-1][x+1] == board[y-3][x+3]:
                if y-2 in even_rows and threat_heights_yellow[x+2] > y-2 and board[y][x] == -1:
                    threat_heights_yellow[x+2] = 5 - (y-2)
                elif y-2 in odd_rows and threat_heights_red[x+2] > y-2 and board[y][x] == 1:
                    threat_heights_red[x+2] = 5 - (y-2)

            elif board[y-3][x+3] == 0 and board[y][x] == board[y-1][x+1] == board[y-2][x+2]:
                if y-3 in even_rows and threat_heights_yellow[x+3] > y-3 and board[y][x] == -1:
                    threat_heights_yellow[x+3] = 5 - (y-3)
                elif y-3 in odd_rows and threat_heights_red[x+3] > y-3 and board[y][x] == 1:
                    threat_heights_red[x+3] = 5 - (y-3)

    # Whoever has the lowest threat height will eventually win
    # Return the player who has the lowest threat height, or 0 if nobody
    return threat_heights_yellow, threat_heights_red

  def calc_move(self, board):
    # Find the number of turns taken by counting the number of player nums
    self.turns_taken = 0
    for row in board:
        for col in row:
            if col == self.player:
                self.turns_taken += 1

    # Check if we have to defend or win
    immediate_threat = self.check_override_move(board)
    if immediate_threat != None:
        return immediate_threat

    # Settable variables
    evalFunc = self.earlyEval
    # depth = 9
    depth = 7
    
    # update any moves we need to stall
    self.get_new_stall_actions(board)

    # Find how deep we should search
    if self.turns_taken > 7:
        # depth = 10
        depth = 7
    if self.turns_taken > 10:
        evalFunc = self.evaluation
        # depth = 11
        depth = 7
    if self.turns_taken > 12:
        depth = 42

    # Run the minimax to find optimal move
    return self.minimax_new(evalFunc, board, depth, -math.inf, math.inf, True, self.player)[1]

  def get_environment_move(self, board, player):
    return {
        "move" : self.get_move(board, player),
        "eval" : 0
        }