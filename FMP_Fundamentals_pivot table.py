import requests
import pandas as pd
from pivottablejs import pivot_ui

pd.options.display.float_format = '{:,.2f}'.format

# Input all required data here
FAANG = ['AAPL', 'GOOG', 'FB', 'AMZN', 'NFLX']
EV = ['TSLA', 'NIO', 'LI', 'XPEV', 'KNDI']
Ecommerce = ['AMZN', 'BABA', 'SE', 'JD']
Tech = ['DBX', 'MSFT', 'GOOG', 'BOX']
Semicon = ['NVDA', 'AMD', 'QCOM', 'SWKS']

company = Semicon
dates = [2020, 2019, 2018, 2017, 2016]

api = '9986f4c3a10c45418d13105f50ee7f94'
millions = 1000000

# Create loop to pulls multiple companies
n = len(company)
m = len(dates)

# Create empty Dataframe to store consolidated table
fundamentals_total = pd.DataFrame()

for i in range(0, n):

    # Request Financial Data from API and load to variables
    IS = requests.get(
        f'https://financialmodelingprep.com/api/v3/income-statement/{company[i]}?apikey={api}').json()
    BS = requests.get(
        f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{company[i]}?apikey={api}').json()
    CF = requests.get(
        f'https://financialmodelingprep.com/api/v3/cash-flow-statement/{company[i]}?apikey={api}').json()

    Ratios = requests.get(
        f'https://financialmodelingprep.com/api/v3/ratios/{company[i]}?apikey={api}').json()
    key_Metrics = requests.get(
        f'https://financialmodelingprep.com/api/v3/key-metrics/{company[i]}?apikey={api}').json()

    profile = requests.get(
        f'https://financialmodelingprep.com/api/v3/profile/{company[i]}?apikey={api}').json()

    # Create empty dictionary and add the financials to it
    financials = {}

    # Loop for the different years
    for item in range(m):
        # print(dates[item])
        financials[dates[item]] = {}

        # Key Metrics
        financials[dates[item]]['Mkt Cap'] = key_Metrics[item]['marketCap'] / millions
        financials[dates[item]]['Debt to Equity'] = key_Metrics[item]['debtToEquity']
        financials[dates[item]]['Debt to Assets'] = key_Metrics[item]['debtToAssets']
        financials[dates[item]]['Revenue per Share'] = key_Metrics[item]['revenuePerShare']
        financials[dates[item]]['NI per Share'] = key_Metrics[item]['netIncomePerShare']

        # From Income Sheet
        financials[dates[item]]['Revenue'] = IS[item]['revenue'] / millions
        financials[dates[item]]['Gross Profit'] = IS[item]['grossProfit'] / millions
        financials[dates[item]]['R&D Expenses'] = IS[item]['researchAndDevelopmentExpenses'] / millions
        financials[dates[item]]['Op Expenses'] = IS[item]['operatingExpenses'] / millions
        financials[dates[item]]['Op Income'] = IS[item]['operatingIncome'] / millions
        financials[dates[item]]['Net Income'] = IS[item]['netIncome'] / millions

        # From Balance Sheet
        # Assets
        financials[dates[item]]['Cash'] = BS[item]['cashAndCashEquivalents'] / millions
        financials[dates[item]]['Inventory'] = BS[item]['inventory'] / millions
        financials[dates[item]]['Cur Assets'] = BS[item]['totalCurrentAssets'] / millions
        financials[dates[item]]['LT Assets'] = BS[item]['totalNonCurrentAssets'] / millions
        financials[dates[item]]['Int Assets'] = BS[item]['intangibleAssets'] / millions
        financials[dates[item]]['Total Assets'] = BS[item]['totalAssets'] / millions
        #Liabilities and Equity
        financials[dates[item]]['Cur Liab'] = BS[item]['totalCurrentLiabilities'] / millions
        financials[dates[item]]['LT Debt'] = BS[item]['longTermDebt'] / millions
        financials[dates[item]]['LT Liab'] = BS[item]['totalNonCurrentLiabilities'] / millions
        financials[dates[item]]['Total Liab'] = BS[item]['totalLiabilities'] / millions
        financials[dates[item]]['SH Equity'] = BS[item]['totalStockholdersEquity'] / millions

        # From Cash Flow Statements
        financials[dates[item]
                   ]['CF Operations'] = CF[item]['netCashProvidedByOperatingActivities'] / millions
        financials[dates[item]]['CF Investing'] = CF[item]['netCashUsedForInvestingActivites'] / millions
        financials[dates[item]
                   ]['CF Financing'] = CF[item]['netCashUsedProvidedByFinancingActivities'] / millions
        financials[dates[item]]['CAPEX'] = CF[item]['capitalExpenditure'] / millions
        financials[dates[item]]['FCF'] = CF[item]['freeCashFlow'] / millions
        financials[dates[item]]['Dividends Paid'] = CF[item]['dividendsPaid'] / millions

        # Income Statement Ratios
        financials[dates[item]]['Gross Profit Margin'] = Ratios[item]['grossProfitMargin']
        financials[dates[item]]['Op Margin'] = Ratios[item]['operatingProfitMargin']
        financials[dates[item]]['Int Coverage'] = Ratios[item]['interestCoverage']
        financials[dates[item]]['Net Profit Margin'] = Ratios[item]['netProfitMargin']
        financials[dates[item]]['Dividend Yield'] = Ratios[item]['dividendYield']

        # BS Ratios
        financials[dates[item]]['Debt-to-Equity Ratio'] = Ratios[item]['debtEquityRatio']
        financials[dates[item]]['Current Ratio'] = Ratios[item]['currentRatio']
        financials[dates[item]]['Operating Cycle'] = Ratios[item]['operatingCycle']
        financials[dates[item]]['Days of AP Outstanding'] = Ratios[item]['daysOfPayablesOutstanding']
        financials[dates[item]]['Cash Conversion Cycle'] = Ratios[item]['cashConversionCycle']

        # Return Ratios
        financials[dates[item]]['ROA'] = Ratios[item]['returnOnAssets']
        financials[dates[item]]['ROE'] = Ratios[item]['returnOnEquity']
        financials[dates[item]]['ROCE'] = Ratios[item]['returnOnCapitalEmployed']
        financials[dates[item]]['Dividend Yield'] = Ratios[item]['dividendYield']

        # Price Ratios
        financials[dates[item]]['PE'] = Ratios[item]['priceEarningsRatio']
        financials[dates[item]]['PS'] = Ratios[item]['priceToSalesRatio']
        financials[dates[item]]['PB'] = Ratios[item]['priceToBookRatio']
        financials[dates[item]]['Price To FCF'] = Ratios[item]['priceToFreeCashFlowsRatio']
        financials[dates[item]]['PEG'] = Ratios[item]['priceEarningsToGrowthRatio']
        financials[dates[item]]['EPS'] = IS[item]['eps']
        financials[dates[item]]['EPS'] = IS[item]['eps']

    # Transform the dictionary into a Pandas
    fundamentals_single = pd.DataFrame.from_dict(financials, orient='index')

    # Add a new column that indicates the stock
    stock_identity = [company[i]] * len(fundamentals_single.index)
    fundamentals_single.insert(0, "Stock", stock_identity, True)

    # Concatenate the 2 dataframes together
    fundamentals_total = pd.concat([fundamentals_total, fundamentals_single])


# Add the date column into the DataFrame to make it suitable to convert into a pivottable
date_column = dates * len(company)
fundamentals_total.insert(0, "Date", date_column, True)


# Calculate Growth measures
#fundamentals_total['CAGR'] = (fundamentals_total[2020]/fundamentals_total[2016])**(1/5) - 1
#fundamentals['2020 growth'] = ((fundamentals[2020] - fundamentals[2019] )/ fundamentals[2019])*100
#fundamentals['2019 growth'] = ((fundamentals[2019] - fundamentals[2018] )/ fundamentals[2018])*100
#fundamentals['2018 growth'] = ((fundamentals[2018] - fundamentals[2017] )/ fundamentals[2017])*100
#fundamentals['2017 growth'] = ((fundamentals[2017] - fundamentals[2016] )/ fundamentals[2016])*100

# Export to Excel
# print(fundamentals_total)
pivot_ui(fundamentals_total)
# with pd.ExcelWriter('fundamentals.xlsx', mode='a') as writer:
#fundamentals_total.to_excel(writer, sheet_name = 'consolidated')
