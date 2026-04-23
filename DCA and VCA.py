#---------------------------------------------------------------------------------------------------------#
# Name of Author: Akash Balakrishnan
# File Created: 4/23/2026
#This program is used for a customer to either use Dollar Cost Averaging or Value Cost Averaging

import pandas as pd
import yfinance as yf

def get_data(ticker, period="3y"):
    stock = yf.Ticker(ticker)
    return stock.history(period)

def run_dca(ticker, amount, frequency):
    print(f"Running DCA for {ticker} with ${amount} every {frequency} time(s) monthly.")
    #DCA calculation logic
    frequency_map = {1: 'ME', 2: '15D'}
    resample_frequency = frequency_map.get(frequency, 'ME')

    data = yf.Ticker(ticker).history(period = "3y", interval = "1d")
    df = data[['Open','Close']].resample(resample_frequency).last()
    df = df.reset_index()
    df['Date'] = df['Date'].dt.date
    df.rename(columns={'Open': 'Price', 'Close': "Market_Close"}, inplace=True)


    df['Amount'] = amount
    df['Quantity'] = df['Amount'] / df['Price']
    df['CUM_QTY'] = df['Quantity'].cumsum()
    df['CUM_Amount'] = df['Amount'].cumsum()
    df['M2M'] = df['CUM_QTY'] * df['Market_Close']
    df['PNL'] = df['M2M'] - df['CUM_Amount']


    # This displays the table
    print("\n" + '=' * 100)
    print("Dollar Cost Averaging Results".center(100))
    print("=" * 100)
    print(df.to_string(index=False, float_format='%.4f'))
    # Display the summary
    print("\n" + '=' * 100)
    print("Summary".center(100))
    print("=" * 100)
    total_invested = df['CUM_Amount'].iloc[-1]
    total_shares = df["CUM_QTY"].iloc[-1]
    PNL = df["PNL"].iloc[-1]
    avg_PNL = df["PNL"].mean()
    max_PNL = df["PNL"].max()
    min_PNL = df["PNL"].min()
    draw_down = (min_PNL/df['CUM_Amount'].iloc[-1]) * 100

    # Print the Results
    print(f"PNL:      ${PNL:,.4f}")
    #print(f"Total Invested: ${total_invested:,.2f}")
    #print(f"Total Shares: {total_shares:,.4f}")
    print(f"Avg. PNL: ${avg_PNL:,.4f}")
    print(f"Max PNL: ${max_PNL:,.4f}")
    print(f"Min PNL: ${min_PNL:,.4f}")
    print(f"DrawDown: {draw_down:.4f}%")




def run_vca(ticker, goal, amount, frequency):
    print(f"Running VCA for {ticker} with a target of ${goal} and this ${amount} every {frequency} time(s) monthly.")
    #VCA calculation logic
    frequency_map = {1: 'ME', 2: '15D'}
    resample_frequency = frequency_map.get(frequency, 'ME')

    data = yf.Ticker(ticker).history(period="3y", interval="1d")
    df = data[['Open', 'Close']].resample(resample_frequency).last()
    df = df.reset_index()
    df['Date'] = df['Date'].dt.date
    df.rename(columns={'Open': 'Price', 'Close': "Market_Close"}, inplace=True)



    df['Goal'] = 0.0
    df['Amount'] = 0.0
    df['Quantity'] = 0.0
    df['CUM_QTY'] = 0.0
    df['CUM_Amount'] = 0.0
    df['Reserve'] = 0.0

    current_shares = 0.0
    total_invested = 0.0
    current_reserve = 0.0
    target_contribution = amount

    #loop is needed for VCA completion
    for i in range(len(df)):
        #Goal calculation
        current_goal = goal * (i + 1)
        price_now = df.iloc[i]['Price']

        current_pv = current_shares * price_now

        #Needed to hit the goal
        needed = current_goal - current_pv
        #Investment vs Reserve
        if needed > 0:
            avaliable_money = target_contribution + current_reserve
            actual_invest = min(needed, avaliable_money)
            current_reserve = max(0, current_reserve - (actual_invest - target_contribution))
        else:
            actual_invest = 0.0
            current_reserve += target_contribution

        qty_bought = actual_invest / price_now
        current_shares += qty_bought
        total_invested += actual_invest

        df.at[i, 'Goal'] = current_goal
        df.at[i, 'Amount'] = actual_invest
        df.at[i, 'Quantity'] = qty_bought
        df.at[i, 'Reserve'] = current_reserve
        df.at[i, 'CUM_QTY'] = current_shares
        df.at[i, 'CUM_Amount'] = total_invested
    df['PV'] = df['CUM_QTY'] * df['Price']
    df['M2M'] = df['CUM_QTY'] * df['Market_Close']
    df['PNL'] = df['M2M'] - df['CUM_Amount']

    # This displays the table
    print("\n" + '=' * 130)
    print("Value Cost Averaging Results".center(130))
    print("=" * 130)
    print(df.to_string(index=False, float_format='%.4f'))
    # Display the summary
    print("\n" + '=' * 130)
    print("Summary".center(130))
    print("=" * 130)
    total_invested = df['CUM_Amount'].iloc[-1]
    total_shares = df["CUM_QTY"].iloc[-1]
    total_PNL = df["PNL"].sum()
    avg_PNL = df["PNL"].mean()
    max_PNL = df["PNL"].max()
    min_PNL = df["PNL"].min()
    percent_PNL = ((df['Goal'].iloc[-1]-df['CUM_Amount'].iloc[-1])/df['Goal'].iloc[-1]) * 100

    # Print the Results
    print(f"Percent PNL: {percent_PNL:,.2f}%")
    #print(f"Total Invested: ${total_invested:,.2f}")
    #print(f"Total Shares: {total_shares:,.4f}")
    #print(f"Total PNL: ${total_PNL:,.4f}")
    print(f"Avg. PNL: ${avg_PNL:,.4f}")
    print(f"Max PNL: ${max_PNL:,.4f}")
    print(f"Min PNL: ${min_PNL:,.4f}")





#main
def main():
    print("---------------------Welcome to DCA or VCA!----------------")
    while True:
        print("-----------------------------------------------------------")
        strategy = input("Choose a strategy! Type 'DCA' or 'VCA' or 'Q' (to quit) ").upper()
        #Quit option if
        if strategy == 'Q':
            break
        if strategy not in ['DCA', 'VCA']:
            print("Invalid strategy, please try again.")
            continue

        #Collect the stock information
        ticker = input("Enter a ticker symbol to analyze (e.g., AAPL): ").upper()

        try:
            frequency = int(input("Enter a frequency (e.g. '1' for MONTH END or '2' Twice MONTHLY): "))


            if strategy == "DCA":
                amount = float(input("Enter the fixed investment of the stock: $"))
                run_dca(ticker, amount, frequency)


            elif strategy == "VCA":
                goal = float(input("Enter the goal value for this stock: $"))
                amount = float(input("Enter the amount you want to invest: $"))
                run_vca(ticker, goal, amount, frequency)

        except ValueError:
            print("Well mistakes do happen, please enter proper amounts.")
            continue

        #The quit option after running
        print("\n" + '=' * 59)
        choice = input("Would you like to continue? (Y/N): ").upper()

        if choice == 'N':
            print("Thanks for choosing to use DCA or VCA. Goodbye!")
            return True


if __name__ == "__main__":
    main()



