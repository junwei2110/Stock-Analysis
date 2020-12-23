import requests
import pandas as pd
import datetime
import sys
from pivottablejs import pivot_ui

pd.options.display.float_format = '{:,.2f}'.format

# Input all required data here
api = '9986f4c3a10c45418d13105f50ee7f94'
millions = 1000000
now = datetime.datetime.now()

FAANG = ['AAPL', 'GOOG', 'FB', 'AMZN', 'NFLX']
EV = ['TSLA', 'NIO', 'LI', 'XPEV', 'KNDI']
Ecommerce = ['AMZN', 'BABA', 'SE', 'JD']
Tech = ['DBX', 'MSFT', 'GOOG', 'BOX']
Semicon = ['NVDA', 'AMD', 'QCOM', 'SWKS']

company = FAANG

# Input Ending Year and number of years for evaluation
end_year = 2019
years = 4

# Conditions to prevent getting wrong year for annual report
if now.year < end_year:
    print("End year cannot be in the future!!")
    sys.exit()
elif now.year == end_year & now.month < 10:
    print("Annual report for the current year not out yet!!")
    sys.exit()

# Creating dates array
dates = []

for i in range(0, years):
    dates.append(end_year - i)

# Create loop to pulls multiple companies
n = len(company)

# Create loop to pull the different years
p = now.year - end_year
m = len(dates)

# Create empty Dataframe to store consolidated table
fundamentals_total = pd.DataFrame()

for i in range(0, n):

    # Request Financial Data from API and load to variables
    IS = requests.get(
        f'https://financialmodelingprep.com/api/v3/income-statement/{company[i]}?apikey={api}').json()
    ISG = requests.get(
        f'https://financialmodelingprep.com/api/v3/income-statement-growth/{company[i]}?apikey={api}').json()
    BS = requests.get(
        f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{company[i]}?apikey={api}').json()
    CF = requests.get(
        f'https://financialmodelingprep.com/api/v3/cash-flow-statement/{company[i]}?apikey={api}').json()
    CFG = requests.get(
        f'https://financialmodelingprep.com/api/v3/cash-flow-statement-growth/{company[i]}?apikey={api}').json()
    Ratios = requests.get(
        f'https://financialmodelingprep.com/api/v3/ratios/{company[i]}?apikey={api}').json()
    key_Metrics = requests.get(
        f'https://financialmodelingprep.com/api/v3/key-metrics/{company[i]}?apikey={api}').json()

    # Create empty dictionary and add the financials to it
    financials = {}

    # Loop for the different years
    for q in range(0, m):
        # Creates an empty nested dictionary, i.e. the year is a main key and each parameter is a subkey within the year
        financials[dates[q]] = {}

        # From Income Sheet
        financials[dates[q]]['Revenue'] = IS[q+p]['revenue'] / millions
        financials[dates[q]]['Revenue Growth'] = ISG[q+p]['growthRevenue'] * 100
        financials[dates[q]]['Gross Profit'] = IS[q+p]['grossProfit'] / millions
        financials[dates[q]]['Gross Profit Growth'] = ISG[q+p]['growthGrossProfit'] * 100
        financials[dates[q]]['R&D Expenses'] = IS[q+p]['researchAndDevelopmentExpenses'] / millions
        financials[dates[q]]['Op Expenses'] = IS[q+p]['operatingExpenses'] / millions
        financials[dates[q]]['Op Income'] = IS[q+p]['operatingIncome'] / millions
        financials[dates[q]]['Op Income Growth'] = ISG[q+p]['growthOperatingIncome'] * 100
        financials[dates[q]]['Net Income'] = IS[q+p]['netIncome'] / millions
        financials[dates[q]]['Net Income Growth'] = ISG[q+p]['growthNetIncome'] * 100

        # From Balance Sheet
        # Assets
        financials[dates[q]]['Cash'] = BS[q+p]['cashAndCashEquivalents'] / millions
        financials[dates[q]]['Inventory'] = BS[q+p]['inventory'] / millions
        financials[dates[q]]['Cur Assets'] = BS[q+p]['totalCurrentAssets'] / millions
        financials[dates[q]]['LT Assets'] = BS[q+p]['totalNonCurrentAssets'] / millions
        financials[dates[q]]['Int Assets'] = BS[q+p]['intangibleAssets'] / millions
        financials[dates[q]]['Total Assets'] = BS[q+p]['totalAssets'] / millions
        #Liabilities and Equity
        financials[dates[q]]['Cur Liab'] = BS[q+p]['totalCurrentLiabilities'] / millions
        financials[dates[q]]['LT Debt'] = BS[q+p]['longTermDebt'] / millions
        financials[dates[q]]['LT Liab'] = BS[q+p]['totalNonCurrentLiabilities'] / millions
        financials[dates[q]]['Total Liab'] = BS[q+p]['totalLiabilities'] / millions
        financials[dates[q]]['SH Equity'] = BS[q+p]['totalStockholdersEquity'] / millions

        # From Cash Flow Statements
        financials[dates[q]
                   ]['CF Operations'] = CF[q+p]['netCashProvidedByOperatingActivities'] / millions
        financials[dates[q]]['CF Investing'] = CF[q +
                                                  p]['netCashUsedForInvestingActivites'] / millions
        financials[dates[q]
                   ]['CF Financing'] = CF[q+p]['netCashUsedProvidedByFinancingActivities'] / millions
        financials[dates[q]]['CAPEX'] = CF[q+p]['capitalExpenditure'] / millions
        financials[dates[q]]['CAPEX growth'] = CFG[q+p]['growthCapitalExpenditure'] * 100
        financials[dates[q]]['FCF'] = CF[q+p]['freeCashFlow'] / millions
        financials[dates[q]]['FCF growth'] = CFG[q+p]['growthFreeCashFlow'] * 100
        financials[dates[q]]['Dividends Paid'] = CF[q+p]['dividendsPaid'] / millions

        # Income Statement Ratios
        financials[dates[q]]['Gross Profit Margin'] = Ratios[q+p]['grossProfitMargin']
        financials[dates[q]]['Op Margin'] = Ratios[q+p]['operatingProfitMargin']
        financials[dates[q]]['Net Profit Margin'] = Ratios[q+p]['netProfitMargin']
        financials[dates[q]]['Dividend Payout Ratio'] = Ratios[q+p]['dividendPayoutRatio']

        # BS Ratios
        financials[dates[q]]['Debt-to-Equity Ratio'] = Ratios[q+p]['debtEquityRatio']
        financials[dates[q]]['LT Debt-to-Equity Ratio'] = BS[q+p]['totalNonCurrentLiabilities'] / \
            BS[q+p]['totalStockholdersEquity']
        financials[dates[q]]['Debt to Assets'] = key_Metrics[q+p]['debtToAssets']
        financials[dates[q]]['Current Ratio'] = Ratios[q+p]['currentRatio']
        financials[dates[q]]['Cash Conversion Cycle'] = Ratios[q+p]['cashConversionCycle']

        # Price Ratios
        financials[dates[q]]['Mkt Cap'] = key_Metrics[q+p]['marketCap'] / millions
        financials[dates[q]]['PE'] = Ratios[q+p]['priceEarningsRatio']
        financials[dates[q]]['PS'] = Ratios[q+p]['priceToSalesRatio']
        financials[dates[q]]['PB'] = Ratios[q+p]['priceToBookRatio']
        financials[dates[q]]['Price To FCF'] = Ratios[q+p]['priceToFreeCashFlowsRatio']
        financials[dates[q]]['PEG'] = Ratios[q+p]['priceEarningsToGrowthRatio']
        financials[dates[q]]['Revenue per Share'] = key_Metrics[q+p]['revenuePerShare']
        financials[dates[q]]['EPS'] = IS[q+p]['eps']

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

# Export to Excel or directly to pivot table
pivot_ui(fundamentals_total)
with pd.ExcelWriter('fundamentals.xlsx', mode='a') as writer:
    fundamentals_total.to_excel(writer, sheet_name='consolidated')
