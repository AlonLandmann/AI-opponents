import numpy as np
from collections import defaultdict

# Kuhn Poker game parameters
CARDS = ['J', 'Q', 'K']
NUM_ACTIONS = 2  # 0 = pass, 1 = bet
NUM_ITERATIONS = 10000

# Utilities
def card_rank(card):
  return CARDS.index(card)

def deal_cards():
  return np.random.choice(CARDS, 2, replace=False)

def is_terminal(history):
  return history in ['pp', 'pbp', 'pbb', 'bp', 'bb']

def get_winner(history, cards):
  if history in ['bb', 'pbb']:
    return 2 if card_rank(cards[1]) > card_rank(cards[0]) else -2
  elif history == 'pbp':
    return 1
  elif history == 'bp':
    return -1
  elif history == 'pp':
    return 1 if card_rank(cards[1]) > card_rank(cards[0]) else -1
  return 0

# Information Set Class
class InformationSet:
  def __init__(self):
    self.regret_sum = np.zeros(NUM_ACTIONS)
    self.strategy = np.ones(NUM_ACTIONS) / NUM_ACTIONS
    self.strategy_sum = np.zeros(NUM_ACTIONS)
  
  def get_strategy(self, realization_weight):
    normalizing_sum = 0
    for a in range(NUM_ACTIONS):
      self.strategy[a] = max(self.regret_sum[a], 0)
      normalizing_sum += self.strategy[a]
    for a in range(NUM_ACTIONS):
      if normalizing_sum > 0:
        self.strategy[a] /= normalizing_sum
      else:
        self.strategy[a] = 1.0 / NUM_ACTIONS
      self.strategy_sum[a] += realization_weight * self.strategy[a]
    return self.strategy
  
  def get_average_strategy(self):
    normalizing_sum = sum(self.strategy_sum)
    if normalizing_sum > 0:
      return self.strategy_sum / normalizing_sum
    else:
      return np.ones(NUM_ACTIONS) / NUM_ACTIONS

# CFR Algorithm
class KuhnTrainer:
  def __init__(self):
    self.node_map = defaultdict(InformationSet)
    
  def train(self):
    utility = 0
    for _ in range(NUM_ITERATIONS):
      cards = deal_cards()
      utility += self.cfr(cards, '', 1, 1)
    return utility
    
  def cfr(self, cards, history, p0, p1):
    plays = len(history)
    player = plays % 2
      
    if is_terminal(history):
      return get_winner(history, cards) * (-1 if player == 0 else 1)
      
    info_set = self.node_map[cards[player] + history]
    strategy = info_set.get_strategy(p0 if player == 0 else p1)
    util = np.zeros(NUM_ACTIONS)
    node_util = 0
      
    for a in range(NUM_ACTIONS):
      next_history = history + ('p' if a == 0 else 'b')
      if player == 0:
        util[a] = -self.cfr(cards, next_history, p0 * strategy[a], p1)
      else:
        util[a] = -self.cfr(cards, next_history, p0, p1 * strategy[a])
      node_util += strategy[a] * util[a]
      
    for a in range(NUM_ACTIONS):
      regret = util[a] - node_util
      info_set.regret_sum[a] += (p1 if player == 0 else p0) * regret
      
    return node_util
    
  def get_strategy(self):
    strategies = {}
    for key, info_set in self.node_map.items():
      strategies[key] = info_set.get_average_strategy()
    return strategies

# Running the CFR Trainer
trainer = KuhnTrainer()
trainer.train()
strategies = trainer.get_strategy()

# Display the strategies
for key, strategy in strategies.items():
  print(f'{key}: {np.round(strategy, 3)}')
