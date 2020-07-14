import random      

class User:
  def __init__(self, name):
      self.name = name

class SocialGraph:
  def __init__(self):
    self.last_id = 0
    self.users = {}
    self.friendships = {}

  def add_friendship(self, user_id, friend_id):
    """
    Creates a bi-directional friendship
    """
    if user_id == friend_id:
      print("WARNING: You cannot be friends with yourself")
    elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
      print("WARNING: Friendship already exists")
    else:
      self.friendships[user_id].add(friend_id)
      self.friendships[friend_id].add(user_id)

  def add_user(self, name):
    """
    Create a new user with a sequential integer ID
    """
    self.last_id += 1  # automatically increment the ID to assign the new user
    self.users[self.last_id] = User(name)
    self.friendships[self.last_id] = set()

  def populate_graph_lecture(self, num_users, avg_friendships):
    self.last_id = 0
    self.users = {}
    self.friendships = {}

    # Add users
    for i in range(0, num_users):
      self.add_user(f"User {i}")

    target_friendships = (num_users * avg_friendships) // 2
    total_friendships = 0
    collisions = 0

    while total_friendships < target_friendships:
      user_id = random.randint(1, self.last_id)
      friend_id = random.randint(1, self.last_id)

      if self.add_friendship(user_id, friend_id):
        total_friendships += 1
      else:
        collisions += 1
      

  def populate_graph(self, num_users, avg_friendships):
    """
    Takes a number of users and an average number of friendships
    as arguments

    Creates that number of users and a randomly distributed friendships
    between those users.

    The number of users must be greater than the average number of friendships.
    """
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

  def get_all_social_paths_lecture(self, user_id):
    visited = {}
    q = []

    q.append([user_id])

    while len(q) > 0:
      path = q.pop(0)

      v = path[-1]

      if v not in visited:
        visited[v] = path

        for n in self.friendships[v]:
          q.append([*path, n])

    return visited

  
  def get_all_social_paths(self, user_id):
    """
    Takes a user's user_id as an argument

    Returns a dictionary containing every user in that user's
    extended network with the shortest friendship path between them.

    The key is the friend's ID and the value is the path.

    self.users[id] = User(name)
    
    self.friendships[u1] = [u2, u3, u4]
    self.friendships[u2] = [u4, u1]
    ...
    
    """

    #
    # Do a BFS search for every Person -- SRC: Person, DST: User
    #
    # BFS will give shortest path
    #

    visited = {}
    results = {}

    for person_id in self.users:
      visited[person_id] = []
      queue = []
      queue.append([person_id])
      results_len = len(results)
      
      while len(queue) > 0:
        path = queue.pop(0)
        sub_person_id = path[-1]

        if sub_person_id not in visited[person_id]:
          visited[person_id].append(sub_person_id)

          if sub_person_id == user_id:
            path.reverse()
            results[person_id] = path # connection found
            break # go to next person

          for friend_id in self.friendships[sub_person_id]:
            path_copy = path.copy()
            path_copy.append(friend_id)
            queue.append(path_copy)
      
      if len(results) == results_len: # if nothing was added then no match was found
        print("Sorry No Connection: " + str(person_id))

    return results


if __name__ == '__main__':
    print("Populating Graph...")
    sg = SocialGraph()
    sg.populate_graph(15, 5)
    print(sg.friendships)
    print("Searching Graph...")
    connections = sg.get_all_social_paths_lecture(5)
    print(connections)

    users_in_ext_network = len(connections) - 1
    total_users = len(sg.users)

    print(f"Perc: {users_in_ext_network / total_users * 100:.2f} ")