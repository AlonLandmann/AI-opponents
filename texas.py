import numpy as np

# training parameters
NUM_ITERATIONS = 1000000

# game parameters
ALL_CARDS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
CARDS = ALL_CARDS[:8]
TREE = {
  'c': {
    'c': ('showdown', 1),
    'b': {
      'f': ('P2', 1),
      'c': ('showdown', 2)
    }
  },
  'b': {
    'f': ('P1', -1),
    'c': ('showdown', 2)
  }
}

# utilities
def card_value(card):
  return len(CARDS) - CARDS.index(card)

def showdown_multiplier(cards):
  return -1 if card_value(cards[0]) > card_value(cards[1]) else 1

def deal_cards():
  return np.random.choice(CARDS, 2, replace = False)

def is_terminal(history):
  return history in ['cc', 'cbf', 'cbc', 'bf', 'bc']

def payoff(history, cards):
  if history == 'cc':
    return 1 * showdown_multiplier(cards)
  elif history in ['bc', 'cbc']:
    return 2 * showdown_multiplier(cards)
  elif history == 'cbf':
    return 1
  elif history == 'bf':
    return -1
  return 0

def determine_actions(history):
  if history in ['', 'c']:
    return ['c', 'b']
  elif history in ['cb', 'b']:
    return ['f', 'c']
  return None  

# information sets
class InformationSet:
  def __init__(self, actions):
    n = len(actions)
    self.actions = actions
    self.regret_sum = np.zeros(n)
    self.strategy = np.ones(n) / n
    self.strategy_sum = np.zeros(n)
    
  def get_strategy(self, realization_weight):
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
    for _ in range(NUM_ITERATIONS):
      cards = deal_cards()
      utility += self.cfr(cards, '', 1, 1)
    return utility / NUM_ITERATIONS
  
  def get_strategy(self):
    strategies = {}
    for key, info_set in self.node_map.items():
      strategies[key] = info_set.get_average_strategy()
    return strategies
  
  def cfr(self, cards, history, p0, p1):
    # determine whose turn it is
    player = len(history) % 2
    
    # return the perspective payoff at a terminal node
    if is_terminal(history):
      return payoff(history, cards) * (-1 if player == 0 else 1)
    
    # create and / or select information set
    key = cards[player] + history
    if not key in self.node_map:
      self.node_map[key] = InformationSet(determine_actions(history))
    info_set = self.node_map[key]
    
    # ...
    strategy = info_set.get_strategy(p0 if player == 0 else p1)
    n = len(strategy)
    util = np.zeros(n)
    node_util = 0
    
    for a in range(n):
      next_history = history + info_set.actions[a]
      if player == 0:
        util[a] = -self.cfr(cards, next_history, p0 * strategy[a], p1)
      else:
        util[a] = -self.cfr(cards, next_history, p0, p1 * strategy[a])
      node_util += strategy[a] * util[a]
    
    for a in range(n):
      regret = util[a] - node_util
      info_set.regret_sum[a] += (p1 if player == 0 else p0) * regret
      
    return node_util
    
# execution
trainer = CfrTrainer()
ev = trainer.train()
strategies = trainer.get_strategy()

# results
print(ev)
for card in CARDS:
  p1bet = strategies[card][1]
  p1call = strategies[card + 'cb'][1]
  p2bet = strategies[card + 'c'][1]
  p2call = strategies[card + 'b'][1]
  print(f'{card}: p1 bet: {p1bet:.3f} p1 call: {p1call:.3f} | p2 bet: {p2bet:.3f} p2 call: {p2call:.3f}')