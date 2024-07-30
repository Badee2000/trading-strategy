'''

Hello,

First of all, thank you for the opportunity.

I hope the code meets your expectations.

I used google search to have some clarification about what is bollinger bands,
How to write it in python,
What libraries should I use
And how to show it in a good way.

I used ChatGPT to give me some more information,
What are the requirements,
What is the right naming for each variable or function
And to give me steps to build a well-written code for that matter.

Main reason to use:
1- numpy: To add signals
2- matplotlib: To show the results in a graph using pyplot.
3- pandas_datareader and yfinance: To fetch data from yahoo finance.

'''
import numpy as np
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
import yfinance as yf

# Override the default pandas_datareader to use Yahoo Finance.
yf.pdr_override()
# Now you can use 'get_data_yahoo()' in pandas_datareader to get the data from yahoo.

# Function to fetch historical stock data


def fetch_stock_data(symbol, start_date, end_date):
    '''
    Get stock data from yahoo.
    '''
    try:
        # Read the data from YahooDailyReader.
        stock_data = pdr.get_data_yahoo(symbol, start=start_date, end=end_date)
        return stock_data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


# Function to calculate Bollinger Bands.
def calculate_bollinger_bands(stock_data, window_size=20, num_of_std=2):
    '''
    Calculate average SMA band and the upper and lower bands.
    '''
    # The moving average of the closing price used as a middle band in Bollinger Bands..
    rolling_mean = stock_data['Close'].rolling(window=window_size).mean()
    # The moving standard devition of the closing price measures the volatility of the stock’s price.
    rolling_std = stock_data['Close'].rolling(window=window_size).std()

    # This is how we calculate the upper and lower band.
    upper_band = rolling_mean + (rolling_std * num_of_std)
    lower_band = rolling_mean - (rolling_std * num_of_std)

    return rolling_mean, upper_band, lower_band


# Implement the Bollinger strategy (Add Sell and Buy Signals).
def bollinger_strategy(stock_data):
    '''
    Sell & Buy Signals.
    Buy When the closing price is below than the lower band.
    Sell When the closing price is above than the upper band.
    '''
    buy_signals = []
    sell_signals = []
    for i in range(len(stock_data)):
        # Generate buy signal when the closing price is below the lower band.
        if stock_data['Close'][i] < stock_data['Lower Band'][i]:
            buy_signals.append(stock_data['Close'][i])
            # np.nan refers that there is no signal for sell_signals(No generating).
            sell_signals.append(np.nan)

        # Generate sell signal when the closing price is above the upper band.
        elif stock_data['Close'][i] > stock_data['Upper Band'][i]:
            sell_signals.append(stock_data['Close'][i])
            # np.nan refers that there is no signal for buy_signals(No generating).
            buy_signals.append(np.nan)

        else:
            # If we didn't meet the above conditions, we don't add any signals.
            buy_signals.append(np.nan)
            sell_signals.append(np.nan)

    return buy_signals, sell_signals


# Main function to run the strategy
def trading_strategy(symbol, start_date, end_date):
    '''
    '''
    # Fetching stock data
    stock_data = fetch_stock_data(symbol, start_date, end_date)

    if stock_data is not None:
        # Calculating Bollinger Bands.
        stock_data['Middle Band'], stock_data['Upper Band'], stock_data['Lower Band'] = calculate_bollinger_bands(
            stock_data)

        # Implementing the trading strategy.
        stock_data['Buy Signal'], stock_data['Sell Signal'] = bollinger_strategy(
            stock_data)

        # Plotting the Bollinger Bands and signals.
        # Window size
        plt.figure(figsize=(12, 6))

        # And here customize what we want the user to see in that window.
        plt.plot(stock_data['Close'], label='Close Price', alpha=0.5)
        plt.plot(stock_data['Middle Band'],
                 label='Middle Band', linestyle='--')
        plt.plot(stock_data['Upper Band'], label='Upper Band', linestyle='--')
        plt.plot(stock_data['Lower Band'], label='Lower Band', linestyle='--')
        plt.scatter(stock_data.index, stock_data['Buy Signal'],
                    label='Buy Signal', marker='^', color='green')
        plt.scatter(stock_data.index, stock_data['Sell Signal'],
                    label='Sell Signal', marker='v', color='red')
        plt.title(f'Strategy for {symbol}')
        plt.legend()
        plt.show()
    else:
        print("No data retrieved. Check the stock symbol and date range.")


# Run the strategy for Apple from 2023 to 2024
trading_strategy('AAPL', '2021-01-01', '2021-12-31')
