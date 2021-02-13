# PortfolioVirtualizer
 A web scraper for your stock portfolio visualization.
 
### Background

After the trend of r/wallstreetbets, there were 2 things I realized put me work on this project: 
1. Shame on those brokers who put restriction on trading like what Robinhood did. I'm not the only one who decided to move away from those brokers but still I have to say the interface of Robinhood is good :)
2. I also need a regulator for my investment habits. During the trend of r/wallstreetbets, people were crazy at chasing high and usually they just changed their portfolio unintentionally.

As the result, I made this virtualizer make your portfolio visualization easy to go. It reads a .csv file which contains your portfolio info:
1. Ticker symbol
2. Share number
3. Average cost
4. Category

And it scrapes Yahoo Finance and compute some properties using your given portfolio, and plot it in a 3D scatter.

![](https://github.com/yeliuyChuy/PortfolioVirtualizer/blob/main/demo_pics/Test.gif)
