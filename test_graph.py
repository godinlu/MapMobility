from src.train_graph import TrainGraph
import pandas as pd

stop_times = pd.read_csv('data/stop_times.txt')
stop_times = stop_times[stop_times['stop_id'].str.contains('Train')]
train_graph = TrainGraph(stop_times)

print(train_graph.graph)


gare_1 = 'StopPoint:OCETrain TER-87726802'
gare_2 = 'StopPoint:OCETrain TER-87747006'


print(train_graph.get_time_between(gare_1, gare_2)/60)

print(train_graph.get_dijkstra(gare_1))

#train_graph.show()