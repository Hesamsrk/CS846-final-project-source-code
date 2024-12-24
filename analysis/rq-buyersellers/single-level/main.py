import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

offers_path = '../IITP-VDLand/Offers_opensea.csv'
characteristics_path = '../IITP-VDLand/Characteristics.csv'
sales_path = '../IITP-VDLand/Sales_opensea.csv'

def buyers():
	offers_df = pd.read_csv(offers_path)
	freq = offers_df['from_account'].value_counts().to_dict()

	# Create a DataFrame from the dictionary
	df = pd.DataFrame(list(freq.items()), columns=['Address', 'Frequency'])

	# Generate random positions for each bubble
	np.random.seed(42)  # For reproducibility
	df['x'] = np.random.rand(len(df))
	df['y'] = np.random.rand(len(df))

	# Plot the bubble chart
	plt.figure(figsize=(10,10))
	plt.scatter(df['x'], df['y'], s=df['Frequency']*0.1, alpha=0.5, edgecolors="w", linewidth=1, color='skyblue')
	plt.axis('off')
	plt.tight_layout()

	plt.savefig('buyers.png', format='png')

	# plt.show()

def sellers():
	sales_df = pd.read_csv(sales_path)
	freq = sales_df['to_account'].value_counts().to_dict()

	# Create a DataFrame from the dictionary
	df = pd.DataFrame(list(freq.items()), columns=['Address', 'Frequency'])

	# Generate random positions for each bubble
	np.random.seed(42)  # For reproducibility
	df['x'] = np.random.rand(len(df))
	df['y'] = np.random.rand(len(df))

	# Plot the bubble chart
	plt.figure(figsize=(10,10))
	plt.scatter(df['x'], df['y'], s=df['Frequency']*15, alpha=0.5, edgecolors="w", linewidth=1, color='lightgreen')
	plt.axis('off')
	plt.tight_layout()

	plt.savefig('sellers.png', format='png')
	
	# plt.show()



def buyer_seller_graph(txn_count = None): # txn_count = number of transactions to include, default=everything (will take few mins to output graph)
	sales_df = pd.read_csv(sales_path)
	sales_df.dropna(subset=['from_account', 'to_account'], inplace=True)
	if txn_count: 
		sales_df = sales_df.head(txn_count) # cut the remaining transactions

	# Aggregate transaction counts for buyers and sellers
	buyer_counts = sales_df['from_account'].value_counts().to_dict()
	seller_counts = sales_df['to_account'].value_counts().to_dict()

	G = nx.Graph()

	# Add nodes for buyers and sellers with their transaction counts as a size attribute
	for buyer, count in buyer_counts.items():
		G.add_node(buyer, type='buyer', size=count)
	for seller, count in seller_counts.items():
		G.add_node(seller, type='seller', size=count)

	# Add edges between buyers and sellers
	for _, row in sales_df.iterrows():
		G.add_edge(row['from_account'], row['to_account'])

	# Set node sizes based on transaction frequency
	node_sizes = [G.nodes[node]['size'] * 20 for node in G.nodes()]  # Scale the size for better visualization

	# Set node colors
	node_colors = ['skyblue' if G.nodes[node]['type'] == 'buyer' else 'lightgreen' for node in G.nodes()]

	# Set dist between each node
	node_dist = 0.2 if not txn_count or txn_count <= 2000 else 0.3 # distance between each node for graphing

	# Draw the network graph
	plt.figure(figsize=(10,10))
	pos = nx.spring_layout(G,k=node_dist)  # Positioning the nodes
	nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.6)
	nx.draw_networkx_edges(G, pos, alpha=0.3, width=0.3)

	plt.axis('off')
	plt.tight_layout()
	name = str(txn_count) if txn_count else 'default'
	output_path = 'buyer_seller_' + name + '.png'
	plt.savefig(output_path, format='png')
	
	# plt.show()


if __name__ == '__main__':
	test()
	# buyers()
	# sellers()
	# buyer_seller_graph(1000)
	# buyer_seller_graph(2000)
	# buyer_seller_graph(4000)
	# buyer_seller_graph() # every transactions

