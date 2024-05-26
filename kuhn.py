import random
import numpy as np

def next(turn):
  return 'P2' if turn == 'P1' else 'P1'

def add_decisions(decisions, tree, player, turn):
  if isinstance(tree, tuple):
    return
  elif turn == player:
    decisions.append(list(tree))
  for action in tree:
    add_decisions(decisions, tree[action], player, next(turn))

def per_card_decisions(tree, player):
  decisions = []
  add_decisions(decisions, tree, player, 'P1')
  return decisions

def per_card_strategies(tree, player):
  decisions = per_card_decisions(tree, player)
  strats = []
  for a in decisions[0]:
    strats.append(a)
  for d in range(1, len(decisions)):
    new_strats = []
    for strat in strats:
      new_strats.extend([strat + a for a in decisions[d]])
    strats = new_strats
  return strats

def all_strategies(tree, n, player):
  per_card = per_card_strategies(tree, player)
  strats = []
  for atomic_strat in per_card:
    strats.append([atomic_strat])
  for h in range(1, n):
    new_strats = []
    for strat in strats:
      new_strats.extend([strat + [atomic_strat]  for atomic_strat in per_card])
    strats = new_strats
  return strats

def w(h1, h2):
  if h1 < h2:
    return -1
  elif h1 > h2:
    return 1
  else:
    return 0

def eval_node(tree, p1, p2, h1, h2, turn):
  if isinstance(tree, tuple):
    if tree[0] == 'showdown':
      return w(h1, h2) * tree[1]
    else:
      return tree[1]
  elif turn == 'P1':
    return eval_node(tree[p1[0]], p1[1:], p2, h1, h2, next(turn))
  else:
    return eval_node(tree[p2[0]], p1, p2[1:], h1, h2, next(turn))
  
def eval_path(tree, p1, p2, h1, h2):
  return eval_node(tree, p1, p2, h1, h2, 'P1')

def eval_strats(tree, n, s1, s2):
  eval = 0
  for h1 in range(n):
    for h2 in range(n):
      if h1 != h2:
        eval += eval_path(tree, s1[h1], s2[h2], h1, h2)
  return eval / (n * (n - 1))

def eval_worst_case(tree, n, strat, player):
  if player == 'P1':
    S2 = all_strategies(tree, n, 'P2')
    evals = [eval_strats(tree, n, strat, s2) for s2 in S2]
    return max(evals)
  else:
    S1 = all_strategies(tree, n, 'P1')
    evals = [eval_strats(tree, n, s1, strat) for s1 in S1]
    return min(evals)

def eval_mixed_vs_pure(tree, n, S, x, pure, mixed_player):
  eval = 0
  if mixed_player == 'P1':
    for i in range(len(S)):
      eval += x[i] * eval_strats(tree, n, S[i], pure)
  else:
    for i in range(len(S)):
      eval += x[i] * eval_strats(tree, n, pure, S[i])
  return eval

def eval_mixed_worst_case(tree, n, x, S1, S2, player):
  if player == 'P1':
    evals = [eval_mixed_vs_pure(tree, n, S1, x, s2, 'P1') for s2 in S2]
    return max(evals)
  else:
    evals = [eval_mixed_vs_pure(tree, n, S2, x, s1, 'P2') for s1 in S1]
    return min(evals)

# random vector in the space
def softmax(x):
  e_x = np.exp(x - np.max(x))
  return e_x / e_x.sum()

def random_solution(z):
  seed = [random.randint(0, z) for i in range(64)]
  return softmax(seed)

def nudge_vector(x, sigma = 0.01):
    # Ensure the vector sums to 1
    assert np.isclose(np.sum(x), 1.0), "The input vector must sum to 1."
    # Ensure all values are between 0 and 1
    # assert np.all((0 <= x) & (x <= 1)), "All values in the input vector must be between 0 and 1."
    
    n = len(x)
    
    for k in range(random.randint(1, 20)):
      # Randomly choose two distinct indices
      i, j = np.random.choice(n, 2, replace=False)
      
      # Draw delta from a Gaussian distribution
      delta = np.random.normal(0, sigma)
      
      # Ensure delta does not violate the constraints
      max_del = min(abs(x[i]), abs(x[j]), abs(1 - x[i]), abs(1 - x[j]))
      delta = np.clip(delta, -max_del, max_del)
      
      # Create a new vector with the adjustment
      new_x = np.copy(x)
      new_x[i] += delta
      new_x[j] -= delta
      
      # Ensure all values remain within [0, 1]
      # assert np.all((0 <= new_x) & (new_x <= 1)), "Nudged values must be between 0 and 1."

      # update x
      x = new_x
    
    return new_x

  

# problem
n = 3
tree = {
  '0': {
    '0': ('showdown', 1),
    '1': {
      '0': ('P2', 1),
      '1': ('showdown', 2)
    }
  },
  '1': {
    '0': ('P1', -1),
    '1': ('showdown', 2)
  }
}

# pre-computation
S1 = all_strategies(tree, n, 'P1')
S2 = all_strategies(tree, n, 'P2')

# simmulated annealing algorithm
x = [1/64] * 64
f = eval_mixed_worst_case(tree, n, x, S1, S2, 'P1')
T = 10e10
c = 0.99
z = 30


for k in range(10000):
  candidate = nudge_vector(x)
  f_candidate = eval_mixed_worst_case(tree, n, candidate, S1, S2, 'P1')
  if np.exp((f - f_candidate)/T) > np.random.uniform():
    x = candidate
    f = f_candidate
  if k % 100 == 0:
    print(f'k: {k}, T: {T}, f: {f:.2}')  
  T = c * T

print(x)
print(f)
