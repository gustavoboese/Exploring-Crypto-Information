# Importing pandas
import pandas as pd

# Importing matplotlib and setting aesthetics for plotting later.
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')

# Reading datasets/coinmarketcap_06122017.csv into pandas
dec6 = pd.read_csv('datasets/coinmarketcap_06122017.csv')

# Selecting the 'id' and the 'market_cap_usd' columns
market_cap_raw = dec6.loc[:, ["id", "market_cap_usd"]]

# print(market_cap_raw.count())

# Filtering out rows without a market capitalization
cap = market_cap_raw.query('market_cap_usd > 0')

# print(cap.count())

# Declaring these now for later use in the plots
TOP_CAP_TITLE = 'Top 10 market capitalization'
TOP_CAP_YLABEL = '% of total cap'

# Selecting the first 10 rows and setting the index
cap10 = cap.head(10)
cap10 = cap10.set_index('id')

# Calculating market_cap_perc
cap10 = cap10.assign(market_cap_perc=lambda x: (x.market_cap_usd / cap.market_cap_usd.sum()) * 100)

# Plotting the barplot with the title defined above
ax = cap10.loc[:, "market_cap_perc"].plot.bar()

ax.set(title=TOP_CAP_TITLE, ylabel=TOP_CAP_YLABEL)

# Colors for the bar plot
COLORS = ['orange', 'green', 'orange', 'cyan', 'cyan', 'blue', 'silver', 'orange', 'red', 'green']

ax = cap10.loc[:, "market_cap_perc"].plot.bar(color=COLORS, log=True)

ax.set(ylabel="USD", xlabel="", title="Top 10 market capitalization")

# Selecting the id, percent_change_24h and percent_change_7d columns
volatility = dec6.loc[:, ["id", "percent_change_24h", "percent_change_7d"]]

volatility = volatility.set_index("id")
volatility = volatility.dropna()

volatility = volatility.sort_values(by="percent_change_24h", ascending=True)


def top10_subplot(volatility_series, title):
    # Making the subplot and the figure for two side by side plots
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 6))

    # Plotting with pandas the barchart for the top 10 losers
    ax = (volatility_series[:10].plot.bar(ax = axes[0]))

    # Setting the figure's main title to the text passed as parameter
    fig.suptitle(title)

    # Setting the ylabel to '% change'
    ax.set_ylabel("% change")

    # Same as above, but for the top 10 winners
    ax = (volatility_series[:-10].plot.bar(ax = axes[1]))

    # Returning this for good practice, might use later
    return fig, ax


DTITLE = "24 hours top losers and winners"

fig, ax = top10_subplot(volatility_series=volatility.percent_change_24h,title=DTITLE)

# Sorting in ascending order
volatility7d = volatility.sort_values(by="percent_change_7d", ascending=True)

WTITLE = "Weekly top losers and winners"

fig.clf()
# Calling the top10_subplot function
fig, ax = top10_subplot(volatility7d.percent_change_7d,WTITLE)

largecaps = cap.query('market_cap_usd > 10000000000')

def capcount(query_string):
    return cap.query(query_string).count().id

# Labels for the plot
LABELS = ["biggish", "micro", "nano"]

# Using capcount count the biggish cryptos
biggish = capcount('market_cap_usd > 300000000')

# Same as above for micro ...
micro = capcount("market_cap_usd < 300000000 & market_cap_usd > 50000000")

# ... and for nano
nano =  capcount('market_cap_usd < 50000000')

# Making a list with the 3 counts
values = [biggish, micro, nano]

# Plotting them with matplotlib
plt.bar(LABELS ,values)
plt.show()