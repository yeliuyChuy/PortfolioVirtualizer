import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

import re
import bs4
import requests
from bs4 import BeautifulSoup

class Stock:
    def __init__(self, ticker_symbol, shares, average_cost, category, ):

        self.ticker_symbol = ticker_symbol
        self.shares = shares
        self.average_cost = average_cost
        self.category = category
        self.stock_data_xml = self.send_request()

        self.cur_value = None
        self.previous_close = None
        self.change = None
        self.percent_change = None
        self.market_value = None
        self.cost = None
        self.todays_return = None
        self.total_return = None

        self.set_stock_prop()

    def set_stock_prop(self):
        self.cur_price = self.get_cur_price()
        self.previous_close = self.get_previous_close()
        self.change = self.get_change()[0]
        self.percent_change = self.get_change()[1]
        self.market_value = self.get_market_value()
        self.cost = self.get_cost()
        self.todays_return = self.get_todays_return()
        self.total_return = self.get_total_return()

    def send_request(self):
        # Send request to Yahoo Finance for the current price of input ticker symbol
        # Concatenate the html link
        stock_on_yf = "https://finance.yahoo.com/quote/" + self.ticker_symbol
        # Send html request
        requests_result = requests.get(stock_on_yf)
        # Pull the data
        stock_in_xml = bs4.BeautifulSoup(requests_result.text, "lxml")

        return stock_in_xml

    def get_cur_price(self):
        # Get Current price
        return float(self.stock_data_xml.find_all("div", {"class":"My(6px) Pos(r) smartphone_Mt(6px)"})[0].find_all("span")[0].text)
    def get_previous_close(self):
        # Get previous close price
        return float(self.stock_data_xml.find_all("tr", {"class":"Bxz(bb) Bdbw(1px) Bdbs(s) Bdc($seperatorColor) H(36px)"})[0].find_all("span")[1].text)
    def get_change(self):
        # Percent Change
        total_change =  self.stock_data_xml.find_all("div", {"class":"My(6px) Pos(r) smartphone_Mt(6px)"})[0].find_all("span")[1].text
        change = float(re.split(r'[()]',total_change)[0])
        percent_change = re.split(r'[()]',total_change)[1]
        return [change, percent_change]
    def get_market_value(self):
        # Market value
        return self.shares * self.cur_price
    def get_cost(self):
        # Cost
        return self.average_cost * self.shares
    def get_todays_return(self):
        #todays return
        return self.shares * self.change
    def get_total_return(self):
        #total return
        return self.market_value - self.cost


class Portfolio:
    def __init__(self, portfolio_csv):
        self.portfolio_df = pd.read_csv(portfolio_csv, index_col=0)

        self.portfolio_list = []
        self.current_price_list = []
        self.previous_close_list = []
        self.change_list = []
        self.percent_change_list = []
        self.market_value_list = []
        self.cost_list = []
        self.todays_return_list = []
        self.total_return_list = []
        self.portfolio_diversity_list = []

        self.read_csv()
        self.expand_df()
        self.compute_portfolio_diversity()
        # self.portfolio_df = self.portfolio_df.set_index('Name')

    def read_csv(self):
        for index, row in self.portfolio_df.iterrows():
            tmp_stock_obj = Stock(ticker_symbol = row['Name'],
                                   shares = row['Shares'],
                                   average_cost = row['Average Cost'],
                                   category = row['Category'])

            self.current_price_list.append(tmp_stock_obj.cur_price)
            self.previous_close_list.append(tmp_stock_obj.previous_close)
            self.change_list.append(tmp_stock_obj.change)
            self.percent_change_list.append(tmp_stock_obj.percent_change)
            self.market_value_list.append(tmp_stock_obj.market_value)
            self.cost_list.append(tmp_stock_obj.cost)
            self.todays_return_list.append(tmp_stock_obj.todays_return)
            self.total_return_list.append(tmp_stock_obj.total_return)
            self.portfolio_list.append(tmp_stock_obj)

    def expand_df(self):
        self.portfolio_df["Current Price"] = self.current_price_list
        self.portfolio_df["Previous Close"] = self.previous_close_list
        self.portfolio_df["Change"] = self.change_list
        self.portfolio_df["Percent Change"] = self.percent_change_list
        self.portfolio_df["Market Value"] = self.market_value_list
        self.portfolio_df["Cost"] = self.cost_list
        self.portfolio_df["Todays Return"] = self.todays_return_list
        self.portfolio_df["Total Return"] = self.total_return_list

    def compute_portfolio_diversity(self):
        # Compute total cost
        total_cost = self.portfolio_df['Cost'].sum()
        #Compute portfolio diversity
        for stock in self.portfolio_list:
            self.portfolio_diversity_list.append(stock.cost/total_cost)
        self.portfolio_df["Portfolio Diversity"] = self.portfolio_diversity_list

    def print(self):
        print(self.portfolio_df)

    def plot(self,x='Category',y='Cost',z='Total Return',size_scalar=10):
        fig = go.Figure(data=go.Scatter3d(
                            x=self.portfolio_df[x],
                            y=self.portfolio_df[y],
                            z=self.portfolio_df[z],
                            hoverinfo="text",
                            text=["<b>{name}</b><br>Change:{change:.2f}({pc})<br>Current Price:{cp:.2f}<br>Average Cost:{ac:.2f}<br>Todays Return:{todayR:.2f}<br>Total Return:{totalR:.2f}<br>Portfolio Diversity:%{pr:.2f}".format(name = row['Name'],
                                    change = row['Change'], pc = row['Percent Change'], ac = row['Average Cost'] ,cp = row['Current Price'],
                                    todayR = row['Todays Return'], totalR = row['Total Return'], pr = row['Portfolio Diversity']*100) for index, row in self.portfolio_df.iterrows()],
                            mode='markers',
                            marker=dict(
                                sizemode='diameter',
                                sizeref=self.portfolio_df['Portfolio Diversity'].max()/size_scalar**2,
                                size=self.portfolio_df['Portfolio Diversity'],
                                color = [float(i.strip('%')) for i in self.portfolio_df['Percent Change']],
                                colorscale = 'rdylgn',
                                colorbar_title = 'Percent<br>Change %',
                                line_color='rgb(140, 140, 170)'
                            )
                        ))

        fig.update_layout(height=800, width=800,
                          title='Examining My Portfolios Return and Change Over Category',
                          scene = dict(xaxis=dict(title=x, titlefont_color='black'),
                                       yaxis=dict(title=y, titlefont_color='black'),
                                       zaxis=dict(title=z, titlefont_color='black')
                           ))
        fig.show()
