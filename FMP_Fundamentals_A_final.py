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
Cloud = ['DBX', 'DOCU']

# Input your API key
api = '9986f4c3a10c45418d13105f50ee7f94'

# Input the companies for evaluation
company = Cloud

# Input number of years for evaluation and ending financial year
end_year = 2019
years = 4

# Rejecting input if end_year is same or greater than the current year
# Rationale is that most companies financial reports for the current year are not out yet
now = datetime.datetime.now()
if end_year >= now.year:
    print("End year cannot be in the future!!")
    sys.exit()


# This value needs to be added to the dictionary in FMP to pull the data from the correct years
# E.g. if our end_year is 2018 but currently we are in 2020, we need to pull one year behind
# The first set in FMP will be the 2019 financial report (assuming we are in year 2020)
p = now.year - end_year - 1

# Create loop to pulls multiple companies
n = len(company)


# Create empty Dataframe to store consolidated table
fundamentals_total = pd.DataFrame()
millions = 1000000

for i in range(0, n):

    # Request Financial Data from API and load to variables
    IS = requests.get(
        f'https://financialmodelingprep.com/api/v3/income-statement/{company[i]}?apikey={api}').json()
    BS = requests.get(
        f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{company[i]}?apikey={api}').json()
    CF = requests.get(
        f'https://financialmodelingprep.com/api/v3/cash-flow-statement/{company[i]}?apikey={api}').json()
    FG = requests.get(
        f'https://financialmodelingprep.com/api/v3/financial-growth/{company[i]}?apikey={api}').json()
    Ratios = requests.get(
        f'https://financialmodelingprep.com/api/v3/ratios/{company[i]}?apikey={api}').json()
    key_Metrics = requests.get(
        f'https://financialmodelingprep.com/api/v3/key-metrics/{company[i]}?apikey={api}').json()

    # Check the first date of the first set in the dictionary (Some companies financial report come out earlier than others)
    # If the financial report comes out earlier than June, assume that the report is for previous year
    first_date = parser.parse(IS[0]['date'])
    if (first_date.year == now.year) & (first_date.month > 5):
        # This means that the current year's financial report for this company is already out, so to make it a ...
        # fair comparison with the others, we will use the next set of data as it will be the previous year's data
        q = 1
    else:
        q = 0

    # Check whether the statements above have even one year of data
    if (len(IS)-p-q <= 0) | (len(BS)-p-q <= 0) | (len(CF)-p-q <= 0) | (len(FG)-p-q <= 0) | (len(Ratios)-p-q <= 0) | (len(key_Metrics)-p-q <= 0):
        print('Data not available on FMP due to %s' % (company[i]))
        print("IS is %s, BS is %s, CF is %s, FG is %s, Ratios is %s, key_Metrics is %s"
              % (len(IS), len(BS), len(CF), len(FG), len(Ratios), len(key_Metrics)))
        sys.exit()

    # Check whether the companies have sufficient data for the number of years specified
    min_data = min(len(IS)-p-q, len(BS)-p-q, len(CF)-p-q, len(FG) -
                   p-q, len(Ratios)-p-q, len(key_Metrics)-p-q)

    if min_data >= years:
        m = years
    else:
        m = min_data

    # Creating the dates array
    dates = []
    for x in range(0, m):
        dates.append(end_year - x)

    # Create empty dictionary and add the financials to it
    financials = {}

    # Loop for the different years
    for j in range(0, m):
        # Creates an empty nested dictionary, i.e. the year is a main key and each parameter is a subkey within the year
        financials[dates[j]] = {}

        # Creates the year column
        financials[dates[j]]['Dates'] = dates[j]

        # From Income Sheet
        financials[dates[j]]['Revenue'] = IS[j+p+q]['revenue'] / millions
        financials[dates[j]]['Revenue Growth'] = FG[j+p+q]['revenueGrowth'] * 100
        financials[dates[j]]['Gross Profit'] = IS[j+p+q]['grossProfit'] / millions
        financials[dates[j]]['Gross Profit Growth'] = FG[j+p+q]['grossProfitGrowth'] * 100
        financials[dates[j]]['R&D Expenses'] = IS[j+p +
                                                  q]['researchAndDevelopmentExpenses'] / millions
        financials[dates[j]]['Op Expenses'] = IS[j+p+q]['operatingExpenses'] / millions
        financials[dates[j]]['Op Income'] = IS[j+p+q]['operatingIncome'] / millions
        financials[dates[j]]['Op Income Growth'] = FG[j+p+q]['operatingIncomeGrowth'] * 100
        financials[dates[j]]['Net Income'] = IS[j+p+q]['netIncome'] / millions
        financials[dates[j]]['Net Income Growth'] = FG[j+p+q]['netIncomeGrowth'] * 100

        # From Balance Sheet
        # Assets
        financials[dates[j]]['Cash'] = BS[j+p+q]['cashAndCashEquivalents'] / millions
        financials[dates[j]]['Inventory'] = BS[j+p+q]['inventory'] / millions
        financials[dates[j]]['Cur Assets'] = BS[j+p+q]['totalCurrentAssets'] / millions
        financials[dates[j]]['LT Assets'] = BS[j+p+q]['totalNonCurrentAssets'] / millions
        financials[dates[j]]['Int Assets'] = BS[j+p+q]['intangibleAssets'] / millions
        financials[dates[j]]['Total Assets'] = BS[j+p+q]['totalAssets'] / millions
        # Liabilities and Equity
        financials[dates[j]]['Cur Liab'] = BS[j+p+q]['totalCurrentLiabilities'] / millions
        financials[dates[j]]['LT Debt'] = BS[j+p+q]['longTermDebt'] / millions
        financials[dates[j]]['LT Liab'] = BS[j+p+q]['totalNonCurrentLiabilities'] / millions
        financials[dates[j]]['Total Liab'] = BS[j+p+q]['totalLiabilities'] / millions
        financials[dates[j]]['SH Equity'] = BS[j+p+q]['totalStockholdersEquity'] / millions

        # From Cash Flow Statements
        financials[dates[j]
                   ]['CF Operations'] = CF[j+p+q]['netCashProvidedByOperatingActivities'] / millions
        financials[dates[j]]['CF Investing'] = CF[j+p +
                                                  q]['netCashUsedForInvestingActivites'] / millions
        financials[dates[j]
                   ]['CF Financing'] = CF[j+p+q]['netCashUsedProvidedByFinancingActivities'] / millions
        financials[dates[j]]['CAPEX'] = CF[j+p+q]['capitalExpenditure'] / millions
        financials[dates[j]]['FCF'] = CF[j+p+q]['freeCashFlow'] / millions
        financials[dates[j]]['FCF growth'] = FG[j+p+q]['freeCashFlowGrowth'] * 100
        financials[dates[j]]['Dividends Paid'] = CF[j+p+q]['dividendsPaid'] / millions

        # Income Statement Ratios
        financials[dates[j]]['Gross Profit Margin'] = Ratios[j+p+q]['grossProfitMargin']
        financials[dates[j]]['Op Margin'] = Ratios[j+p+q]['operatingProfitMargin']
        financials[dates[j]]['Net Profit Margin'] = Ratios[j+p+q]['netProfitMargin']
        financials[dates[j]]['Dividend Payout Ratio'] = Ratios[j+p+q]['dividendPayoutRatio']

        # BS Ratios
        financials[dates[j]]['Debt-to-Equity Ratio'] = Ratios[j+p+q]['debtEquityRatio']
        financials[dates[j]]['LT Debt-to-Equity Ratio'] = BS[j+p+q]['totalNonCurrentLiabilities'] / \
            BS[j]['totalStockholdersEquity']
        financials[dates[j]]['Debt to Assets'] = key_Metrics[j+p+q]['debtToAssets']
        financials[dates[j]]['Current Ratio'] = Ratios[j+p+q]['currentRatio']
        financials[dates[j]]['Cash Conversion Cycle'] = Ratios[j+p+q]['cashConversionCycle']

        # Price Ratios
        financials[dates[j]]['Mkt Cap'] = key_Metrics[j+p+q]['marketCap'] / millions
        financials[dates[j]]['PE'] = Ratios[j+p+q]['priceEarningsRatio']
        financials[dates[j]]['PS'] = Ratios[j+p+q]['priceToSalesRatio']
        financials[dates[j]]['PB'] = Ratios[j+p+q]['priceToBookRatio']
        financials[dates[j]]['Price To FCF'] = Ratios[j+p+q]['priceToFreeCashFlowsRatio']
        financials[dates[j]]['PEG'] = Ratios[j+p+q]['priceEarningsToGrowthRatio']
        financials[dates[j]]['Revenue per Share'] = key_Metrics[j+p+q]['revenuePerShare']
        financials[dates[j]]['EPS'] = IS[j+p+q]['eps']

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
    fundamentals_total.to_excel(writer, sheet_name='consolidated')
