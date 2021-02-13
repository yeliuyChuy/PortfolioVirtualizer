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
4. Category(Yes, this is ambiguous because everyone has their own evaluation on their holding. But by doing this, you have to think about the type of whay your are holding now and give it ONLY ONE TYPE)

The given example.csv:

| Name  | Shares | Average Cost  | Category |
| :------------ |:---------------:| -----:|
| T | 100 | 26.8 | Blue Chip |
| AAPL | 60 | 114.17 | Income |
| UPWK | 30 | 32.42 | Growth |
| STPK | 20 | 21.95 | Speculative |

The Virtualizer then scrapes Yahoo Finance and compute some properties based on your portfolio, and plot it in a 3D scatter. Feel free to add any feature you want!

![](https://github.com/yeliuyChuy/PortfolioVirtualizer/blob/main/demo_pics/Test.gif)
