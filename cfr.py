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

tree1 = {
  'path': [],
  'type': 'chance',
  'cont': [
    {
      'path': ['K'],
      'type': 'player',
      'cont': [
        {
          'path': ['K', 'b'],
          'type': 'opponent',
          'cont': [
            {
              'path': ['K', 'b', 'c'],
              'type': 'terminal',
              'payoff': 'showdown'
            },
            {
              'path': ['K', 'b', 'f'],
              'type': 'terminal',
              'payoff': 1
            }
          ]
        },
        {
          'path': ['K', 'c'],
          'type': 'opponent',
          'cont': [
            {
              'path': ['K', 'c', 'b'],
              'type': 'player',
              'children': [
                {
                  'path': ['K', 'c', 'b', 'f'],
                  'type': 'terminal',
                  'payoff': -1
                },
                {
                  'path': ['K', 'c', 'b', 'c'],
                  'type': 'terminal',
                  'payoff': 'showdown'
                }
              ]
            },
            {
              'path': ['K', 'c', 'c'],
              'type': 'terminal',
              'payoff': 'showdown'
            }
          ]
        }
      ]
    },
    {
      'path': ['Q'],
      'type': 'player',
      'cont': [
        {
          'path': ['Q', 'b'],
          'type': 'opponent',
          'cont': [
            {
              'path': ['Q', 'b', 'c'],
              'type': 'terminal',
              'payoff': 'showdown'
            },
            {
              'path': ['Q', 'b', 'f'],
              'type': 'terminal',
              'payoff': 1
            }
          ]
        },
        {
          'path': ['Q', 'c'],
          'type': 'opponent',
          'cont': [
            {
              'path': ['Q', 'c', 'b'],
              'type': 'player',
              'children': [
                {
                  'path': ['Q', 'c', 'b', 'f'],
                  'type': 'terminal',
                  'payoff': -1
                },
                {
                  'path': ['Q', 'c', 'b', 'c'],
                  'type': 'terminal',
                  'payoff': 'showdown'
                }
              ]
            },
            {
              'path': ['Q', 'c', 'c'],
              'type': 'terminal',
              'payoff': 'showdown'
            }
          ]
        }
      ]
    },
    {
      'path': ['J'],
      'type': 'player',
      'cont': [
        {
          'path': ['J', 'b'],
          'type': 'opponent',
          'cont': [
            {
              'path': ['J', 'b', 'c'],
              'type': 'terminal',
              'payoff': 'showdown'
            },
            {
              'path': ['J', 'b', 'f'],
              'type': 'terminal',
              'payoff': 1
            }
          ]
        },
        {
          'path': ['J', 'c'],
          'type': 'opponent',
          'cont': [
            {
              'path': ['J', 'c', 'b'],
              'type': 'player',
              'children': [
                {
                  'path': ['J', 'c', 'b', 'f'],
                  'type': 'terminal',
                  'payoff': -1
                },
                {
                  'path': ['J', 'c', 'b', 'c'],
                  'type': 'terminal',
                  'payoff': 'showdown'
                }
              ]
            },
            {
              'path': ['J', 'c', 'c'],
              'type': 'terminal',
              'payoff': 'showdown'
            }
          ]
        }
      ]
    }
  ]
}
tree2 = {
  'path': [],
  'type': 'chance',
  'cont': [
    {
      'path': ['K'],
      'type': 'opponent',
      'cont': [
        {
          'path': ['K', 'b'],
          'type': 'player',
          'cont': [
            {
              'path': ['K', 'b', 'c'],
              'type': 'terminal',
              'payoff': 'showdown'
            },
            {
              'path': ['K', 'b', 'f'],
              'type': 'terminal',
              'payoff': -1
            }
          ]
        },
        {
          'path': ['K', 'c'],
          'type': 'player',
          'cont': [
            {
              'path': ['K', 'c', 'b'],
              'type': 'opponent',
              'children': [
                {
                  'path': ['K', 'c', 'b', 'f'],
                  'type': 'terminal',
                  'payoff': 1
                },
                {
                  'path': ['K', 'c', 'b', 'c'],
                  'type': 'terminal',
                  'payoff': 'showdown'
                }
              ]
            },
            {
              'path': ['K', 'c', 'c'],
              'type': 'terminal',
              'payoff': 'showdown'
            }
          ]
        }
      ]
    },
    {
      'path': ['Q'],
      'type': 'opponent',
      'cont': [
        {
          'path': ['Q', 'b'],
          'type': 'player',
          'cont': [
            {
              'path': ['Q', 'b', 'c'],
              'type': 'terminal',
              'payoff': 'showdown'
            },
            {
              'path': ['Q', 'b', 'f'],
              'type': 'terminal',
              'payoff': -1
            }
          ]
        },
        {
          'path': ['Q', 'c'],
          'type': 'player',
          'cont': [
            {
              'path': ['Q', 'c', 'b'],
              'type': 'opponent',
              'children': [
                {
                  'path': ['Q', 'c', 'b', 'f'],
                  'type': 'terminal',
                  'payoff': 1
                },
                {
                  'path': ['Q', 'c', 'b', 'c'],
                  'type': 'terminal',
                  'payoff': 'showdown'
                }
              ]
            },
            {
              'path': ['Q', 'c', 'c'],
              'type': 'terminal',
              'payoff': 'showdown'
            }
          ]
        }
      ]
    },
    {
      'path': ['J'],
      'type': 'opponent',
      'cont': [
        {
          'path': ['J', 'b'],
          'type': 'player',
          'cont': [
            {
              'path': ['J', 'b', 'c'],
              'type': 'terminal',
              'payoff': 'showdown'
            },
            {
              'path': ['J', 'b', 'f'],
              'type': 'terminal',
              'payoff': -1
            }
          ]
        },
        {
          'path': ['J', 'c'],
          'type': 'player',
          'cont': [
            {
              'path': ['J', 'c', 'b'],
              'type': 'opponent',
              'children': [
                {
                  'path': ['J', 'c', 'b', 'f'],
                  'type': 'terminal',
                  'payoff': 1
                },
                {
                  'path': ['J', 'c', 'b', 'c'],
                  'type': 'terminal',
                  'payoff': 'showdown'
                }
              ]
            },
            {
              'path': ['J', 'c', 'c'],
              'type': 'terminal',
              'payoff': 'showdown'
            }
          ]
        }
      ]
    }   
  ]
}


def walk_trees(node1, node2, path, prob1, prob2):
  if node1['type'] == 'terminal':
    return 
  if node1['type'] == 'player' and node2['type'] == 'opponent':
    # compute something
    for action1 in node1['cont']:
      # find corresponding child nodes
      child1 = action1
      child2 = None
      last_action = child1['path'][-1]
      for action2 in node2['cont']:
        if last_action == action2['path'][-1]:
          child2 = action2
      
      # dive deeper
      (u_sigma_Ir1_a, u_sigma_r2_a) = walk_trees(child1, child2, path, )

