"""  BFS to find shortest path
How to Solve Graph Problems

1. Translate the problem into graph terminology
2. Build the graph
3. Traverse / Search

"""

word_set = set()

with open("words.txt", "r") as f:
  for line in f:
    line = line.strip()
    word_set.add(line.lower())

import string

letters = list(string.ascii_lowercase)

def get_neighbors(word):
  neighbors = []

  word_letters = list(word)

  # for each letter in word
  for i in range(len(word_letters)):
    # replace with all letters
    for letter in letters:
      #copy list
      t = list(word_letters)
      t[i] = letter
      w = "".join(t)
      if w in word_set and w not in word:
        neighbors.append(w)
    # see if we form a word


  return neighbors

print(get_neighbors("food"))


# BFS (queue of lists of paths)
import queue

def find_word_connections(begin_word, end_word):
  visited = set()

  q = queue.Queue()

  q.put([begin_word])

  while not q.empty():
    path = q.get()

    cur_word = path[-1] # last element

    if cur_word not in visited:
      visited.add(cur_word)

      if cur_word == end_word:
        return path

      neighbor_words = get_neighbors(cur_word)
      
      for neighbor_word in neighbor_words:
        path_copy = list(path)
        path_copy.append(neighbor_word)
        q.put(path_copy)

  return None

print(find_word_connections("food", "carp"))