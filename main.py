from bsedata.bse import BSE
import time

# Inputs
money = int(input('Enter amount you want to invest : '))
shares = int(input('Enter no of Shares you want to buy/sell in each transaction : '))
stop_loss = float(input('Enter Stop Loss Amount (in %): '))
book_profit = float(input('Enter Book Profit Amount (in %): '))

# Processing (% to integer)
stop_loss = 1 - (stop_loss / 100)
book_profit = 1 + (book_profit / 100)

# Server
print('\n\nConnecting to Server .....')
test = BSE(update_codes=True)
print('Authorization Successful .....')
print('Fetching Data .....\n')
initial = test.getQuote('500113')
currentTime = initial['updatedOn']

initial_amount = money
transactions = 0
stocks = 0
counter = 0
last_buy_price = float(initial['currentValue'])

while currentTime != '28 Jun 21 | 4:00 PM':

    invest = stocks * float(initial['currentValue'])
    market_price = float(initial['currentValue'])

    data1 = test.getQuote('500113')
    print(data1['updatedOn'], '\t', data1['currentValue'])
    time.sleep(60)
    data2 = test.getQuote('500113')
    print(data2['updatedOn'], '\t', data2['currentValue'])

    if abs(float(data1['currentValue']) - float(data2['currentValue'])) <= 0.05:
        print('Doji Pattern in the last 1 min.\n')

        # Bullish
        if float(data1['currentValue']) - float(data2['currentValue']) <= 0 and shares * float(
                initial['currentValue']) < money:
            money -= shares * float(initial['currentValue'])
            invest += shares * float(initial['currentValue'])
            stocks += shares
            last_buy_price = float(initial['currentValue'])
            print('\nBULL: Bought ', shares, ' at ', float(initial['currentValue']), '|| Cash Left = ', money,
                  '|| Invested = ', invest, '|| Current shares = ', stocks)
            transactions += 1

        # Bearish
        if float(data1['currentValue']) - float(data2['currentValue']) > 0 and transactions > 0 and stocks > 0:
            money += shares * float(initial['currentValue'])
            invest -= shares * float(initial['currentValue'])
            stocks -= shares
            print('\nBEAR: Sold ', shares, ' at ', float(initial['currentValue']), '|| Cash Left = ', money,
                  '|| Invested = ', invest, '|| Current shares = ', stocks)
            transactions += 1


        # Book Profit
        if market_price > book_profit * last_buy_price and transactions > 0 and stocks > 0:
            money += shares * float(initial['currentValue'])
            invest -= shares * float(initial['currentValue'])
            stocks -= shares
            print('\nBKPF: Sold ', shares, ' at ', float(initial['currentValue']), '|| Cash Left = ', money,
                  '|| Invested = ', invest, '|| Current shares = ', stocks)
            transactions += 1

        # Stop Loss
        if market_price < stop_loss * last_buy_price and transactions > 0 and stocks > 0:
            money += shares * float(initial['currentValue'])
            invest -= shares * float(initial['currentValue'])
            stocks -= shares
            print('\nSTLS: Sold ', shares, ' at ', float(initial['currentValue']), '|| Cash Left = ', money,
                  '|| Invested = ', invest, '|| Current shares = ', stocks)
            transactions += 1

    else:
        print('No Doji Pattern in the last 1 min.\n')

    currentTime = data2['updatedOn']

print('\nProcess completed.')

gross = float(initial['currentValue']) * stocks + money
print("\n\n\n\tTotal Amount   : Rs. ", gross)
print("\tInitial Amount : Rs. ", initial_amount)
print("\tProfit / Loss  : Rs. ", gross - initial_amount)
print('\n\tThanks for using Trading Bot !!!')