from viresclient import set_token
import datetime as dt
from viresclient import SwarmRequest
import matplotlib as mpl
import matplotlib.pyplot as plt

#set_token("https://vires.services/ows")
# (you will now be prompted to enter the token)

request = SwarmRequest('https://vires.services/ows')

#print('check 1')
request.set_collection("SW_OPER_EFIA_LP_1B")
request.set_products(
    measurements=["Ne"]
)
#print('check 2')
# Fetch data from a given time interval
# - Specify times as ISO-8601 strings or Python datetime
data = request.get_between(
    start_time="2014-01-01T00:00",
    end_time="2015-12-31T23:59"
)
# Load the data as an xarray.Dataset
#print('check 3')
ds = data.as_xarray()

print(ds)
df = ds.to_dataframe()
print(df)

df = df.drop(df[df['Latitude'] > 69].index)
df = df.drop(df[df['Latitude'] < 55].index)
df = df.drop(df[df['Longitude'] > 25].index)
df = df.drop(df[df['Longitude'] < 10].index)
print(df)
df = df[['Ne']]
plot = df.plot()

plt.show()
