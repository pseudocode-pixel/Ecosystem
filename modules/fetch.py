import yfinance as yf

def fetch_stock(symbol, start, end):
    df=yf.download(symbol,start=start,end=end,auto_adjust=True,progress=False)
    return df[['Open','High','Low','Close','Volume']].dropna()

