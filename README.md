# StonkBot
StonkBot is a Discord bot that fetches stock data based on user commands and queries. StonkBot achieves this using the RealStonks API to fetch information requeseted by the user. Users may fetch data of a single stock at a time or create a list of stocks that will be stored in a databse under their Discord username. Users are allowed up to 10 stocks at a time in their list, and can request the price/volume of all stocks in their list using one command.

*Users are limited to 10 stocks per list as the API can only handle on request per second per user - resulting in up to 10 seconds per response if a user has a full list*

## Commands
- '?price [ticker]' will fetch the price of a given stock
- '?volume [ticker]' will fetch the volume of a stock
- '?list' returns the items in your list and has the following *modifiers*:
  - 'add [ticker]' will add a stock to your list
  - 'remove [ticker]' will remove a stock from your list
  - 'price [ticker]' will return the price of all tickers in your list
  - 'volume [ticker]' will return the volume of all tickers in your list

## Image Examples

