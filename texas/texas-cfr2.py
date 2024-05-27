import numpy as np

# training parameters
NUM_ITERATIONS = 10000000

# game parameters
N = 3
CARDS = ['K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'][:N]
TREE = {
  'c': {
    'c': ('showdown', 1),
    '1': {
      'f': ('fixed', 1),
      'c': ('showdown', 2),
      '1': {
        'f': ('fixed', -2),
        'c': ('showdown', 3)
      }
    },
    '2': {
      'f': ('fixed', 1),
      'c': ('showdown', 3)
    }
  },
  '1': {
    'f': ('fixed', -1),
    'c': ('showdown', 2),
    '1': {
      'f': ('fixed', 2),
      'c': ('showdown', 3)
    }
  },
  '2': {
    'f': ('fixed', -1),
    'c': ('showdown', 3)
  }
}

# utilities
def card_value(card):
  return len(CARDS) - CARDS.index(card)

def showdown_multiplier(cards):
  return -1 if card_value(cards[0]) > card_value(cards[1]) else 1

def deal_cards():
  return np.random.choice(CARDS, 2, replace = False)

# some precomputation
terminal_histories = {}
non_terminal_histories = {}

def check_tree(node, h):
  if isinstance(node, tuple):
    terminal_histories[h] = node
  else:
    non_terminal_histories[h] = list(node.keys())
    for a in node:
      check_tree(node[a], h + a)

check_tree(TREE, '')

def is_terminal(history):
  return history in terminal_histories

def payoff(history, cards):
  payoff_info = terminal_histories[history]
  if payoff_info[0] == 'fixed':
    return payoff_info[1]
  return payoff_info[1] * showdown_multiplier(cards)

def determine_actions(history):
  return non_terminal_histories[history]

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
      utility += self.cfr(cards, '', 1, 1)
      if k % (NUM_ITERATIONS // 100) == 0:
        print(f'{100 * k / NUM_ITERATIONS:.2f}%')
    return utility / NUM_ITERATIONS
  
  def get_strategy(self):
    strategies = {}
    for key, info_set in self.node_map.items():
      strategies[key] = {
        'actions': info_set.actions,
        'strategy': info_set.get_average_strategy()
      }
    return strategies
  
  def cfr(self, cards, history, p0, p1):
    # determine whose turn it is
    player = len(history) % 2
    
    # return the payoff at a terminal node
    if is_terminal(history):
      return payoff(history, cards) * (-1 if player == 0 else 1)

    # create and / or select information set
    key = cards[player] + history
    if not key in self.node_map:
      self.node_map[key] = InformationSet(determine_actions(history))
    info_set = self.node_map[key]
    
    # update strategy and the sum, and retrieve strategy to work with it
    strategy = info_set.update_strategy(p0 if player == 0 else p1)
    
    # define variables for recursive call and regret update
    n = len(strategy)
    utilities = np.zeros(n)
    node_utility = 0
    
    # recursive call
    for a in range(n):
      next_history = history + info_set.actions[a]
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

# execution
trainer = CfrTrainer()
ev = trainer.train()
strategies = trainer.get_strategy()
    
# results
print(ev)

for history in non_terminal_histories:
  for card in CARDS:
    key = card + history
    actions = strategies[key]['actions']
    distr = strategies[key]['strategy']
    print(f'i: {key}, a: {actions}, s: {np.round(distr, 3)}')
    