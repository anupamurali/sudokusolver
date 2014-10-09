"""
Implemented by the wonderful Anupa Murali & Elliot Silva!
"""

from copy import deepcopy
import timeit

class Sudoku:
  def __init__(self, board):
    self.board = board

  def __str__(self):
    boardString = '\n'
    for row in self.board:
      boardString += str(row) + '\n'
    return boardString

  def _getFirstEmptySquare(self):
    """
    Arguments:
      self = an instantiation of a Sudoku board

    Returns:
      (x,y) = coordinates of the first empty square
              in the Sudoku board, going from top left
              to bottom right
    """
    for x in xrange(0,9):
      for y in xrange(0,9):
        if not self.board[x][y]:
          return (x, y)
    return None

  def _getMostConstrainedEmptySquare(self):
    """
    Arguments:
      self = an instantiation of a Sudoku board

    Returns:
      (x,y) = coordinates of the most constrained empty
              square, the square with the least possible
              number of values that could be placed there
              without directly violating the constraints
              imposed by the currently non-empty squares
    """
    minLen = 10
    emptySquare = (0,0)
    for x in xrange(0,9):
      for y in xrange(0,9):
        if not self.board[x][y]:
          numVals = len(self._getPossibleValsFor((x,y)))
          if numVals == 1:
            return (x,y)
          if numVals < minLen:
            minLen = numVals
            emptySquare = (x,y)
    return emptySquare

  # PART 3: Swap out the implementation after implementing part 3
  def _getEmptySquare(self):
    # return self._getFirstEmptySquare()
    return self._getMostConstrainedEmptySquare()

  def _getRow(self, x):
    return list(self.board[x])

  def _getCol(self, y):
    return [row[y] for row in self.board]

  def _getBox(self, x, y):
    rowmin, rowmax = x / 3 * 3, x / 3 * 3 + 3
    colmin, colmax = y / 3 * 3, y / 3 * 3 + 3
    nums = [] 
    for x in xrange(rowmin, rowmax):
      for y in xrange(colmin, colmax):
        nums.append(self.board[x][y])
    return nums

  def _crossOff(self, values, nums):
    for n in nums:
      if n: values[n-1] = None

  def _getPossibleValsFor(self, emptySquare):
    x = emptySquare[0]
    y = emptySquare[1]
    values = range(1,10)
    row = self._getRow(x)
    col = self._getCol(y)
    box = self._getBox(x, y)
    self._crossOff(values, row)
    self._crossOff(values, col)
    self._crossOff(values, box)
    return [v for v in values if v]

  def _fillEmptySquare(self, emptySquare, val):
    newBoard = deepcopy(self.board)
    newBoard[emptySquare[0]][emptySquare[1]] = val
    return Sudoku(newBoard)

  def _forwardCheck(self):
    """
    Arguments:
      self = an instantiation of a Sudoku board

    Returns:
      True if for each empty square in this Sudoku board
        there is at least one value that could go there
        without directly violating constraints imposed
        by the currently non-empty squares
      False otherwise
    """
    for x in xrange(0,9):
      for y in xrange(0,9):
        if not self.board[x][y]:
          if len(self._getPossibleValsFor((x,y))) == 0:
            return False
    return True

  #####################################################################
  ## Get most constrained empty square, fill it in with all possible ##
  ## values.                                                         ##
  ## Return array of Sudoku instances                                ##
  #####################################################################
  def _getAllSuccessors(self):
    """
    Arguments:
      self = an instantiation of a Sudoku board

    Returns:
      list of Sudoku boards, each with a different
      possible value in an empty square that won't
      directly conflict with the constraints imposed
      by the currently non-empty squares
    """
    emptySquare = self._getEmptySquare()
    possValues = self._getPossibleValsFor(emptySquare)
    def fillInWithVal(val): return self._fillEmptySquare(emptySquare, val)
    return map(fillInWithVal, possValues)

  def _getSuccessorsWithForwardChecking(self):
    """
    Arguments:
      self = an instantiation of a Sudoku board

    Returns:
      list of Sudoku boards, each with a different
      possible value in an empty square

    Notes:
      same as _getAllSuccessors except we only return
      boards if every other empty square has at least one
      possible value that won't directly violate the constraints
      imposed by the currently non-empty squares, including the
      newest one we are potentially deciding whether to add
    """
    return [s for s in self._getAllSuccessors() if s._forwardCheck()]

  # PART 2: Swap out the implementation after implementing part 2
  def getSuccessors(self):
    # return self._getAllSuccessors()
    return self._getSuccessorsWithForwardChecking()

  def isFinalState(self):
    return self._getFirstEmptySquare() == None

def solveCSP(problem):
  statesExplored = 0
  fringe = [problem]
  while fringe:
    state = fringe.pop()
    statesExplored += 1
    if state.isFinalState():
      print 'Number of explored: ' + str(statesExplored)
      return state
    else:
      successors = state.getSuccessors()  
      fringe.extend(successors)
  return None

if __name__ == "__main__":
  setup = '''
from __main__ import Sudoku
from __main__ import solveCSP

mySudokuBoard = [[None, None, None, None, None, 8, 9, None, 2],
          [6, None, 4, 3, None, None, None, None, None],
          [None, None, None, 5, 9, None, None, None, None],
          [None, None, 5, 7, None, 3, None, None, 9],
          [7, None, None, None, 4, None, None, None, None],
          [None, None, 9, None, None, None, 3, None, 5],
          [None, 8, None, None, None, 4, None, None, None],
          [None, 4, 1, None, None, None, None, 3, None],
          [2, None, None, 1, 5, None, None, None, None]]
mySudokuPuzzle = Sudoku(mySudokuBoard)


mySudokuPuzzle = Sudoku(mySudokuBoard)
'''

  solveSudoku = '''
print 'Solution: ' + str(solveCSP(mySudokuPuzzle))
'''

  print 'Time elapsed: ' + str(timeit.timeit(solveSudoku, setup = setup, number = 1))

