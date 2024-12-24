import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

offers_path = '../IITP-VDLand/Offers_opensea.csv'
characteristics_path = '../IITP-VDLand/Characteristics.csv'
sales_path = '../IITP-VDLand/Sales_opensea.csv'
sales_et_path = '../IITP-VDLand/Sales_ethereum.csv'

def gas_timeline():
	"""
	Show the timeline of the gas prices and number of transactions
	"""
	# Initial setup
	sales_et_df = pd.read_csv(sales_et_path)
	sales_et_df['gas_price'] = sales_et_df['gas_price'] / (10 ** 9) # Gas fees are in Gwei unit
	sales_et_df['block_timestamp'] = sales_et_df['block_timestamp'].apply(lambda x: x if 'UTC' in x else x + ' UTC') # some cleanup
	sales_et_df['block_timestamp'] = pd.to_datetime(sales_et_df['block_timestamp'], utc=True) # change to python datetime format

	# Aggregate to get average gas price and total number of transactions, group by dates
	daily_data = sales_et_df.set_index('block_timestamp').resample('D').agg({
		'gas_price': 'mean',
		'transaction_hash': 'count'
	})
	daily_data.rename(columns={'gas_price': 'avg_gas_price', 'transaction_hash': 'transaction_count'}, inplace=True)

	# Create plot
	fig, ax1 = plt.subplots(figsize=(14, 7))

	# Plot the average gas price on the left y-axis
	ax1.set_xlabel('Timeline')
	ax1.set_ylabel('Average Gas Price (Gwei)')
	line1, = ax1.plot(daily_data.index, daily_data['avg_gas_price'], color='tab:blue', label='Average Gas Price')
	ax1.tick_params(axis='y')

	# Create a second y-axis for the number of transactions
	ax2 = ax1.twinx()
	ax2.set_ylabel('Number of Transactions')
	line2, = ax2.plot(daily_data.index, daily_data['transaction_count'], color='tab:orange', label='Number of Transactions')
	ax2.tick_params(axis='y')

	# Title and layout
	plt.title('Daily Average Gas Price and Number of Transactions')
	fig.tight_layout()
	fig.legend(handles=[line1, line2], loc='upper center', bbox_to_anchor=(0.5, 0.9), ncol=1) # adjusts legend to be x-middle (0.5) and y-below-title (0.8)

	plt.savefig('gas_timeline.png', format='png')
	
	# plt.show()


def gas_price_distribution(value=None): 
	"""
	outputs the distribution for all gas prices (which contains some outliers, hence require to shift the scale to log)
	OR 
	outputs the distribution for gas prices <= value 
	"""
	sales_et_df = pd.read_csv(sales_et_path)
	sales_et_df['gas_price'] = sales_et_df['gas_price'] / (10 ** 9) # Gas fees are in Gwei unit

	# Calculate median and mean
	median = sales_et_df['gas_price'].median()
	mean = sales_et_df['gas_price'].mean()

	# Plot histogram
	fig = plt.figure(figsize=(12, 8))
	plt.xlabel('Gas Price (Gwei)')
	plt.ylabel('Number of Transactions')
	plt.title('Distribution of Gas Prices')

	# Filter only gas price <= value for better visualization
	filtered_df = sales_et_df
	if value: 
		filtered_df = sales_et_df[sales_et_df['gas_price'] <= value]
		his = sns.histplot(filtered_df['gas_price'], bins=50, kde=True, color='skyblue')
		his.lines[0].set_color('red') # for curve to be red
	else: # show everything
		plt.hist(filtered_df['gas_price'], bins=50, color='skyblue', edgecolor='black')
		plt.yscale('log')  # Use log scale for extremely large values of gas prices
		plt.ylabel('Number of Transactions (log scale)')
	
	# Plot median and mean lines
	plt.axvline(median, color='tab:orange', linestyle='dashed', linewidth=2, label=f'Median: {median:.2f}')
	plt.axvline(mean, color='tab:green', linestyle='dashed', linewidth=2, label=f'Mean: {mean:.2f}')
	plt.legend()
	plt.tight_layout()

	# Save figure
	name = str(value) if value else 'default'
	output_path = 'gasprices_' + name + '.png'
	plt.savefig(output_path, format='png')
	
	# plt.show()


if __name__ == '__main__':
	gas_timeline()
	gas_price_distribution(100)
	gas_price_distribution(200) # price <= 200 
	gas_price_distribution() # everything

