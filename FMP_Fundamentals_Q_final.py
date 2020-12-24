import requests
import pandas as pd
import datetime
from dateutil import parser
from pivottablejs import pivot_ui
import sys

pd.options.display.float_format = '{:,.2f}'.format

FAANG = ['AAPL', 'GOOG', 'FB', 'AMZN', 'NFLX']
EV = ['TSLA', 'NIO', 'LI', 'XPEV', 'KNDI']
Ecommerce = ['AMZN', 'BABA', 'SE', 'JD']
Tech = ['DBX', 'MSFT', 'GOOG', 'BOX']
Semicon = ['NVDA', 'AMD', 'QCOM', 'SWKS']
Cloud = ['DBX', 'BOX']

# Input your API key
api = '9986f4c3a10c45418d13105f50ee7f94'

# Input the companies for evaluation
company = ['AAPL', 'FB']

# Input number of quarters for evaluation and ending financial year
quarters_num = 5
end_year = 2020
end_quar = 3

# Rejecting input if end_quar is in current quarter or date is in the future
now = datetime.datetime.now()
now_quarter = pd.Timestamp(datetime.date(now.year, now.month, now.day)).quarter
if (end_year > now.year) | (end_quar > 12) | ((now_quarter == end_quar) & (end_year == now.year)):
    print("Date cannot be in the current quarter or in the future!!")
    sys.exit()

# Need to add this p to pull the right quarter data from FMP
p = (now_quarter - end_quar - 1) + 4 * (now.year - end_year)

# Create loop to pulls multiple companies
n = len(company)

# Create empty Dataframe to store consolidated table
fundamentals_total = pd.DataFrame()
millions = 1000000

for i in range(0, n):

    # Request Financial Data from API and load to variables
    IS = requests.get(
        f'https://financialmodelingprep.com/api/v3/income-statement/{company[i]}?period=quarter&apikey={api}').json()
    BS = requests.get(
        f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{company[i]}?period=quarter&apikey={api}').json()
    CF = requests.get(
        f'https://financialmodelingprep.com/api/v3/cash-flow-statement/{company[i]}?period=quarter&apikey={api}').json()
    Ratios = requests.get(
        f'https://financialmodelingprep.com/api/v3/ratios/{company[i]}?period=quarter&apikey={api}').json()
    key_Metrics = requests.get(
        f'https://financialmodelingprep.com/api/v3/key-metrics/{company[i]}?period=quarter&apikey={api}').json()
    FG = requests.get(
        f'https://financialmodelingprep.com/api/v3/financial-growth/{company[i]}?period=quarter&apikey={api}').json()

    # Create empty dictionary and add the financials to it
    financials = {}

    # Loop for the different quarters
    for j in range(0, quarters_num):
        # Creates an empty nested dictionary, i.e. the year is a main key and each parameter is a subkey within the year
        financials[j] = {}

        # Year and Quarter
        # Pulling the date from FMP and converting it into datetime format
        date_FMP = parser.parse(IS[j+p]['date'])
        # Changing the FMP date into a string in the format (YYYY Q1/2/3/4)
        date_input = str(date_FMP.year) + " Q" + \
            str(pd.Timestamp(datetime.date(date_FMP.year, date_FMP.month, date_FMP.day)).quarter)

        # From Income Sheet
        financials[j]['Date'] = date_input
        financials[j]['Revenue'] = IS[j+p]['revenue'] / millions
        financials[j]['Revenue Growth'] = FG[j+p]['revenueGrowth'] * 100
        financials[j]['Gross Profit'] = IS[j+p]['grossProfit'] / millions
        financials[j]['Gross Profit Growth'] = FG[j+p]['grossProfitGrowth'] * 100
        financials[j]['R&D Expenses'] = IS[j+p]['researchAndDevelopmentExpenses'] / millions
        financials[j]['Op Expenses'] = IS[j+p]['operatingExpenses'] / millions
        financials[j]['Op Income'] = IS[j+p]['operatingIncome'] / millions
        financials[j]['Op Income Growth'] = FG[j+p]['operatingIncomeGrowth'] * 100
        financials[j]['Net Income'] = IS[j+p]['netIncome'] / millions
        financials[j]['Net Income Growth'] = FG[j+p]['netIncomeGrowth'] * 100

        # From Balance Sheet
        # Assets
        financials[j]['Cash'] = BS[j+p]['cashAndCashEquivalents'] / millions
        financials[j]['Inventory'] = BS[j+p]['inventory'] / millions
        financials[j]['Cur Assets'] = BS[j+p]['totalCurrentAssets'] / millions
        financials[j]['LT Assets'] = BS[j+p]['totalNonCurrentAssets'] / millions
        financials[j]['Int Assets'] = BS[j+p]['intangibleAssets'] / millions
        financials[j]['Total Assets'] = BS[j+p]['totalAssets'] / millions
        # Liabilities and Equity
        financials[j]['Cur Liab'] = BS[j+p]['totalCurrentLiabilities'] / millions
        financials[j]['LT Debt'] = BS[j+p]['longTermDebt'] / millions
        financials[j]['LT Liab'] = BS[j+p]['totalNonCurrentLiabilities'] / millions
        financials[j]['Total Liab'] = BS[j+p]['totalLiabilities'] / millions
        financials[j]['SH Equity'] = BS[j+p]['totalStockholdersEquity'] / millions

        # From Cash Flow Statements
        financials[j]['CF Operations'] = CF[j+p]['netCashProvidedByOperatingActivities'] / millions
        financials[j]['CF Investing'] = CF[j+p]['netCashUsedForInvestingActivites'] / millions
        financials[j]['CF Financing'] = CF[j +
                                           p]['netCashUsedProvidedByFinancingActivities'] / millions
        financials[j]['CAPEX'] = CF[j+p]['capitalExpenditure'] / millions
        financials[j]['FCF'] = CF[j+p]['freeCashFlow'] / millions
        financials[j]['FCF growth'] = FG[j+p]['freeCashFlowGrowth'] * 100
        financials[j]['Dividends Paid'] = CF[j+p]['dividendsPaid'] / millions

        # Income Statement Ratios
        financials[j]['Gross Profit Margin'] = Ratios[j+p]['grossProfitMargin']
        financials[j]['Op Margin'] = Ratios[j+p]['operatingProfitMargin']
        financials[j]['Net Profit Margin'] = Ratios[j+p]['netProfitMargin']
        financials[j]['Dividend Payout Ratio'] = Ratios[j+p]['dividendPayoutRatio']

        # BS Ratios
        financials[j]['Debt-to-Equity Ratio'] = Ratios[j+p]['debtEquityRatio']
        financials[j]['LT Debt-to-Equity Ratio'] = BS[j+p]['totalNonCurrentLiabilities'] / \
            BS[j]['totalStockholdersEquity']
        financials[j]['Debt to Assets'] = key_Metrics[j+p]['debtToAssets']
        financials[j]['Current Ratio'] = Ratios[j+p]['currentRatio']
        financials[j]['Cash Conversion Cycle'] = Ratios[j+p]['cashConversionCycle']

        # Price Ratios
        financials[j]['Mkt Cap'] = key_Metrics[j+p]['marketCap'] / millions
        financials[j]['PE'] = Ratios[j+p]['priceEarningsRatio']
        financials[j]['PS'] = Ratios[j+p]['priceToSalesRatio']
        financials[j]['PB'] = Ratios[j+p]['priceToBookRatio']
        financials[j]['Price To FCF'] = Ratios[j+p]['priceToFreeCashFlowsRatio']
        financials[j]['PEG'] = Ratios[j+p]['priceEarningsToGrowthRatio']
        financials[j]['Revenue per Share'] = key_Metrics[j+p]['revenuePerShare']
        financials[j]['EPS'] = IS[j+p]['eps']

    # Transform the dictionary into a Pandas
    fundamentals_single = pd.DataFrame.from_dict(financials, orient='index')

    # Add a new column that indicates the stock
    stock_identity = [company[i]] * len(fundamentals_single.index)
    fundamentals_single.insert(0, "Stock", stock_identity, True)

    # Concatenate the 2 dataframes together
    fundamentals_total = pd.concat([fundamentals_total, fundamentals_single])


# Export to Excel or directly to pivot table
pivot_ui(fundamentals_total)
with pd.ExcelWriter('fundamentals.xlsx', mode='a') as writer:
    fundamentals_total.to_excel(writer, sheet_name='consolidated_quarter')
