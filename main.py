from flask import Flask, render_template_string, request
import yfinance as yf
from datetime import datetime
import json
import os

app = Flask(__name__)

DATA_FILE = 'data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'analyses': [], 'portfolio': []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

COMPANIES = {
    'msft': 'MSFT', 'microsoft': 'MSFT', 'apple': 'AAPL', 'goog': 'GOOGL', 'google': 'GOOGL',
    'amazon': 'AMZN', 'amzn': 'AMZN', 'meta': 'META', 'facebook': 'META', 'nvda': 'NVDA',
    'nvidia': 'NVDA', 'tsla': 'TSLA', 'tesla': 'TSLA', 'jpm': 'JPM', 'jp': 'JPM',
    'visa': 'V', 'v': 'V', 'unh': 'UNH', 'jnj': 'JNJ', 'johnson': 'JNJ', 'wmt': 'WMT',
    'walt': 'WMT', 'walmart': 'WMT', 'pg': 'PG', 'procter': 'PG', 'xom': 'XOM',
    'exxon': 'XOM', 'ma': 'MA', 'mastercard': 'MA', 'hd': 'HD', 'home': 'HD',
    'bac': 'BAC', 'bank': 'BAC', 'abbv': 'ABBV', 'abbvie': 'ABBV', 'pfe': 'PFE',
    'pfizer': 'PFE', 'kering': 'KER.PA', 'ker': 'KER.PA', 'airbus': 'AIR.PA', 'air': 'AIR.PA', 'lvmh': 'MC.PA',
    'mc': 'MC.PA', 'hermes': 'RMS.PA', 'rms': 'RMS.PA', 'danone': 'BN.PA',
    'bn': 'BN.PA', 'total': 'TTE.PA', 'tte': 'TTE.PA', 'sanofi': 'SAN.PA',
    'san': 'SAN.PA', 'orange': 'ORA.PA', 'ora': 'ORA.PA', 'vodafone': 'VOD',
    'vod': 'VOD', 'sap': 'SAP', 'siemens': 'SIE.DE', 'sie': 'SIE.DE',
    'bmw': 'BMW.DE', 'volkswagen': 'VOW.DE', 'vow': 'VOW.DE', 'linde': 'LIN',
    'asml': 'ASML', 'shell': 'SHEL', 'shel': 'SHEL', 'bp': 'BP',
    'hsbc': 'HSBA.L', 'hsba': 'HSBA.L', 'barclays': 'BARC.L', 'barc': 'BARC.L',
    'diageo': 'DGE.L', 'dge': 'DGE.L', 'nestle': 'NESN.SW', 'novartis': 'NOVN.SW',
    'novn': 'NOVN.SW', 'roche': 'ROG.SW', 'rog': 'ROG.SW', 'ubs': 'UBSG.SW',
    'ubsg': 'UBSG.SW', 'avgo': 'AVGO', 'broadcom': 'AVGO', 'ko': 'KO', 'coca': 'KO',
    'cocacola': 'KO', 'pep': 'PEP', 'pepsi': 'PEP', 'lliy': 'LLY', 'eli': 'LLY',
    'eli lilly': 'LLY', 'cost': 'COST', 'costco': 'COST', 'dis': 'DIS', 'disney': 'DIS',
    'wfc': 'WFC', 'wells': 'WFC', 'csco': 'CSCO', 'cisco': 'CSCO', 'mcd': 'MCD',
    'mcdonald': 'MCD', 'tmo': 'TMO', 'thermo': 'TMO', 'dhr': 'DHR', 'danaher': 'DHR',
    'intc': 'INTC', 'intel': 'INTC', 'amd': 'AMD', 'qs': 'QS', 'quantumscape': 'QS',
    'pltr': 'PLTR', 'palantir': 'PLTR', 'palo alto': 'PANW', 'panw': 'PANW', 'tsm': 'TSM', 'taiwan': 'TSM', 'nvo': 'NVO',
    'novo': 'NVO', 'baba': 'BABA', 'alibaba': 'BABA', 'sbux': 'SBUX', 'starbucks': 'SBUX',
    'nke': 'NKE', 'nike': 'NKE', 'orcl': 'ORCL', 'oracle': 'ORCL', 'crm': 'CRM',
    'salesforce': 'CRM', 'adbe': 'ADBE', 'adobe': 'ADBE', 'pypl': 'PYPL', 'paypal': 'PYPL',
    'sq': 'SQ', 'block': 'SQ', 'shop': 'SHOP', 'shopify': 'SHOP', 'spot': 'SPOT',
    'spotify': 'SPOT', 'net': 'NET', 'cloudflare': 'NET', 'dd': 'DD', 'datadog': 'DD',
    'snow': 'SNOW', 'snowflake': 'SNOW', 'zm': 'ZM', 'zoom': 'ZM', 'twlo': 'TWLO',
    'twilio': 'TWLO', 'ub': 'UB', 'uber': 'UB', 'lyft': 'LYFT', 'airbnb': 'ABNB',
    'abnb': 'ABNB', 'dkng': 'DKNG', 'draftkings': 'DKNG', 'coin': 'COIN',
    'coinbase': 'COIN', 'mu': 'MU', 'micron': 'MU', 'lrcx': 'LRCX', 'lam': 'LRCX',
    'amat': 'AMAT', 'applied': 'AMAT', 'klac': 'KLAC', 'ter': 'TER', 'teradyne': 'TER',
    'qrvo': 'QRVO', 'qorvo': 'QRVO', 'swks': 'SWKS', 'skyworks': 'SWKS', 'on': 'ON',
    'onn': 'ON', 'txn': 'TXN', 'texas': 'TXN', 'adi': 'ADI', 'analog': 'ADI',
    'mchp': 'MCHP', 'microchip': 'MCHP', 'hpq': 'HPQ', 'hp': 'HPQ', 'dell': 'DELL',
    'spy': 'SPY', 'qqq': 'QQQ', 'iwm': 'IWM', 'dia': 'DIA', 'tlt': 'TLT', 'gld': 'GLD',
    'nio': 'NIO', 'xpev': 'XPEV', 'li': 'LI', 'li auto': 'LI', 'rivn': 'RIVN',
    'rivian': 'RIVN', 'f': 'F', 'ford': 'F', 'gm': 'GM', 'general motors': 'GM',
    'tm': 'TM', 'toyota': 'TM', 'ge': 'GE', 'general electric': 'GE', 'cat': 'CAT',
    'caterpillar': 'CAT', 'mmm': 'MMM', 'dupont': 'DD', 'ibm': 'IBM', 'oris': 'ORIS',
    'axp': 'AXP', 'american': 'AXP', 'c': 'C', 'citi': 'C', 'citigroup': 'C',
    'gs': 'GS', 'goldman': 'GS', 'goldman sachs': 'GS', 'ms': 'MS', 'morgan': 'MS',
    'schw': 'SCHW', 'charles': 'SCHW', 'nsc': 'NSC', 'norfolk': 'NSC', 'unp': 'UNP',
    'union': 'UNP', 'lmt': 'LMT', 'lockheed': 'LMT', 'rtx': 'RTX', 'raytheon': 'RTX',
    'ba': 'BA', 'boeing': 'BA', 'hon': 'HON', 'honeywell': 'HON', 'ups': 'UPS',
    'usps': 'UPS', 'fedex': 'FDX', 'fdx': 'FDX', 'dhl': 'DHL', 'uber': 'UB',
    'lyft': 'LYFT', 'airbnb': 'ABNB', 'booking': 'BKNG', 'bkng': 'BKNG', 'expe': 'EXPE',
    'expedia': 'EXPE', 'marriott': 'MAR', 'mar': 'MAR', 'hilton': 'HLT', 'hlt': 'HLT',
    'starwood': 'MAR', 'cmcsa': 'CMCSA', 'comcast': 'CMCSA', 'charter': 'CHTR',
    'cht r': 'CHTR', 't': 'T', 'att': 'T', 'vz': 'VZ', 'verizon': 'VZ',
    'tmus': 'TMUS', 'tmobile': 'TMUS', 'nflx': 'NFLX', 'netflix': 'NFLX',
    'disney': 'DIS', 'wb': 'WB', 'weibo': 'WB', 'snap': 'SNAP', 'pinterest': 'PINS',
    'pins': 'PINS', 'twtr': 'TWTR', 'twitter': 'TWTR', 'meta': 'META', 'reddit': 'RDDT',
    'rddt': 'RDDT', 'pdd': 'PDD', 'pd d': 'PDD', 'jd': 'JD', 'jd.com': 'JD',
    'bidu': 'BIDU', 'baidu': 'BIDU', 'ntfx': 'NTFX', 'spotify': 'SPOT', 'spot': 'SPOT',
    'roku': 'ROKU', 'para': 'PARA', 'paramount': 'PARA', 'wbd': 'WBD', 'warner': 'WBD',
    'fox': 'FOXA', 'foxa': 'FOXA', 'cbs': 'PARA', 'vz': 'VZ', 'sirius': 'SIRI',
    'siri': 'SIRI', 'amcx': 'AMCX', 'disa': 'DIS', 'lyv': 'LYV', 'live nation': 'LYV',
    'tmus': 'TMUS', 'att': 'T', 'mmm': 'MMM', 'lowes': 'LOW', 'low': 'LOW',
    'home depot': 'HD', 'hd': 'HD', 'tgt': 'TGT', 'target': 'TGT', 'wmt': 'WMT',
    'cost': 'COST', 'dollar': 'DG', 'dg': 'DG', 'five below': 'FIVE', 'five': 'FIVE',
    'tjx': 'TJX', 'ross': 'ROST', 'rost': 'ROST', 'burlington': 'BURL', 'burl': 'BURL',
    'ulta': 'ULTA', 'ulta': 'ULTA', 'oros': 'OROS', 'nordstrom': 'JWN', 'jwn': 'JWN',
    'kohls': 'KSS', 'kss': 'KSS', 'macy': 'M', 'macy': 'M', 'bbby': 'BBBY',
    'bed bath': 'BBY', 'bbby': 'BBBY', 'williams': 'WMB', 'wmb': 'WMB', 'eog': 'EOG',
    'eog': 'EOG', 'cvx': 'CVX', 'chevron': 'CVX', 'slb': 'SLB', 'schlumberger': 'SLB',
    'hal': 'HAL', 'halliburton': 'HAL', 'cop': 'COP', 'conoco': 'COP', 'psx': 'PSX',
    'phillips': 'PSX', 'vlo': 'VLO', 'valero': 'VLO', 'tsl a': 'TSLA', 'tsla': 'TSLA',
    'f': 'F', 'ford': 'F', 'gm': 'GM', 'tm': 'TM', 'toyota': 'TM', 'h mc': 'HMC',
    'honda': 'HMC', 'stla': 'STLA', 'stellantis': 'STLA', 'racer': 'RACE', 'ferrari': 'RACE',
    'nio': 'NIO', 'xpev': 'XPEV', 'li': 'LI', 'rivn': 'RIVN', 'lc id': 'LCID',
    'lucid': 'LCID', 'fisker': 'FSR', 'fsr': 'FSR', 'arrival': 'ARVL', 'arvl': 'ARVL',
    'nio': 'NIO', 'wkhs': 'WKHS', 'workhorse': 'WKHS', 'kndi': 'KNDI', 'kandi': 'KNDI',
    'xl': 'XL', 'exi': 'EXI', 'aray': 'ARAY', 'unicc': 'UNF', 'unif': 'UNF',
    'tsla': 'TSLA', 'spy': 'SPY', 'qqq': 'QQQ', 'iwm': 'IWM', 'dia': 'DIA',
    'gld': 'GLD', 'slv': 'SLV', 'tlt': 'TLT', 'tbt': 'TBT', 'sso': 'SSO',
    'upro': 'UPRO', 'tqqq': 'TQQQ', 'soxl': 'SOXL', 'labu': 'LABU', 'xle': 'XLE',
    'xlf': 'XLF', 'xlk': 'XLK', 'xlu': 'XLU', 'xly': 'XLY', 'xlp': 'XLP',
    'xlc': 'XLC', 'xbi': 'XBI', 'iyr': 'IYR', 'xlb': 'XLB', 'xme': 'XME',
    'smh': 'SMH', 'igv': 'IGV', 'finx': 'FINX', 'botz': 'BOTZ', 'robo': 'ROBO',
    'artemis': 'ARKB', 'bitcoin': 'ARKB', 'bitq': 'BITQ', 'btc': 'ARKB', 'sq': 'SQ',
    'pypl': 'PYPL', 'v': 'V', 'ma': 'MA', 'axp': 'AXP', 'coi n': 'COIN',
    'coin': 'COIN', 'hoo dy': 'HOOD', 'hood': 'HOOD', 'sf ix': 'SFIX', 'sfix': 'SFIX',
    ' Etsy': 'ETSY', 'etsy': 'ETSY', 'shp': 'SHOP', 'grub': 'GRUB', 'doordash': 'DASH',
    'dash': 'DASH', 'ub': 'UB', 'lyft': 'LYFT', 'airbnb': 'ABNB', 'bkng': 'BKNG',
    'expe': 'EXPE', 'mar': 'MAR', 'hl t': 'HLT', 'ritz': 'MAR', 'hilton': 'HLT',
    'mcd': 'MCD', 'mcdonald': 'MCD', 'sbux': 'SBUX', 'starbucks': 'SBUX',
    'yum': 'YUM', 'yums': 'YUM', 'dpz': 'DPZ', 'domino': 'DPZ', 'pzza': 'PZZA',
    'papa': 'PZZA', 'qsr': 'QSR', 'restaurant': 'QSR', 'jack': 'JACK', 'jm': 'JACK',
    'wen': 'WEN', 'wendy': 'WEN', 'sonc': 'SONC', 'sonic': 'SONC', 'chuy': 'CHUY',
    'chuy': 'CHUY', 'wh': 'WH', 'wingstop': 'WING', 'wing': 'WING', 'locm': 'LOCM',
    'wing': 'WING', 'dri': 'DRI', 'darden': 'DRI', 'olive': 'OLLI', 'olli': 'OLLI',
    'bkh': 'BKH', 'bell': 'BKH', 'mgr': 'MGR', 'mGM': 'MGM', 'mgm': 'MGM',
    'wynn': 'WYNN', 'wynn': 'WYNN', 'czr': 'CZR', 'caesars': 'CZR', 'mgm': 'MGM',
    'edri': 'EDRI', 'rush': 'RUSH', 'rush st': 'RUSH', 'gan': 'GAN', 'gan': 'GAN',
    'penn': 'PENN', 'penn': 'PENN', 'bet': 'BET', 'betmg': 'BETM', 'evri': 'EVRI',
    'evri': 'EVRI', 'prty': 'PRTY', 'party': 'PRTY', 'mat': 'MAT', 'mattel': 'MAT',
    'has': 'HAS', 'hasbro': 'HAS', 'ntdo': 'NTDOY', 'nintendo': 'NTDOY',
    'ea': 'EA', 'electronic': 'EA', 'ttwo': 'TTWO', 'take2': 'TTWO', 'atvi': 'ATVI',
    'activision': 'ATVI', 'ubisoft': 'UBSFY', 'ubisfy': 'UBSFY', 'sci entific': 'SNE',
    'sony': 'SNE', 'rmbl': 'RMBL', 'rumble': 'RMBL', 'mtch': 'MTCH', 'match': 'MTCH',
    'grp': 'GRPN', 'groupon': 'GRPN', 'trip': 'TRIP', 'tripadvisor': 'TRIP',
    'yr:': 'YR', 'expe': 'EXPE', 'mar': 'MAR', 'bkng': 'BKNG', 'hn h': 'HNI',
    'hni': 'HNI', 'legs': 'LEG', 'leggett': 'LEG', 'fls': 'FLS', 'flowserve': 'FLS',
    'g ud': 'GUD', 'gud': 'GUD', 'itt': 'ITT', 'i t': 'ITT', 'dov': 'DOV',
    'dover': 'DOV', 'etn': 'ETN', 'eaton': 'ETN', 'emr': 'EMR', 'emerson': 'EMR',
    'hon': 'HON', 'honeywell': 'HON', 'rock': 'ROC', 'rockwell': 'ROC', 'snap': 'SNAP',
    'snap': 'SNAP', 'pinterest': 'PINS', 'pins': 'PINS', 'twtr': 'TWTR', 'twitter': 'TWTR',
    'meta': 'META', 'fb': 'META', 'snap': 'SNAP', 'tiktok': 'BILI', 'bili': 'BILI',
    'douyin': 'BILI', 'spotify': 'SPOT', 'apple': 'AAPL', 'netflix': 'NFLX',
    'disney': 'DIS', 'comcast': 'CMCSA', 'charter': 'CHTR', 'verizon': 'VZ',
    'at&t': 'T', 'att': 'T', 'tmobile': 'TMUS', 'lumen': 'LUMN', 'lumn': 'LUMN',
    'alphabet': 'GOOGL', 'alphabet': 'GOOGL', 'microsoft': 'MSFT', 'amazon': 'AMZN',
    'nvidia': 'NVDA', 'tsla': 'TSLA', 'meta': 'META', 'apple': 'AAPL',
}

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
    beta = info.get('beta', 0) or 0
    div_yield = info.get('dividendYield', 0) or 0
    
    try:
        hist = yf.Ticker(ticker).history(period='1y')
        prices = hist['Close']
        rsi = calc_rsi(prices)
        ma50 = calc_ma(prices, 50)
        ma200 = calc_ma(prices, 200)
        
        if len(prices) > 20:
            support = prices.rolling(window=20).min().iloc[-1]
            resistance = prices.rolling(window=20).max().iloc[-1]
        else:
            support, resistance = price * 0.9, price * 1.1
        
        trend = 'UPTREND' if ma50 and ma200 and ma50 > ma200 else 'DOWNTREND' if ma50 and ma200 else 'NEUTRAL'
        
        daily_returns = prices.pct_change().dropna()
        volatility = daily_returns.std()
        avg_return = daily_returns.mean()
        
        if beta and beta > 0:
            market_vol = volatility / 1.1 if beta > 0 else volatility
        else:
            market_vol = volatility
        
        weekly_vol = volatility * (5 ** 0.5)
        monthly_vol = volatility * (20 ** 0.5)
        sixmonth_vol = volatility * ((6 * 20) ** 0.5)
        
        if trend == 'DOWNTREND':
            forecast_1w = price * (1 + avg_return * 5 - weekly_vol * 1.5)
            forecast_1m = price * (1 + avg_return * 20 - monthly_vol * 1.5)
            forecast_6m = price * (1 + avg_return * 120 - sixmonth_vol * 1.5)
        elif trend == 'UPTREND':
            forecast_1w = price * (1 + avg_return * 5 + weekly_vol * 0.8)
            forecast_1m = price * (1 + avg_return * 20 + monthly_vol * 0.8)
            forecast_6m = price * (1 + avg_return * 120 + sixmonth_vol * 0.8)
        else:
            forecast_1w = price * (1 - weekly_vol * 1.2)
            forecast_1m = price * (1 - monthly_vol * 1.2)
            forecast_6m = price * (1 - sixmonth_vol * 1.2)
        
        worst_1w = price * (1 - weekly_vol * 2)
        worst_1m = price * (1 - monthly_vol * 2)
        worst_6m = price * (1 - sixmonth_vol * 2)
        
    except Exception as e:
        rsi, ma50, ma200, support, resistance, trend = None, None, None, price * 0.9, price * 1.1, 'NEUTRAL'
        forecast_1w, forecast_1m, forecast_6m = price, price, price
        worst_1w, worst_1m, worst_6m = price, price, price

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
    scores['cash_debt'] = 10 if total_cash > total_debt else 8 if total_cash > total_debt * 0.5 else 6 if total_cash > 0 else 3
    
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

    target_buy = price * 0.75 if total_score > 7 else price * 0.85 if total_score > 6 else price * 0.90

    return {
        'ticker': ticker, 'name': name, 'sector': sector, 'industry': industry,
        'price': price, 'score': total_score, 'target_buy': target_buy,
        'pe_ratio': pe, 'fwd_pe': fwd_pe, 'peg': peg, 'pb': pb, 'ps': ps,
        'de': de, 'rc': rc, 'cr': cr, 'roe': roe, 'roa': roa, 'roic': roic,
        'mg': mg, 'om': om, 'gm': gm, 'rev_growth': rev_growth, 'earn_growth': earn_growth,
        'fcf': fcf, 'ocf': ocf, 'total_cash': total_cash, 'total_debt': total_debt,
        'mcap': mcap, 'shares': shares, 'week52_high': week52_high, 'week52_low': week52_low,
        'distance_high': distance_high, 'distance_low': distance_low,
        'rsi': rsi, 'ma50': ma50, 'ma200': ma200, 'support': support, 'resistance': resistance,
        'trend': trend, 'beta': beta, 'div_yield': div_yield,
        'forecast_1w': forecast_1w, 'forecast_1m': forecast_1m, 'forecast_6m': forecast_6m,
        'worst_1w': worst_1w, 'worst_1m': worst_1m, 'worst_6m': worst_6m,
    }

def get_news_links(ticker):
    return {
        'tradingview': f'https://www.tradingview.com/symbols/{ticker}',
        'google': f'https://www.google.com/finance/quote/{ticker}:NYSE',
        'yahoo': f'https://finance.yahoo.com/quote/{ticker}',
        'quiver': f'https://www.quiverquant.com/stock/{ticker}',
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
        .nav { display: flex; gap: 10px; justify-content: center; margin-bottom: 20px; flex-wrap: wrap; }
        .nav a { padding: 10px 20px; background: #1a1a25; color: #00d4ff; text-decoration: none; border-radius: 25px; }
        .nav a:hover { background: #222; }
        .sources { background: #12121a; border-radius: 15px; padding: 20px; margin-top: 30px; }
        .sources h3 { color: #00d4ff; margin-bottom: 15px; }
        .sources ul { list-style: none; padding: 0; }
        .sources li { padding: 8px 0; border-bottom: 1px solid #222; }
        .sources a { color: #00ff88; text-decoration: none; }
        .sources a:hover { text-decoration: underline; }
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
            <a href="/watchlist">Watchlist</a>
            <a href="/sources">Sources</a>
        </div>
        <div class="sources">
            <h3>Financial Information Sources</h3>
            <ul>
                <li><strong>Trading:</strong> <a href="https://www.tradingview.com" target="_blank">TradingView</a>, <a href="https://www.google.com/finance" target="_blank">Google Finance</a>, <a href="https://finance.yahoo.com" target="_blank">Yahoo Finance</a>, <a href="https://www.quiverquant.com" target="_blank">Quiver Quantitative</a></li>
                <li><strong>Economic Culture:</strong> <a href="https://www.youtube.com/@Finary" target="_blank">Finary (YouTube)</a>, <a href="https://www.lesechos.fr" target="_blank">Les Echos</a></li>
                <li><strong>Economic Info:</strong> <a href="https://www.ig.com/fr/infos-economiques" target="_blank">IG Infos Economiques</a>, <a href="https://www.ig.com/fr/finance" target="_blank">IG Finance</a>, <a href="https://www.aktionaire.com" target="_blank">L'Aktionnaire</a>, <a href="https://www.bloomberg.com" target="_blank">Bloomberg</a>, <a href="https://www.wsj.com" target="_blank">WSJ</a>, <a href="https://www.ft.com" target="_blank">Financial Times</a></li>
                <li><strong>News:</strong> <a href="https://www.nytimes.com" target="_blank">NY Times</a>, <a href="https://www.afp.com" target="_blank">AFP</a>, <a href="https://www.reuters.com" target="_blank">Reuters</a>, <a href="https://www.lemonde.fr" target="_blank">Le Monde</a></li>
                <li><strong>YouTube:</strong> <a href="https://www.youtube.com/@LeDessousDesCartes" target="_blank">Le Dessous des Cartes</a>, <a href="https://www.youtube.com/c/wsj" target="_blank">WSJ</a>, <a href="https://www.youtube.com/c/CNBC" target="_blank">CNBC</a>, <a href="https://www.youtube.com/c/Bloomberg" target="_blank">Bloomberg</a></li>
            </ul>
        </div>
    </div>
</body>
</html>
'''

ANALYSIS_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>{{ data.ticker }} - Analysis</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0a0a0f; color: #e0e0e0; min-height: 100vh; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
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
        .news-link:hover { background: #222; }
        .nav { display: flex; gap: 10px; justify-content: center; margin-bottom: 20px; flex-wrap: wrap; }
        .nav a { padding: 10px 20px; background: #1a1a25; color: #00d4ff; text-decoration: none; border-radius: 25px; }
        .buy-target { background: #00ff88; color: #000; padding: 20px; border-radius: 10px; text-align: center; margin-top: 20px; font-size: 1.5em; font-weight: bold; }
        .section-title { color: #00d4ff; margin: 20px 0 10px 0; font-size: 1.2em; }
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
            <a href="/watchlist">Watchlist</a>
            <a href="/sources">Sources</a>
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
                <div class="stat"><div class="stat-label">Price</div><div class="stat-value">${{ "%.2f"|format(data.price) }}</div></div>
                <div class="stat"><div class="stat-label">P/E</div><div class="stat-value {% if data.pe_ratio < 25 %}stat-good{% elif data.pe_ratio < 40 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.pe_ratio) if data.pe_ratio else 'N/A' }}</div></div>
                <div class="stat"><div class="stat-label">Forward P/E</div><div class="stat-value {% if data.fwd_pe < 20 %}stat-good{% elif data.fwd_pe < 35 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.fwd_pe) if data.fwd_pe else 'N/A' }}</div></div>
                <div class="stat"><div class="stat-label">PEG</div><div class="stat-value {% if data.peg < 1.5 %}stat-good{% elif data.peg < 3 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.2f"|format(data.peg) if data.peg else 'N/A' }}</div></div>
                <div class="stat"><div class="stat-label">P/B</div><div class="stat-value {% if data.pb < 5 %}stat-good{% elif data.pb < 10 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.pb) if data.pb else 'N/A' }}</div></div>
                <div class="stat"><div class="stat-label">P/S</div><div class="stat-value {% if data.ps < 5 %}stat-good{% elif data.ps < 10 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.ps) if data.ps else 'N/A' }}</div></div>
            </div>
        </div>
        
        <div class="card">
            <div class="section-title">PROFITABILITY</div>
            <div class="grid">
                <div class="stat"><div class="stat-label">ROE</div><div class="stat-value {% if data.roe > 0.15 %}stat-good{% elif data.roe > 0.08 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.roe * 100) if data.roe else 'N/A' }}%</div></div>
                <div class="stat"><div class="stat-label">ROA</div><div class="stat-value {% if data.roa > 0.05 %}stat-good{% elif data.roa > 0.02 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.roa * 100) if data.roa else 'N/A' }}%</div></div>
                <div class="stat"><div class="stat-label">ROIC</div><div class="stat-value {% if data.roic > 15 %}stat-good{% elif data.roic > 8 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.roic) if data.roic else 'N/A' }}%</div></div>
                <div class="stat"><div class="stat-label">Profit Margin</div><div class="stat-value {% if data.mg > 0.15 %}stat-good{% elif data.mg > 0.05 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.mg * 100) if data.mg else 'N/A' }}%</div></div>
                <div class="stat"><div class="stat-label">Op Margin</div><div class="stat-value {% if data.om > 0.15 %}stat-good{% elif data.om > 0.08 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.om * 100) if data.om else 'N/A' }}%</div></div>
                <div class="stat"><div class="stat-label">Gross Margin</div><div class="stat-value {% if data.gm > 0.30 %}stat-good{% elif data.gm > 0.20 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.gm * 100) if data.gm else 'N/A' }}%</div></div>
            </div>
        </div>
        
        <div class="card">
            <div class="section-title">GROWTH</div>
            <div class="grid">
                <div class="stat"><div class="stat-label">Revenue Growth</div><div class="stat-value {% if data.rev_growth > 0.10 %}stat-good{% elif data.rev_growth > 0 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.rev_growth * 100) if data.rev_growth else 'N/A' }}%</div></div>
                <div class="stat"><div class="stat-label">Earnings Growth</div><div class="stat-value {% if data.earn_growth > 0.10 %}stat-good{% elif data.earn_growth > 0 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.earn_growth * 100) if data.earn_growth else 'N/A' }}%</div></div>
            </div>
        </div>
        
        <div class="card">
            <div class="section-title">SOLVENCY</div>
            <div class="grid">
                <div class="stat"><div class="stat-label">D/E</div><div class="stat-value {% if data.de < 1 %}stat-good{% elif data.de < 2 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.de) if data.de else 'N/A' }}</div></div>
                <div class="stat"><div class="stat-label">Current Ratio</div><div class="stat-value {% if data.rc > 1.5 %}stat-good{% elif data.rc > 1 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.2f"|format(data.rc) if data.rc else 'N/A' }}</div></div>
                <div class="stat"><div class="stat-label">Cash Ratio</div><div class="stat-value {% if data.cr > 0.5 %}stat-good{% elif data.cr > 0.2 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.2f"|format(data.cr) if data.cr else 'N/A' }}</div></div>
            </div>
        </div>
        
        <div class="card">
            <div class="section-title">CASH FLOW</div>
            <div class="grid">
                <div class="stat"><div class="stat-label">FCF</div><div class="stat-value {% if data.fcf > 0 %}stat-good{% else %}stat-bad{% endif %}">${{ "%.0f"|format(data.fcf / 1e9) if data.fcf else 0 }}B</div></div>
                <div class="stat"><div class="stat-label">OCF</div><div class="stat-value {% if data.ocf > 0 %}stat-good{% else %}stat-bad{% endif %}">${{ "%.0f"|format(data.ocf / 1e9) if data.ocf else 0 }}B</div></div>
                <div class="stat"><div class="stat-label">Cash</div><div class="stat-value">${{ "%.0f"|format(data.total_cash / 1e9) if data.total_cash else 0 }}B</div></div>
                <div class="stat"><div class="stat-label">Debt</div><div class="stat-value">${{ "%.0f"|format(data.total_debt / 1e9) if data.total_debt else 0 }}B</div></div>
            </div>
        </div>
        
        <div class="card">
            <div class="section-title">TECHNICAL</div>
            <div class="grid">
                <div class="stat"><div class="stat-label">RSI</div><div class="stat-value {% if data.rsi and data.rsi < 30 %}stat-good{% elif data.rsi and data.rsi > 70 %}stat-bad{% endif %}">{{ "%.1f"|format(data.rsi) if data.rsi else 'N/A' }}</div></div>
                <div class="stat"><div class="stat-label">MA50</div><div class="stat-value">${{ "%.2f"|format(data.ma50) if data.ma50 else 'N/A' }}</div></div>
                <div class="stat"><div class="stat-label">MA200</div><div class="stat-value">${{ "%.2f"|format(data.ma200) if data.ma200 else 'N/A' }}</div></div>
                <div class="stat"><div class="stat-label">Support</div><div class="stat-value">${{ "%.2f"|format(data.support) if data.support else 'N/A' }}</div></div>
                <div class="stat"><div class="stat-label">Resistance</div><div class="stat-value">${{ "%.2f"|format(data.resistance) if data.resistance else 'N/A' }}</div></div>
                <div class="stat"><div class="stat-label">Trend</div><div class="stat-value {% if data.trend == 'UPTREND' %}stat-good{% elif data.trend == 'DOWNTREND' %}stat-bad{% endif %}">{{ data.trend }}</div></div>
            </div>
        </div>
        
        <div class="card">
            <div class="section-title">PRICE FORECAST (Normal Case)</div>
            <p style="color:#888;margin-bottom:15px;font-size:0.9em;">Based on volatility and current trend</p>
            <div class="grid">
                <div class="stat">
                    <div class="stat-label">1 Week</div>
                    <div class="stat-value">${{ "%.2f"|format(data.forecast_1w) if data.forecast_1w else 'N/A' }}</div>
                    <div style="font-size:0.8em;color:#00ff88;">{{ "%.1f"|format((data.forecast_1w / data.price - 1) * 100) if data.forecast_1w else '0' }}%%</div>
                </div>
                <div class="stat">
                    <div class="stat-label">1 Month</div>
                    <div class="stat-value">${{ "%.2f"|format(data.forecast_1m) if data.forecast_1m else 'N/A' }}</div>
                    <div style="font-size:0.8em;color:#00ff88;">{{ "%.1f"|format((data.forecast_1m / data.price - 1) * 100) if data.forecast_1m else '0' }}%%</div>
                </div>
                <div class="stat">
                    <div class="stat-label">6 Months</div>
                    <div class="stat-value">${{ "%.2f"|format(data.forecast_6m) if data.forecast_6m else 'N/A' }}</div>
                    <div style="font-size:0.8em;color:#00ff88;">{{ "%.1f"|format((data.forecast_6m / data.price - 1) * 100) if data.forecast_6m else '0' }}%%</div>
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
                <p>Market Cap: ${{ "%.0f"|format(data.mcap / 1e12) if data.mcap else 0 }}T | BETA: {{ "%.2f"|format(data.beta) if data.beta else 'N/A' }} | Dividend: {{ "%.2f"|format(data.div_yield * 100) if data.div_yield else 0 }}%%</p>
            </div>
        </div>
        
        <div class="card">
            <div class="section-title">NEWS & INFO</div>
            <div class="news-links">
                <a href="{{ news.tradingview }}" target="_blank" class="news-link">TradingView</a>
                <a href="{{ news.google }}" target="_blank" class="news-link">Google Finance</a>
                <a href="{{ news.yahoo }}" target="_blank" class="news-link">Yahoo Finance</a>
                <a href="{{ news.quiver }}" target="_blank" class="news-link">Quiver Quantitative</a>
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <a href="/save/{{ data.ticker }}" style="background: #00d4ff; color: #000; padding: 15px 30px; border-radius: 10px; text-decoration: none; font-weight: bold;">Save Analysis</a>
        </div>
    </div>
</body>
</html>
'''

SIMPLE_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
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
        .card { background: #12121a; border-radius: 15px; padding: 25px; margin-bottom: 20px; }
        .sources-list { list-style: none; padding: 0; }
        .sources-list li { padding: 15px 0; border-bottom: 1px solid #333; }
        .sources-list strong { color: #00d4ff; }
        .sources-list a { color: #00ff88; text-decoration: none; }
        .sources-list a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <h1>{{ title }}</h1>
        <div class="nav">
            <a href="/">Home</a>
            <a href="/portfolio">Portfolio</a>
            <a href="/saved">Saved Analyses</a>
            <a href="/watchlist">Watchlist</a>
            <a href="/sources">Sources</a>
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
    try:
        ticker = request.args.get('ticker', '').upper().strip()
        if not ticker:
            return render_template_string(HOMEPAGE)
        if ticker.lower() in COMPANIES:
            ticker = COMPANIES[ticker.lower()]
        
        data = analyze_stock(ticker)
        if not data:
            return render_template_string(HOMEPAGE + '<p style="text-align:center;color:#ff4444;">Ticker not found. Try again.</p>')
        
        news = get_news_links(ticker)
        return render_template_string(ANALYSIS_PAGE, data=data, news=news)
    except Exception as e:
        return render_template_string(HOMEPAGE + f'<p style="text-align:center;color:#ff4444;">Error: {str(e)}</p>')

@app.route('/save/<ticker>')
def save(ticker):
    try:
        data = analyze_stock(ticker)
        if data:
            all_data = load_data()
            all_data['analyses'].append({
                'ticker': data['ticker'],
                'date': datetime.now().strftime('%Y-%m-%d'),
                'score': data['score'],
                'price': data['price'],
                'target_buy': data['target_buy'],
                'sector': data['sector']
            })
            save_data(all_data)
            return f'<p style="text-align:center;color:#00ff88;padding:50px;background:#0a0a0f;color:#fff;">Analysis for {ticker} saved!</p><p style="text-align:center;"><a href="/saved" style="color:#00d4ff;">View Saved</a></p>'
        return f'<p style="text-align:center;color:#ff4444;">Could not analyze {ticker}</p>'
    except Exception as e:
        return f'<p style="text-align:center;color:#ff4444;">Error: {str(e)}</p>'

@app.route('/saved')
def saved():
    all_data = load_data()
    if not all_data['analyses']:
        content = '<p style="text-align:center;color:#888;">No saved analyses yet.</p>'
    else:
        content = '<table><tr><th>Ticker</th><th>Date</th><th>Score</th><th>Price</th><th>Target</th></tr>'
        for a in all_data['analyses']:
            score_class = 'score-good' if a['score'] >= 7 else 'score-medium' if a['score'] >= 5 else 'score-bad'
            content += f'<tr><td><a href="/analyze?ticker={a["ticker"]}" style="color:#00d4ff;">{a["ticker"]}</a></td><td>{a["date"]}</td><td class="score {score_class}">{a["score"]:.1f}</td><td>${a["price"]:.2f}</td><td>${a["target_buy"]:.2f}</td></tr>'
        content += '</table>'
    return render_template_string(SIMPLE_PAGE, title='Saved Analyses', content=content)

@app.route('/portfolio')
def portfolio():
    all_data = load_data()
    if not all_data['portfolio']:
        content = '<p style="text-align:center;color:#888;">Portfolio empty.</p>'
    else:
        content = '<table><tr><th>Ticker</th><th>Date</th></tr>'
        for p in all_data['portfolio']:
            content += f'<tr><td>{p["ticker"]}</td><td>{p["date"]}</td></tr>'
        content += '</table>'
    return render_template_string(SIMPLE_PAGE, title='Portfolio', content=content)

@app.route('/watchlist')
def watchlist():
    buy_now = [
        {'ticker': 'AAPL', 'reason': 'Strong fundamentals, services growth'},
        {'ticker': 'MSFT', 'reason': 'Cloud leadership, AI integration'},
        {'ticker': 'NVDA', 'reason': 'AI chip dominance'},
        {'ticker': 'GOOGL', 'reason': 'AI & search moat'},
        {'ticker': 'AMZN', 'reason': 'AWS growth, efficiency'},
        {'ticker': 'META', 'reason': 'AI boost, buybacks'},
        {'ticker': 'SAP', 'reason': 'Cloud transition, ERPNOVN.SW'},
        {'ticker': 'ASML', 'reason': 'EUV monopoly'},
        {'ticker': 'LVMH', 'reason': 'Luxury resilience'},
    ]
    
    watch_future = [
        {'ticker': 'TSLA', 'reason': 'Waiting for margin recovery'},
        {'ticker': 'PLTR', 'reason': 'AI government contracts'},
        {'ticker': 'SNOW', 'reason': 'High valuation, watch for entry'},
        {'ticker': 'ARM', 'reason': 'IPO watch, new player'},
        {'ticker': 'RIVN', 'reason': 'EV market share building'},
        {'ticker': 'SMCI', 'reason': 'AI server demand, volatile'},
        {'ticker': 'PALANTIR', 'reason': 'AI momentum'},
        {'ticker': 'PANW', 'reason': 'Cybersecurity leader, AI security'},
    ]
    
    content = '''
    <div class="card">
        <h2 style="color:#00ff88;margin-bottom:20px;">Actions Intéressantes (Acheter)</h2>
        <p style="color:#888;margin-bottom:20px;">Actions avec fondamentaux solides, prêtes à acheter</p>
        <table>
            <tr><th>Ticker</th><th>Raison</th><th></th></tr>
    '''
    for s in buy_now:
        content += f'''<tr>
            <td><a href="/analyze?ticker={s['ticker']}" style="color:#00d4ff;font-weight:bold;">{s['ticker']}</a></td>
            <td style="color:#ccc;">{s['reason']}</td>
            <td><a href="/save/{s['ticker']}" style="background:#00d4ff;color:#000;padding:5px 15px;border-radius:5px;text-decoration:none;font-size:0.85em;">Analyser</a></td>
        </tr>'''
    
    content += '''
        </table>
    </div>
    <div class="card">
        <h2 style="color:#ffaa00;margin-bottom:20px;">Actions à Surveiller (Futur)</h2>
        <p style="color:#888;margin-bottom:20px;">Actions à regarder pour une entrée future</p>
        <table>
            <tr><th>Ticker</th><th>Raison</th><th></th></tr>
    '''
    for s in watch_future:
        content += f'''<tr>
            <td><a href="/analyze?ticker={s['ticker']}" style="color:#00d4ff;font-weight:bold;">{s['ticker']}</a></td>
            <td style="color:#ccc;">{s['reason']}</td>
            <td><a href="/save/{s['ticker']}" style="background:#ffaa00;color:#000;padding:5px 15px;border-radius:5px;text-decoration:none;font-size:0.85em;">Analyser</a></td>
        </tr>'''
    
    content += '</table></div>'
    
    return render_template_string(SIMPLE_PAGE, title='Watchlist', content=content)

@app.route('/sources')
def sources():
    content = '''
    <div class="card">
        <h2 style="color:#00d4ff;margin-bottom:20px;">Financial Information Sources</h2>
        <h3 style="color:#fff;margin:20px 0 10px;">Surveillance Actions</h3>
        <ul class="sources-list">
            <li><strong>TradingView</strong> - <a href="https://www.tradingview.com" target="_blank">tradingview.com</a> - Charts & analysis</li>
            <li><strong>Google Finance</strong> - <a href="https://www.google.com/finance" target="_blank">google.com/finance</a> - Real-time quotes</li>
            <li><strong>Yahoo Finance</strong> - <a href="https://finance.yahoo.com" target="_blank">finance.yahoo.com</a> - Financial data</li>
            <li><strong>Quiver Quantitative</strong> - <a href="https://www.quiverquant.com" target="_blank">quiverquant.com</a> - Alternative data</li>
        </ul>
        
        <h3 style="color:#fff;margin:20px 0 10px;">Culture Economique</h3>
        <ul class="sources-list">
            <li><strong>Finary (YouTube)</strong> - <a href="https://www.youtube.com/@Finary" target="_blank">YouTube Channel</a> - French finance education</li>
            <li><strong>Les Echos</strong> - <a href="https://www.lesechos.fr" target="_blank">lesechos.fr</a> - French business news</li>
        </ul>
        
        <h3 style="color:#fff;margin:20px 0 10px;">Information Economique</h3>
        <ul class="sources-list">
            <li><strong>IG - Infos Economiques</strong> - <a href="https://www.ig.com/fr/infos-economiques" target="_blank">ig.com/fr/infos-economiques</a></li>
            <li><strong>IG Finance</strong> - <a href="https://www.ig.com/fr/finance" target="_blank">ig.com/fr/finance</a></li>
            <li><strong>L'Aktionnaire</strong> - <a href="https://www.aktionaire.com" target="_blank">aktionaire.com</a> - French market info</li>
            <li><strong>Bloomberg</strong> - <a href="https://www.bloomberg.com" target="_blank">bloomberg.com</a> + <a href="https://www.bloomberg.com/mobile" target="_blank">App</a></li>
            <li><strong>Wall Street Journal</strong> - <a href="https://www.wsj.com" target="_blank">wsj.com</a> + <a href="https://www.wsj.com/mobile" target="_blank">App</a></li>
            <li><strong>Financial Times</strong> - <a href="https://www.ft.com" target="_blank">ft.com</a> + App</li>
        </ul>
        
        <h3 style="color:#fff;margin:20px 0 10px;">Information Generale</h3>
        <ul class="sources-list">
            <li><strong>NY Times</strong> - <a href="https://www.nytimes.com" target="_blank">nytimes.com</a> - Business section</li>
            <li><strong>AFP</strong> - <a href="https://www.afp.com" target="_blank">afp.com</a> - News agency</li>
            <li><strong>Reuters</strong> - <a href="https://www.reuters.com" target="_blank">reuters.com</a> - Financial news</li>
            <li><strong>Le Monde</strong> - <a href="https://www.lemonde.fr" target="_blank">lemonde.fr</a> - Economy</li>
        </ul>
        
        <h3 style="color:#fff;margin:20px 0 10px;">YouTube Channels</h3>
        <ul class="sources-list">
            <li><strong>Le Dessous des Cartes</strong> - <a href="https://www.youtube.com/@LeDessousDesCartes" target="_blank">YouTube</a> - Geopolitics</li>
            <li><strong>Wall Street Journal</strong> - <a href="https://www.youtube.com/c/wsj" target="_blank">YouTube</a></li>
            <li><strong>CNBC</strong> - <a href="https://www.youtube.com/c/CNBC" target="_blank">YouTube</a> + <a href="https://www.youtube.com/c/CNBCi" target="_blank">International</a></li>
            <li><strong>Bloomberg</strong> - <a href="https://www.youtube.com/c/Bloomberg" target="_blank">YouTube</a></li>
        </ul>
    </div>
    '''
    return render_template_string(SIMPLE_PAGE, title='Sources', content=content)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
