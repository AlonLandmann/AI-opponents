import math
import copy

# functions
def look(pos, i, j, direction, nr_cells):
  result = []
  for r in range(nr_cells):
    if direction == 'horizontal':
      result.append(pos[i][j + r])
    if direction == 'vertical':
      result.append(pos[i + r][j])
    if direction == 'down-right':
      result.append(pos[i + r][j + r])
    if direction == 'down-left':
      result.append(pos[i + r][j - r])
  return result

def scan(pos, pattern):
  matches = []
  n = len(pattern)
  for i in range(0, 6):
    for j in range(0, 8 - n):
      if look(pos, i, j, 'horizontal', n) == pattern:
        matches.append((i, j))
  for i in range(0, 7 - n):
    for j in range(0, 7):
      if look(pos, i, j, 'vertical', n) == pattern:
        matches.append((i, j))
  for i in range(0, 7 - n):
    for j in range(0, 8 - n):
      if look(pos, i, j, 'down-right', n) == pattern:
        matches.append((i, j))
  for i in range(0, 7 - n):
    for j in range(n - 1, 7):
      if look(pos, i, j, 'down-left', n) == pattern:
        matches.append((i, j))
  return matches

def determine_result(pos):
  if scan(pos, ['X', 'X', 'X', 'X']): return 'X wins'
  if scan(pos, ['O', 'O', 'O', 'O']): return 'O wins'
  for j in range(0, 7):
    if pos[0][j] == '-': return 'undecided'
  return 'draw'

def determine_evaluation(pos):
  result = determine_result(pos)
  eval_map = { 'X wins': 1, 'draw': 0, 'O wins': -1 }
  if result in eval_map:
    return eval_map[result]
  doubleX = len(scan(pos, ['-', 'X', 'X', 'X', '-']))
  doubleO = len(scan(pos, ['-', 'O', 'O', 'O', '-']))
  singleX = len(scan(pos, ['-', 'X', 'X', 'X'])) + len(scan(pos, ['X', 'X', 'X', '-'])) - 2 * doubleX
  singleO = len(scan(pos, ['-', 'X', 'X', 'X'])) + len(scan(pos, ['X', 'X', 'X', '-'])) - 2 * doubleO
  centralX = centralO = totalX = totalO = 0
  double_factor = single_factor = central_factor = 0
  for i in range(0, 6):
    for j in range(0, 7):
      if pos[i][j] == 'X':
        totalX += 1
        if i in [1, 4]: centralX += 1
        if i in [2, 3]: centralX += 2
        if j in [0, 6]: centralX += 1
        if j in [1, 5]: centralX += 2
        if j in [2, 4]: centralX += 5
        if j in [3]: centralX += 8
      if pos[i][j] == 'O':
        totalO += 1
        if i in [1, 4]: centralO += 1
        if i in [2, 3]: centralO += 2
        if j in [0, 6]: centralO += 1
        if j in [1, 5]: centralO += 2
        if j in [2, 4]: centralO += 5
        if j in [3]: centralO += 8
  if doubleX + doubleO:
    double_factor = (doubleX - doubleO) / (doubleX + doubleO)
  if singleX + singleO:
    single_factor = (singleX - singleO) / (singleX + singleO)
  if totalX and totalO:
    central_factor = (centralX / totalX) - (centralO / totalO)
  raw = 0.80 * double_factor + 0.15 * single_factor + 0.05 * central_factor
  return math.atan(raw) / math.pi

def determine_turn(pos):
  def flatten(pos):
    result = []
    for i in range(0, 6):
      result.extend(pos[i])
    return result
  
  flat_pos = flatten(pos)
  countX = flat_pos.count('X')
  countO = flat_pos.count('O')
  if countX <= countO:
    return 'X'
  else:
    return 'O'

def make_a_move(pos, j, turn):
  new_pos = copy.deepcopy(pos)
  if new_pos[0][j] == '-':
    for i in range(5, -1, -1):
      if new_pos[i][j] == '-':
        new_pos[i][j] = turn
        break
  return new_pos

def ab_edge_dive(pos, ab_value, depth, depth_limit):
  turn = determine_turn(pos)
  result = determine_result(pos)
  eval = determine_evaluation(pos)
  if result != 'undecided' or depth == depth_limit:
    return { 'eval': eval }
  evals = []
  moves = []
  ab_send = None
  for j in range(7):
    if pos[0][j] == '-':
      new_pos = make_a_move(pos, j, turn)
      dive_results = ab_edge_dive(new_pos, ab_send, depth + 1, depth_limit)
      if turn == 'X' and dive_results['eval'] == 1:
        return { 'eval': 1, 'move': j }
      if turn == 'O' and dive_results['eval'] == -1:
        return { 'eval': -1, 'move': j }
      if turn == 'X' and ab_value != None and dive_results['eval'] > ab_value:
        return { 'eval': dive_results['eval'] }
      if turn == 'O' and ab_value != None and dive_results['eval'] < ab_value:
        return { 'eval': dive_results['eval'] }
      evals.append(dive_results['eval'])
      moves.append(j)
      if turn == 'X':
        ab_send = max(evals)
      if turn == 'O':
        ab_send = min(evals)
  if turn == 'X':
    return { 'eval': max(evals), 'move': moves[evals.index(max(evals))] }
  if turn == 'O':
    return { 'eval': min(evals), 'move': moves[evals.index(min(evals))] }
  
def paint(pos):
  string = ''
  for i in range(6):
    for j in range(7):
      string += pos[i][j]
      if j == 6:
        string += '\n'
      else:
        string += ' '
  print(string)

def validated_input(first_msg, repeat_msg, valid_inputs):
  for attempt in range(100):
    msg = first_msg if attempt == 0 else repeat_msg
    input_received = input(msg)
    if input_received in valid_inputs:
      return input_received

# script
demo_position = [
  ['1', '2', '3', '4', '5', '6', '7'],
  ['1', '2', '3', '4', '5', '6', '7'],
  ['1', '2', '3', '4', '5', '6', '7'],
  ['1', '2', '3', '4', '5', '6', '7'],
  ['1', '2', '3', '4', '5', '6', '7'],
  ['1', '2', '3', '4', '5', '6', '7']
]
position = [
  ['-', '-', '-', '-', '-', '-', '-'],
  ['-', '-', '-', '-', '-', '-', '-'],
  ['-', '-', '-', '-', '-', '-', '-'],
  ['-', '-', '-', '-', '-', '-', '-'],
  ['-', '-', '-', '-', '-', '-', '-'],
  ['-', '-', '-', '-', '-', '-', '-']
]
print('''Welcome to Connect-4 almost unbeatable!
The columns of the board are numbered from 1 to 7 as shown below.
To make a move, enter the number of the target column.\n''')
paint(demo_position)
first_msg = 'First, please enter a number from 1 to 5 to select the strength of the computer: '
repeat_msg = 'Please enter a number from 1 to 5: '
strength = validated_input(first_msg, repeat_msg, [str(i) for i in range(1, 6)])
symbol_input = input('''Please enter the character X if you want to start the game
or any other character if you want the computer to start: ''')
player = 'X' if symbol_input in ['X', 'x'] else 'O'
print('Thank you and good luck...')
if player == 'X':
  paint(position)
while determine_result(position) == 'undecided':
  turn = determine_turn(position)
  if turn == player:
    first_msg = 'Enter your move: '
    repeat_msg = 'Please enter a number corresponding to an empty column: '
    empty_cols = [str(j + 1) for j in range(7) if position[0][j] == '-']
    move_input = validated_input(first_msg, repeat_msg, empty_cols)
    position = make_a_move(position, int(move_input) - 1, turn)
  else:
    print('The computer is thinking...')
    dive_result = ab_edge_dive(position, None, 0, int(strength))
    print(f"Computer evaluation: {dive_result['eval']:.2f}")
    position = make_a_move(position, int(dive_result['move']), turn)
  paint(position)
print(determine_result(position))
print('Thank you for playing!')