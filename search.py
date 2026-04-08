"""
Module de recherche d'entreprises - correspondance ticker <-> nom
Inclut une base de données complète des entreprises majeures
"""

from typing import Dict, List, Optional, Tuple


COMPANY_DATABASE: Dict[str, Dict] = {
    # Tech Giants
    "MSFT": {"name": "Microsoft Corporation", "ticker": "MSFT", "sector": "Technology", "industry": "Software"},
    "AAPL": {"name": "Apple Inc.", "ticker": "AAPL", "sector": "Technology", "industry": "Consumer Electronics"},
    "GOOGL": {"name": "Alphabet Inc. Class A", "ticker": "GOOGL", "sector": "Technology", "industry": "Internet Services"},
    "GOOG": {"name": "Alphabet Inc. Class C", "ticker": "GOOG", "sector": "Technology", "industry": "Internet Services"},
    "META": {"name": "Meta Platforms Inc.", "ticker": "META", "sector": "Technology", "industry": "Social Media"},
    "AMZN": {"name": "Amazon.com Inc.", "ticker": "AMZN", "sector": "Consumer Cyclical", "industry": "E-commerce"},
    "NVDA": {"name": "NVIDIA Corporation", "ticker": "NVDA", "sector": "Technology", "industry": "Semiconductors"},
    "TSLA": {"name": "Tesla Inc.", "ticker": "TSLA", "sector": "Consumer Cyclical", "industry": "Auto Manufacturers"},
    "AVGO": {"name": "Broadcom Inc.", "ticker": "AVGO", "sector": "Technology", "industry": "Semiconductors"},
    "ORCL": {"name": "Oracle Corporation", "ticker": "ORCL", "sector": "Technology", "industry": "Software"},
    "CRM": {"name": "Salesforce Inc.", "ticker": "CRM", "sector": "Technology", "industry": "Software"},
    "AMD": {"name": "Advanced Micro Devices", "ticker": "AMD", "sector": "Technology", "industry": "Semiconductors"},
    "INTC": {"name": "Intel Corporation", "ticker": "INTC", "sector": "Technology", "industry": "Semiconductors"},
    "QCOM": {"name": "QUALCOMM Inc.", "ticker": "QCOM", "sector": "Technology", "industry": "Semiconductors"},
    "TXN": {"name": "Texas Instruments", "ticker": "TXN", "sector": "Technology", "industry": "Semiconductors"},
    "ADBE": {"name": "Adobe Inc.", "ticker": "ADBE", "sector": "Technology", "industry": "Software"},
    "NFLX": {"name": "Netflix Inc.", "ticker": "NFLX", "sector": "Communication Services", "industry": "Entertainment"},
    "PYPL": {"name": "PayPal Holdings", "ticker": "PYPL", "sector": "Financial Services", "industry": "Payment Processing"},
    "UBER": {"name": "Uber Technologies", "ticker": "UBER", "sector": "Technology", "industry": "Software"},
    "ABNB": {"name": "Airbnb Inc.", "ticker": "ABNB", "sector": "Consumer Cyclical", "industry": "Lodging"},
    "SHOP": {"name": "Shopify Inc.", "ticker": "SHOP", "sector": "Technology", "industry": "Software"},
    "SNOW": {"name": "Snowflake Inc.", "ticker": "SNOW", "sector": "Technology", "industry": "Software"},
    "PLTR": {"name": "Palantir Technologies", "ticker": "PLTR", "sector": "Technology", "industry": "Software"},
    "DDOG": {"name": "Datadog Inc.", "ticker": "DDOG", "sector": "Technology", "industry": "Software"},
    "NET": {"name": "Cloudflare Inc.", "ticker": "NET", "sector": "Technology", "industry": "Software"},
    "CRWD": {"name": "CrowdStrike Holdings", "ticker": "CRWD", "sector": "Technology", "industry": "Software"},
    "ZS": {"name": "Zscaler Inc.", "ticker": "ZS", "sector": "Technology", "industry": "Software"},
    "PANW": {"name": "Palo Alto Networks", "ticker": "PANW", "sector": "Technology", "industry": "Software"},
    "NOW": {"name": "ServiceNow Inc.", "ticker": "NOW", "sector": "Technology", "industry": "Software"},
    "INTU": {"name": "Intuit Inc.", "ticker": "INTU", "sector": "Technology", "industry": "Software"},
    "MSI": {"name": "Motorola Solutions", "ticker": "MSI", "sector": "Technology", "industry": "Communication Equipment"},
    
    # Finance - Banques
    "JPM": {"name": "JPMorgan Chase & Co.", "ticker": "JPM", "sector": "Financial Services", "industry": "Banking"},
    "BAC": {"name": "Bank of America", "ticker": "BAC", "sector": "Financial Services", "industry": "Banking"},
    "WFC": {"name": "Wells Fargo & Company", "ticker": "WFC", "sector": "Financial Services", "industry": "Banking"},
    "GS": {"name": "Goldman Sachs", "ticker": "GS", "sector": "Financial Services", "industry": "Investment Banking"},
    "MS": {"name": "Morgan Stanley", "ticker": "MS", "sector": "Financial Services", "industry": "Investment Banking"},
    "C": {"name": "Citigroup Inc.", "ticker": "C", "sector": "Financial Services", "industry": "Banking"},
    "BLK": {"name": "BlackRock Inc.", "ticker": "BLK", "sector": "Financial Services", "industry": "Asset Management"},
    "SCHW": {"name": "Charles Schwab", "ticker": "SCHW", "sector": "Financial Services", "industry": "Brokerage"},
    "AXP": {"name": "American Express", "ticker": "AXP", "sector": "Financial Services", "industry": "Credit Services"},
    "V": {"name": "Visa Inc.", "ticker": "V", "sector": "Financial Services", "industry": "Payment Processing"},
    "MA": {"name": "Mastercard Inc.", "ticker": "MA", "sector": "Financial Services", "industry": "Payment Processing"},
    
    # Pharma & Healthcare
    "UNH": {"name": "UnitedHealth Group", "ticker": "UNH", "sector": "Healthcare", "industry": "Health Insurance"},
    "LLY": {"name": "Eli Lilly and Company", "ticker": "LLY", "sector": "Healthcare", "industry": "Pharmaceuticals"},
    "JNJ": {"name": "Johnson & Johnson", "ticker": "JNJ", "sector": "Healthcare", "industry": "Pharmaceuticals"},
    "PFE": {"name": "Pfizer Inc.", "ticker": "PFE", "sector": "Healthcare", "industry": "Pharmaceuticals"},
    "ABBV": {"name": "AbbVie Inc.", "ticker": "ABBV", "sector": "Healthcare", "industry": "Pharmaceuticals"},
    "MRK": {"name": "Merck & Co.", "ticker": "MRK", "sector": "Healthcare", "industry": "Pharmaceuticals"},
    "TMO": {"name": "Thermo Fisher Scientific", "ticker": "TMO", "sector": "Healthcare", "industry": "Diagnostics"},
    "ABT": {"name": "Abbott Laboratories", "ticker": "ABT", "sector": "Healthcare", "industry": "Medical Devices"},
    "DHR": {"name": "Danaher Corporation", "ticker": "DHR", "sector": "Healthcare", "industry": "Medical Devices"},
    "AMGN": {"name": "Amgen Inc.", "ticker": "AMGN", "sector": "Healthcare", "industry": "Biotechnology"},
    "ISRG": {"name": "Intuitive Surgical", "ticker": "ISRG", "sector": "Healthcare", "industry": "Medical Devices"},
    "MDT": {"name": "Medtronic plc", "ticker": "MDT", "sector": "Healthcare", "industry": "Medical Devices"},
    "SYK": {"name": "Stryker Corporation", "ticker": "SYK", "sector": "Healthcare", "industry": "Medical Devices"},
    "REGN": {"name": "Regeneron Pharmaceuticals", "ticker": "REGN", "sector": "Healthcare", "industry": "Biotechnology"},
    "VRTX": {"name": "Vertex Pharmaceuticals", "ticker": "VRTX", "sector": "Healthcare", "industry": "Biotechnology"},
    "BIIB": {"name": "Biogen Inc.", "ticker": "BIIB", "sector": "Healthcare", "industry": "Biotechnology"},
    "MRNA": {"name": "Moderna Inc.", "ticker": "MRNA", "sector": "Healthcare", "industry": "Biotechnology"},
    "CVS": {"name": "CVS Health", "ticker": "CVS", "sector": "Healthcare", "industry": "Retail"},
    
    # Energy
    "XOM": {"name": "Exxon Mobil", "ticker": "XOM", "sector": "Energy", "industry": "Oil & Gas"},
    "CVX": {"name": "Chevron Corporation", "ticker": "CVX", "sector": "Energy", "industry": "Oil & Gas"},
    "COP": {"name": "ConocoPhillips", "ticker": "COP", "sector": "Energy", "industry": "Oil & Gas"},
    "SLB": {"name": "Schlumberger", "ticker": "SLB", "sector": "Energy", "industry": "Oilfield Services"},
    "EOG": {"name": "EOG Resources", "ticker": "EOG", "sector": "Energy", "industry": "Oil & Gas"},
    "OXY": {"name": "Occidental Petroleum", "ticker": "OXY", "sector": "Energy", "industry": "Oil & Gas"},
    "PSX": {"name": "Phillips 66", "ticker": "PSX", "sector": "Energy", "industry": "Oil & Gas Refining"},
    "NEE": {"name": "NextEra Energy", "ticker": "NEE", "sector": "Utilities", "industry": "Utilities"},
    "DUK": {"name": "Duke Energy", "ticker": "DUK", "sector": "Utilities", "industry": "Utilities"},
    "SO": {"name": "Southern Company", "ticker": "SO", "sector": "Utilities", "industry": "Utilities"},
    "ENPH": {"name": "Enphase Energy", "ticker": "ENPH", "sector": "Technology", "industry": "Solar"},
    "SEDG": {"name": "SolarEdge Technologies", "ticker": "SEDG", "sector": "Technology", "industry": "Solar"},
    
    # Consumer
    "WMT": {"name": "Walmart Inc.", "ticker": "WMT", "sector": "Consumer Defensive", "industry": "Retail"},
    "PG": {"name": "Procter & Gamble", "ticker": "PG", "sector": "Consumer Defensive", "industry": "Consumer Goods"},
    "KO": {"name": "Coca-Cola Company", "ticker": "KO", "sector": "Consumer Defensive", "industry": "Beverages"},
    "PEP": {"name": "PepsiCo Inc.", "ticker": "PEP", "sector": "Consumer Defensive", "industry": "Beverages"},
    "COST": {"name": "Costco Wholesale", "ticker": "COST", "sector": "Consumer Defensive", "industry": "Retail"},
    "MDLZ": {"name": "Mondelez International", "ticker": "MDLZ", "sector": "Consumer Defensive", "industry": "Food"},
    "TGT": {"name": "Target Corporation", "ticker": "TGT", "sector": "Consumer Defensive", "industry": "Retail"},
    "LOW": {"name": "Lowe's Companies", "ticker": "LOW", "sector": "Consumer Cyclical", "industry": "Retail"},
    "HD": {"name": "Home Depot", "ticker": "HD", "sector": "Consumer Cyclical", "industry": "Retail"},
    "MCD": {"name": "McDonald's Corporation", "ticker": "MCD", "sector": "Consumer Cyclical", "industry": "Restaurants"},
    "SBUX": {"name": "Starbucks Corporation", "ticker": "SBUX", "sector": "Consumer Cyclical", "industry": "Restaurants"},
    "NKE": {"name": "Nike Inc.", "ticker": "NKE", "sector": "Consumer Cyclical", "industry": "Apparel"},
    "LVS": {"name": "Las Vegas Sands", "ticker": "LVS", "sector": "Consumer Cyclical", "industry": "Casinos"},
    "MAR": {"name": "Marriott International", "ticker": "MAR", "sector": "Consumer Cyclical", "industry": "Lodging"},
    "HLT": {"name": "Hilton Worldwide", "ticker": "HLT", "sector": "Consumer Cyclical", "industry": "Lodging"},
    
    # Industrials
    "CAT": {"name": "Caterpillar Inc.", "ticker": "CAT", "sector": "Industrials", "industry": "Machinery"},
    "BA": {"name": "Boeing Company", "ticker": "BA", "sector": "Industrials", "industry": "Aerospace"},
    "HON": {"name": "Honeywell International", "ticker": "HON", "sector": "Industrials", "industry": "Conglomerate"},
    "GE": {"name": "General Electric", "ticker": "GE", "sector": "Industrials", "industry": "Conglomerate"},
    "RTX": {"name": "RTX Corporation", "ticker": "RTX", "sector": "Industrials", "industry": "Aerospace"},
    "LMT": {"name": "Lockheed Martin", "ticker": "LMT", "sector": "Industrials", "industry": "Aerospace"},
    "DE": {"name": "Deere & Company", "ticker": "DE", "sector": "Industrials", "industry": "Machinery"},
    "UPS": {"name": "United Parcel Service", "ticker": "UPS", "sector": "Industrials", "industry": "Transportation"},
    "FDX": {"name": "FedEx Corporation", "ticker": "FDX", "sector": "Industrials", "industry": "Transportation"},
    "UBER": {"name": "Uber Technologies", "ticker": "UBER", "sector": "Technology", "industry": "Software"},
    "SPOT": {"name": "Spotify Technology", "ticker": "SPOT", "sector": "Communication Services", "industry": "Entertainment"},
    
    # Telecom
    "T": {"name": "AT&T Inc.", "ticker": "T", "sector": "Communication Services", "industry": "Telecom"},
    "VZ": {"name": "Verizon Communications", "ticker": "VZ", "sector": "Communication Services", "industry": "Telecom"},
    "TMUS": {"name": "T-Mobile US", "ticker": "TMUS", "sector": "Communication Services", "industry": "Telecom"},
    "DIS": {"name": "Walt Disney Company", "ticker": "DIS", "sector": "Communication Services", "industry": "Entertainment"},
    
    # Real Estate
    "PLD": {"name": "Prologis Inc.", "ticker": "PLD", "sector": "Real Estate", "industry": "REIT"},
    "AMT": {"name": "American Tower", "ticker": "AMT", "sector": "Real Estate", "industry": "REIT"},
    "EQIX": {"name": "Equinix Inc.", "ticker": "EQIX", "sector": "Real Estate", "industry": "REIT"},
    "SPG": {"name": "Simon Property Group", "ticker": "SPG", "sector": "Real Estate", "industry": "REIT"},
    
    # Materials
    "LIN": {"name": "Linde plc", "ticker": "LIN", "sector": "Materials", "industry": "Chemicals"},
    "APD": {"name": "Air Products", "ticker": "APD", "sector": "Materials", "industry": "Chemicals"},
    "SHW": {"name": "Sherwin-Williams", "ticker": "SHW", "sector": "Materials", "industry": "Chemicals"},
    "FCX": {"name": "Freeport-McMoRan", "ticker": "FCX", "sector": "Materials", "industry": "Copper"},
    "NEM": {"name": "Newmont Corporation", "ticker": "NEM", "sector": "Materials", "industry": "Gold"},
    "AA": {"name": "Alcoa Corporation", "ticker": "AA", "sector": "Materials", "industry": "Aluminum"},
    
    # Additional Tech/AI
    "AI": {"name": "C3.ai Inc.", "ticker": "AI", "sector": "Technology", "industry": "Software"},
    "SMCI": {"name": "Super Micro Computer", "ticker": "SMCI", "sector": "Technology", "industry": "Hardware"},
    "DELL": {"name": "Dell Technologies", "ticker": "DELL", "sector": "Technology", "industry": "Hardware"},
    "HPE": {"name": "Hewlett Packard Enterprise", "ticker": "HPE", "sector": "Technology", "industry": "Hardware"},
    "ANET": {"name": "Arista Networks", "ticker": "ANET", "sector": "Technology", "industry": "Networking"},
    
    # Crypto Related
    "COIN": {"name": "Coinbase Global", "ticker": "COIN", "sector": "Financial Services", "industry": "Financial Technology"},
    "MSTR": {"name": "MicroStrategy", "ticker": "MSTR", "sector": "Technology", "industry": "Software"},
    "SQ": {"name": "Block Inc.", "ticker": "SQ", "sector": "Financial Services", "industry": "Payment Processing"},
    
    # European Companies (ADRs)
    "ASML": {"name": "ASML Holding", "ticker": "ASML", "sector": "Technology", "industry": "Semiconductors"},
    "SAP": {"name": "SAP SE", "ticker": "SAP", "sector": "Technology", "industry": "Software"},
    "TM": {"name": "Toyota Motor", "ticker": "TM", "sector": "Consumer Cyclical", "industry": "Auto Manufacturers"},
    "SONY": {"name": "Sony Group", "ticker": "SONY", "sector": "Technology", "industry": "Consumer Electronics"},
    "BABA": {"name": "Alibaba Group", "ticker": "BABA", "sector": "Consumer Cyclical", "industry": "E-commerce"},
    "TSM": {"name": "Taiwan Semiconductor", "ticker": "TSM", "sector": "Technology", "industry": "Semiconductors"},
    "NVO": {"name": "Novo Nordisk", "ticker": "NVO", "sector": "Healthcare", "industry": "Pharmaceuticals"},
    "BYDDF": {"name": "BYD Company", "ticker": "BYDDF", "sector": "Consumer Cyclical", "industry": "Auto Manufacturers"},
    
    # ETFs - US Market
    "SPY": {"name": "SPDR S&P 500 ETF", "ticker": "SPY", "sector": "ETF", "industry": "Large Cap US"},
    "VOO": {"name": "Vanguard S&P 500 ETF", "ticker": "VOO", "sector": "ETF", "industry": "Large Cap US"},
    "IVV": {"name": "iShares Core S&P 500 ETF", "ticker": "IVV", "sector": "ETF", "industry": "Large Cap US"},
    "VTI": {"name": "Vanguard Total Stock Market ETF", "ticker": "VTI", "sector": "ETF", "industry": "Total US Market"},
    "QQQ": {"name": "Invesco QQQ Trust", "ticker": "QQQ", "sector": "ETF", "industry": "NASDAQ 100"},
    "QQQM": {"name": "Invesco NASDAQ 100 ETF", "ticker": "QQQM", "sector": "ETF", "industry": "NASDAQ 100"},
    "IWM": {"name": "iShares Russell 2000 ETF", "ticker": "IWM", "sector": "ETF", "industry": "Small Cap US"},
    "DIA": {"name": "SPDR Dow Jones ETF", "ticker": "DIA", "sector": "ETF", "industry": "Dow 30"},
    
    # ETFs - International
    "VXUS": {"name": "Vanguard Total International Stock ETF", "ticker": "VXUS", "sector": "ETF", "industry": "International"},
    "IXUS": {"name": "iShares Core MSCI Total International Stock ETF", "ticker": "IXUS", "sector": "ETF", "industry": "International"},
    "EFA": {"name": "iShares MSCI EAFE ETF", "ticker": "EFA", "sector": "ETF", "industry": "Developed Markets"},
    "EEM": {"name": "iShares MSCI Emerging Markets ETF", "ticker": "EEM", "sector": "ETF", "industry": "Emerging Markets"},
    "VWO": {"name": "Vanguard FTSE Emerging Markets ETF", "ticker": "VWO", "sector": "ETF", "industry": "Emerging Markets"},
    
    # ETFs - Sectors
    "XLK": {"name": "Technology Select Sector SPDR", "ticker": "XLK", "sector": "ETF", "industry": "Technology"},
    "XLF": {"name": "Financial Select Sector SPDR", "ticker": "XLF", "sector": "ETF", "industry": "Financials"},
    "XLE": {"name": "Energy Select Sector SPDR", "ticker": "XLE", "sector": "ETF", "industry": "Energy"},
    "XLV": {"name": "Health Care Select Sector SPDR", "ticker": "XLV", "sector": "ETF", "industry": "Healthcare"},
    "XLC": {"name": "Communication Services Select Sector SPDR", "ticker": "XLC", "sector": "ETF", "industry": "Communication"},
    "XLY": {"name": "Consumer Discretionary Select Sector SPDR", "ticker": "XLY", "sector": "ETF", "industry": "Consumer Discretionary"},
    "XLP": {"name": "Consumer Staples Select Sector SPDR", "ticker": "XLP", "sector": "ETF", "industry": "Consumer Staples"},
    "XLB": {"name": "Materials Select Sector SPDR", "ticker": "XLB", "sector": "ETF", "industry": "Materials"},
    "XLI": {"name": "Industrial Select Sector SPDR", "ticker": "XLI", "sector": "ETF", "industry": "Industrials"},
    "XLRE": {"name": "Real Estate Select Sector SPDR", "ticker": "XLRE", "sector": "ETF", "industry": "Real Estate"},
    "XLU": {"name": "Utilities Select Sector SPDR", "ticker": "XLU", "sector": "ETF", "industry": "Utilities"},
    
    # ETFs - Growth/Value
    "VUG": {"name": "Vanguard Growth ETF", "ticker": "VUG", "sector": "ETF", "industry": "Growth"},
    "VTV": {"name": "Vanguard Value ETF", "ticker": "VTV", "sector": "ETF", "industry": "Value"},
    "IWF": {"name": "iShares Russell 1000 Growth ETF", "ticker": "IWF", "sector": "ETF", "industry": "Growth"},
    "IWD": {"name": "iShares Russell 1000 Value ETF", "ticker": "IWD", "sector": "ETF", "industry": "Value"},
    "SCHG": {"name": "Schwab US Large-Cap Growth ETF", "ticker": "SCHG", "sector": "ETF", "industry": "Growth"},
    "SCHD": {"name": "Schwab US Dividend Equity ETF", "ticker": "SCHD", "sector": "ETF", "industry": "Dividend"},
    "VYM": {"name": "Vanguard High Dividend Yield ETF", "ticker": "VYM", "sector": "ETF", "industry": "Dividend"},
    
    # ETFs - Bonds
    "BND": {"name": "Vanguard Total Bond Market ETF", "ticker": "BND", "sector": "ETF", "industry": "US Bonds"},
    "AGG": {"name": "iShares Core US Aggregate Bond ETF", "ticker": "AGG", "sector": "ETF", "industry": "US Bonds"},
    "TLT": {"name": "iShares 20+ Year Treasury Bond ETF", "ticker": "TLT", "sector": "ETF", "industry": "Treasury Bonds"},
    "IEF": {"name": "iShares 7-10 Year Treasury Bond ETF", "ticker": "IEF", "sector": "ETF", "industry": "Treasury Bonds"},
    "LQD": {"name": "iShares iBoxx $ Investment Grade Corporate Bond ETF", "ticker": "LQD", "sector": "ETF", "industry": "Corporate Bonds"},
    "HYG": {"name": "iShares iBoxx $ High Yield Corporate Bond ETF", "ticker": "HYG", "sector": "ETF", "industry": "High Yield Bonds"},
    
    # ETFs - Thematic
    "ARKK": {"name": "ARK Innovation ETF", "ticker": "ARKK", "sector": "ETF", "industry": "Innovation"},
    "SOXX": {"name": "iShares Semiconductor ETF", "ticker": "SOXX", "sector": "ETF", "industry": "Semiconductors"},
    "SMH": {"name": "VanEck Semiconductor ETF", "ticker": "SMH", "sector": "ETF", "industry": "Semiconductors"},
    "KWEB": {"name": "KraneShares CSI China Internet ETF", "ticker": "KWEB", "sector": "ETF", "industry": "China Internet"},
    "FXI": {"name": "iShares China Large-Cap ETF", "ticker": "FXI", "sector": "ETF", "industry": "China"},
    "GDX": {"name": "VanEck Gold Miners ETF", "ticker": "GDX", "sector": "ETF", "industry": "Gold Miners"},
    "GLD": {"name": "SPDR Gold Shares", "ticker": "GLD", "sector": "ETF", "industry": "Gold"},
    "SLV": {"name": "iShares Silver Trust", "ticker": "SLV", "sector": "ETF", "industry": "Silver"},
    "USO": {"name": "United States Oil Fund", "ticker": "USO", "sector": "ETF", "industry": "Oil"},
    "UNG": {"name": "United States Natural Gas Fund", "ticker": "UNG", "sector": "ETF", "industry": "Natural Gas"},
    
    # ETFs - Volatility
    "VXX": {"name": "iPath Series B S&P 500 VIX Short-Term ETN", "ticker": "VXX", "sector": "ETF", "industry": "Volatility"},
    
    # Leveraged/Inverse ETFs
    "TQQQ": {"name": "ProShares UltraPro QQQ", "ticker": "TQQQ", "sector": "ETF", "industry": "Leveraged"},
    "SQQQ": {"name": "ProShares UltraShort QQQ", "ticker": "SQQQ", "sector": "ETF", "industry": "Inverse"},
    "SPXL": {"name": "Direxion Daily S&P 500 Bull 3X ETF", "ticker": "SPXL", "sector": "ETF", "industry": "Leveraged"},
    "SPXS": {"name": "Direxion Daily S&P 500 Bear 3X ETF", "ticker": "SPXS", "sector": "ETF", "industry": "Inverse"},
    
    # European ETFs
    "IEFA": {"name": "iShares Core MSCI EAFE ETF", "ticker": "IEFA", "sector": "ETF", "industry": "Developed Markets"},
    "IEMG": {"name": "iShares Core MSCI Emerging Markets ETF", "ticker": "IEMG", "sector": "ETF", "industry": "Emerging Markets"},
    
    # ESG ETFs
    "ESGU": {"name": "iShares ESG Aware MSCI USA ETF", "ticker": "ESGU", "sector": "ETF", "industry": "ESG"},
    "SUSA": {"name": "iShares ESG Aware MSCI USA Small-Cap ETF", "ticker": "SUSA", "sector": "ETF", "industry": "ESG"},
}

COMPANY_ALIASES: Dict[str, str] = {
    # Microsoft
    "microsoft": "MSFT",
    "msft": "MSFT",
    
    # Apple
    "apple": "AAPL",
    "aapl": "AAPL",
    
    # Google/Alphabet
    "google": "GOOGL",
    "alphabet": "GOOGL",
    "googl": "GOOGL",
    "goog": "GOOG",
    
    # Meta/Facebook
    "meta": "META",
    "facebook": "META",
    "fb": "META",
    
    # Amazon
    "amazon": "AMZN",
    "amzn": "AMZN",
    
    # NVIDIA
    "nvidia": "NVDA",
    "nvda": "NVDA",
    
    # Tesla
    "tesla": "TSLA",
    "tsla": "TSLA",
    
    # JPMorgan
    "jpmorgan": "JPM",
    "jpm": "JPM",
    "chase": "JPM",
    
    # Bank of America
    "bank of america": "BAC",
    "boa": "BAC",
    "bac": "BAC",
    
    # Goldman Sachs
    "goldman": "GS",
    "goldman sachs": "GS",
    "gs": "GS",
    
    # Morgan Stanley
    "morgan stanley": "MS",
    "ms": "MS",
    
    # Wells Fargo
    "wells fargo": "WFC",
    "wfc": "WFC",
    
    # Eli Lilly
    "eli lilly": "LLY",
    "lilly": "LLY",
    "lly": "LLY",
    
    # Johnson & Johnson
    "johnson": "JNJ",
    "jj": "JNJ",
    "jnj": "JNJ",
    
    # Pfizer
    "pfizer": "PFE",
    "pfe": "PFE",
    
    # UnitedHealth
    "unitedhealth": "UNH",
    "united health": "UNH",
    "unh": "UNH",
    
    # Exxon
    "exxon": "XOM",
    "exxon mobil": "XOM",
    "xom": "XOM",
    
    # Chevron
    "chevron": "CVX",
    "cvx": "CVX",
    
    # Walmart
    "walmart": "WMT",
    "wmt": "WMT",
    
    # Coca-Cola
    "coca cola": "KO",
    "coca-cola": "KO",
    "coke": "KO",
    "ko": "KO",
    
    # Pepsi
    "pepsi": "PEP",
    "pepsico": "PEP",
    "pep": "PEP",
    
    # Procter & Gamble
    "procter": "PG",
    "p&g": "PG",
    "pg": "PG",
    
    # Disney
    "disney": "DIS",
    "dis": "DIS",
    
    # Netflix
    "netflix": "NFLX",
    "nflx": "NFLX",
    
    # Visa
    "visa": "V",
    "v": "V",
    
    # Mastercard
    "mastercard": "MA",
    "mc": "MA",
    "ma": "MA",
    
    # AMD
    "amd": "AMD",
    "advanced micro": "AMD",
    
    # Intel
    "intel": "INTC",
    "intc": "INTC",
    
    # Broadcom
    "broadcom": "AVGO",
    "avgo": "AVGO",
    
    # PayPal
    "paypal": "PYPL",
    "pypl": "PYPL",
    
    # Oracle
    "oracle": "ORCL",
    "orcl": "ORCL",
    
    # Salesforce
    "salesforce": "CRM",
    "crm": "CRM",
    
    # Adobe
    "adobe": "ADBE",
    "adbe": "ADBE",
    
    # Boeing
    "boeing": "BA",
    "ba": "BA",
    
    # Caterpillar
    "caterpillar": "CAT",
    "cat": "CAT",
    
    # Home Depot
    "home depot": "HD",
    "hd": "HD",
    
    # McDonald's
    "mcdonalds": "MCD",
    "mcd": "MCD",
    
    # Starbucks
    "starbucks": "SBUX",
    "sbux": "SBUX",
    
    # Nike
    "nike": "NKE",
    "nke": "NKE",
    
    # Lockheed Martin
    "lockheed": "LMT",
    "lmt": "LMT",
    
    # CostCo
    "costco": "COST",
    "cost": "COST",
    
    # AT&T
    "at&t": "T",
    "att": "T",
    "t": "T",
    
    # Verizon
    "verizon": "VZ",
    "vz": "VZ",
    
    # T-Mobile
    "t-mobile": "TMUS",
    "tmobile": "TMUS",
    "tmus": "TMUS",
    
    # Costco
    "costco": "COST",
    
    # Shopify
    "shopify": "SHOP",
    "shop": "SHOP",
    
    # Snowflake
    "snowflake": "SNOW",
    "snow": "SNOW",
    
    # Palantir
    "palantir": "PLTR",
    "pltr": "PLTR",
    
    # CrowdStrike
    "crowdstrike": "CRWD",
    "crwd": "CRWD",
    
    # ServiceNow
    "servicenow": "NOW",
    "now": "NOW",
    
    # Datadog
    "datadog": "DDOG",
    "ddog": "DDOG",
    
    # Cloudflare
    "cloudflare": "NET",
    
    # Zscaler
    "zscaler": "ZS",
    "zs": "ZS",
    
    # Palo Alto
    "palo alto": "PANW",
    "panw": "PANW",
    
    # Tesla
    "tesla": "TSLA",
    
    # Uber
    "uber": "UBER",
    
    # Airbnb
    "airbnb": "ABNB",
    "abnb": "ABNB",
    
    # Bitcoin/Crypto
    "bitcoin": "MSTR",
    "microstrategy": "MSTR",
    
    # Coinbase
    "coinbase": "COIN",
    "coin": "COIN",
    
    # TSMC
    "tsmc": "TSM",
    "taiwan semiconductor": "TSM",
    
    # ASML
    "asml": "ASML",
    
    # Novo Nordisk
    "novo": "NVO",
    "novo nordisk": "NVO",
    
    # Toyota
    "toyota": "TM",
    
    # Alibaba
    "alibaba": "BABA",
    "baba": "BABA",
    
    # ETFs
    "spy": "SPY",
    "spdr": "SPY",
    "s&p 500": "SPY",
    "voo": "VOO",
    "vanguard s&p 500": "VOO",
    "ivv": "IVV",
    "ishares sp 500": "IVV",
    "vti": "VTI",
    "vanguard total": "VTI",
    "qqq": "QQQ",
    "nasdaq 100": "QQQ",
    "qqqm": "QQQM",
    "iwm": "IWM",
    "russell 2000": "IWM",
    "dia": "DIA",
    "dow jones": "DIA",
    "vxus": "VXUS",
    "international": "VXUS",
    "efa": "EFA",
    "msci eafe": "EFA",
    "eem": "EEM",
    "emerging markets": "EEM",
    "vwo": "VWO",
    "xlk": "XLK",
    "technology": "XLK",
    "xlf": "XLF",
    "financials": "XLF",
    "xle": "XLE",
    "energy": "XLE",
    "xlv": "XLV",
    "healthcare": "XLV",
    "xlc": "XLC",
    "communication": "XLC",
    "xly": "XLY",
    "consumer discretionary": "XLY",
    "xlp": "XLP",
    "consumer staples": "XLP",
    "xlb": "XLB",
    "materials": "XLB",
    "xli": "XLI",
    "industrials": "XLI",
    "xlre": "XLRE",
    "real estate": "XLRE",
    "xlu": "XLU",
    "utilities": "XLU",
    "vug": "VUG",
    "growth": "VUG",
    "vtv": "VTV",
    "value": "VTV",
    "schd": "SCHD",
    "dividend": "SCHD",
    "bnd": "BND",
    "bonds": "BND",
    "tlt": "TLT",
    "treasury": "TLT",
    "gld": "GLD",
    "gold": "GLD",
    "gdx": "GDX",
    "gold miners": "GDX",
    "slv": "SLV",
    "silver": "SLV",
    "uso": "USO",
    "oil": "USO",
    "arKK": "ARKK",
    "ark innovation": "ARKK",
    "soxx": "SOXX",
    "semiconductor": "SOXX",
    "smh": "SMH",
}


class CompanySearch:
    def __init__(self):
        self._build_search_index()
    
    def _build_search_index(self):
        self._ticker_to_company = COMPANY_DATABASE
        self._name_to_company = {}
        for ticker, info in COMPANY_DATABASE.items():
            name_lower = info["name"].lower()
            self._name_to_company[name_lower] = info
            for word in name_lower.split():
                if word not in self._name_to_company:
                    self._name_to_company[word] = info
    
    def resolve(self, query: str) -> Optional[str]:
        query_clean = query.strip().upper()
        
        if query_clean in self._ticker_to_company:
            return query_clean
        
        if query_clean in COMPANY_ALIASES:
            return COMPANY_ALIASES[query_clean]
        
        query_lower = query.strip().lower()
        if query_lower in COMPANY_ALIASES:
            return COMPANY_ALIASES[query_lower]
        
        for ticker, info in self._ticker_to_company.items():
            if query_lower in info["name"].lower() or info["name"].lower() in query_lower:
                return ticker
        
        return None
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        query_lower = query.lower()
        results = []
        
        for ticker, info in self._ticker_to_company.items():
            score = 0
            if query_lower == ticker.lower():
                score = 100
            elif query_lower in info["name"].lower():
                score = 80
            elif info["name"].lower() in query_lower:
                score = 60
            elif any(word.startswith(query_lower) for word in info["name"].lower().split()):
                score = 40
            
            if score > 0:
                results.append((score, info))
        
        results.sort(key=lambda x: x[0], reverse=True)
        return [info for _, info in results[:limit]]
    
    def get_company_info(self, query: str) -> Optional[Dict]:
        ticker = self.resolve(query)
        if ticker and ticker in self._ticker_to_company:
            return self._ticker_to_company[ticker]
        return None
    
    def get_all_tickers(self) -> List[str]:
        return list(self._ticker_to_company.keys())
    
    def get_by_sector(self, sector: str) -> List[Dict]:
        return [info for info in self._ticker_to_company.values() 
                if info.get("sector", "").lower() == sector.lower()]
    
    def get_sectors(self) -> List[str]:
        sectors = set()
        for info in self._ticker_to_company.values():
            if info.get("sector"):
                sectors.add(info["sector"])
        return sorted(list(sectors))
