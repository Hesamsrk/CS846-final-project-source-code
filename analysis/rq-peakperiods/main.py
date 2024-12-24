import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

offers_path = '../IITP-VDLand/Offers_opensea.csv'
characteristics_path = '../IITP-VDLand/Characteristics.csv'
sales_path = '../IITP-VDLand/Sales_opensea.csv'

def biddings():
	offers_df = pd.read_csv(offers_path)
	timestamps = pd.to_datetime(offers_df['event_timestamp'], format='%Y-%m-%d %H:%M:%S.%f').dt.hour
	hours_freq = timestamps.value_counts().sort_index()

	hours = list(range(24))
	plt.figure(figsize=(12, 6))
	plt.plot(hours, hours_freq, marker='o', linestyle='--', color='orange')
	plt.xlabel('Hour of the Day')
	plt.ylabel('Number of Biddings')
	plt.title('Number of Biddings per Hour')
	plt.xticks(hours)
	plt.grid(True)
	plt.tight_layout()

	plt.savefig('peak_biddings.png', format='png')
	# plt.show()

def sales():
	sales_df = pd.read_csv(sales_path)
	timestamps = pd.to_datetime(sales_df['event_timestamp'], format='%Y-%m-%d %H:%M:%S').dt.hour
	hours_freq = timestamps.value_counts().sort_index()

	hours = list(range(24))
	plt.figure(figsize=(12, 6))
	plt.plot(hours, hours_freq, marker='o', linestyle='--', color='green')
	plt.xlabel('Hour of the Day')
	plt.ylabel('Number of Transactions')
	plt.title('Number of Transactions per Hour')
	plt.xticks(hours)
	plt.grid(True)
	plt.tight_layout()

	plt.savefig('peak_sales.png', format='png')
	# plt.show()


def ratio_bidding_sales():
	offers_df = pd.read_csv(offers_path)
	timestamps = pd.to_datetime(offers_df['event_timestamp'], format='%Y-%m-%d %H:%M:%S.%f').dt.hour
	biddings_freq = timestamps.value_counts().sort_index()

	sales_df = pd.read_csv(sales_path)
	timestamps = pd.to_datetime(sales_df['event_timestamp'], format='%Y-%m-%d %H:%M:%S').dt.hour
	sales_freq = timestamps.value_counts().sort_index()

	ratio_freq = [round(biddings_freq[h] / sales_freq[h],2) for h in range(24)]

	hours = list(range(24))
	plt.figure(figsize=(12, 6))
	plt.plot(hours, ratio_freq, marker='o', linestyle='--', color='blue')
	plt.xlabel('Hour of the Day')
	plt.ylabel('Ratio of Bids to Sales')
	plt.title('Bid/Sales Ratio per Hour')
	plt.xticks(hours)
	plt.grid(True)
	plt.tight_layout()

	plt.savefig('ratio_bid_sales.png', format='png')
	# plt.show()

if __name__ == '__main__':
	biddings()
	sales()
	ratio_bidding_sales()

