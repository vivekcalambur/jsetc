from __future__ import division
from strategy import Strategy

class FairValue(Strategy):
	fairValues = {"AAPL": [None,None], "BOND": [None,None], "GOOG": [None,None], "MSFT": [None,None], "NOKFH": [None,None], "NOKUS": [None,None], "XLK": [None,None]}

	def __init__(self):
		return

	def updateValues(data, fv):
		symb = data['symb']
		buys = data['buy']
		sells = data['sell']
		# TODO median
		if(len(buys)>0):
			mean_buy = sum([price for price, size in buys]) / len(buys)
			if(fairValues[symb][0]==None):
				fairValues[symb][0] = mean_buy
			else:
				fairValues[symb][0] = (fairValues[symb][0] + mean_buy)/2
		if(len(sells)>0):
			mean_sell = sum([price for price, size in sells])/ len(sells)
			if(fairValues[symb][1]==None):
				fairValues[symb][1] = mean_sell
			else:
				fairValues[symb][1] = (fairValues[symb][0] + mean_sell)/2

	def trade(data):
		"""Given the data in the book, decides whether we should make a trade.
		Returns a list of trades (buy/sell, symbol, price, size).
		"""
		trades = []
		fv = sum(fairValues[data['symb']])
		if(fv[0]==None or fv[1]==None):
			return
		fv = sum(fv)/2
		updateValues(data)
		for entry in data['buy']:
			if(entry['price']>fv):
				trades += ['SELL', data['symb'], entry['price'], entry['size']]
		for entry in data['sell']:
			if(entry['price']<fv):
				trades += ['BUY', data['symb'], entry['price'], entry['size']]
		return trades