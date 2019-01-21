'''
PriorityQueue is a data type which is like a regular queue or stack
but where additionally each element has a "priority" associated with it
'''

#import heapq
from heapdict import heapdict
import copy

sPosition_a = ()
gPosition_a = ()

sPosition_b = ()
gPosition_b = ()

inputFile_a = open('pathfinding_a.txt', 'r')
inputFile_b = open('pathfinding_b.txt', 'r')

# read all the inputs into a list so we can iterate through each request
inputList_a = inputFile_a.read().split('\n')
inputList_b = inputFile_b.read().split('\n')

for i in range(len(inputList_a)):
  inputList_a[i] = list(inputList_a[i])
  if 'S' in inputList_a[i]:
    sPosition_a = (i, inputList_a[i].index('S'))
  if 'G' in inputList_a[i]:
    gPosition_a = (i, inputList_a[i].index('G'))

for i in range(len(inputList_b)):
  inputList_b[i] = list(inputList_b[i])
  if 'S' in inputList_b[i]:
    sPosition_b = (i, inputList_b[i].index('S'))
  if 'G' in inputList_b[i]:
    gPosition_b = (i, inputList_b[i].index('G'))

#print(sPosition,gPosition)


def get_adjacent_cells(current):
  """
  Returns adjacent cells to a cell
  Clockwise starting from the cell on the right
  """
  row = current[0]
  col = current[1]
  cells = [] #stored as tuples (row, col)

  if col<len(inputList_a[0])-1 and inputList_a[row][col+1] != 'X':
    cells.append((row,col+1)) #right
  if row < len(inputList_a)-1 and inputList_a[row+1][col] != 'X':
    cells.append((row+1, col)) #down
  if col > 0 and inputList_a[row][col-1] != 'X':
    cells.append((row, col-1)) #left
  if row > 0 and inputList_a[row-1][col] != 'X':
    cells.append((row-1, col)) #up
  #print(cells)
  return cells

def get_adjacent_cell_diagonal(current):
  """
  Returns adjacent cells to a cell
  Clockwise starting from the cell on the right
  """
  row = current[0]
  col = current[1]
  cells = [] #stored as tuples (row, col)

  if col<len(inputList_b[0])-1 and inputList_b[row][col+1] != 'X':
    cells.append((row,col+1)) #right
  if row < len(inputList_b)-1 and inputList_b[row+1][col] != 'X':
    cells.append((row+1, col)) #down
  if col > 0 and inputList_b[row][col-1] != 'X':
    cells.append((row, col-1)) #left
  if row > 0 and inputList_b[row-1][col] != 'X':
    cells.append((row-1, col)) #up
    
  #diagonal cells
  if col<len(inputList_b[0])-1 and row <len(inputList_b)-1 and inputList_b[row+1][col+1] != 'X':
    cells.append((row+1,col+1))
  if col > 0 and row <len(inputList_b)-1 and inputList_b[row+1][col-1] != 'X':
    cells.append((row+1,col-1))
  if col > 0 and row>0 and inputList_b[row-1][col-1] != 'X':
    cells.append((row-1,col-1))
  if col<len(inputList_b[0])-1 and row > 0 and inputList_b[row-1][col+1] != 'X':
    cells.append((row-1,col+1))
    
  #print(cells)
  return cells


def findpath_a():
  frontier = heapdict()
  frontier[sPosition_a] = 0 #push start to top of priority queue
  came_from = {} #key = node, value = parent
  cost_so_far = {} #start point to current node
  
  came_from[sPosition_a] = None
  cost_so_far[sPosition_a]=0

  nextPos = sPosition_a

  while len(frontier)>0:

    curPos = frontier.popitem() 
    curPos = curPos[0]
    
    if inputList_a[curPos[0]][curPos[1]] == 'G':
      break
    
    neighbours = get_adjacent_cells(curPos)
    
    for next in neighbours:
        new_cost = cost_so_far[curPos] + heuristic(curPos,next)
        if next not in cost_so_far or new_cost<cost_so_far[next]:
          cost_so_far[next]=new_cost
          priority = new_cost + heuristic(gPosition_a, next)
          frontier[next] = priority
          came_from[next] = curPos


  draw_path(came_from, inputList_a,sPosition_a,gPosition_a)

def findpath_b():
  frontier = heapdict()
  frontier[sPosition_b] = 0 #push start to top of priority queue
  came_from = {} #key = node, value = parent
  cost_so_far = {} #start point to current node
  
  came_from[sPosition_b] = None
  cost_so_far[sPosition_b]=0

  nextPos = sPosition_b

  while len(frontier)>0:

    curPos = frontier.popitem() 
    curPos = curPos[0]
    #print("current pos",curPos) 
    
    if inputList_b[curPos[0]][curPos[1]] == 'G':
      break
    
    neighbours = get_adjacent_cell_diagonal(curPos)
    
    for next in neighbours:
        new_cost = cost_so_far[curPos] + heuristic(curPos,next)
        if next not in cost_so_far or new_cost<cost_so_far[next]:
          cost_so_far[next]=new_cost
          priority = new_cost + heuristic(gPosition_b, next)
          frontier[next] = priority
          came_from[next] = curPos


  draw_path(came_from,inputList_b,sPosition_b,gPosition_b)
      
def draw_path(came_from,resultList,sPos,gPos):
  path = []
  current = gPos
  path = [current]
  while current != sPos:
    current = came_from[current]
    path.append(current)
  path.append(sPos)
  path.reverse

  for ele in path:
    if resultList[ele[0]][ele[1]] != 'S' and resultList[ele[0]][ele[1]] != 'G':
      resultList[ele[0]][ele[1]] = 'P'
    
def heuristic(a,b):
  '''
  The heuristic function of A*
  Using the manhattan distance
  '''
  (r1,c1)=a
  (r2,c2)=b
  return abs(r1-r2) + abs(c1-c2)
  

if __name__=='__main__':
  findpath_a()
  outputFile_a = open('pathfinding_a.out.txt', 'a')
  outputFile_a.write("A* Algorithm\n")
  outputFile_b = open('pathfinding_b.out.txt','a')
  outputFile_b.write("A* Algorithm\n")
  print("A* Algorithm part a")
  for ele in inputList_a:
    print(ele)
    result = ' '.join(ele)
    result += "\n"
    outputFile_a.write(result)
  outputFile_a.close()
  
  print("A* Algorithm part b")
  findpath_b()
  for ele in inputList_b:
    print(ele)
    result = ' '.join(ele)
    result += "\n"
    outputFile_b.write(result)
  outputFile_b.close()
                    
