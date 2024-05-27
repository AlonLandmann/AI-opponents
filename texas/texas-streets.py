import numpy as np

# training parameters
NUM_ITERATIONS = 10000000

# game parameters
N = 3
CARDS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'][:N]
STACK_SIZE = 20

# utilities
def card_value(card):
  return len(CARDS) - CARDS.index(card)

def showdown_multiplier(cards):
  if cards[0] == cards[2]:
    return -1
  if cards[1] == cards[2]:
    return 1
  if card_value(cards[0]) > card_value(cards[1]):
    return -1
  if card_value(cards[0]) < card_value(cards[1]):
    return 1
  return 0

def deal_cards():
  deck = CARDS + CARDS
  return np.random.choice(deck, 3, replace = False)
  deck = CARDS + CARDS
  deck.remove(cards[0])
  deck.remove(cards[1])
  return np.random.choice(deck, 2, replace = False)

def is_river(history):
  for card in CARDS:
    if card in history:
      return True
  return False

def get_board(history):
  for card in CARDS:
    if card in history:
      return card
  return None

def is_raise(action):
  return isinstance(action, int)

def node_type(history):
  if len(history) <= 1:
    return 'player'
  elif history[-1] == 'f':
    return 'fold'
  elif is_raise(history[-2]) and history[-1] == 'c':
    return 'showdown' if is_river(history) else 'chance'
  elif history[-2] == 'c' and history[-1] == 'c':
    return 'showdown' if is_river(history) else 'chance'
  return 'player'

def is_terminal(history):
  return node_type(history) in ['fold', 'showdown']

def get_player(history):
  last_street = history.copy()
  if is_river(history):
    board = get_board(history)
    last_street = history[history.index(board) + 1:]
  return len(last_street) % 2

def get_low_and_high(history):
  low = 1
  high = 1
  count = 0
  for a in reversed(history):
    if is_raise(a) and count == 0:
      high = a
      count = 1
    elif is_raise(a) and count == 1:
      low = a
      break
  return (low, high)

def get_payoff(history, cards):
  low, high = get_low_and_high(history)
  player = get_player(history)
  type = node_type(history)
  if type == 'fold':
    return low * (-1 if player == 0 else 1)
  elif type == 'showdown':
    return  high * showdown_multiplier(cards)
  return None

def facing_check_or_new(stakes):
  actions = ['c']
  for a in range(stakes + 1, STACK_SIZE + 1):
    actions.append(a)
  return actions

def facing_raise(stakes, raise_size):
  actions = ['f', 'c']
  for a in range(stakes + raise_size, STACK_SIZE):
    actions.append(a)
  actions.append(STACK_SIZE)
  return actions

def get_actions(history):
  low, high = get_low_and_high(history)
  if history == []:
    return facing_check_or_new(1)
  else:
    last = history[-1]
    if last in CARDS or last == 'c':
      return facing_check_or_new(high)
    elif is_raise(last):
      return facing_raise(high, high - low)
  return None
    

# script
# cards = deal_cards()
# print(cards)

# h = [
#   [],
#   ['c'],
#   ['c', 4],
#   ['c', 4, 'c'],
#   ['c', 4, 'c', cards[2]],
#   ['c', 4, 'c', cards[2], 7],
#   ['c', 4, 'c', cards[2], 7, 12],
#   ['c', 4, 'c', cards[2], 7, 12, 'f'],
#   ['c', 4, 'c', cards[2], 7, 12, 'c'],
#   ['c', 4, 'c', cards[2], 7, 12, 17],
#   ['c', 4, 'c', cards[2], 7, 12, 17, 'f'],
#   ['c', 4, 'c', cards[2], 7, 12, 17, 'c']
# ]

# for history in h:
#   print(history)
#   print(f'is river: {is_river(history)}')
#   print(f'get board: {get_board(history)}')
#   print(f'node type: {node_type(history)}')
#   print(f'is_terminal: {is_terminal(history)}')
#   print(f'get_player: {get_player(history)}')
#   print(f'get_payoff: {get_payoff(history, cards)}')
#   print(f'get_actions: {get_actions(history)}')
    

# # information sets
# class InformationSet:
#   def __init__(self, actions):
#     n = len(actions)
#     self.actions = actions
#     self.strategy = np.ones(n) / n
#     self.strategy_sum = np.zeros(n)
#     self.regret_sum = np.zeros(n)
  
#   def update_strategy(self, realization_weight):
#     n = len(self.actions)
#     normalizing_sum = 0
#     for a in range(n):
#       self.strategy[a] = max(self.regret_sum[a], 0)
#       normalizing_sum += self.strategy[a]
#     for a in range(n):
#       if normalizing_sum > 0:
#         self.strategy[a] /= normalizing_sum
#       else:
#         self.strategy[a] = 1.0 / n
#       self.strategy_sum[a] += realization_weight * self.strategy[a]
#     return self.strategy
  
#   def get_average_strategy(self):
#     n = len(self.actions)
#     normalizing_sum = sum(self.strategy_sum)
#     if normalizing_sum > 0:
#       return self.strategy_sum / normalizing_sum
#     else:
#       return np.ones(n) / n

# # cfr algorithm
# class CfrTrainer:
#   def __init__(self):
#     self.node_map = {}
  
#   def train(self):
#     utility = 0
#     for k in range(NUM_ITERATIONS):
#       cards = deal_cards()
#       utility += self.cfr(cards, '', 1, 1)
#       if k % (NUM_ITERATIONS // 100) == 0:
#         print(f'{100 * k / NUM_ITERATIONS:.2f}%')
#     return utility / NUM_ITERATIONS
  
#   def get_strategy(self):
#     strategies = {}
#     for key, info_set in self.node_map.items():
#       strategies[key] = {
#         'actions': info_set.actions,
#         'strategy': info_set.get_average_strategy()
#       }
#     return strategies
  
#   def cfr(self, cards, history, p0, p1):
#     # determine whose turn it is
#     player = determine_turn(history)