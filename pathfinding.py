DOWN_RIGHT = 'DOWN_RIGHT'
UP_RIGHT='UP_RIGHT'
DOWN_LEFT='DOWN_LEFT'
UP_LEFT='UP_LEFT'

DOWN='DOWN'
UP = 'UP'
RIGHT= 'RIGHT'
LEFT = 'LEFT'
NULL='NULL'



def initializeBoard(inputList):
  sPosition = ()
  gPosition = ()
  movingDirection = ''
  rightMove = 0
  downMove = 0

  for i in range(len(inputList)):
    if 'S' in inputList[i]:
      sPosition = (i, inputList[i].index('S'))
    if 'G' in inputList[i]:
      gPosition = (i, inputList[i].index('G'))
  if sPosition[1] < gPosition[1]:
    if sPosition[0] > gPosition[0]:
      movingDirection = UP_RIGHT
      rightMove = 1
      downMove = -1
    elif sPosition[0] < gPosition[0]:
      movingDirection = DOWN_RIGHT
      rightMove = 1
      downMove = 1
    else:
      movingDirection = RIGHT
      rightMove = 1
      downMove = 1
  elif sPosition[1] > gPosition[1]:
    if sPosition[0] < gPosition[0]:
      movingDirection = DOWN_LEFT
      rightMove = -1
      downMove = 1
    elif sPosition[0] > gPosition[0]:
      movingDirection = UP_LEFT
      rightMove = -1
      downMove = -1
    else:
      movingDirection = LEFT
      downMove = 1
      rightMove = -1
  else:
    if sPosition[0] < gPosition[0]:
      movingDirection = DOWN
      downMove = 1
      rightMove = 1
    elif sPosition[0] > gPosition[0]:
      movingDirection = UP
      rightMove = 1
      downMove = -1
    else:
      movingDirection = NULL
      rightMove = 0
      downMove = 0
  return {"sPosition":sPosition, "gPosition":gPosition, "movingDirection":movingDirection, "rightMove":rightMove, "downMove":downMove}


# check if the targeted position is within the board and add the position to the path stack
def checkPosition(inputList, row, column, visitedNodes, pathStack = []):
  if row <= len(inputList)-1 and row >= 0 and column >= 0 and column <= len(inputList[0])-1 and inputList[row][column] != 'X' and (row, column) not in visitedNodes:
    pathStack.insert(0, (row, column))
    return True
  else:
    return False

# check if the targeted position is our destination
def checkDestination(inputList, row, column):
  return column <= len(inputList[0])-1 and column >= 0 and row >=0 and row <= len(inputList)-1 and inputList[row][column] == 'G'

def greedyDiagonal(inputList, sPosition, gPosition, movingDirection, rightMove, downMove):
  pathStack = []
  pathStack.insert(0, sPosition)
  visitedNodes={}
  while len(pathStack) > 0:
    curPos = pathStack.pop(0)
    row = curPos[0]
    column = curPos[1]
    visitedNodes[curPos] = True
    originalLen = len(pathStack)

    # if one of the next moves is our destination, return the function
    if checkDestination(inputList, row, column+rightMove):
      inputList[row][column] = 'P'
      break
    if checkDestination(inputList, row+downMove, column):
      inputList[row][column] = 'P'
      break
    if checkDestination(inputList, row, column-rightMove):
      inputList[row][column] = 'P'
      break
    if checkDestination(inputList, row-downMove, column):
      inputList[row][column] = 'P'
      break

    if checkDestination(inputList, row-downMove, column-rightMove):
      inputList[row][column] = 'P'
      break
    if checkDestination(inputList, row+downMove, column+rightMove):
      inputList[row][column] = 'P'
      break
    if checkDestination(inputList, row-downMove, column-rightMove):
      inputList[row][column] = 'P'
      break
    if checkDestination(inputList, row+downMove, column+rightMove):
      inputList[row][column] = 'P'
      break

    if movingDirection == DOWN or movingDirection == UP:
      #if the current position is on the right side of the destination
      if column > gPosition[1]:
        if not checkPosition(inputList, row, column-rightMove, visitedNodes, pathStack):
          checkPosition(inputList, row, column+rightMove, visitedNodes, pathStack)
        if not checkPosition(inputList, row+downMove, column-rightMove, visitedNodes, pathStack):
          checkPosition(inputList, row+downMove, column+rightMove, visitedNodes, pathStack)
      elif column < gPosition[1]: #if the current position is on the left side of the destination
        if not checkPosition(inputList, row, column+rightMove, visitedNodes, pathStack):
          checkPosition(inputList, row, column-rightMove, visitedNodes, pathStack)
        if not checkPosition(inputList, row+downMove, column+rightMove, visitedNodes, pathStack):
          checkPosition(inputList, row+downMove, column-rightMove, visitedNodes, pathStack)
      else: #if the current position is on the same column of the destination
        checkPosition(inputList, row, column+rightMove, visitedNodes, pathStack)
        checkPosition(inputList, row, column-rightMove, visitedNodes, pathStack)
        checkPosition(inputList, row+downMove, column+rightMove, visitedNodes, pathStack)
        checkPosition(inputList, row+downMove, column-rightMove, visitedNodes, pathStack)
      #this will be added either way to move up or down directly
      checkPosition(inputList, row+downMove, column, visitedNodes, pathStack)
    elif movingDirection == RIGHT or movingDirection == LEFT:
      if row > gPosition[0]: # the current position is below the destination
        if not checkPosition(inputList, row-downMove, column, visitedNodes, pathStack):
          checkPosition(inputList, row+downMove, column, visitedNodes, pathStack)
        if not checkPosition(inputList, row-downMove, column+rightMove, visitedNodes, pathStack):
          checkPosition(inputList, row+downMove, column+rightMove, visitedNodes, pathStack)
      elif row < gPosition[0]: # the current position is above the destination
        if not checkPosition(inputList, row+downMove, column, visitedNodes, pathStack):
          checkPosition(inputList, row-downMove, column, visitedNodes, pathStack)
        if not checkPosition(inputList, row+downMove, column+rightMove, visitedNodes, pathStack):
          checkPosition(inputList, row-downMove, column+rightMove, visitedNodes, pathStack)
      else: # the current position is on the same row with the destination
        checkPosition(inputList, row+downMove, column, visitedNodes, pathStack)
        checkPosition(inputList, row-downMove, column, visitedNodes, pathStack)
        checkPosition(inputList, row+downMove, column+rightMove, visitedNodes, pathStack)
        checkPosition(inputList, row-downMove, column+rightMove, visitedNodes, pathStack)
      #this will be added either way to move right or left directly 
      checkPosition(inputList, row, column+rightMove, visitedNodes, pathStack)    
    else: # if the moving direction is none of up, down, left or right.
      checkPosition(inputList, row, column-rightMove, visitedNodes, pathStack)
      checkPosition(inputList, row+downMove, column-rightMove, visitedNodes, pathStack)
      checkPosition(inputList, row, column+rightMove, visitedNodes, pathStack)
      checkPosition(inputList, row+downMove, column, visitedNodes, pathStack)
      checkPosition(inputList, row+downMove, column+rightMove, visitedNodes, pathStack)
    curLen = len(pathStack)
    if originalLen != curLen:
      # curPos = pathStack.pop(0)
      if curPos != sPosition:
        inputList[row][column] = 'P'
  return inputList

def greedy(inputList, sPosition, gPosition, movingDirection, rightMove, downMove):
  pathStack = []
  pathStack.insert(0, sPosition)
  visitedNodes={}
  while len(pathStack) > 0:
    curPos = pathStack.pop(0)
    row = curPos[0]
    column = curPos[1]
    visitedNodes[curPos] = True
    originalLen = len(pathStack)
    # if one of the next moves is our destination, return the function
    if checkDestination(inputList, row, column+rightMove):
      inputList[row][column] = 'P'
      break
    if checkDestination(inputList, row+downMove, column):
      inputList[row][column] = 'P'
      break
    if checkDestination(inputList, row, column-rightMove):
      inputList[row][column] = 'P'
      break
    if checkDestination(inputList, row-downMove, column):
      inputList[row][column] = 'P'
      break

    #if we are going either up or down, we need to optimize on the routes
    if movingDirection == DOWN or movingDirection == UP:

      #if the current position is on the right side of the destination
      if column > gPosition[1]:
        if not checkPosition(inputList, row, column-rightMove, visitedNodes, pathStack):
          checkPosition(inputList, row, column+rightMove, visitedNodes, pathStack)
      elif column < gPosition[1]: #if the current position is on the left side of the destination
        if not checkPosition(inputList, row, column+rightMove, visitedNodes, pathStack):
          checkPosition(inputList, row, column-rightMove, visitedNodes, pathStack)
      else: #if the current position is on the same column of the destination
        checkPosition(inputList, row, column-rightMove, visitedNodes, pathStack)
        checkPosition(inputList, row, column+rightMove, visitedNodes, pathStack)
      checkPosition(inputList, row+downMove, column, visitedNodes, pathStack)
    elif movingDirection == RIGHT or movingDirection == LEFT:
      #if the current position is below the destination
      if row > gPosition[0]:
        if not checkPosition(inputList, row-downMove, column, visitedNodes, pathStack):
          checkPosition(inputList, row+downMove, column, visitedNodes, pathStack)
      elif row < gPosition[0]: #if the current position is above the destination
        if not checkPosition(inputList, row+downMove, column, visitedNodes, pathStack):
          checkPosition(inputList, row-downMove, column, visitedNodes, pathStack)
      else: #if the current position is on the same row of the destination
        checkPosition(inputList, row-downMove, column, visitedNodes, pathStack)
        checkPosition(inputList, row+downMove, column, visitedNodes, pathStack)
      checkPosition(inputList, row, column+rightMove, visitedNodes, pathStack)
    else:
      #if it's none of UP, DOWN, RIGHT, LEFT direction, we can simply add the wanted direction/
      checkPosition(inputList, row, column+rightMove, visitedNodes, pathStack)
      checkPosition(inputList, row+downMove, column, visitedNodes, pathStack)
  
    curLen = len(pathStack)
    if originalLen != curLen:
      # curPos = pathStack.pop(0)
      if curPos != sPosition:
        inputList[row][column] = 'P'
  return inputList
if __name__=='__main__':
  inputFile = open('pathfinding_a.txt', 'r')
  # read all the inputs into a list so we can iterate through each request
  inputList = inputFile.read().split('\n')
  inputLists = []
  tmpList = []
  # add all the matrix into a inputLists
  for i in range(len(inputList)):
    if inputList[i] != '':
      inputList[i] = list(inputList[i])
      tmpList.append(inputList[i])
    else:
      inputLists.append(tmpList)
      tmpList= []
  inputLists.append(tmpList)

  outputFile = open('pathfinding_a_out.txt', 'a')
  outputFile.write('Greedy\n')
  #iterate through each matrix to output solution
  for eachInput in inputLists:
    configuration = initializeBoard(eachInput)
    result = greedy(eachInput, configuration["sPosition"], configuration["gPosition"], configuration["movingDirection"], configuration["rightMove"], configuration["downMove"])
    for line in result:
      resultStr = ''
      for ele in line:
        resultStr += ele
      outputFile.write(resultStr + '\n')
      resultStr = ''
    outputFile.write('\n')
  

  inputFile_b = open('pathfinding_b.txt', 'r')
  # read all the inputs into a list so we can iterate through each request
  inputList_b = inputFile_b.read().split('\n')
  inputLists_b = []
  tmpList = []
  # add all the matrix into a inputLists
  for i in range(len(inputList_b)):
    if inputList_b[i] != '':
      inputList_b[i] = list(inputList_b[i])
      tmpList.append(inputList_b[i])
    else:
      inputLists_b.append(tmpList)
      tmpList= []
  inputLists_b.append(tmpList)

  outputFile = open('pathfinding_b_out.txt', 'a')
  outputFile.write('Greedy\n')
  #iterate through each matrix to output solutions
  for eachInput in inputLists_b:
    configuration = initializeBoard(eachInput)
    result = greedyDiagonal(eachInput, configuration["sPosition"], configuration["gPosition"], configuration["movingDirection"], configuration["rightMove"], configuration["downMove"])
    for line in result:
      resultStr = ''
      for ele in line:
        resultStr += ele
      outputFile.write(resultStr + '\n')
      resultStr = ''
    outputFile.write('\n')
  