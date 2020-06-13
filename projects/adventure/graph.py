class Graph:
  def __init__(self):
      self.vertices = {}
      self.frozen_count = 0

  def add_vertex(self, vertex_id):
    if vertex_id not in self.vertices:
      self.vertices[vertex_id] = set()
    else:
      raise KeyError("Vertex already exists")

  def has_vertex(self, vertex_id):
    return vertex_id in self.vertices

  def add_edge(self, v1, v2):
    if v1 not in self.vertices:
      raise KeyError(f"Vertex not found: {v1}")

    if v2 not in self.vertices:
      raise KeyError(f"Vertex not found: {v2}")

    if v2 in self.vertices[v1]:
      raise KeyError("Edge already exists")

    self.vertices[v1].add(v2)

  def get_neighbors(self, vertex_id):
    if vertex_id not in self.vertices:
      raise KeyError("Vertex not found")

    if self.frozen_count > 0: # corruption detection on
      item_count = 0
      for v in self.vertices:
        for _ in self.vertices[v]:
          item_count += 1
      if item_count != self.frozen_count:
        raise ValueError("Graph as been COMPRIMISED")

    return self.vertices[vertex_id].copy() # SUPER IMPORTANT

  def freeze(self): # enables corruption detection
    self.frozen_count = 0

    for v in self.vertices:
      for _ in self.vertices[v]:
        self.frozen_count += 1


  def __len__(self):
    return len(self.vertices)