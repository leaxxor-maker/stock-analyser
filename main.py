from flask import Flask, render_template_string
import yfinance as yf
from datetime import datetime
import sqlite3
import math
import os

app = Flask(__name__)

COMPANIES = {
    'msft': 'MSFT', 'microsoft': 'MSFT', 'apple': 'AAPL', 'goog': 'GOOGL',
    'google': 'GOOGL', 'amazon': 'AMZN', 'amzn': 'AMZN', 'meta': 'META',
    'facebook': 'META', 'nvda': 'NVDA', 'nvidia': 'NVDA', 'tsla': 'TSLA',
    'tesla': 'TSLA', 'jpm': 'JPM', 'jp': 'JPM', 'v': 'V', 'visa': 'V',
    'unh': 'UNH', 'johnson': 'JNJ', 'jnj': 'JNJ', 'wmt': 'WMT', 'walt': 'WMT',
    'pg': 'PG', 'procter': 'PG', 'xom': 'XOM', 'exxon': 'XOM', 'ma': 'MA',
    'mastercard': 'MA', 'hd': 'HD', 'home': 'HD', 'bac': 'BAC', 'bank': 'BAC',
    'abbv': 'ABBV', 'abbvie': 'ABBV', 'pfe': 'PFE', 'pfizer': 'PFE',
    'avgo': 'AVGO', 'broadcom': 'AVGO', 'ko': 'KO', 'coca': 'KO', 'pep': 'PEP',
    'lliy': 'LLY', 'eli': 'LLY', 'cost': 'COST', 'costco': 'COST', 'aapl': 'AAPL',
    'dis': 'DIS', 'wfc': 'WFC', 'wells': 'WFC', 'csco': 'CSCO', 'cisco': 'CSCO',
    'mcd': 'MCD', 'mcdonald': 'MCD', 'tmo': 'TMO', 'thermo': 'TMO', 'dhr': 'DHR',
    'danaher': 'DHR', 'intc': 'INTC', 'intel': 'INTC', 'amd': 'AMD', 'amdb': 'AMD',
    'qs': 'QS', 'quantumscape': 'QS', 'pltr': 'PLTR', 'palantir': 'PLTR',
    'tsm': 'TSM', 'taiwan': 'TSM', 'nvo': 'NVO', 'novo': 'NVO', 'asml': 'ASML',
    'baba': 'BABA', 'alibaba': 'BABA', 'sbux': 'SBUX', 'starbucks': 'SBUX',
    'nke': 'NKE', 'nike': 'NKE', 'orcl': 'ORCL', 'oracle': 'ORCL', 'crm': 'CRM',
    'salesforce': 'CRM', 'adbe': 'ADBE', 'adobe': 'ADBE', 'pypl': 'PYPL',
    'paypal': 'PYPL', 'sq': 'SQ', 'block': 'SQ', 'shop': 'SHOP', 'shopify': 'SHOP',
    'spot': 'SPOT', 'spotify': 'SPOT', 'net': 'NET', 'cloudflare': 'NET', 'dd': 'DD',
    'datadog': 'DD', 'snow': 'SNOW', 'snowflake': 'SNOW', 'zm': 'ZM', 'zoom': 'ZM',
    'twlo': 'TWLO', 'twilio': 'TWLO', 'ub': 'UB', 'uber': 'UB', 'lyft': 'LYFT',
    'airbnb': 'ABNB', 'abnb': 'ABNB', 'dkng': 'DKNG', 'draftkings': 'DKNG',
    'coin': 'COIN', 'coinbase': 'COIN', 'mu': 'MU', 'micron': 'MU', 'lrcx': 'LRCX',
    'lam': 'LRCX', 'amat': 'AMAT', 'applied': 'AMAT', 'klac': 'KLAC', 'klac': 'KLAC',
    'ter': 'TER', 'teradyne': 'TER', 'qrvo': 'QRVO', 'qorvo': 'QRVO', 'swks': 'SWKS',
    'skyworks': 'SWKS', 'on': 'ON', 'onn': 'ON', 'txn': 'TXN', 'texas': 'TXN',
    'ADI': 'ADI', 'analog': 'ADI', 'mchp': 'MCHP', 'microchip': 'MCHP',
    'mxim': 'MXIM', 'maxim': 'MXIM', 'hpq': 'HPQ', 'hp': 'HPQ', 'dELL': 'DELL',
    'dell': 'DELL', 'lnt': 'LNT', 'atvi': 'ATVI', 'activision': 'ATVI', 'ea': 'EA',
    'electronic': 'EA', 'ttwo': 'TTWO', 'take2': 'TTWO', 'ubisoft': 'UBSFY',
    'ubisfy': 'UBSFY', 'ntdo': 'NTDOY', 'nintendo': 'NTDOY', 'se': 'SE',
    'sea': 'SE', 'ntf': 'NTF', 'roku': 'ROKU', 'nflx': 'NFLX', 'netflix': 'NFLX',
    'disney': 'DIS', 'dis': 'DIS', 'cmcsa': 'CMCSA', 'comcast': 'CMCSA',
    'chtr': 'CHTR', 'charter': 'CHTR', 't': 'T', 'att': 'T', 'vz': 'VZ',
    'verizon': 'VZ', 'tmus': 'TMUS', 'tmobile': 'TMUS', 'amzn': 'AMZN',
    'cvx': 'CVX', 'chevron': 'CVX', 'bp': 'BP', 'shell': 'SHEL', 'shel': 'SHEL',
    'total': 'TOT', 'tot': 'TOT', 'enbk': 'ENBK', 'ener': 'ENBK', 'slb': 'SLB',
    'schlumberger': 'SLB', 'hal': 'HAL', 'halliburton': 'HAL', 'oih': 'OIH',
    'slbh': 'SLBH', 'xies': 'XLE', 'energy': 'XLE', 'f': 'F', 'ford': 'F', 'gm': 'GM',
    'general': 'GM', 'tm': 'TM', 'toyota': 'TM', 'hmc': 'HMC', 'honda': 'HMC',
    'fca': 'STLA', 'fiat': 'STLA', 'stla': 'STLA', 'racing': 'RACE', 'ferrari': 'RACE',
    'rmbl': 'RMBL', 'rumble': 'RMBL', 'parasolid': 'PslXd', 'tandem': 'TNDM',
    ' TandemDmi': 'TNDM', 'autodesk': 'ADSK', 'adsk': 'ADSK', 'ansys': 'ANSS',
    'anss': 'ANSS', 'cdns': 'CDNS', 'cadence': 'CDNS', 'snps': 'SNPS', 'synopsy': 'SNPS',
    'mrvl': 'MRVL', 'marvell': 'MRVL', 'ipgphotobook': 'IPGP', 'ipg': 'IPGP',
    'lmlr': 'LMLR', 'luminar': 'LMLR', 'laZR': 'LAZR', 'lazard': 'LAZR', 'gs': 'GS',
    'goldman': 'GS', 'ms': 'MS', 'morgan': 'MS', 'blsk': 'BLSK', 'bluescope': 'BLSK',
    'axp': 'AXP', 'american': 'AXP', 'c': 'C', 'citi': 'C', 'schw': 'SCHW',
    'charles': 'SCHW', 'ax': 'AX', 'ax', 'trin': 'TRIN', 'spgi': 'SPGI',
    'spglobal': 'SPGI', 'mktx': 'MKTX', 'market': 'MKTX', 'ice': 'ICE', 'intercont': 'ICE',
    'ndaq': 'NDAQ', 'nasdaq': 'NDAQ', 'ibo': 'IBO', 'ibobot': 'IBO', 'morn': 'MORN',
    'morningstar': 'MORN', 'bfam': 'BFAM', ' pearson': 'PSO', 'hlf': 'HLF',
    'herbalife': 'HLF', 'chln': 'CHLN', 'charleston': 'CHLN', 'i': 'I', 'intuit': 'INTU',
    'intu': 'INTU', 'wtw': 'WTW', 'willis': 'WTW', 'aon': 'AON', 'ajg': 'AJG',
    'arthur': 'AJG', 'Marsh': 'MMC', 'marsh': 'MMC', 'mmc': 'MMC', 'spgi': 'SPGI',
    'spglobal': 'SPGI', 'dlo': 'DLO', 'dlocal': 'DLO', 'visa': 'V', 'ma': 'MA',
    'mastercard': 'MA', 'pypl': 'PYPL', 'paypal': 'PYPL', 'sq': 'SQ', 'block': 'SQ',
    'afrm': 'AFRM', 'affirm': 'AFRM', 'asai': 'ASAI', 'assurant': 'ASAI', 'brk': 'BRK',
    'berkshire': 'BRK', 'blt': 'BLT', 'blmx': 'BLT', 'cboe': 'CBOE', 'cinf': 'CINF',
    'cincinnati': 'CINF', 'cna': 'CNA', 'come': 'CNA', 'econg': 'ECONG', 'econg': 'EVO',
    'etn': 'ETN', 'eaton': 'ETN', 'emr': 'EMR', 'emerson': 'EMR', 'fdx': 'FDX',
    'fedex': 'FDX', 'gen': 'GEN', 'gen': 'GEN', 'gild': 'GILD', 'gilead': 'GILD',
    'glw': 'GLW', 'corning': 'GLW', 'gs': 'GS', 'goldman': 'GS', 'hlt': 'HLT',
    'hilton': 'HLT', 'hsy': 'HSY', 'hershey': 'HSY', 'ibm': 'IBM', 'intc': 'INTC',
    'intel': 'INTC', 'j': 'J', 'jacobs': 'J', 'jnj': 'JNJ', 'johnson': 'JNJ', 'jpm': 'JPM',
    'jp': 'JPM', 'k': 'K', 'kellogg': 'K', 'ko': 'KO', 'coca': 'KO', 'leg': 'LEG',
    'leggett': 'LEG', 'lmt': 'LMT', 'lockheed': 'LMT', 'lyb': 'LYB', 'lyondell': 'LYB',
    'mcd': 'MCD', 'mcdonald': 'MCD', 'mmm': 'MMM', 'mmm': 'MMM', 'mo': 'MO', 'altria': 'MO',
    'mrk': 'MRK', 'merck': 'MRK', 'nsc': 'NSC', 'norfolk': 'NSC', 'nue': 'NUE',
    'nucor': 'NUE', 'pcar': 'PCAR', 'paccar': 'PCAR', 'pg': 'PG', 'procter': 'PG',
    'ph': 'PH', 'ph': 'PH', 'pnc': 'PNC', 'pnc': 'PNC', 'pru': 'PRU', 'prudent': 'PRU',
    'psy': 'Psy', 'psy': 'Psy', 'rtx': 'RTX', 'raytheon': 'RTX', 'sre': 'SRE',
    'sempra': 'SRE', 'spgi': 'SPGI', 'spglobal': 'SPGI', 'stz': 'STZ', 'constell': 'STZ',
    't': 'T', 'att': 'T', 'tap': 'TAP', 'molson': 'TAP', 'tsn': 'TSN', 'tyson': 'TSN',
    'unh': 'UNH', 'united': 'UNH', 'unp': 'UNP', 'union': 'UNP', 'utx': 'UTX',
    'unitedtech': 'UTX', 'v': 'V', 'visa': 'V', 'vlo': 'VLO', 'valero': 'VLO', 'vz': 'VZ',
    'verizon': 'VZ', 'wab': 'WAB', 'westing': 'WAB', 'wmb': 'WMB', 'williams': 'WMB',
    'wmt': 'WMT', 'walt': 'WMT', 'wynn': 'WYNN', 'wynn': 'WYNN', 'yum': 'YUM',
    'yum': 'YUM', 'zion': 'ZION', 'zionsb': 'ZION', 'spy': 'SPY', 'qqq': 'QQQ',
    'iwm': 'IWM', 'dia': 'DIA', 'tlt': 'TLT', 'gld': 'GLD', 'slv': 'SLV', 'bitq': 'BITQ',
    'bitcoin': 'BITQ', 'sqft': 'SQFT', 'ark': 'ARKK', 'arkk': 'ARKK', 'soxl': 'SOXL',
    'tesla': 'TSLA', 'tsla': 'TSLA', 'nio': 'NIO', 'xpev': 'XPEV', 'li': 'LI', 'rivn': 'RIVN',
    'f': 'F', 'ford': 'F', 'gm': 'GM', 'tm': 'TM', 'hpq': 'HPQ', 'dELL': 'DELL',
}

def get_db():
    conn = sqlite3.connect('analyses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS analyses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, ticker TEXT, date TEXT,
                  score REAL, price REAL, target_buy REAL, sector TEXT,
                  pe_ratio REAL, peg_ratio REAL, de_ratio REAL, roe REAL,
                  revenue_growth REAL, profit_margin REAL, operating_margin REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS portfolio
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, ticker TEXT, shares REAL,
                  avg_price REAL, date_added TEXT)''')
    conn.commit()
    return conn

def get_info(ticker):
    try:
        stock = yf.Ticker(ticker)
        return stock.info
    except:
        return {}

def calc_rsi(prices, period=14):
    if len(prices) < period + 1:
        return None
    deltas = prices.diff()
    gain = deltas.where(deltas > 0, 0).rolling(window=period).mean()
    loss = (-deltas.where(deltas < 0, 0)).rolling(window=period).mean()
    rs = gain / loss.replace(0, float('inf'))
    return 100 - (100 / (1 + rs)).iloc[-1]

def calc_ma(prices, period):
    if len(prices) < period:
        return None
    return prices.rolling(window=period).mean().iloc[-1]

def analyze_stock(ticker):
    info = get_info(ticker)
    if not info or 'regularMarketPrice' not in info:
        return None

    price = info.get('regularMarketPrice', 0)
    name = info.get('shortName', ticker)
    sector = info.get('sector', 'Unknown')
    industry = info.get('industry', 'Unknown')
    
    pe = info.get('trailingPE', 0) or 0
    fwd_pe = info.get('forwardPE', 0) or 0
    peg = info.get('pegRatio', 0) or 0
    pb = info.get('priceToBook', 0) or 0
    ps = info.get('priceToSalesTrailing12Months', 0) or 0
    de = info.get('debtToEquity', 0) or 0
    rc = info.get('currentRatio', 0) or 0
    cr = info.get('cashRatio', 0) or 0
    roe = info.get('returnOnEquity', 0) or 0
    roa = info.get('returnOnAssets', 0) or 0
    roic = info.get('roi', 0) or 0
    mg = info.get('profitMargins', 0) or 0
    om = info.get('operatingMargins', 0) or 0
    gm = info.get('grossMargins', 0) or 0
    rev_growth = info.get('revenueGrowth', 0) or 0
    earn_growth = info.get('earningsGrowth', 0) or 0
    fcf = info.get('freeCashflow', 0) or 0
    ocf = info.get('operatingCashflow', 0) or 0
    total_cash = info.get('totalCash', 0) or 0
    total_debt = info.get('totalDebt', 0) or 0
    shares = info.get('sharesOutstanding', 0) or 0
    mcap = info.get('marketCap', 0) or 0
    week52_high = info.get('fiftyTwoWeekHigh', 0) or 0
    week52_low = info.get('fiftyTwoWeekLow', 0) or 0
    avg_volume = info.get('averageVolume', 0) or 0
    beta = info.get('beta', 0) or 0
    div_yield = info.get('dividendYield', 0) or 0
    
    try:
        hist = yf.Ticker(ticker).history(period='1y')
        prices = hist['Close']
        rsi = calc_rsi(prices)
        ma50 = calc_ma(prices, 50)
        ma200 = calc_ma(prices, 200)
        current_price = prices.iloc[-1]
        
        if len(prices) > 20:
            support = prices.rolling(window=20).min().iloc[-1]
            resistance = prices.rolling(window=20).max().iloc[-1]
        else:
            support, resistance = price * 0.9, price * 1.1
        
        trend = 'UPTREND' if ma50 and ma200 and ma50 > ma200 else 'DOWNTREND' if ma50 and ma200 else 'NEUTRAL'
    except:
        rsi, ma50, ma200, support, resistance, trend = None, None, None, price * 0.9, price * 1.1, 'NEUTRAL'

    scores = {}
    
    if pe > 0 and pe < 100:
        scores['pe'] = 10 if pe < 15 else 8 if pe < 20 else 6 if pe < 25 else 4 if pe < 35 else 2
    else:
        scores['pe'] = 5
    scores['fwd_pe'] = 10 if fwd_pe < 15 else 8 if fwd_pe < 20 else 6 if fwd_pe < 30 else 3
    scores['peg'] = 10 if peg < 1 else 8 if peg < 1.5 else 6 if peg < 2 else 4 if peg < 3 else 2
    scores['pb'] = 10 if pb < 2 else 8 if pb < 4 else 6 if pb < 6 else 4 if pb < 10 else 2
    scores['ps'] = 10 if ps < 2 else 8 if ps < 5 else 6 if ps < 10 else 3
    
    scores['roe'] = 10 if roe > 0.20 else 8 if roe > 0.15 else 6 if roe > 0.10 else 4 if roe > 0.05 else 2
    scores['roa'] = 10 if roa > 0.10 else 8 if roa > 0.05 else 6 if roa > 0.02 else 3
    scores['roic'] = 10 if roic > 0.15 else 8 if roic > 0.10 else 6 if roic > 0.05 else 3
    
    scores['profit_margin'] = 10 if mg > 0.20 else 8 if mg > 0.15 else 6 if mg > 0.10 else 4 if mg > 0.05 else 2
    scores['op_margin'] = 10 if om > 0.20 else 8 if om > 0.15 else 6 if om > 0.10 else 4 if om > 0.05 else 2
    scores['gross_margin'] = 10 if gm > 0.40 else 8 if gm > 0.30 else 6 if gm > 0.20 else 4 if gm > 0.10 else 2
    
    scores['rev_growth'] = 10 if rev_growth > 0.20 else 8 if rev_growth > 0.10 else 6 if rev_growth > 0.05 else 4 if rev_growth > 0 else 2
    scores['earn_growth'] = 10 if earn_growth > 0.20 else 8 if earn_growth > 0.10 else 6 if earn_growth > 0.05 else 3
    
    scores['de'] = 10 if de < 0.5 else 8 if de < 1 else 6 if de < 2 else 4 if de < 3 else 2
    scores['rc'] = 10 if rc > 2 else 8 if rc > 1.5 else 6 if rc > 1 else 4 if rc > 0.5 else 2
    scores['cr'] = 10 if cr > 1 else 8 if cr > 0.5 else 6 if cr > 0.2 else 3
    
    scores['fcf_ratio'] = 10 if fcf > 0 and price > 0 and fcf / (shares * price) > 0.05 else 6 if fcf > 0 else 3
    scores['ocf_ratio'] = 10 if ocf > 0 and om > 0.1 else 6 if ocf > 0 else 3
    
    if total_cash > total_debt:
        scores['cash_debt'] = 10
    elif total_cash > total_debt * 0.5:
        scores['cash_debt'] = 8
    elif total_cash > 0:
        scores['cash_debt'] = 6
    else:
        scores['cash_debt'] = 3
    
    valuation = (scores['pe'] * 2 + scores['fwd_pe'] + scores['peg'] + scores['pb'] + scores['ps']) / 6 * 0.25
    profitability = (scores['roe'] + scores['roa'] + scores['roic']) / 3 * 0.20
    growth = (scores['rev_growth'] + scores['earn_growth'] + scores['profit_margin'] + scores['op_margin']) / 4 * 0.20
    solvency = (scores['de'] + scores['rc'] + scores['cr']) / 3 * 0.15
    cash_flow = (scores['fcf_ratio'] + scores['ocf_ratio'] + scores['cash_debt']) / 3 * 0.10
    quality = (scores['gross_margin'] + scores['profit_margin'] + scores['op_margin']) / 3 * 0.07
    momentum = (10 - abs(rsi - 50) / 5) if rsi else 5
    momentum = max(0, min(10, momentum)) * 0.03
    
    total_score = valuation + profitability + growth + solvency + cash_flow + quality + momentum
    
    if week52_high > week52_low:
        distance_high = (week52_high - price) / week52_high * 100
        distance_low = (price - week52_low) / week52_low * 100
    else:
        distance_high, distance_low = 0, 0

    pe_ratio = pe
    target_buy = price * 0.75 if total_score > 7 else price * 0.85 if total_score > 6 else price * 0.90

    return {
        'ticker': ticker, 'name': name, 'sector': sector, 'industry': industry,
        'price': price, 'score': total_score, 'target_buy': target_buy,
        'pe_ratio': pe_ratio, 'fwd_pe': fwd_pe, 'peg': peg, 'pb': pb, 'ps': ps,
        'de': de, 'rc': rc, 'cr': cr, 'roe': roe, 'roa': roa, 'roic': roic,
        'mg': mg, 'om': om, 'gm': gm, 'rev_growth': rev_growth, 'earn_growth': earn_growth,
        'fcf': fcf, 'ocf': ocf, 'total_cash': total_cash, 'total_debt': total_debt,
        'mcap': mcap, 'shares': shares, 'week52_high': week52_high, 'week52_low': week52_low,
        'distance_high': distance_high, 'distance_low': distance_low,
        'rsi': rsi, 'ma50': ma50, 'ma200': ma200, 'support': support, 'resistance': resistance,
        'trend': trend, 'beta': beta, 'div_yield': div_yield, 'avg_volume': avg_volume,
        'scores': scores
    }

def get_news_links(ticker):
    return {
        'yahoo': f'https://finance.yahoo.com/quote/{ticker}',
        'seeking': f'https://seekingalpha.com/symbol/{ticker}',
        'benzinga': f'https://www.benzinga.com/stock-articles/{ticker}',
        'finviz': f'https://finviz.com/quote.ashx?t={ticker}',
        'marketwatch': f'https://www.marketwatch.com/investing/stock/{ticker}',
        'cnbc': f'https://www.cnbc.com/quotes/{ticker}',
    }

HOMEPAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Stock Analyzer Pro v2</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0a0a0f; color: #e0e0e0; min-height: 100vh; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        h1 { color: #00d4ff; text-align: center; margin-bottom: 30px; font-size: 2em; }
        .search-box { display: flex; gap: 10px; justify-content: center; margin-bottom: 30px; }
        input { padding: 15px 20px; font-size: 18px; border: 2px solid #333; border-radius: 10px; background: #1a1a25; color: #fff; width: 300px; }
        button { padding: 15px 30px; font-size: 18px; background: #00d4ff; color: #000; border: none; border-radius: 10px; cursor: pointer; font-weight: bold; }
        button:hover { background: #00b8e6; }
        .card { background: #12121a; border-radius: 15px; padding: 25px; margin-bottom: 20px; border: 1px solid #222; }
        .ticker { color: #00d4ff; font-size: 2em; font-weight: bold; }
        .name { color: #888; font-size: 1.2em; margin-bottom: 10px; }
        .score { font-size: 3em; font-weight: bold; text-align: center; }
        .score-good { color: #00ff88; } .score-medium { color: #ffaa00; } .score-bad { color: #ff4444; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 20px; }
        .stat { background: #1a1a25; padding: 15px; border-radius: 10px; text-align: center; }
        .stat-label { color: #666; font-size: 0.85em; margin-bottom: 5px; }
        .stat-value { font-size: 1.4em; font-weight: bold; color: #fff; }
        .stat-good { color: #00ff88; } .stat-medium { color: #ffaa00; } .stat-bad { color: #ff4444; }
        .news-links { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 20px; }
        .news-link { background: #1a1a25; padding: 10px 20px; border-radius: 25px; color: #00d4ff; text-decoration: none; font-size: 0.9em; }
        .news-link:hover { background: #222; }
        .nav { display: flex; gap: 10px; justify-content: center; margin-bottom: 20px; flex-wrap: wrap; }
        .nav a { padding: 10px 20px; background: #1a1a25; color: #00d4ff; text-decoration: none; border-radius: 25px; }
        .nav a:hover { background: #222; }
        .macro-card { background: #12121a; border-radius: 10px; padding: 15px; margin-bottom: 10px; }
        .positive { color: #00ff88; } .negative { color: #ff4444; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #333; }
        th { color: #00d4ff; }
        .buy { background: #00ff88; color: #000; padding: 5px 15px; border-radius: 5px; font-weight: bold; }
        .sell { background: #ff4444; color: #fff; padding: 5px 15px; border-radius: 5px; font-weight: bold; }
        .hold { background: #ffaa00; color: #000; padding: 5px 15px; border-radius: 5px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Stock Analyzer Pro v2</h1>
        <form action="/analyze" method="get" class="search-box">
            <input type="text" name="ticker" placeholder="Enter ticker (AAPL, msft...)">
            <button type="submit">Analyze</button>
        </form>
        <div class="nav">
            <a href="/">Home</a>
            <a href="/portfolio">Portfolio</a>
            <a href="/saved">Saved Analyses</a>
            <a href="/macro">Macro Calendar</a>
        </div>
        <p style="text-align: center; color: #666;">Enter any ticker symbol (MSFT, AAPL, TSLA...) or company name</p>
    </div>
</body>
</html>
'''

ANALYSIS_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>{{ ticker }} - Analysis</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0a0a0f; color: #e0e0e0; min-height: 100vh; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        h1 { color: #00d4ff; margin-bottom: 5px; }
        .name { color: #888; margin-bottom: 20px; }
        .nav { display: flex; gap: 10px; justify-content: center; margin-bottom: 20px; flex-wrap: wrap; }
        .nav a { padding: 10px 20px; background: #1a1a25; color: #00d4ff; text-decoration: none; border-radius: 25px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 20px; }
        .card { background: #12121a; border-radius: 15px; padding: 25px; margin-bottom: 20px; border: 1px solid #222; }
        .ticker { color: #00d4ff; font-size: 2em; font-weight: bold; }
        .score { font-size: 4em; font-weight: bold; text-align: center; margin: 20px 0; }
        .score-good { color: #00ff88; } .score-medium { color: #ffaa00; } .score-bad { color: #ff4444; }
        .stat { background: #1a1a25; padding: 15px; border-radius: 10px; text-align: center; }
        .stat-label { color: #666; font-size: 0.85em; margin-bottom: 5px; }
        .stat-value { font-size: 1.4em; font-weight: bold; color: #fff; }
        .stat-good { color: #00ff88; } .stat-medium { color: #ffaa00; } .stat-bad { color: #ff4444; }
        .news-links { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 20px; }
        .news-link { background: #1a1a25; padding: 10px 20px; border-radius: 25px; color: #00d4ff; text-decoration: none; font-size: 0.9em; }
        .buy-target { background: #00ff88; color: #000; padding: 20px; border-radius: 10px; text-align: center; margin-top: 20px; font-size: 1.5em; font-weight: bold; }
        .section-title { color: #00d4ff; margin: 20px 0 10px 0; font-size: 1.2em; }
        .recommendation { padding: 20px; border-radius: 10px; text-align: center; font-size: 1.5em; font-weight: bold; margin-top: 20px; }
        .buy { background: rgba(0,255,136,0.2); color: #00ff88; border: 2px solid #00ff88; }
        .sell { background: rgba(255,68,68,0.2); color: #ff4444; border: 2px solid #ff4444; }
        .hold { background: rgba(255,170,0,0.2); color: #ffaa00; border: 2px solid #ffaa00; }
        .positive { color: #00ff88; } .negative { color: #ff4444; }
        table { width: 100%%; border-collapse: collapse; margin-top: 15px; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #333; }
        th { color: #00d4ff; }
    </style>
</head>
<body>
    <div class="container">
        <div class="nav">
            <a href="/">Home</a>
            <a href="/portfolio">Portfolio</a>
            <a href="/saved">Saved Analyses</a>
            <a href="/macro">Macro Calendar</a>
        </div>
        <div class="card">
            <div class="ticker">{{ data.ticker }}</div>
            <div class="name">{{ data.name }} | {{ data.sector }} | {{ data.industry }}</div>
            <div class="score {% if data.score >= 7 %}score-good{% elif data.score >= 5 %}score-medium{% else %}score-bad{% endif %}">
                {{ "%.1f"|format(data.score) }}/10
            </div>
            <div style="text-align: center; color: #888;">
                {% if data.score >= 7 %}EXCELLENT{% elif data.score >= 5 %}GOOD{% else %}WEAK{% endif %} - 
                {% if data.score >= 7 %}STRONG BUY{% elif data.score >= 5 %}HOLD{% else %}AVOID{% endif %}
            </div>
        </div>
        
        <div class="card">
            <div class="section-title">PRICE & VALUATION</div>
            <div class="grid">
                <div class="stat">
                    <div class="stat-label">Current Price</div>
                    <div class="stat-value">${{ "%.2f"|format(data.price) }}</div>
                </div>
                <div class="stat">
                    <div class="stat-label">P/E Ratio</div>
                    <div class="stat-value {% if data.pe_ratio < 25 %}stat-good{% elif data.pe_ratio < 40 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.pe_ratio) if data.pe_ratio else 'N/A' }}</div>
                </div>
                <div class="stat">
                    <div class="stat-label">Forward P/E</div>
                    <div class="stat-value {% if data.fwd_pe < 20 %}stat-good{% elif data.fwd_pe < 35 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.fwd_pe) if data.fwd_pe else 'N/A' }}</div>
                </div>
                <div class="stat">
                    <div class="stat-label">PEG Ratio</div>
                    <div class="stat-value {% if data.peg < 1.5 %}stat-good{% elif data.peg < 3 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.2f"|format(data.peg) if data.peg else 'N/A' }}</div>
                </div>
                <div class="stat">
                    <div class="stat-label">P/B Ratio</div>
                    <div class="stat-value {% if data.pb < 5 %}stat-good{% elif data.pb < 10 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.pb) if data.pb else 'N/A' }}</div>
                </div>
                <div class="stat">
                    <div class="stat-label">P/S Ratio</div>
                    <div class="stat-value {% if data.ps < 5 %}stat-good{% elif data.ps < 10 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.ps) if data.ps else 'N/A' }}</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <div class="section-title">PROFITABILITY</div>
            <div class="grid">
                <div class="stat">
                    <div class="stat-label">ROE</div>
                    <div class="stat-value {% if data.roe > 0.15 %}stat-good{% elif data.roe > 0.08 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.roe * 100) if data.roe else 'N/A' }}%</div>
                </div>
                <div class="stat">
                    <div class="stat-label">ROA</div>
                    <div class="stat-value {% if data.roa > 0.05 %}stat-good{% elif data.roa > 0.02 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.roa * 100) if data.roa else 'N/A' }}%</div>
                </div>
                <div class="stat">
                    <div class="stat-label">ROIC</div>
                    <div class="stat-value {% if data.roic > 0.15 %}stat-good{% elif data.roic > 0.08 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.roic) if data.roic else 'N/A' }}%</div>
                </div>
                <div class="stat">
                    <div class="stat-label">Profit Margin</div>
                    <div class="stat-value {% if data.mg > 0.15 %}stat-good{% elif data.mg > 0.05 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.mg * 100) if data.mg else 'N/A' }}%</div>
                </div>
                <div class="stat">
                    <div class="stat-label">Operating Margin</div>
                    <div class="stat-value {% if data.om > 0.15 %}stat-good{% elif data.om > 0.08 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.om * 100) if data.om else 'N/A' }}%</div>
                </div>
                <div class="stat">
                    <div class="stat-label">Gross Margin</div>
                    <div class="stat-value {% if data.gm > 0.30 %}stat-good{% elif data.gm > 0.20 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.gm * 100) if data.gm else 'N/A' }}%</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <div class="section-title">GROWTH</div>
            <div class="grid">
                <div class="stat">
                    <div class="stat-label">Revenue Growth</div>
                    <div class="stat-value {% if data.rev_growth > 0.10 %}stat-good{% elif data.rev_growth > 0 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.rev_growth * 100) if data.rev_growth else 'N/A' }}%</div>
                </div>
                <div class="stat">
                    <div class="stat-label">Earnings Growth</div>
                    <div class="stat-value {% if data.earn_growth > 0.10 %}stat-good{% elif data.earn_growth > 0 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.earn_growth * 100) if data.earn_growth else 'N/A' }}%</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <div class="section-title">SOLVENCY</div>
            <div class="grid">
                <div class="stat">
                    <div class="stat-label">D/E Ratio</div>
                    <div class="stat-value {% if data.de < 1 %}stat-good{% elif data.de < 2 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.de) if data.de else 'N/A' }}</div>
                </div>
                <div class="stat">
                    <div class="stat-label">Current Ratio</div>
                    <div class="stat-value {% if data.rc > 1.5 %}stat-good{% elif data.rc > 1 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.2f"|format(data.rc) if data.rc else 'N/A' }}</div>
                </div>
                <div class="stat">
                    <div class="stat-label">Cash Ratio</div>
                    <div class="stat-value {% if data.cr > 0.5 %}stat-good{% elif data.cr > 0.2 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.2f"|format(data.cr) if data.cr else 'N/A' }}</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <div class="section-title">CASH FLOW</div>
            <div class="grid">
                <div class="stat">
                    <div class="stat-label">Free Cash Flow</div>
                    <div class="stat-value {% if data.fcf > 0 %}stat-good{% else %}stat-bad{% endif %}">${{ "%.0f"|format(data.fcf / 1e9) if data.fcf else 0 }}B</div>
                </div>
                <div class="stat">
                    <div class="stat-label">Operating Cash Flow</div>
                    <div class="stat-value {% if data.ocf > 0 %}stat-good{% else %}stat-bad{% endif %}">${{ "%.0f"|format(data.ocf / 1e9) if data.ocf else 0 }}B</div>
                </div>
                <div class="stat">
                    <div class="stat-label">Cash</div>
                    <div class="stat-value">${{ "%.0f"|format(data.total_cash / 1e9) if data.total_cash else 0 }}B</div>
                </div>
                <div class="stat">
                    <div class="stat-label">Total Debt</div>
                    <div class="stat-value">${{ "%.0f"|format(data.total_debt / 1e9) if data.total_debt else 0 }}B</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <div class="section-title">TECHNICAL ANALYSIS</div>
            <div class="grid">
                <div class="stat">
                    <div class="stat-label">RSI (14)</div>
                    <div class="stat-value {% if data.rsi and data.rsi < 30 %}stat-good{% elif data.rsi and data.rsi > 70 %}stat-bad{% endif %}">{{ "%.1f"|format(data.rsi) if data.rsi else 'N/A' }}</div>
                </div>
                <div class="stat">
                    <div class="stat-label">MA 50</div>
                    <div class="stat-value">${{ "%.2f"|format(data.ma50) if data.ma50 else 'N/A' }}</div>
                </div>
                <div class="stat">
                    <div class="stat-label">MA 200</div>
                    <div class="stat-value">${{ "%.2f"|format(data.ma200) if data.ma200 else 'N/A' }}</div>
                </div>
                <div class="stat">
                    <div class="stat-label">Support</div>
                    <div class="stat-value">${{ "%.2f"|format(data.support) if data.support else 'N/A' }}</div>
                </div>
                <div class="stat">
                    <div class="stat-label">Resistance</div>
                    <div class="stat-value">${{ "%.2f"|format(data.resistance) if data.resistance else 'N/A' }}</div>
                </div>
                <div class="stat">
                    <div class="stat-label">Trend</div>
                    <div class="stat-value {% if data.trend == 'UPTREND' %}stat-good{% elif data.trend == 'DOWNTREND' %}stat-bad{% endif %}">{{ data.trend }}</div>
                </div>
                <div class="stat">
                    <div class="stat-label">52W High</div>
                    <div class="stat-value">${{ "%.2f"|format(data.week52_high) if data.week52_high else 'N/A' }}</div>
                </div>
                <div class="stat">
                    <div class="stat-label">52W Low</div>
                    <div class="stat-value">${{ "%.2f"|format(data.week52_low) if data.week52_low else 'N/A' }}</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <div class="section-title">BUY TARGET</div>
            <div class="buy-target">
                Target Buy Price: ${{ "%.2f"|format(data.target_buy) }}
                <div style="font-size: 0.6em; margin-top: 10px; color: #888;">
                    ({{ "%.0f"|format((data.target_buy / data.price - 1) * 100) }}%% discount)
                </div>
            </div>
            <div style="margin-top: 20px; padding: 20px; background: #1a1a25; border-radius: 10px;">
                <h3 style="color: #00d4ff; margin-bottom: 10px;">Market Cap: ${{ "%.0f"|format(data.mcap / 1e12) if data.mcap else 0 }}T</h3>
                <p>BETA: {{ "%.2f"|format(data.beta) if data.beta else 'N/A' }} | 
                Dividend: {{ "%.2f"|format(data.div_yield * 100) if data.div_yield else 0 }}%% | 
                Volume: {{ "%.0f"|format(data.avg_volume / 1e6) if data.avg_volume else 0 }}M</p>
            </div>
        </div>
        
        <div class="card">
            <div class="section-title">NEWS & INFO</div>
            <div class="news-links">
                <a href="{{ news.yahoo }}" target="_blank" class="news-link">Yahoo Finance</a>
                <a href="{{ news.seeking }}" target="_blank" class="news-link">Seeking Alpha</a>
                <a href="{{ news.benzinga }}" target="_blank" class="news-link">Benzinga</a>
                <a href="{{ news.finviz }}" target="_blank" class="news-link">Finviz</a>
                <a href="{{ news.marketwatch }}" target="_blank" class="news-link">MarketWatch</a>
                <a href="{{ news.cnbc }}" target="_blank" class="news-link">CNBC</a>
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <a href="/save/{{ data.ticker }}" style="background: #00d4ff; color: #000; padding: 15px 30px; border-radius: 10px; text-decoration: none; font-weight: bold;">Save Analysis</a>
            <a href="/add/{{ data.ticker }}" style="background: #00ff88; color: #000; padding: 15px 30px; border-radius: 10px; text-decoration: none; font-weight: bold; margin-left: 10px;">Add to Portfolio</a>
        </div>
    </div>
</body>
</html>
'''

PORTFOLIO_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Portfolio</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0a0a0f; color: #e0e0e0; min-height: 100vh; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        h1 { color: #00d4ff; margin-bottom: 20px; }
        .nav { display: flex; gap: 10px; justify-content: center; margin-bottom: 20px; flex-wrap: wrap; }
        .nav a { padding: 10px 20px; background: #1a1a25; color: #00d4ff; text-decoration: none; border-radius: 25px; }
        table { width: 100%%; border-collapse: collapse; }
        th, td { padding: 15px; text-align: left; border-bottom: 1px solid #333; }
        th { color: #00d4ff; }
        .total { font-size: 2em; font-weight: bold; color: #00ff88; text-align: right; margin: 20px 0; }
        .positive { color: #00ff88; } .negative { color: #ff4444; }
        .card { background: #12121a; border-radius: 15px; padding: 25px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>My Portfolio</h1>
        <div class="nav">
            <a href="/">Home</a>
            <a href="/portfolio">Portfolio</a>
            <a href="/saved">Saved Analyses</a>
            <a href="/macro">Macro Calendar</a>
        </div>
        {{ content|safe }}
    </div>
</body>
</html>
'''

MACRO_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Macro Calendar</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0a0a0f; color: #e0e0e0; min-height: 100vh; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        h1 { color: #00d4ff; margin-bottom: 20px; }
        .nav { display: flex; gap: 10px; justify-content: center; margin-bottom: 20px; flex-wrap: wrap; }
        .nav a { padding: 10px 20px; background: #1a1a25; color: #00d4ff; text-decoration: none; border-radius: 25px; }
        .macro-card { background: #12121a; border-radius: 10px; padding: 20px; margin-bottom: 15px; }
        .macro-title { color: #fff; font-size: 1.2em; font-weight: bold; margin-bottom: 10px; }
        .macro-date { color: #00d4ff; margin-bottom: 5px; }
        .macro-impact { display: inline-block; padding: 3px 10px; border-radius: 5px; font-size: 0.85em; margin-left: 10px; }
        .high { background: #ff4444; color: #fff; }
        .medium { background: #ffaa00; color: #000; }
        .low { background: #00d4ff; color: #000; }
        .positive { color: #00ff88; } .negative { color: #ff4444; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Macro Economic Calendar</h1>
        <div class="nav">
            <a href="/">Home</a>
            <a href="/portfolio">Portfolio</a>
            <a href="/saved">Saved Analyses</a>
            <a href="/macro">Macro Calendar</a>
        </div>
        {{ content|safe }}
    </div>
</body>
</html>
'''

SAVED_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Saved Analyses</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0a0a0f; color: #e0e0e0; min-height: 100vh; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        h1 { color: #00d4ff; margin-bottom: 20px; }
        .nav { display: flex; gap: 10px; justify-content: center; margin-bottom: 20px; flex-wrap: wrap; }
        .nav a { padding: 10px 20px; background: #1a1a25; color: #00d4ff; text-decoration: none; border-radius: 25px; }
        table { width: 100%%; border-collapse: collapse; }
        th, td { padding: 15px; text-align: left; border-bottom: 1px solid #333; }
        th { color: #00d4ff; }
        .score { font-weight: bold; }
        .score-good { color: #00ff88; } .score-medium { color: #ffaa00; } .score-bad { color: #ff4444; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Saved Analyses</h1>
        <div class="nav">
            <a href="/">Home</a>
            <a href="/portfolio">Portfolio</a>
            <a href="/saved">Saved Analyses</a>
            <a href="/macro">Macro Calendar</a>
        </div>
        {{ content|safe }}
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HOMEPAGE)

@app.route('/analyze')
def analyze():
    ticker = request.args.get('ticker', '').upper().strip()
    if ticker.lower() in COMPANIES:
        ticker = COMPANIES[ticker.lower()]
    if not ticker:
        return render_template_string(HOMEPAGE)
    
    data = analyze_stock(ticker)
    if not data:
        return render_template_string(HOMEPAGE + '<p style="text-align:center;color:#ff4444;">Ticker not found or data unavailable</p>')
    
    news = get_news_links(ticker)
    return render_template_string(ANALYSIS_PAGE, data=data, news=news)

@app.route('/save/<ticker>')
def save(ticker):
    data = analyze_stock(ticker)
    if data:
        conn = get_db()
        c = conn.cursor()
        c.execute('''INSERT INTO analyses (ticker, date, score, price, target_buy, sector, pe_ratio, peg_ratio, de_ratio, roe, revenue_growth, profit_margin, operating_margin)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (data['ticker'], datetime.now().strftime('%Y-%m-%d'), data['score'], data['price'], data['target_buy'], data['sector'],
                   data['pe_ratio'], data['peg_ratio'], data['de'], data['roe'], data['rev_growth'], data['mg'], data['om']))
        conn.commit()
        conn.close()
    return f'<p style="text-align:center;color:#00ff88;padding:50px;">Analysis for {ticker} saved!</p><p style="text-align:center;"><a href="/">Back to Home</a></p>'

@app.route('/saved')
def saved():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM analyses ORDER BY date DESC')
    rows = c.fetchall()
    conn.close()
    
    if not rows:
        content = '<p style="text-align:center;color:#888;">No saved analyses yet.</p>'
    else:
        content = '<table><tr><th>Ticker</th><th>Date</th><th>Score</th><th>Price</th><th>Target Buy</th><th>Sector</th></tr>'
        for row in rows:
            score_class = 'score-good' if row[3] >= 7 else 'score-medium' if row[3] >= 5 else 'score-bad'
            content += f'<tr><td><a href="/analyze?ticker={row[1]}" style="color:#00d4ff;">{row[1]}</a></td><td>{row[2]}</td><td class="score {score_class}">{row[3]:.1f}</td><td>${row[4]:.2f}</td><td>${row[5]:.2f}</td><td>{row[6]}</td></tr>'
        content += '</table>'
    
    return render_template_string(SAVED_PAGE, content=content)

@app.route('/portfolio')
def portfolio():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM portfolio')
    rows = c.fetchall()
    conn.close()
    
    if not rows:
        content = '<p style="text-align:center;color:#888;">Your portfolio is empty.</p><p style="text-align:center;"><a href="/" style="color:#00d4ff;">Find stocks to add</a></p>'
    else:
        content = '<table><tr><th>Ticker</th><th>Shares</th><th>Avg Price</th><th>Date Added</th></tr>'
        for row in rows:
            content += f'<tr><td><a href="/analyze?ticker={row[1]}" style="color:#00d4ff;">{row[1]}</a></td><td>{row[2]}</td><td>${row[3]:.2f}</td><td>{row[4]}</td></tr>'
        content += '</table>'
    
    return render_template_string(PORTFOLIO_PAGE, content=content)

@app.route('/add/<ticker>')
def add_portfolio(ticker):
    return f'''
    <html><body style="background:#0a0a0f;color:#fff;font-family:sans-serif;padding:50px;text-align:center;">
    <h2 style="color:#00d4ff;">Add {ticker} to Portfolio</h2>
    <form action="/portfolio/add" method="post">
        <input type="hidden" name="ticker" value="{ticker}">
        <p>Shares: <input type="number" name="shares" step="0.01" required style="padding:10px;font-size:1.2em;"></p>
        <p>Avg Price: <input type="number" name="price" step="0.01" required style="padding:10px;font-size:1.2em;"></p>
        <button type="submit" style="padding:15px 30px;font-size:1.2em;background:#00ff88;border:none;cursor:pointer;">Add</button>
    </form>
    <p><a href="/" style="color:#00d4ff;">Back to Home</a></p>
    </body></html>
    '''

@app.route('/macro')
def macro():
    events = [
        {'date': 'Weekly', 'title': 'Initial Jobless Claims', 'impact': 'medium', 'desc': 'Weekly unemployment claims'},
        {'date': 'Weekly', 'title': 'EIA Crude Oil Inventories', 'impact': 'medium', 'desc': 'Oil supply data'},
        {'date': 'Wednesday', 'title': 'MBA Mortgage Applications', 'impact': 'low', 'desc': 'Home loan applications'},
        {'date': 'Thursday', 'title': 'Retail Sales', 'impact': 'high', 'desc': 'Consumer spending indicator'},
        {'date': 'Thursday', 'title': 'Jobless Claims', 'impact': 'medium', 'desc': 'Weekly unemployment data'},
        {'date': 'Friday', 'title': 'Michigan Consumer Sentiment', 'impact': 'medium', 'desc': 'Consumer confidence index'},
    ]
    
    strategies = {
        'bull': {
            'title': 'BULL MARKET STRATEGIES',
            'strategies': [
                'Growth stocks with high earnings growth',
                'Technology & Innovation sector',
                'Momentum trading strategies',
                'Leveraged ETFs (UPRO, TQQQ)',
                'Reduced cash allocation',
                'Focus on ROC and ROE metrics'
            ]
        },
        'bear': {
            'title': 'BEAR MARKET STRATEGIES',
            'strategies': [
                'Defensive sectors: Healthcare, Utilities, Consumer Staples',
                'Value stocks with low P/E and P/B',
                'Dividend aristocrats',
                'Inverse ETFs (SH, SPXU)',
                'Increase cash position',
                'Focus on debt-to-equity ratio'
            ]
        }
    }
    
    content = '<div style="margin-bottom:30px;"><h2 style="color:#00d4ff;margin-bottom:15px;">Upcoming Events</h2>'
    for e in events:
        content += f'''
        <div class="macro-card">
            <div class="macro-date">{e['date']} <span class="macro-impact {e['impact']}">{e['impact'].upper()}</span></div>
            <div class="macro-title">{e['title']}</div>
            <p style="color:#888;">{e['desc']}</p>
        </div>
        '''
    
    content += '<h2 style="color:#00d4ff;margin:30px 0 15px;">Market Strategies</h2>'
    
    for mkt in ['bull', 'bear']:
        content += f'<div class="macro-card"><h3 style="color:{"#00ff88" if mkt=="bull" else "#ff4444"};">{strategies[mkt]["title"]}</h3><ul>'
        for s in strategies[mkt]['strategies']:
            content += f'<li style="margin:8px 0;">{s}</li>'
        content += '</ul></div>'
    
    content += '</div>'
    return render_template_string(MACRO_PAGE, content=content)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
