"""
Connected Components
--------------------
Parts of the graph that are connected, but disjoint from other parts of the
graph.

To count connected componets:
    For each node:
        if node not visited:
            traverse from that node
            increment counter

"""



def get_neighbors(row, col, matrix):
  neighbors = []
  
  if row > 0 and matrix[row - 1][col] == 1:
    neighbors.append((row - 1, col))
  if row < len(matrix) - 1 and matrix[row + 1][col] == 1:
    neighbors.append((row + 1, col))
  if col > 0 and matrix[row][col - 1] == 1:
    neighbors.append((row, col - 1))
  if col < len(matrix[0]) - 1 and matrix[row][col + 1] == 1:
    neighbors.append((row, col + 1))

  return neighbors

def dft(row, col, matrix, visited):
  s = []
  s.append((row, col))

  while len(s) > 0:
    row, col = s.pop()

    if visited[row][col] == False:
       visited[row][col] = True

       for neighbor in get_neighbors(row, col, matrix):
         s.append(neighbor)


matrix  = [[0, 1, 0, 1, 0],
           [1, 1, 0, 1, 1],
           [0, 0, 1, 0, 0],
           [0, 0, 1, 0, 0],
           [1, 1, 0, 0, 0]]

island_count = 0

visited = []

for _ in range(len(matrix)):
  visited.append([False] * len(matrix[0]))

for row in range(len(matrix)):
  for col in range(len(matrix[row])):
    if visited[row][col] == False:
      if matrix[row][col] == 1:
        dft(row, col, matrix, visited)

        island_count += 1

print(island_count)

import random

class Graph:

  def populate_graph(self, num_users, avg_friendships):
    # Reset graph
    self.last_id = 0
    self.users = {}
    self.friendships = {}

    # Add users
    for i in range(0, num_users):
      self.add_user(f"User {i}")

      # Create Frienships
      # Generate all possible friendship combinations
      possible_friendships = []

      # Avoid duplicates by ensuring the first number is smaller than the second
      for user_id in self.users:
        for friend_id in range(user_id + 1, self.last_id + 1):
            possible_friendships.append((user_id, friend_id))

      # Shuffle the possible friendships
      random.shuffle(possible_friendships)

      # Create friendships for the first X pairs of the list
      # X is determined by the formula: num_users * avg_friendships // 2
      # Need to divide by 2 since each add_friendship() creates 2 friendships
      for i in range(num_users * avg_friendships // 2):
        friendship = possible_friendships[i]
        self.add_friendship(friendship[0], friendship[1])

  def add_user(self, user_name):
    pass

  def add_friendship(self, user_name):
    pass