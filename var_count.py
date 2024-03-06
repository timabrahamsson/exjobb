import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.ticker as ticker
mpl.rcParams['agg.path.chunksize'] = 10000

data_big = pd.read_csv(r"C:\Skola\År 5\Exjobb\Sweposdata\norra_norrland.csv", sep=';', decimal=",", header=0, names=["Datetime", "Measurement"])#, parse_dates=date_col, dtype = dtypes)
data_small = pd.read_csv(r"C:\Skola\År 5\Exjobb\Sweposdata\210101_230307\norra_norrland_small.csv", sep=';', decimal=",", header=0, names=["Datetime", "Measurement"])#, parse_dates=date_col)
data = pd.concat([data_big, data_small])

con_dates = {"Datetime": "int"}

print('Before drops\n')
print(data.head())
print(data.tail())

data['Datetime'] = pd.to_datetime(data['Datetime'], errors='coerce')
data = data.dropna()
data = data.reset_index(drop=True)
data = data.drop(data[data['Measurement'] < 20].index)

#data = data[~data.index.duplicated()]
#data = data.drop_duplicates(subset='Datetime')

#data['Datetime'] = [time.time() for time in data['Datetime']]
data['Datetime'] = data['Datetime'].apply(lambda x: x.replace(year=2000, month=1, day=1))
data = data.sort_values(by='Datetime', ascending=True)
print('After drops and date change')
print(data.head())
print(data.tail())
print(data.shape)

data = data.groupby('Datetime').agg({'Measurement':'count'})

print('After agg sum\n')
print(data.head())
print(data.tail())
print(data.shape)

color = 'tab:red'
fig, ax = plt.subplots()
plot = data.plot(title="Northern Norrland between 2013 och 2023", color=color, ax=ax)
plot.set_xlabel('Time of day')
plot.set_ylabel('High disturbance measurements', color=color)
ax.legend(['min Δvar = 20 cm'])
plot.tick_params(axis='y', labelcolor=color)

plot.set_ylim([0, 600])
plot.xaxis.set_major_locator(ticker.MultipleLocator(21600))

plt.show()
