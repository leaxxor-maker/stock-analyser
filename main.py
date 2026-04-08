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
    return {'analyses': [], 'portfolio': [], 'watchlist': []}

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
    
    # ETFs - US Market
    'spy': 'SPY', 'spdr': 'SPY', "s&p 500": 'SPY', 'voo': 'VOO', 'ivv': 'IVV',
    'vti': 'VTI', 'qqq': 'QQQ', 'qqqm': 'QQQM', 'iwm': 'IWM', 'dia': 'DIA',
    
    # ETFs - International
    'vxus': 'VXUS', 'efa': 'EFA', 'eem': 'EEM', 'vwo': 'VWO',
    
    # ETFs - Sectors
    'xlk': 'XLK', 'xlf': 'XLF', 'xle': 'XLE', 'xlv': 'XLV', 'xly': 'XLY',
    'xlp': 'XLP', 'xlb': 'XLB', 'xli': 'XLI', 'xlre': 'XLRE', 'xlu': 'XLU',
    
    # ETFs - Growth/Value
    'vug': 'VUG', 'vtv': 'VTV', 'iwf': 'IWD', 'schg': 'SCHG', 'schd': 'SCHD', 'vym': 'VYM',
    
    # ETFs - Bonds
    'bnd': 'BND', 'agg': 'AGG', 'tlt': 'TLT', 'ief': 'IEF', 'lqd': 'LQD', 'hyg': 'HYG',
    
    # ETFs - Thematic
    'arkk': 'ARKK', 'soxx': 'SOXX', 'smh': 'SMH', 'kweb': 'KWEB', 'fxi': 'FXI',
    'gdx': 'GDX', 'gld': 'GLD', 'slv': 'SLV', 'uso': 'USO', 'ung': 'UNG',
    
    # ETFs - Leveraged
    'tqqq': 'TQQQ', 'sqqq': 'SQQQ', 'spxl': 'SPXL', 'spxs': 'SPXS',
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
    <title>Stock Analyzer Pro v3</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        :root {
            --bg-primary: #0a0a0f;
            --bg-secondary: #12121a;
            --bg-tertiary: #1a1a25;
            --accent-cyan: #00d4ff;
            --accent-green: #00ff88;
            --accent-gold: #ffd700;
            --accent-orange: #ff6b35;
            --text-primary: #ffffff;
            --text-secondary: #a0a0a0;
            --text-muted: #666680;
            --border-color: rgba(255, 255, 255, 0.08);
        }
        body { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(180deg, #0a0a0f 0%, #12121a 100%); color: #e0e0e0; min-height: 100vh; }
        .bg-pattern { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(ellipse at 20% 20%, rgba(0, 212, 255, 0.08) 0%, transparent 50%), radial-gradient(ellipse at 80% 80%, rgba(0, 255, 136, 0.05) 0%, transparent 50%); z-index: -1; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        
        /* Nav */
        .navbar { display: flex; justify-content: space-between; align-items: center; padding: 1rem 2rem; background: rgba(10, 10, 15, 0.85); backdrop-filter: blur(20px); border-bottom: 1px solid var(--border-color); position: sticky; top: 0; z-index: 100; }
        .logo { display: flex; align-items: center; gap: 0.75rem; font-family: 'Playfair Display', serif; font-size: 1.5rem; font-weight: 700; color: #fff; text-decoration: none; }
        .logo-icon { width: 40px; height: 40px; background: linear-gradient(135deg, #00d4ff, #00ff88); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; }
        .logo span:last-child { background: linear-gradient(135deg, #00d4ff, #00ff88); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .nav { display: flex; gap: 0.5rem; }
        .nav a { color: #a0a0a0; text-decoration: none; padding: 0.6rem 1rem; border-radius: 8px; font-weight: 500; font-size: 0.9rem; transition: all 0.25s ease; }
        .nav a:hover, .nav a.active { background: rgba(0, 212, 255, 0.1); color: #00d4ff; }
        
        /* Hero */
        .hero { text-align: center; padding: 4rem 0; }
        .hero h1 { font-family: 'Playfair Display', serif; font-size: 3.5rem; font-weight: 700; margin-bottom: 1rem; background: linear-gradient(135deg, #fff 0%, #00d4ff 50%, #00ff88 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
        .hero p { font-size: 1.2rem; color: #a0a0a0; max-width: 600px; margin: 0 auto 2rem; }
        
        /* Search */
        .search-container { max-width: 600px; margin: 0 auto; position: relative; }
        .search-input { width: 100%; padding: 1.25rem 1.5rem; padding-left: 3.5rem; border-radius: 16px; border: 2px solid var(--border-color); background: var(--bg-tertiary); color: #fff; font-size: 1.1rem; transition: all 0.3s ease; }
        .search-input:focus { outline: none; border-color: var(--accent-cyan); box-shadow: 0 0 30px rgba(0, 212, 255, 0.2); }
        .search-icon { position: absolute; left: 1.25rem; top: 50%; transform: translateY(-50%); color: var(--text-muted); font-size: 1.25rem; }
        .search-btn { display: block; width: 100%; padding: 1rem; margin-top: 1rem; background: linear-gradient(135deg, #00d4ff, #0099cc); color: #0a0a0f; border: none; border-radius: 12px; font-size: 1rem; font-weight: 600; cursor: pointer; }
        .search-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(0, 212, 255, 0.4); }
        
        /* Quick Tags */
        .quick-tags { display: flex; flex-wrap: wrap; gap: 0.5rem; justify-content: center; margin-top: 1.5rem; }
        .quick-tag { padding: 0.4rem 0.9rem; background: var(--bg-tertiary); border: 1px solid var(--border-color); border-radius: 20px; color: #a0a0a0; font-size: 0.85rem; text-decoration: none; transition: all 0.25s ease; }
        .quick-tag:hover { background: rgba(0, 212, 255, 0.15); color: var(--accent-cyan); border-color: var(--accent-cyan); }
        
        /* Ticker */
        .market-ticker { display: flex; gap: 2rem; padding: 1rem 1.5rem; background: var(--bg-secondary); border-radius: 12px; margin: 2rem 0; overflow-x: auto; }
        .ticker-item { display: flex; align-items: center; gap: 0.75rem; white-space: nowrap; }
        .ticker-symbol { font-family: 'JetBrains Mono', monospace; font-weight: 600; color: #fff; }
        .ticker-price { font-family: 'JetBrains Mono', monospace; color: #a0a0a0; }
        .ticker-change { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; font-weight: 500; }
        .ticker-up { color: var(--accent-green); }
        .ticker-down { color: #ff4757; }
        
        /* Section */
        .section-title { font-family: 'Playfair Display', serif; font-size: 1.75rem; font-weight: 600; margin: 2rem 0 1.5rem; display: flex; align-items: center; gap: 0.75rem; }
        .section-title::before { content: ''; width: 4px; height: 28px; background: linear-gradient(180deg, var(--accent-cyan), var(--accent-green)); border-radius: 2px; }
        
        /* Featured News */
        .featured-news { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 2rem; }
        .featured-card { position: relative; border-radius: 20px; overflow: hidden; height: 400px; }
        .featured-image { width: 100%; height: 100%; object-fit: cover; transition: transform 0.5s ease; }
        .featured-card:hover .featured-image { transform: scale(1.05); }
        .featured-overlay { position: absolute; bottom: 0; left: 0; right: 0; padding: 2rem; background: linear-gradient(transparent, rgba(0, 0, 0, 0.9)); }
        .featured-category { display: inline-block; padding: 0.35rem 0.85rem; background: var(--accent-orange); color: white; font-size: 0.75rem; font-weight: 600; border-radius: 4px; text-transform: uppercase; margin-bottom: 0.75rem; }
        .featured-title { font-family: 'Playfair Display', serif; font-size: 1.75rem; font-weight: 700; margin-bottom: 0.5rem; }
        .featured-title a { color: white; text-decoration: none; }
        .featured-title a:hover { text-decoration: underline; }
        .featured-meta { color: rgba(255, 255, 255, 0.7); font-size: 0.85rem; }
        
        /* News Grid */
        .news-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }
        .news-card { background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 16px; overflow: hidden; transition: all 0.3s ease; }
        .news-card:hover { transform: translateY(-4px); border-color: rgba(0, 212, 255, 0.3); box-shadow: 0 4px 24px rgba(0, 0, 0, 0.4); }
        .news-image { width: 100%; height: 160px; object-fit: cover; background: linear-gradient(135deg, var(--bg-tertiary), var(--bg-secondary)); }
        .news-content { padding: 1.25rem; }
        .news-category { display: inline-block; padding: 0.25rem 0.75rem; background: rgba(0, 212, 255, 0.15); color: var(--accent-cyan); font-size: 0.75rem; font-weight: 600; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.75rem; }
        .news-title { font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem; line-height: 1.4; }
        .news-title a { color: #fff; text-decoration: none; }
        .news-title a:hover { color: var(--accent-cyan); }
        .news-meta { font-size: 0.8rem; color: var(--text-muted); }
        
        /* Cards */
        .card { background: var(--bg-secondary); border-radius: 16px; padding: 1.5rem; margin-bottom: 1.5rem; border: 1px solid var(--border-color); }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
        .stat-card { background: var(--bg-tertiary); border-radius: 12px; padding: 1.25rem; text-align: center; border: 1px solid var(--border-color); transition: all 0.3s ease; }
        .stat-card:hover { border-color: var(--accent-cyan); }
        .stat-value { font-family: 'JetBrains Mono', monospace; font-size: 2rem; font-weight: 700; color: var(--accent-cyan); margin-bottom: 0.25rem; }
        .stat-label { color: var(--text-muted); font-size: 0.85rem; }
        
        @media (max-width: 768px) {
            .navbar { flex-direction: column; gap: 1rem; }
            .nav { flex-wrap: wrap; justify-content: center; }
            .hero h1 { font-size: 2.5rem; }
            .featured-news { grid-template-columns: 1fr; }
            .featured-card { height: 300px; }
            .featured-title { font-size: 1.4rem; }
        }
    </style>
</head>
<body>
    <div class="bg-pattern"></div>
    <nav class="navbar">
        <a href="/" class="logo">
            <div class="logo-icon">📈</div>
            <span>Stock Analyzer</span>
        </a>
        <div class="nav">
            <a href="/" class="active">Accueil</a>
            <a href="/analyze">Analyser</a>
            <a href="/watchlist">Watchlist</a>
            <a href="/saved">Analyses</a>
            <a href="/stocks">Stocks</a>
            <a href="/sources">Sources</a>
        </div>
    </nav>
    
    <div class="container">
        <section class="hero">
            <h1>L'Analyse Boursière, Simplifiée</h1>
            <p>Analysez des actions et ETF avec des indicateurs financiers professionnels. Des décisions éclairées, à portée de main.</p>
            
            <div class="search-container">
                <form action="/analyze" method="get" style="width:100%;display:flex;flex-direction:column;gap:1rem;">
                    <div style="position:relative;">
                        <span class="search-icon">🔍</span>
                        <input type="text" name="ticker" class="search-input" placeholder="Rechercher une action ou un ETF..." id="homeSearch">
                    </div>
                    <button type="submit" class="search-btn">Analyser</button>
                </form>
            </div>
            
            <div class="quick-tags">
                <span style="color: var(--text-muted);">Actions:</span>
                <a href="/analyze?ticker=SPY" class="quick-tag">S&P 500</a>
                <a href="/analyze?ticker=QQQ" class="quick-tag">NASDAQ</a>
                <a href="/analyze?ticker=MSFT" class="quick-tag">Microsoft</a>
                <a href="/analyze?ticker=AAPL" class="quick-tag">Apple</a>
                <a href="/analyze?ticker=NVDA" class="quick-tag">NVIDIA</a>
                <a href="/analyze?ticker=TSLA" class="quick-tag">Tesla</a>
            </div>
        </section>
        
        <div class="market-ticker">
            <div class="ticker-item"><span class="ticker-symbol">SPY</span><span class="ticker-price">$502.35</span><span class="ticker-change ticker-up">+1.2%</span></div>
            <div class="ticker-item"><span class="ticker-symbol">QQQ</span><span class="ticker-price">$438.20</span><span class="ticker-change ticker-up">+1.8%</span></div>
            <div class="ticker-item"><span class="ticker-symbol">DIA</span><span class="ticker-price">$398.50</span><span class="ticker-change ticker-up">+0.4%</span></div>
            <div class="ticker-item"><span class="ticker-symbol">VWO</span><span class="ticker-price">$43.25</span><span class="ticker-change ticker-down">-0.3%</span></div>
            <div class="ticker-item"><span class="ticker-symbol">TLT</span><span class="ticker-price">$96.80</span><span class="ticker-change ticker-down">-0.5%</span></div>
            <div class="ticker-item"><span class="ticker-symbol">GLD</span><span class="ticker-price">$189.45</span><span class="ticker-change ticker-up">+0.8%</span></div>
        </div>
        
        <h2 class="section-title">À la une</h2>
        <div class="featured-news">
            <article class="featured-card">
                <img src="https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&q=80" alt="Bourse" class="featured-image">
                <div class="featured-overlay">
                    <span class="featured-category">Marchés</span>
                    <h3 class="featured-title"><a href="#">Les marchés actions atteignent de nouveaux records historiques</a></h3>
                    <p class="featured-meta">Il y a 2 heures • Bloomberg</p>
                </div>
            </article>
            <article class="featured-card">
                <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&q=80" alt="Tech" class="featured-image">
                <div class="featured-overlay">
                    <span class="featured-category">Technologie</span>
                    <h3 class="featured-title"><a href="#">L'IA pousse NVIDIA vers les 900 milliards de capitalisation</a></h3>
                    <p class="featured-meta">Il y a 4 heures • Reuters</p>
                </div>
            </article>
        </div>
        
        <h2 class="section-title">Actualités du jour</h2>
        <div class="news-grid">
            <article class="news-card">
                <img src="https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?w=400&q=80" alt="Fed" class="news-image">
                <div class="news-content">
                    <span class="news-category">Macro</span>
                    <h3 class="news-title"><a href="#">La Fed maintient ses taux, les marchés positifs</a></h3>
                    <p class="news-meta">Il y a 1h • Les Echos</p>
                </div>
            </article>
            <article class="news-card">
                <img src="https://images.unsplash.com/photo-1518186285589-2f7649de83e0?w=400&q=80" alt="Crypto" class="news-image">
                <div class="news-content">
                    <span class="news-category">Crypto</span>
                    <h3 class="news-title"><a href="#">Bitcoin dépasse les 70 000$ sur fond d'intérêt institutionnel</a></h3>
                    <p class="news-meta">Il y a 2h • CoinDesk</p>
                </div>
            </article>
            <article class="news-card">
                <img src="https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&q=80" alt="Energy" class="news-image">
                <div class="news-content">
                    <span class="news-category">Énergie</span>
                    <h3 class="news-title"><a href="#">Le brut Brent stable à $85 le baril</a></h3>
                    <p class="news-meta">Il y a 3h • AFP</p>
                </div>
            </article>
            <article class="news-card">
                <img src="https://images.unsplash.com/photo-1565514020176-0223a8e73e48?w=400&q=80" alt="Tech" class="news-image">
                <div class="news-content">
                    <span class="news-category">Technologie</span>
                    <h3 class="news-title"><a href="#">Apple présente ses nouvelles innovations</a></h3>
                    <p class="news-meta">Il y a 5h • WSJ</p>
                </div>
            </article>
            <article class="news-card">
                <img src="https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=400&q=80" alt="Finance" class="news-image">
                <div class="news-content">
                    <span class="news-category">Finance</span>
                    <h3 class="news-title"><a href="#">JPMorgan dépasse les attentes au T1</a></h3>
                    <p class="news-meta">Il y a 6h • Bloomberg</p>
                </div>
            </article>
            <article class="news-card">
                <img src="https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=400&q=80" alt="Europe" class="news-image">
                <div class="news-content">
                    <span class="news-category">Europe</span>
                    <h3 class="news-title"><a href="#">Le CAC 40 progresse de 0.8%</a></h3>
                    <p class="news-meta">Il y a 7h • Le Monde</p>
                </div>
            </article>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card"><div class="stat-value">150+</div><div class="stat-label">Actions</div></div>
            <div class="stat-card"><div class="stat-value">50+</div><div class="stat-label">ETF</div></div>
            <div class="stat-card"><div class="stat-value">15+</div><div class="stat-label">Métriques</div></div>
            <div class="stat-card"><div class="stat-value">100%</div><div class="stat-label">Gratuit</div></div>
        </div>
    </div>
    
    <script>
    </script>
</body>
</html>
'''

ANALYSIS_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>{{ data.ticker }} - Analysis</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        :root {
            --bg-primary: #0a0a0f;
            --bg-secondary: #12121a;
            --bg-tertiary: #1a1a25;
            --accent-cyan: #00d4ff;
            --accent-green: #00ff88;
            --accent-gold: #ffd700;
            --text-primary: #ffffff;
            --text-secondary: #a0a0a0;
            --text-muted: #666680;
            --border-color: rgba(255, 255, 255, 0.08);
        }
        body { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; background: linear-gradient(180deg, #0a0a0f 0%, #12121a 100%); color: #e0e0e0; min-height: 100vh; }
        .bg-pattern { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(ellipse at 20% 20%, rgba(0, 212, 255, 0.08) 0%, transparent 50%), radial-gradient(ellipse at 80% 80%, rgba(0, 255, 136, 0.05) 0%, transparent 50%); z-index: -1; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        
        .navbar { display: flex; justify-content: space-between; align-items: center; padding: 1rem 2rem; background: rgba(10, 10, 15, 0.85); backdrop-filter: blur(20px); border-bottom: 1px solid var(--border-color); position: sticky; top: 0; z-index: 100; border-radius: 0 0 16px 16px; margin-bottom: 2rem; }
        .logo { display: flex; align-items: center; gap: 0.75rem; font-family: 'Playfair Display', serif; font-size: 1.5rem; font-weight: 700; color: #fff; text-decoration: none; }
        .logo-icon { width: 40px; height: 40px; background: linear-gradient(135deg, #00d4ff, #00ff88); border-radius: 10px; display: flex; align-items: center; justify-content: center; }
        .nav { display: flex; gap: 0.5rem; flex-wrap: wrap; justify-content: center; }
        .nav a { color: #a0a0a0; text-decoration: none; padding: 0.6rem 1rem; border-radius: 8px; font-weight: 500; font-size: 0.9rem; transition: all 0.25s ease; }
        .nav a:hover, .nav a.active { background: rgba(0, 212, 255, 0.1); color: #00d4ff; }
        
        .card { background: var(--bg-secondary); border-radius: 16px; padding: 1.5rem; margin-bottom: 1.5rem; border: 1px solid var(--border-color); }
        .ticker-header { display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem; margin-bottom: 1.5rem; }
        .ticker-info h1 { font-family: 'Playfair Display', serif; font-size: 2.5rem; color: var(--accent-cyan); }
        .ticker-name { color: var(--text-secondary); font-size: 1.1rem; margin-top: 0.5rem; }
        .ticker-sector { display: inline-block; padding: 0.3rem 0.8rem; background: var(--bg-tertiary); border-radius: 20px; font-size: 0.8rem; color: var(--text-muted); margin-top: 0.5rem; }
        
        .score-display { text-align: center; padding: 2rem; background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(0, 255, 136, 0.05)); border-radius: 16px; border: 1px solid var(--border-color); }
        .score-value { font-family: 'JetBrains Mono', monospace; font-size: 4rem; font-weight: 700; }
        .score-good { color: var(--accent-green); }
        .score-medium { color: var(--accent-gold); }
        .score-bad { color: #ff4757; }
        .score-label { font-size: 1rem; color: var(--text-muted); margin-top: 0.5rem; }
        .recommendation { display: inline-block; padding: 0.5rem 1.5rem; border-radius: 25px; font-weight: 600; margin-top: 1rem; }
        .rec-buy { background: rgba(0, 255, 136, 0.15); color: var(--accent-green); }
        .rec-hold { background: rgba(255, 215, 0, 0.15); color: var(--accent-gold); }
        .rec-sell { background: rgba(255, 71, 87, 0.15); color: #ff4757; }
        
        .section-title { font-family: 'Playfair Display', serif; font-size: 1.4rem; font-weight: 600; margin: 1.5rem 0 1rem; color: var(--accent-cyan); display: flex; align-items: center; gap: 0.5rem; }
        .section-title::before { content: ''; width: 4px; height: 24px; background: linear-gradient(180deg, var(--accent-cyan), var(--accent-green)); border-radius: 2px; }
        
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; }
        .stat { background: var(--bg-tertiary); padding: 1rem; border-radius: 12px; text-align: center; border: 1px solid var(--border-color); transition: all 0.3s ease; }
        .stat:hover { border-color: var(--accent-cyan); }
        .stat-label { color: var(--text-muted); font-size: 0.8rem; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.5px; }
        .stat-value { font-family: 'JetBrains Mono', monospace; font-size: 1.3rem; font-weight: 600; color: var(--text-primary); }
        .stat-good { color: var(--accent-green); } .stat-medium { color: var(--accent-gold); } .stat-bad { color: #ff4757; }
        
        .chart-container { background: var(--bg-tertiary); border-radius: 16px; padding: 1rem; margin-bottom: 1.5rem; border: 1px solid var(--border-color); overflow: hidden; }
        .chart-container iframe { width: 100%; height: 400px; border: none; }
        
        .buy-target { background: linear-gradient(135deg, var(--accent-green), #00cc6a); color: #000; padding: 1.5rem; border-radius: 16px; text-align: center; font-size: 1.5rem; font-weight: 700; margin-top: 1.5rem; }
        .buy-target .discount { font-size: 0.9rem; opacity: 0.8; margin-top: 0.5rem; font-weight: 500; }
        
        .news-links { display: flex; gap: 0.75rem; flex-wrap: wrap; margin-top: 1rem; }
        .news-link { padding: 0.75rem 1.25rem; background: var(--bg-tertiary); border: 1px solid var(--border-color); border-radius: 25px; color: var(--accent-cyan); text-decoration: none; font-size: 0.9rem; transition: all 0.3s ease; }
        .news-link:hover { background: rgba(0, 212, 255, 0.1); border-color: var(--accent-cyan); }
        
        .action-buttons { display: flex; gap: 1rem; flex-wrap: wrap; justify-content: center; margin-top: 2rem; }
        .btn { padding: 1rem 2rem; border-radius: 12px; font-weight: 600; text-decoration: none; transition: all 0.3s ease; }
        .btn-primary { background: linear-gradient(135deg, var(--accent-cyan), #0099cc); color: var(--bg-primary); }
        .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(0, 212, 255, 0.4); }
        .btn-secondary { background: var(--bg-tertiary); color: var(--accent-gold); border: 1px solid var(--border-color); }
        .btn-secondary:hover { background: rgba(255, 215, 0, 0.1); border-color: var(--accent-gold); }
        
        @media (max-width: 768px) {
            .navbar { flex-direction: column; gap: 1rem; }
            .ticker-info h1 { font-size: 1.8rem; }
            .score-value { font-size: 3rem; }
        }
    </style>
</head>
<body>
    <div class="bg-pattern"></div>
    <nav class="navbar">
        <a href="/" class="logo">
            <div class="logo-icon">📈</div>
            <span>Stock Analyzer</span>
        </a>
        <div class="nav">
            <a href="/">Accueil</a>
            <a href="/analyze">Analyser</a>
            <a href="/watchlist">Watchlist</a>
            <a href="/saved">Analyses</a>
            <a href="/stocks">Stocks</a>
        </div>
    </nav>
    
    <div class="container">
        <div class="card">
            <div class="ticker-header">
                <div class="ticker-info">
                    <h1>{{ data.ticker }}</h1>
                    <div class="ticker-name">{{ data.name }}</div>
                    <span class="ticker-sector">{{ data.sector }} | {{ data.industry }}</span>
                </div>
            </div>
            
            <div class="score-display">
                <div class="score-value {% if data.score >= 7 %}score-good{% elif data.score >= 5 %}score-medium{% else %}score-bad{% endif %}">
                    {{ "%.1f"|format(data.score) }}/10
                </div>
                <div class="score-label">
                    {% if data.score >= 7 %}EXCELLENT{% elif data.score >= 5 %}GOOD{% else %}WEAK{% endif %}
                </div>
                <div class="recommendation {% if data.score >= 7 %}rec-buy{% elif data.score >= 5 %}rec-hold{% else %}rec-sell{% endif %}">
                    {% if data.score >= 7 %}STRONG BUY{% elif data.score >= 5 %}HOLD{% else %}AVOID{% endif %}
                </div>
            </div>
        </div>
        
        <div class="chart-container">
            <iframe src="https://www.tradingview.com/widget/advanced-chart/?symbol={{ data.ticker }}" allowtransparency="true" frameborder="0"></iframe>
        </div>
        
        <h2 class="section-title">Prix & Valorisation</h2>
        <div class="grid">
            <div class="stat"><div class="stat-label">Prix</div><div class="stat-value">${{ "%.2f"|format(data.price) }}</div></div>
            <div class="stat"><div class="stat-label">P/E</div><div class="stat-value {% if data.pe_ratio < 25 %}stat-good{% elif data.pe_ratio < 40 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.pe_ratio) if data.pe_ratio else 'N/A' }}</div></div>
            <div class="stat"><div class="stat-label">Forward P/E</div><div class="stat-value {% if data.fwd_pe < 20 %}stat-good{% elif data.fwd_pe < 35 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.fwd_pe) if data.fwd_pe else 'N/A' }}</div></div>
            <div class="stat"><div class="stat-label">PEG</div><div class="stat-value {% if data.peg < 1.5 %}stat-good{% elif data.peg < 3 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.2f"|format(data.peg) if data.peg else 'N/A' }}</div></div>
            <div class="stat"><div class="stat-label">P/B</div><div class="stat-value {% if data.pb < 5 %}stat-good{% elif data.pb < 10 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.pb) if data.pb else 'N/A' }}</div></div>
            <div class="stat"><div class="stat-label">P/S</div><div class="stat-value {% if data.ps < 5 %}stat-good{% elif data.ps < 10 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.ps) if data.ps else 'N/A' }}</div></div>
        </div>
        
        <h2 class="section-title">Rentabilité</h2>
        <div class="grid">
            <div class="stat"><div class="stat-label">ROE</div><div class="stat-value {% if data.roe > 0.15 %}stat-good{% elif data.roe > 0.08 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.roe * 100) if data.roe else 'N/A' }}%</div></div>
            <div class="stat"><div class="stat-label">ROA</div><div class="stat-value {% if data.roa > 0.05 %}stat-good{% elif data.roa > 0.02 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.roa * 100) if data.roa else 'N/A' }}%</div></div>
            <div class="stat"><div class="stat-label">ROIC</div><div class="stat-value {% if data.roic > 15 %}stat-good{% elif data.roic > 8 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.roic) if data.roic else 'N/A' }}%</div></div>
            <div class="stat"><div class="stat-label">Marge Nette</div><div class="stat-value {% if data.mg > 0.15 %}stat-good{% elif data.mg > 0.05 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.mg * 100) if data.mg else 'N/A' }}%</div></div>
            <div class="stat"><div class="stat-label">Marge Op.</div><div class="stat-value {% if data.om > 0.15 %}stat-good{% elif data.om > 0.08 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.om * 100) if data.om else 'N/A' }}%</div></div>
            <div class="stat"><div class="stat-label">Marge brute</div><div class="stat-value {% if data.gm > 0.30 %}stat-good{% elif data.gm > 0.20 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.gm * 100) if data.gm else 'N/A' }}%</div></div>
        </div>
        
        <h2 class="section-title">Croissance</h2>
        <div class="grid">
            <div class="stat"><div class="stat-label">Croissance Revenus</div><div class="stat-value {% if data.rev_growth > 0.10 %}stat-good{% elif data.rev_growth > 0 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.rev_growth * 100) if data.rev_growth else 'N/A' }}%</div></div>
            <div class="stat"><div class="stat-label">Croissance Bénéfices</div><div class="stat-value {% if data.earn_growth > 0.10 %}stat-good{% elif data.earn_growth > 0 %}stat-medium{% else %}stat-bad{% endif %}">{{ "%.1f"|format(data.earn_growth * 100) if data.earn_growth else 'N/A' }}%</div></div>
        </div>
        
        <h2 class="section-title">Technique</h2>
        <div class="grid">
            <div class="stat"><div class="stat-label">RSI</div><div class="stat-value {% if data.rsi and data.rsi < 30 %}stat-good{% elif data.rsi and data.rsi > 70 %}stat-bad{% endif %}">{{ "%.1f"|format(data.rsi) if data.rsi else 'N/A' }}</div></div>
            <div class="stat"><div class="stat-label">MA50</div><div class="stat-value">${{ "%.2f"|format(data.ma50) if data.ma50 else 'N/A' }}</div></div>
            <div class="stat"><div class="stat-label">MA200</div><div class="stat-value">${{ "%.2f"|format(data.ma200) if data.ma200 else 'N/A' }}</div></div>
            <div class="stat"><div class="stat-label">Support</div><div class="stat-value">${{ "%.2f"|format(data.support) if data.support else 'N/A' }}</div></div>
            <div class="stat"><div class="stat-label">Résistance</div><div class="stat-value">${{ "%.2f"|format(data.resistance) if data.resistance else 'N/A' }}</div></div>
            <div class="stat"><div class="stat-label">Tendance</div><div class="stat-value {% if data.trend == 'UPTREND' %}stat-good{% elif data.trend == 'DOWNTREND' %}stat-bad{% endif %}">{{ data.trend }}</div></div>
        </div>
        
        <h2 class="section-title">Prévisions de prix</h2>
        <div class="grid">
            {% set change_1w = ((data.forecast_1w / data.price - 1) * 100) if data.forecast_1w else 0 %}
            {% set change_1m = ((data.forecast_1m / data.price - 1) * 100) if data.forecast_1m else 0 %}
            {% set change_6m = ((data.forecast_6m / data.price - 1) * 100) if data.forecast_6m else 0 %}
            <div class="stat">
                <div class="stat-label">1 Semaine</div>
                <div class="stat-value">${{ "%.2f"|format(data.forecast_1w) if data.forecast_1w else 'N/A' }}</div>
                <div class="stat-value {% if change_1w > 0 %}stat-good{% elif change_1w < 0 %}stat-bad{% endif %}" style="font-size:1rem;">{{ "%.1f"|format(change_1w) }}%</div>
            </div>
            <div class="stat">
                <div class="stat-label">1 Mois</div>
                <div class="stat-value">${{ "%.2f"|format(data.forecast_1m) if data.forecast_1m else 'N/A' }}</div>
                <div class="stat-value {% if change_1m > 0 %}stat-good{% elif change_1m < 0 %}stat-bad{% endif %}" style="font-size:1rem;">{{ "%.1f"|format(change_1m) }}%</div>
            </div>
            <div class="stat">
                <div class="stat-label">6 Mois</div>
                <div class="stat-value">${{ "%.2f"|format(data.forecast_6m) if data.forecast_6m else 'N/A' }}</div>
                <div class="stat-value {% if change_6m > 0 %}stat-good{% elif change_6m < 0 %}stat-bad{% endif %}" style="font-size:1rem;">{{ "%.1f"|format(change_6m) }}%</div>
            </div>
        </div>
        
        <div class="buy-target">
            Prix d'achat cible: ${{ "%.2f"|format(data.target_buy) }}
            <div class="discount">({{ "%.0f"|format((data.target_buy / data.price - 1) * 100) }}% de remise)</div>
        </div>
        
        <div class="card" style="margin-top: 1.5rem;">
            <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:1rem;">
                <div>
                    <div class="stat-label">Market Cap</div>
                    <div class="stat-value">${{ "%.2f"|format(data.mcap / 1e12) if data.mcap else 0 }}T</div>
                </div>
                <div>
                    <div class="stat-label">BETA</div>
                    <div class="stat-value">{{ "%.2f"|format(data.beta) if data.beta else 'N/A' }}</div>
                </div>
                <div>
                    <div class="stat-label">Dividende</div>
                    <div class="stat-value">{{ "%.2f"|format(data.div_yield * 100) if data.div_yield else 0 }}%</div>
                </div>
            </div>
        </div>
        
        <h2 class="section-title">Liens & Info</h2>
        <div class="news-links">
            <a href="{{ news.tradingview }}" target="_blank" class="news-link">📊 TradingView</a>
            <a href="{{ news.google }}" target="_blank" class="news-link">🔍 Google Finance</a>
            <a href="{{ news.yahoo }}" target="_blank" class="news-link">📈 Yahoo Finance</a>
            <a href="{{ news.quiver }}" target="_blank" class="news-link">📉 Quiver Quantitative</a>
        </div>
        
        <div class="action-buttons">
            <a href="/save/{{ data.ticker }}" class="btn btn-primary">Sauvegarder</a>
            <a href="/add-watchlist/{{ data.ticker }}" class="btn btn-secondary">Ajouter à la watchlist</a>
        </div>
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
            analysis = {
                'id': len(all_data['analyses']) + 1,
                'ticker': data['ticker'],
                'name': data['name'],
                'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'score': data['score'],
                'price': data['price'],
                'target_buy': data['target_buy'],
                'sector': data['sector'],
                'pe_ratio': data.get('pe_ratio', 0),
                'peg': data.get('peg', 0),
                'roe': data.get('roe', 0),
                'rev_growth': data.get('rev_growth', 0),
                'rsi': data.get('rsi', 0),
                'trend': data.get('trend', 'NEUTRAL'),
                'support': data.get('support', 0),
                'resistance': data.get('resistance', 0),
                'forecast_1w': data.get('forecast_1w', 0),
                'forecast_1m': data.get('forecast_1m', 0),
                'forecast_6m': data.get('forecast_6m', 0),
            }
            all_data['analyses'].append(analysis)
            save_data(all_data)
            return f'<p style="text-align:center;color:#00ff88;padding:50px;background:#0a0a0f;color:#fff;">Analysis for {ticker} saved!</p><p style="text-align:center;"><a href="/saved" style="color:#00d4ff;">View Saved Analyses</a></p>'
        return f'<p style="text-align:center;color:#ff4444;">Could not analyze {ticker}</p>'
    except Exception as e:
        return f'<p style="text-align:center;color:#ff4444;">Error: {str(e)}</p>'

@app.route('/saved')
def saved():
    all_data = load_data()
    if not all_data['analyses']:
        content = '<p style="text-align:center;color:#888;">No saved analyses yet. Analyze a stock and click "Save Analysis" to save it here.</p>'
    else:
        content = '<div style="overflow-x:auto;"><table style="min-width:600px;"><tr><th>#</th><th>Ticker</th><th>Name</th><th>Date</th><th>Score</th><th>Price</th><th>Target</th><th></th></tr>'
        for a in reversed(all_data['analyses']):
            score_class = 'score-good' if a['score'] >= 7 else 'score-medium' if a['score'] >= 5 else 'score-bad'
            content += f'''<tr>
                <td>{a.get('id', '')}</td>
                <td style="color:#00d4ff;font-weight:bold;">{a['ticker']}</td>
                <td style="color:#888;">{a.get('name', a['ticker'])}</td>
                <td>{a['date']}</td>
                <td class="score {score_class}">{a['score']:.1f}</td>
                <td>${a['price']:.2f}</td>
                <td>${a['target_buy']:.2f}</td>
                <td><a href="/saved/{a.get('id', a['ticker'])}" style="background:#00d4ff;color:#000;padding:5px 15px;border-radius:5px;text-decoration:none;font-size:0.85em;">View</a></td>
            </tr>'''
        content += '</table></div>'
    return render_template_string(SIMPLE_PAGE, title=f'Saved Analyses ({len(all_data["analyses"])})', content=content)

@app.route('/saved/<int:analysis_id>')
def view_saved(analysis_id):
    all_data = load_data()
    analysis = next((a for a in all_data['analyses'] if a.get('id') == analysis_id), None)
    if not analysis:
        return '<p style="text-align:center;color:#ff4444;">Analysis not found. <a href="/saved" style="color:#00d4ff;">Back to Saved</a></p>'
    
    change_1w = ((analysis.get('forecast_1w', 0) / analysis['price'] - 1) * 100) if analysis.get('forecast_1w') else 0
    change_1m = ((analysis.get('forecast_1m', 0) / analysis['price'] - 1) * 100) if analysis.get('forecast_1m') else 0
    change_6m = ((analysis.get('forecast_6m', 0) / analysis['price'] - 1) * 100) if analysis.get('forecast_6m') else 0
    
    score_class = 'score-good' if analysis['score'] >= 7 else 'score-medium' if analysis['score'] >= 5 else 'score-bad'
    recommendation = 'STRONG BUY' if analysis['score'] >= 7 else 'HOLD' if analysis['score'] >= 5 else 'AVOID'
    
    content = f'''
    <div class="card">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;">
            <div>
                <div class="ticker" style="color:#00d4ff;font-size:2em;font-weight:bold;">{analysis['ticker']}</div>
                <div style="color:#888;">{analysis.get('name', analysis['ticker'])} | {analysis.get('sector', 'Unknown')}</div>
            </div>
            <div style="text-align:right;">
                <div style="color:#888;font-size:0.9em;">Saved on {analysis['date']}</div>
            </div>
        </div>
        <div class="score {score_class}" style="font-size:3em;text-align:center;margin:20px 0;">{analysis['score']:.1f}/10</div>
        <div style="text-align:center;color:#888;">{recommendation}</div>
    </div>
    
    <div class="card">
        <h3 style="color:#00d4ff;margin-bottom:15px;">Key Metrics (at time of save)</h3>
        <div class="grid">
            <div class="stat"><div class="stat-label">Price</div><div class="stat-value">${analysis['price']:.2f}</div></div>
            <div class="stat"><div class="stat-label">Target Buy</div><div class="stat-value stat-good">${analysis['target_buy']:.2f}</div></div>
            <div class="stat"><div class="stat-label">P/E</div><div class="stat-value">{analysis.get('pe_ratio', 'N/A')}</div></div>
            <div class="stat"><div class="stat-label">PEG</div><div class="stat-value">{analysis.get('peg', 'N/A')}</div></div>
            <div class="stat"><div class="stat-label">ROE</div><div class="stat-value">{analysis.get('roe', 0) * 100:.1f}%</div></div>
            <div class="stat"><div class="stat-label">Revenue Growth</div><div class="stat-value">{analysis.get('rev_growth', 0) * 100:.1f}%</div></div>
        </div>
    </div>
    
    <div class="card">
        <h3 style="color:#00d4ff;margin-bottom:15px;">Technical (at time of save)</h3>
        <div class="grid">
            <div class="stat"><div class="stat-label">RSI</div><div class="stat-value">{analysis.get('rsi', 'N/A')}</div></div>
            <div class="stat"><div class="stat-label">Trend</div><div class="stat-value">{analysis.get('trend', 'NEUTRAL')}</div></div>
            <div class="stat"><div class="stat-label">Support</div><div class="stat-value">${analysis.get('support', 0):.2f}</div></div>
            <div class="stat"><div class="stat-label">Resistance</div><div class="stat-value">${analysis.get('resistance', 0):.2f}</div></div>
        </div>
    </div>
    
    <div class="card">
        <h3 style="color:#00d4ff;margin-bottom:15px;">Price Forecast (at time of save)</h3>
        <div class="grid">
            <div class="stat">
                <div class="stat-label">1 Week</div>
                <div class="stat-value">${analysis.get('forecast_1w', 0):.2f}</div>
                <div style="font-size:0.8em;color:{"#00ff88" if change_1w > 0 else "#ff4444" if change_1w < 0 else "#888"};">{change_1w:.1f}%</div>
            </div>
            <div class="stat">
                <div class="stat-label">1 Month</div>
                <div class="stat-value">${analysis.get('forecast_1m', 0):.2f}</div>
                <div style="font-size:0.8em;color:{"#00ff88" if change_1m > 0 else "#ff4444" if change_1m < 0 else "#888"};">{change_1m:.1f}%</div>
            </div>
            <div class="stat">
                <div class="stat-label">6 Months</div>
                <div class="stat-value">${analysis.get('forecast_6m', 0):.2f}</div>
                <div style="font-size:0.8em;color:{"#00ff88" if change_6m > 0 else "#ff4444" if change_6m < 0 else "#888"};">{change_6m:.1f}%</div>
            </div>
        </div>
    </div>
    
    <div style="text-align:center;margin-top:20px;">
        <a href="/analyze?ticker={analysis['ticker']}" style="background:#00d4ff;color:#000;padding:15px 30px;border-radius:10px;text-decoration:none;font-weight:bold;">See Current Analysis</a>
        <a href="/saved" style="background:#1a1a25;color:#00d4ff;padding:15px 30px;border-radius:10px;text-decoration:none;margin-left:10px;">Back to Saved</a>
    </div>
    '''
    return render_template_string(SIMPLE_PAGE, title=f'{analysis["ticker"]} - {analysis["date"]}', content=content)

@app.route('/delete/<int:analysis_id>')
def delete_analysis(analysis_id):
    all_data = load_data()
    all_data['analyses'] = [a for a in all_data['analyses'] if a.get('id') != analysis_id]
    save_data(all_data)
    return f'<p style="text-align:center;color:#ff4444;padding:50px;">Analysis deleted!</p><p style="text-align:center;"><a href="/saved" style="color:#00d4ff;">Back to Saved</a></p>'

@app.route('/add-watchlist/<ticker>')
def add_watchlist(ticker):
    all_data = load_data()
    ticker_upper = ticker.upper().strip()
    if ticker_upper.lower() in COMPANIES:
        ticker_upper = COMPANIES[ticker_upper.lower()]
    if not any(w.get('ticker') == ticker_upper for w in all_data['watchlist']):
        all_data['watchlist'].append({
            'id': len(all_data['watchlist']) + 1,
            'ticker': ticker_upper,
            'date_added': datetime.now().strftime('%Y-%m-%d')
        })
        save_data(all_data)
        return f'<p style="text-align:center;color:#00ff88;padding:50px;background:#0a0a0f;">{ticker_upper} added to your watchlist!</p><p style="text-align:center;"><a href="/my-watchlist" style="color:#00d4ff;">View Watchlist</a></p>'
    return f'<p style="text-align:center;color:#ffaa00;padding:50px;background:#0a0a0f;">{ticker_upper} is already in your watchlist!</p><p style="text-align:center;"><a href="/my-watchlist" style="color:#00d4ff;">View Watchlist</a></p>'

@app.route('/remove-watchlist/<int:watchlist_id>')
def remove_watchlist(watchlist_id):
    all_data = load_data()
    all_data['watchlist'] = [w for w in all_data['watchlist'] if w.get('id') != watchlist_id]
    save_data(all_data)
    return f'<p style="text-align:center;color:#ff4444;padding:50px;background:#0a0a0f;">Removed from watchlist!</p><p style="text-align:center;"><a href="/my-watchlist" style="color:#00d4ff;">Back to Watchlist</a></p>'

@app.route('/my-watchlist')
def my_watchlist():
    all_data = load_data()
    if not all_data['watchlist']:
        content = '''
        <div class="card">
            <h2 style="color:#ffaa00;margin-bottom:20px;">Your Personal Watchlist</h2>
            <p style="color:#888;text-align:center;">Your watchlist is empty.</p>
            <p style="color:#888;text-align:center;margin-top:20px;">Search for a stock and click "Add to Watchlist" to add it.</p>
        </div>
        '''
    else:
        content = '<div class="card"><h2 style="color:#ffaa00;margin-bottom:20px;">Your Personal Watchlist</h2><table><tr><th>#</th><th>Ticker</th><th>Date Added</th><th></th><th></th></tr>'
        for w in reversed(all_data['watchlist']):
            content += f'''<tr>
                <td>{w.get('id', '')}</td>
                <td><a href="/analyze?ticker={w['ticker']}" style="color:#00d4ff;font-weight:bold;">{w['ticker']}</a></td>
                <td>{w.get('date_added', '')}</td>
                <td><a href="/analyze?ticker={w['ticker']}" style="background:#00d4ff;color:#000;padding:5px 15px;border-radius:5px;text-decoration:none;font-size:0.85em;">Analyze</a></td>
                <td><a href="/remove-watchlist/{w.get('id', '')}" onclick="return confirm('Remove {w['ticker']} from watchlist?')" style="background:#ff4444;color:#fff;padding:5px 15px;border-radius:5px;text-decoration:none;font-size:0.85em;">Remove</a></td>
            </tr>'''
        content += '</table></div>'
    return render_template_string(SIMPLE_PAGE, title=f'My Watchlist ({len(all_data["watchlist"])})', content=content)

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
    
    etf_picks = [
        {'ticker': 'SPY', 'reason': 'S&P 500 - Diversification passive'},
        {'ticker': 'QQQ', 'reason': 'NASDAQ 100 - Tech exposure'},
        {'ticker': 'VOO', 'reason': 'Vanguard S&P 500 - Low fees'},
        {'ticker': 'VTI', 'reason': 'Total US Market - Broad exposure'},
        {'ticker': 'GLD', 'reason': 'Gold - Inflation hedge'},
        {'ticker': 'BND', 'reason': 'Bonds - Stability'},
        {'ticker': 'SCHD', 'reason': 'Dividends - Income'},
    ]
    
    content = '''
    <div class="card">
        <h2 style="color:#00ff88;margin-bottom:20px;">Top ETF Picks</h2>
        <p style="color:#888;margin-bottom:20px;">Les meilleurs ETF pour diversifier votre portefeuille</p>
        <table>
            <tr><th>Ticker</th><th>Raison</th><th></th></tr>
    '''
    for s in etf_picks:
        content += f'''<tr>
            <td><a href="/analyze?ticker={s['ticker']}" style="color:#ffd700;font-weight:bold;">{s['ticker']}</a></td>
            <td style="color:#ccc;">{s['reason']}</td>
            <td><a href="/save/{s['ticker']}" style="background:#ffd700;color:#000;padding:5px 15px;border-radius:5px;text-decoration:none;font-size:0.85em;">Analyser</a></td>
        </tr>'''
    
    content += '''
        </table>
    </div>
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

STOCKS_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Stocks Database</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0a0a0f; color: #e0e0e0; min-height: 100vh; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        h1 { color: #00d4ff; margin-bottom: 20px; }
        .nav { display: flex; gap: 10px; justify-content: center; margin-bottom: 20px; flex-wrap: wrap; }
        .nav a { padding: 10px 20px; background: #1a1a25; color: #00d4ff; text-decoration: none; border-radius: 25px; }
        .search-box { display: flex; gap: 10px; margin-bottom: 30px; flex-wrap: wrap; }
        input { padding: 15px 20px; font-size: 18px; border: 2px solid #333; border-radius: 10px; background: #1a1a25; color: #fff; width: 300px; }
        button { padding: 15px 30px; font-size: 18px; background: #00d4ff; color: #000; border: none; border-radius: 10px; cursor: pointer; font-weight: bold; }
        .result { background: #12121a; border-radius: 15px; padding: 25px; margin-bottom: 20px; }
        .result-found { border: 2px solid #00ff88; }
        .result-notfound { border: 2px solid #ff4444; }
        .ticker-big { font-size: 2em; font-weight: bold; color: #00d4ff; }
        .result-btn { display: inline-block; background: #00d4ff; color: #000; padding: 10px 20px; border-radius: 10px; text-decoration: none; margin-top: 15px; }
        .all-stocks { background: #12121a; border-radius: 15px; padding: 25px; margin-top: 30px; }
        .stock-tag { display: inline-block; background: #1a1a25; padding: 8px 15px; margin: 5px; border-radius: 20px; color: #00d4ff; text-decoration: none; font-size: 0.9em; }
        .stock-tag:hover { background: #222; }
        .count { color: #888; margin-bottom: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Stocks Database</h1>
        <div class="nav">
            <a href="/">Home</a>
            <a href="/portfolio">Portfolio</a>
            <a href="/saved">Saved Analyses</a>
            <a href="/watchlist">Watchlist</a>
            <a href="/my-watchlist">My Watchlist</a>
            <a href="/stocks">Stocks</a>
            <a href="/sources">Sources</a>
        </div>
        <form action="/stocks" method="get" class="search-box">
            <input type="text" name="q" placeholder="Search ticker or name (ex: apple, AAPL)" value="{{ query }}">
            <button type="submit">Search</button>
        </form>
        {% if result %}
            <div class="result {% if result.found %}result-found{% else %}result-notfound{% endif %}">
                {% if result.found %}
                    <div class="ticker-big">{{ result.ticker }}</div>
                    <p style="color:#00ff88;margin-top:10px;">Available! Enter this ticker to analyze.</p>
                    <a href="/analyze?ticker={{ result.ticker }}" class="result-btn">Analyze {{ result.ticker }}</a>
                {% else %}
                    <div style="color:#ff4444;font-size:1.5em;">Not in database</div>
                    <p style="color:#888;margin-top:10px;">Try searching on Yahoo Finance directly.</p>
                    <a href="https://finance.yahoo.com/quote/{{ query }}" target="_blank" class="result-btn" style="background:#ff4444;">Search on Yahoo Finance</a>
                {% endif %}
            </div>
        {% endif %}
        <div class="all-stocks">
            <div class="count">{{ count }} stocks available</div>
            <div>
            {% for ticker in tickers %}
                <a href="/analyze?ticker={{ ticker }}" class="stock-tag">{{ ticker }}</a>
            {% endfor %}
            </div>
        </div>
    </div>
</body>
</html>
'''

@app.route('/stocks')
def stocks():
    query = request.args.get('q', '').strip().lower()
    result = None
    if query:
        if query in COMPANIES:
            result = {'found': True, 'ticker': COMPANIES[query]}
        elif query.upper() in COMPANIES.values():
            result = {'found': True, 'ticker': query.upper()}
        else:
            result = {'found': False, 'query': query}
    
    tickers = sorted(set(COMPANIES.values()))
    return render_template_string(
        STOCKS_HTML,
        query=query,
        result=result,
        tickers=tickers,
        count=len(tickers)
    )

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
