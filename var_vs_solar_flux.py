import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime
import matplotlib.ticker as ticker
mpl.rcParams['agg.path.chunksize'] = 10000

# Om du kolla på götaland, kom ihåg att inte ha decimal=","
data_big = pd.read_csv(r"C:\Skola\År 5\Exjobb\Sweposdata\götaland.csv", sep=';', decimal=",", header=0, names=["Datetime", "Measurement"])#, parse_dates=date_col, dtype = dtypes)
data_small = pd.read_csv(r"C:\Skola\År 5\Exjobb\Sweposdata\210101_230307\götaland_small.csv", sep=';', decimal=",", names=["Datetime", "Measurement"])#, parse_dates=date_col)
sun_data = pd.read_csv(r"C:\Skola\År 5\Exjobb\Soldata\penticton_radio_flux.csv", header=0, names=["Datetime", " Sun Measurement"])
data = pd.concat([data_big, data_small])

con_dates = {"Datetime": "int"}
sun_data['Datetime'] = sun_data['Datetime'].astype(int)
print(data.head(3))
print(data.tail(3))
sun_data['Datetime'] = pd.to_datetime(sun_data['Datetime'], unit='D', origin='julian', errors='coerce')

data['Datetime'] = pd.to_datetime(data['Datetime'], errors='coerce')
data = data.dropna()
data = data.reset_index(drop=True)
#data = data[~data.index.duplicated()]
#data = data.drop_duplicates(subset='Datetime')

print('Before Month group')

print(sun_data.shape)
print(data.shape)

data['Measurement'] = data.groupby(pd.Grouper(freq='1ME', key='Datetime')).transform('mean')
sun_data['Sun Measurement'] = sun_data.groupby(pd.Grouper(freq='1ME', key='Datetime')).transform('mean')

print('After Month group')

print(sun_data.shape)
print(data.shape)

#data['Datetime'] = [time.time() for time in data['Datetime']]
data = data.sort_values(by= 'Datetime', ascending=True)
sun_data = sun_data.sort_values(by= 'Datetime', ascending=True)

data = data.groupby(['Datetime']).agg({'Measurement':'mean'})
sun_data = sun_data.groupby(['Datetime']).agg({'Sun Measurement':'mean'})


print(sun_data.shape)
print(data.shape)

merge = sun_data.merge(data, left_index=True, right_index=True, how='inner')
print(merge)

corr = data['Measurement'].corr(sun_data['Sun Measurement'])
"""
X = merge[['Sun Measurement']]
y = merge[['Measurement']]
regressor = LinearRegression()
regressor.fit(X, y)
fig, ax = plt.subplots()
plt.scatter(X, y, color='red')
plt.plot(X, regressor.predict(X), color='blue')
ax.legend([f"Correlation Coefficient = {corr}"])
plt.title('f10.7 vs Ionospheric disturbance Götaland 2013-2023')
plt.xlabel('f10.7 [SFU]')
plt.ylabel('Variation [cm]')
plt.show()
"""
color = 'tab:red'

ax1 = sun_data.plot(title="Götaland", color=color)
ax1.set_xlabel('time (year)')
ax1.set_ylabel('Solar Flux [SFU]', color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax1.legend([f"Correlation Coefficient = {corr}"])
ax2 = ax1.twinx()
color = 'tab:blue'
data.plot(ax=ax2)
ax2.set_ylabel('Variance [cm]', color=color)  # we already handled the x-label with ax1
ax2.tick_params(axis='y', labelcolor=color)
ax2.get_legend().remove()

print('Correlation Coefficient:\n')
print(corr)

#plot.set_ylim([0, 20])
#plot.xaxis.set_major_locator(ticker.MultipleLocator(21600))

plt.show()
