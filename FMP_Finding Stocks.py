import requests
import pandas as pd
from pivottablejs import pivot_ui

pd.options.display.float_format = '{:,.2f}'.format

# Sectors include technology,

# Input your API key
api_FMPC = 'f5fc1f8bd64c0288e56bb21b10840d1f'
api_FMP = '9986f4c3a10c45418d13105f50ee7f94'

# Sector:
# Consumer Cyclical - Energy - Technology - Industrials - Financial Services
# Basic Materials - Communication Services - Consumer Defensive - Healthcare
# Real Estate - Utilities -Industrial Goods-Financial-Services-Conglomerates
sector = 'Technology'

# marketCapMoreThan OR marketCapLowerThan : Number
marketcapeqn = 'marketCapMoreThan'
marketcapvalue = 1000000000

# Limit the number of pulls
limit = 100

# Getting the list of stocks
companies = requests.get(
    f'https://financialmodelingprep.com/api/v3/stock-screener?{marketcapeqn}={marketcapvalue}&sector={sector}&limit={limit}&apikey={api_FMP}').json()

stock_list = []
stocklist = ""

for stock in companies:
    stock_list.append(stock['symbol'])
    if len(stock_list) == 1:
        stocklist = stock['symbol']
    else:
        stocklist = stocklist + "," + stock['symbol']


# Start pulling data for each of the companies in the stock list
pricing = requests.get(
    f'https://financialmodelingprep.com/api/v3/quote/{stocklist}?apikey={api_FMP}').json()
metrics = {}

for i in range(0, len(pricing)):

    for j in range(0, len(stock_list)):
        if stock_list[j] == pricing[i]['symbol']:
            metrics[stock_list[j]] = {}
            metrics[stock_list[j]]["Stock"] = pricing[i]["symbol"]
            metrics[stock_list[j]]["Price"] = pricing[i]["price"]
            metrics[stock_list[j]]["50-day Moving Average"] = pricing[i]["priceAvg50"]
            metrics[stock_list[j]]["200-day Moving Average"] = pricing[i]["priceAvg200"]
            metrics[stock_list[j]]["PE Ratio"] = pricing[i]["pe"]

            if pricing[i]["price"] is None:
                break
            else:
                metrics[stock_list[j]]["Delta from 50-Avg"] = pricing[i]["price"] - \
                    pricing[i]["priceAvg50"]
                metrics[stock_list[j]]["Delta from 200-Avg"] = pricing[i]["price"] - \
                    pricing[i]["priceAvg200"]


# Transform the dictionary into a Pandas
metrics_df = pd.DataFrame.from_dict(metrics, orient='index')

# Export to Excel or directly to pivot table
pivot_ui(metrics_df)
with pd.ExcelWriter('stock select.xlsx', mode='a') as writer:
    metrics_df.to_excel(writer, sheet_name='trial')
