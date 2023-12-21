from src.train_graph import TrainGraph
import pandas as pd

stop_times = pd.read_csv('data/stop_times.txt')
stop_times = stop_times[stop_times['stop_id'].str.contains('Train')]
train_graph = TrainGraph(stop_times)

print(train_graph.graph)
#train_graph.show()