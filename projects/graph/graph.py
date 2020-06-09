"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        if vertex_id not in self.vertices:
          self.vertices[vertex_id] = set()
        else:
          raise KeyError("Vertex already exists")

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 not in self.vertices:
          raise KeyError(f"Vertex not found: {v1}")
        elif v2 not in self.vertices:
          raise KeyError(f"Vertex not found: {v2}")

        self.vertices[v1].add(v2)
        self.vertices[v2].add(v1)

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        if vertex_id not in self.vertices:
          raise KeyError("Vertex not found")

        return self.vertices

    def bft(self, starting_vertex):
      if starting_vertex not in self.vertices:
        raise KeyError("Starting vertex not found")

      queue = Queue() # LIFO
      visited = set()

      queue.enqueue(starting_vertex)

      while queue.size() > 0:
        vertex = queue.dequeue()
        if vertex not in visited:
          visited.add(vertex)
          for v in self.vertices[vertex]:
            queue.enqueue(v)

      print(visited)

    def dft(self, starting_vertex):
      if starting_vertex not in self.vertices:
        raise KeyError("Starting vertex not found")
        
      stack = Stack() # FIFO
      visted = set()
      
      stack.push(starting_vertex)

      while stack.size() > 0:
        vertex = stack.pop()
        if vertex not in visted:
          visted.add(vertex)
          for v in self.vertices[vertex]:
            stack.push(v)

      print(visted)

    def dft_recursive(self, starting_vertex):
      if starting_vertex not in self.vertices:
        raise KeyError("Starting vertex not found")
      
      visited = set()
      
      def visit(vertex):
        if vertex in visited:
          return
        visited.add(vertex)
        for v in self.vertices[vertex]:
          visit(v)
      
      visit(starting_vertex)

      print(visited)

    def bfs(self, starting_vertex, destination_vertex):
      if starting_vertex not in self.vertices:
        raise KeyError("Starting vertex not found")
      if destination_vertex not in self.vertices:
        raise KeyError("Destination vertex not found")

      print(f"bfs: start={starting_vertex}, dest={destination_vertex}")

      queue = Queue()
      visited = set()

      queue.enqueue([starting_vertex])  # queue of paths (lists), copy
      
      """
      {1: {2, 7}, 2: {1, 3, 4}, 3: {2, 5, 6}, 4: {2, 6, 7}, 5: {3}, 6: {3, 4, 7}, 7: {1, 4, 6}}
      START = 1
      END = 6
      QUEUE [START]
      QUEUE = (1)

      --WHILE QUEUE NOT EMPTY--
      
      DEQUEUE INTO PATH
      PATH = [1]
      QUEUE = ()
      1 = PATH[-1]
      V = 1
      1 NOT IN VISITED
        VISITED = [1]
        V == END ?
          NO
        QUEUE [PATH, 2]
        QUEUE [PATH, 7]
        QUEUE = ([1, 2], [1, 7])
      
      DEQUEUE INTO PATH
      PATH = [1, 7]
      QUEUE = ([1, 2])
      7 = PATH[-1]
      V = 7
      7 NOT IN VISITED
        VISITED = [1, 7]
        V == END ?
          NO
        QUEUE [PATH, 1]
        QUEUE [PATH, 4]
        QUEUE [PATH, 6]
        QUEUE = ([1, 7, 1], [1, 7, 4], [1, 7, 6])
      
      DEQUEUE INTO PATH
      PATH = [1, 7, 6]
      QUEUE = ([1, 7, 1], [1, 7, 4])
      6 = PATH[-1]
      V = 6
      6 NOT IN VISITED
        VISTED = [1, 7, 6]
        V == END ?
          YES
          RETURN PATH
      """
      
      while queue.size() > 0:
        vertex_path = queue.dequeue()
        vertex = vertex_path[-1] # last item because of LIFO

        if vertex not in visited:
          visited.add(vertex)

          if vertex == destination_vertex:
            return vertex_path

          for v in self.vertices[vertex]:
            # add v to a copy of path and queue it
            vertex_path_copy = list(vertex_path)
            vertex_path_copy.append(v)
            queue.enqueue(vertex_path_copy)

      return None

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        pass  # TODO

    def dfs_recursive(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        pass  # TODO

if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    graph.dft(1)
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6))
    print(graph.dfs_recursive(1, 6))
