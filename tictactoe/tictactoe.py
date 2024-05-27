# functions
def determine_result(position):
  has_empty_cell = False
  for i in range(3):
    horiX = horiO = vertX = vertO = 0
    for j in range(3):
      if position[i * 3 + j] == '-': has_empty_cell = True
      if position[i * 3 + j] == 'X': horiX += 1
      if position[i * 3 + j] == 'O': horiO += 1
      if position[j * 3 + i] == 'X': vertX += 1
      if position[j * 3 + i] == 'O': vertO += 1
    if horiX == 3 or vertX == 3: return 'X wins'
    if horiO == 3 or vertO == 3: return 'O wins'
  if position[0] == 'X' and position[4] == 'X' and position[8] == 'X': return 'X wins';
  if position[2] == 'X' and position[4] == 'X' and position[6] == 'X': return 'X wins';
  if position[0] == 'O' and position[4] == 'O' and position[8] == 'O': return 'O wins';
  if position[2] == 'O' and position[4] == 'O' and position[6] == 'O': return 'O wins';
  if has_empty_cell:
    return 'undecided'
  else:
    return 'draw'

def determine_evaluation(result):
  eval_map = { 'X wins': 1, 'draw': 0, 'O wins': -1, 'undecided': None }
  return eval_map[result]

def determine_turn(position):
  countX = position.count('X')
  countO = position.count('O')
  if countX <= countO:
    return 'X'
  else:
    return 'O'

def make_a_move(position, cell, symbol):
  new_position = position.copy()
  if new_position[cell] == '-':
    new_position[cell] = symbol
  return new_position

def dive(position):
  turn = determine_turn(position)
  result = determine_result(position)
  eval = determine_evaluation(result)
  if result != 'undecided':
    return { 'eval': eval }
  evals = []
  moves = []
  for i in range(9):
    if position[i] == '-':
      new_position = make_a_move(position, i, turn)
      new_dive_results = dive(new_position)
      evals.append(new_dive_results['eval'])
      moves.append(i)
  if turn == 'X':
    return {
      'eval': max(evals),
      'move': moves[evals.index(max(evals))]
    }
  if turn == 'O':
    return {
      'eval': min(evals),
      'move': moves[evals.index(min(evals))]
    }
  
def paint(position):
  string = ''
  for i in range(9):
    string += position[i]
    if i % 3 == 2:
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
demo_position = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
position = ['-', '-', '-', '-', '-', '-', '-', '-', '-']
print('''Welcome to TicTacToe unbeatable!\n
The squares of the board are numbered from 1-9 as shown:\n''')
paint(demo_position)
print('To make a move, enter the number of the target square.')
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
    repeat_msg = 'Please enter a number corresponding to an empty cell: '
    empty_cells = [str(i + 1) for i in range(9) if position[i] == '-']
    move_input = validated_input(first_msg, repeat_msg, empty_cells)
    position = make_a_move(position, int(move_input) - 1, turn)
  else:
    print('The computer is thinking...')
    dive_result = dive(position)
    position = make_a_move(position, int(dive_result['move']), turn)
  paint(position)
print(determine_result(position))
print('Thank you for playing!')
