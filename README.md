Dollar Cost Averaging is an investment strategy that an individual has a set fixed investment on a particular stock in which they can choose to invest monthly or bi-monthly. Value Cost Averaging is another investment strategy similar to Dollar Cost Averaging but the main difference is they also have a goal they want to hit with that particular stock. In this program a user enters a the investment strategy DCA or VCA, then they enter the ticker symbol (the stock they want to invest in), frequency is entered, fixed amount is then entered (for DCA), but for VCA there is no fixed amount instead there is amount to invest, and a goal.
The algorithm is set to back test with 3 years of historical data from Yahoo Finance and the tickers should also match those in Yahoo Finance. 

After the user inputs there is a ledger that is displayed which include: Date, Price (Opening Price of that stock on that particular day), Market_Close (Closing price on that day of the particular stock),
                                                                        Amount (Fixed Investment Amount), Quantity (which is Amount divided by Price), CUM_QTY (Cumulative Quantity which is sum of all the quanitities bought),
									CUM_Amount (Cumulative Amount is the sum of the amount invested), M2M (Mark to Money is cumulative quanitity into the closing price), PNL (PNL is the profit and loss which is calculated by M2M minus CUM_Amount).
---------------------------------------------------------------------> DCA


After the user inputs there is a ledger that is displayed which include: Date, Price (Opening Price of that stock on that particular day), Market_Close (Closing price on that day of the particular stock),
                                                                         Goal, Amount, Quantity, CUM_QTY (Cumulative Quantity), CUM_Amount (Cumulative Amount), Reserve (Cumulation of money that won't be invested), 
									 PV (Portfolio Value), M2M (Mark To Money), and PNL (Profit and Loss).
---------------------------------------------------------------------> VCA


After the ledger is diplayed a summary with values are also displayed which include but aren't limited to PNL (Average...) or Percent PNL(Average...). Changes in the summary will be linked to the choosing of different investment strategies.
