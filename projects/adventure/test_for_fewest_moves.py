from explore_graph_3 import explore_graph, build_graph
from ast import literal_eval

map_file = "projects/adventure/maps/main_maze.txt"
room_direction_graph = literal_eval(open(map_file, "r").read())

room_graph = build_graph(room_direction_graph)
room_list = room_graph.vertices.keys()

lowest_num_moves = 0
lowest_num_moves_room = None

for room_id in room_list:
  print(f"Exploring room {room_id}....")
  
  move_list = explore_graph(room_direction_graph, room_id)
  num_moves = len(move_list)

  if num_moves < lowest_num_moves or lowest_num_moves == 0:
    lowest_num_moves = num_moves
    lowest_num_moves_room = room_id

  print(f"Room {room_id} will take {num_moves} moves.")
  print(f"Room {lowest_num_moves_room} is fastest with {lowest_num_moves} moves.")

# Room 331 is fastest with 978 moves.