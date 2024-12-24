import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

offers_path = '../IITP-VDLand/Offers_opensea.csv'
characteristics_path = '../IITP-VDLand/Characteristics.csv'
sales_path = '../IITP-VDLand/Sales_opensea.csv'

class ProfitDays: 

	def __init__(self):
		self.read_eth_prices()
		self.compute_distribution()
		self.statistics()

	def read_eth_prices(self):
		# Source: https://finance.yahoo.com/quote/ETH-USD/history/
		# where Yahoo sourced the data from CoinMarketCap
		eth_usd_df = pd.read_csv('ETH-USD.csv')
		self.eth_usd_map = eth_usd_df.set_index('Date')['Close'].to_dict()

	def compute_distribution(self):
		sales_df = pd.read_csv(sales_path)
		sales_df['event_timestamp'] = pd.to_datetime(sales_df['event_timestamp'], format='%Y-%m-%d %H:%M:%S') # cleanup to datetime format

		# Convert and get the accurate ETH-USD pricing
		sales_df.loc[sales_df['payment_token_symbol'] == 'ETH', 'usd_price'] = sales_df['event_timestamp'].dt.strftime('%Y-%m-%d') \
																				.map(self.eth_usd_map).round(2)

		sellers, buyers = set(sales_df['seller_address']), set(sales_df['winner_address'])
		total_users = sellers | buyers
		overlaps = sellers & buyers

		print(f'Total number of buyers = {len(buyers)}')
		print(f'Total number of sellers = {len(sellers)}')
		print(f'Total number of users (both buyers and sellers) = {len(total_users)}')
		print(f'Total number of arbitrage users = {len(overlaps)}')
		print(f'Total percentage of arbitrage users = {round(len(overlaps) / len(total_users) * 100, 2)}%')

		# Compute the profit for each transaction of arbitrage
		profits_days = [] # array of (profit from the txn, amount of days waited to be transacted)
		for user_address in overlaps: 
			seller_txns = sales_df[sales_df['seller_address'] == user_address]
			buyer_txns = sales_df[sales_df['winner_address'] == user_address]

			# Merge the rows to get the rows where the buyer is the seller
			merged_df = pd.merge(seller_txns, buyer_txns, on='token_id', suffixes=('_seller', '_buyer'))

			# Filter valid rows where you can only sell after you buy (cannot sell, then buy because haven't got the item)
			merged_df = merged_df[merged_df['event_timestamp_seller'] > merged_df['event_timestamp_buyer']]

			# Get the number of days difference between selling and buying, modify the "60/60/24" to change to min_diff/hour_diff/day_diff
			merged_df['days_diff'] = (merged_df['event_timestamp_seller'] - merged_df['event_timestamp_buyer']).dt.total_seconds()/60/60/24

			# Get the profits
			for _, row in merged_df.iterrows():
				sell_price = row['sale_price_seller'] / (10 ** row['decimals_seller']) * row['usd_price_seller'] # usd sell price
				buy_price = row['sale_price_buyer'] / (10 ** row['decimals_buyer']) * row['usd_price_buyer'] # usd buy price
				days_diff = row['days_diff']
				profit_price = sell_price - buy_price

				profits_days.append((profit_price, days_diff))

		self.profits_days = profits_days

	def statistics(self):
		# Compute statitics for profits and days
		profits = [pd[0] for pd in self.profits_days]
		days = [pd[1] for pd in self.profits_days]

		mean_profit = np.mean(profits)
		median_profit = np.median(profits)
		min_profit = np.min(profits)
		max_profit = np.max(profits)

		mean_day = np.mean(days)
		median_day = np.median(days)
		min_day = np.min(days)
		max_day = np.max(days)

		print(f'Profit: Mean = {mean_profit}, Median = {median_profit}, Min = {min_profit}, Max = {max_profit}')
		print(f'Days Arbitrage: Mean = {mean_day}, Median = {median_day}, Min = {min_day}, Max = {max_day}')

		self.profits_stat = [mean_profit, median_profit, min_profit, max_profit]
		self.days_stat = [mean_day, median_day, min_day, max_day]


	def profits_days_scatter(self, value=None):
		profits_days = self.profits_days
		if value: # trim for profit >= -value and <= value
			profits_days = [pd for pd in profits_days if -value <= pd[0] <= value]

		profits = [pd[0] for pd in profits_days]
		days = [pd[1] for pd in profits_days]

		# Plot scatter
		plt.figure(figsize=(10, 6))
		plt.scatter(days, profits, color='skyblue', marker='o')

		# Plot median and mean line
		mean_profit, median_profit = self.profits_stat[0], self.profits_stat[1]

		plt.axhline(y=mean_profit, color='tab:orange', linestyle='dashed', label=f'Mean Profit: ${mean_profit:.2f}')
		plt.axhline(y=median_profit, color='tab:green', linestyle='dashed', label=f'Median Profit: ${median_profit:.2f}')
		
		plt.title('Profits vs. Days Arbitraged')
		plt.xlabel('Days Arbitraged')
		plt.ylabel('Profits ($USD)')

		plt.grid(True)
		plt.tight_layout()
		plt.legend()

		name = str(value) if value else 'default'
		output_path = 'profits_days_' + name + '.png'
		plt.savefig(output_path, format='png')
		
		# plt.show()


if __name__ == '__main__':
	pd = ProfitDays()
	pd.profits_days_scatter(1000)
	pd.profits_days_scatter(10000)
	pd.profits_days_scatter()

