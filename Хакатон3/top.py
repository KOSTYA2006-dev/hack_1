import csv 
 
import numpy as np 
import yfinance as yf 
from pandas import DataFrame, Series 
from scipy.optimize import minimize 
 
with open('shares.csv', encoding="utf8") as csv_file: 
    r = list(csv.DictReader(csv_file, delimiter=',')) 
    r.sort(key=lambda x: list(x.values())[0]) 
    tickers = [i['tickers'] for i in r] 
    count = [int(i['count']) for i in r] 
 
d = DataFrame(count, tickers, ['кол-во акций']).transpose() 
port = Series(map(lambda x: x / sum(count), count), tickers, name='доля акций') 
d = d.append(port * 100) 
 
data = yf.download(tickers, period='3mo')['Adj Close'] 
data_change = data.pct_change() 
cost = data.tail(1).squeeze(axis=0) 
cost.name = 'цена за одну акцию' 
print(cost) 
d = d.append(cost) 
 
daily_yield = data_change.mean() 
daily_yield.name = 'средняя дневная доходность' 
d = d.append(daily_yield) 
 
dividend_yield = daily_yield * 365 / cost * 100 
dividend_yield.name = 'дивидендная доходность' 
d = d.append(dividend_yield) 
 
share_price = cost * count 
share_price.name = 'цена акций' 
d = d.append(share_price) 
 
port_cost = sum(share_price) 
 
p_cost = share_price / port_cost 
p_cost.name = 'доля цены акций' 
d = d.append(p_cost) 
 
print(d.round(1)) 
print(daily_yield) 
print(port_cost, end='\n\n')  # цена портфеля 
 
cov = data_change.cov() 
 
 
def risk(x): 
    x = Series(x, tickers) 
    return np.sqrt(np.matmul(np.matmul(cov.values, x), x)) 
 
 
def d_yield(x): 
    x = Series(x, tickers) 
    return sum(daily_yield * x) 
 
 
print(d_yield(port)) 
print(risk(port)) 
print() 
 
x = Series([0, 0, 0, 0.5, 0, 0.5], tickers, name='доля акций') 
x_share_price = x * port_cost 
print(x_share_price) 
print(cost) 
x_count = x_share_price / cost 
print(x_count) 
x_port = x_count / sum(x_count) 
print(d_yield(x)) 
print(risk(x)) 
print(x_port) 
print(d_yield(x_port)) 
print(risk(x_port)) 
 
p = 2.6852868375966197 
x0 = np.zeros(len(port)) 
# sum(port_cost * x / cost / sum(cost)) 
# list(map(lambda y: y / sum(port_cost * x / cost), port_cost * x / cost)) 
bounds = tuple((0.0, 1.0) for i in range(len(port))) 
con1 = {'type': 'eq', 'fun': lambda x: sum(x) - 1} 
con2 = {'type': 'ineq', 'fun': lambda x: p - risk(x) * 100} 
cons = [con1, con2] 
sol = minimize(lambda x: -d_yield(x), x0, 
               method='SLSQP', bounds=bounds, constraints=cons) 
print(sol.x) 
print(d_yield(sol.x) * 100) 
print(risk(sol.x) * 100)
print(port - Series(sol.x, tickers))