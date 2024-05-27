import numpy as np

# training parameters
NUM_ITERATIONS = 1000

# game parameters
N = 3
CARDS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'][:N]
STACK_SIZE = 2
FILE_ID = 2

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
    return 'folded'
  elif is_raise(history[-2]) and history[-1] == 'c':
    return 'showdown' if is_river(history) else 'chance'
  elif history[-2] == 'c' and history[-1] == 'c':
    return 'showdown' if is_river(history) else 'chance'
  return 'player'

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

def get_payoff(history, ntype, player, cards):
  low, high = get_low_and_high(history)
  assert ntype in ['folded', 'showdown']
  if ntype == 'folded':
    return low * (-1 if player == 0 else 1)
  return  high * showdown_multiplier(cards)

def facing_check_or_new(stakes):
  actions = ['c']
  for a in range(stakes + 1, STACK_SIZE + 1):
    actions.append(a)
  return actions

def facing_raise(stakes, raise_size):
  actions = ['f', 'c']
  if stakes < STACK_SIZE:
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

def unique_key(history, player, cards):
  key = cards[player]
  for a in history:
    key += ',' + str(a)
  return key

# information sets
class InformationSet:
  def __init__(self, actions):
    n = len(actions)
    self.actions = actions
    self.strategy = np.ones(n) / n
    self.strategy_sum = np.zeros(n)
    self.regret_sum = np.zeros(n)
  
  def update_strategy(self, realization_weight):
    n = len(self.actions)
    normalizing_sum = 0
    for a in range(n):
      self.strategy[a] = max(self.regret_sum[a], 0)
      normalizing_sum += self.strategy[a]
    for a in range(n):
      if normalizing_sum > 0:
        self.strategy[a] /= normalizing_sum
      else:
        self.strategy[a] = 1.0 / n
      self.strategy_sum[a] += realization_weight * self.strategy[a]
    return self.strategy
  
  def get_average_strategy(self):
    n = len(self.actions)
    normalizing_sum = sum(self.strategy_sum)
    if normalizing_sum > 0:
      return self.strategy_sum / normalizing_sum
    else:
      return np.ones(n) / n

# cfr algorithm
class CfrTrainer:
  def __init__(self):
    self.node_map = {}
  
  def train(self):
    utility = 0
    for k in range(NUM_ITERATIONS):
      cards = deal_cards()
      utility += self.cfr(cards, [], 1, 1)
      if k % (NUM_ITERATIONS // 100) == 0:
        print(f'{100 * k / NUM_ITERATIONS:.2f}%')
    return utility / NUM_ITERATIONS

  def cfr(self, cards, history, p0, p1):
    # determine the node type
    ntype = node_type(history)
    
    # determine whose turn it is
    player = get_player(history)
    
    # return the payoff at a terminal node
    if ntype in ['folded', 'showdown']:
      return get_payoff(history, ntype, player, cards)  * (-1 if player == 0 else 1)
    
    # make sure we are at a player node
    assert ntype == 'player'
    
    # create and / or select information set
    key = unique_key(history, player, cards)
    if not key in self.node_map:
      self.node_map[key] = InformationSet(get_actions(history))
    info_set = self.node_map[key]
    
    # update strategy and the sum, and retrieve strategy to work with it
    strategy = info_set.update_strategy(p0 if player == 0 else p1)
    
    # define variables for recursive call and regret update
    n = len(strategy)
    utilities = np.zeros(n)
    node_utility = 0
    
    # recursive call
    for a in range(n):
      next_history = history + [info_set.actions[a]]
      if node_type(next_history) == 'chance':
        next_history = next_history + [cards[2]]
      if player == 0:
        utilities[a] = -self.cfr(cards, next_history, p0 * strategy[a], p1)
      else:
        utilities[a] = -self.cfr(cards, next_history, p0, p1 * strategy[a])
      node_utility += strategy[a] * utilities[a]
    
    # update regret
    for a in range(n):
      regret = utilities[a] - node_utility
      info_set.regret_sum[a] += (p1 if player == 0 else p0) * regret
    
    # return expected node utility
    return node_utility
  
  def get_results(self):
    spots = {}
    for key, info_set in self.node_map.items():
      if not key[2:] in spots:
        spots[key[2:]] = {
          'actions': info_set.actions,
          key[0]: info_set.get_average_strategy()
        }
      else:
        spots[key[2:]][key[0]] = info_set.get_average_strategy()
    return spots
  
# script
trainer = CfrTrainer()
ev = trainer.train()
spots = trainer.get_results()
str = f'ev: {ev}\n'
for spot in spots:
  str += spot + '\n'
  for info in spots[spot]:
    to_print = np.round(spots[spot][info], 3) if info != 'actions' else spots[spot][info]
    str += f'{info}: {to_print}\n'
filename = f'../results/N_{N}_STACK_{STACK_SIZE}_ITER_{NUM_ITERATIONS}_ID_{FILE_ID}.txt'
f = open(filename, 'w')
f.write(str)
f.close()

  
    


