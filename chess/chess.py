# functions
def color(piece):
  if piece in {'K', 'Q', 'R', 'N', 'B', 'o'}: return 'w'
  if piece in {'k', 'q', 'r', 'n', 'b', 'x'}: return 'b'
  return '-'

def target_type(piece, target):
  if target == '-': return '-'
  elif color(piece) == color(target): return 'friend'
  else: return 'foe'

def range_to_edge(i, j, direction):
  if direction == 'n': return range(1, i + 1)
  if direction == 's': return range(1, 8 - i)
  if direction == 'e': return range(1, 8 - j)
  if direction == 'w': return range(1, j + 1)

def look(pos, i, j, direction):
  result = []
  for r in range_to_edge(i, j, direction):
    if direction == 'n': result.append({ 'piece': pos[i - r][j], 'i': i - r, 'j': j })
    if direction == 's': result.append({ 'piece': pos[i + r][j], 'i': i + r, 'j': j })
    if direction == 'e': result.append({ 'piece': pos[i][j + r], 'i': i, 'j': j + r })
    if direction == 'w': result.append({ 'piece': pos[i][j - r], 'i': i, 'j': j - r })
  return result

def rook_moves(pos, i, j):
  moves = []
  for direction in ['n', 's', 'w', 'e']:
    view = look(pos, i, j, direction)
    # try to be more and more functional here
    for square in view:
      if square['piece'] == '-':
        moves.append((square['i'], square['j']))
      elif target_type(pos[i][j], square['piece']) == 'foe':
        moves.append((square['i'], square['j']))
        break
      else:
        break
  return moves

# script
starting_position = [
  ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
  ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
  ['-', '-', '-', '-', '-', '-', '-', '-'],
  ['-', '-', '-', '-', 'R', '-', '-', '-'],
  ['-', '-', '-', '-', '-', '-', '-', '-'],
  ['-', '-', '-', '-', '-', '-', '-', '-'],
  ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
  ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
]

starting_turn = 'w'