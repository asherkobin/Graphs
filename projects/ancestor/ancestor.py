def find_longest_path(paths):
  longest_path = []
  
  for path in paths:
    if len(path) > len(longest_path):
      longest_path = path
    elif len(path) == len(longest_path):
      if path[-1] < longest_path[-1]: # resolve conflict via lowest ancestor
        longest_path = path
  
  return longest_path

def get_all_paths(person, ancestry_table):
  all_paths = []
  stack = [[person]]

  # good ol' path creation
  
  while len(stack) >  0:
    path = stack.pop()
    parent = path[-1]
    if parent in ancestry_table:
      for child in ancestry_table[parent]:
        new_path = path.copy()
        new_path.append(child)
        stack.append(new_path)
    else:
      all_paths.append(path)

  return all_paths

def create_ancestry_table(ancestors):
  ancestry_table = {}
  
  for relationship in ancestors:
    child, parent = relationship
    if parent in ancestry_table:
      ancestry_table[parent].append(child)
    else:
      ancestry_table[parent] = [child]

  return ancestry_table

def earliest_ancestor(ancestors, person):

  # build a table of child to parent(s) relations

  ancestry_table = create_ancestry_table(ancestors)
    
  if person not in ancestry_table: # person has no parents
    return -1
  
  # generate all possible paths for the person so we can later compare lenghts
  
  all_paths = get_all_paths(person, ancestry_table)

  # find the longest path
  
  longest_path = find_longest_path(all_paths)

  return longest_path[-1] # only care about the earliest person
