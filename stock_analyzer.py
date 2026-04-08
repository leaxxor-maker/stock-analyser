#!/usr/bin/env python3
"""
Stock Analyzer Pro v2 - Avec News, Analyse Technique et Calendrier Macro
Inclut les méthodologies de Goldman Sachs, Citadel, Two Sigma
"""

import os
import sys
import sqlite3
import json
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from pathlib import Path

try:
    import yfinance as yf
except ImportError:
    os.system(f"{sys.executable} -m pip install yfinance")
    import yfinance as yf

try:
    from flask import Flask, request, redirect
except ImportError:
    os.system(f"{sys.executable} -m pip install flask markupsafe")
    from flask import Flask, request, redirect

app = Flask(__name__)

# ============================================================================
# BASE DE DONNÉES ENTREPRISES
# ============================================================================

COMPANY_DB = {
    # TECH
    "MSFT": {"name": "Microsoft", "sector": "Tech", "industry": "Software"},
    "AAPL": {"name": "Apple", "sector": "Tech", "industry": "Electronics"},
    "GOOGL": {"name": "Alphabet", "sector": "Tech", "industry": "Internet"},
    "META": {"name": "Meta", "sector": "Tech", "industry": "Social Media"},
    "AMZN": {"name": "Amazon", "sector": "Tech", "industry": "E-commerce"},
    "NVDA": {"name": "NVIDIA", "sector": "Tech", "industry": "Semiconductors"},
    "TSLA": {"name": "Tesla", "sector": "Auto/AI", "industry": "EV"},
    "AVGO": {"name": "Broadcom", "sector": "Tech", "industry": "Semiconductors"},
    "ORCL": {"name": "Oracle", "sector": "Tech", "industry": "Software"},
    "CRM": {"name": "Salesforce", "sector": "Tech", "industry": "Software"},
    "ADBE": {"name": "Adobe", "sector": "Tech", "industry": "Software"},
    "AMD": {"name": "AMD", "sector": "Tech", "industry": "Semiconductors"},
    "INTC": {"name": "Intel", "sector": "Tech", "industry": "Semiconductors"},
    "QCOM": {"name": "QUALCOMM", "sector": "Tech", "industry": "Semiconductors"},
    "NOW": {"name": "ServiceNow", "sector": "Tech", "industry": "Software"},
    "SNOW": {"name": "Snowflake", "sector": "Tech", "industry": "Cloud"},
    "PLTR": {"name": "Palantir", "sector": "Tech", "industry": "AI"},
    "CRWD": {"name": "CrowdStrike", "sector": "Tech", "industry": "Security"},
    "NET": {"name": "Cloudflare", "sector": "Tech", "industry": "Security"},
    "ZS": {"name": "Zscaler", "sector": "Tech", "industry": "Security"},
    "PANW": {"name": "Palo Alto", "sector": "Tech", "industry": "Security"},
    "DDOG": {"name": "Datadog", "sector": "Tech", "industry": "Monitoring"},
    "ANET": {"name": "Arista Networks", "sector": "Tech", "industry": "Networking"},
    "SMCI": {"name": "Super Micro", "sector": "Tech", "industry": "Hardware"},
    "DELL": {"name": "Dell", "sector": "Tech", "industry": "Hardware"},
    
    # FINANCE
    "JPM": {"name": "JPMorgan", "sector": "Finance", "industry": "Banking"},
    "BAC": {"name": "Bank of America", "sector": "Finance", "industry": "Banking"},
    "WFC": {"name": "Wells Fargo", "sector": "Finance", "industry": "Banking"},
    "GS": {"name": "Goldman Sachs", "sector": "Finance", "industry": "Investment"},
    "MS": {"name": "Morgan Stanley", "sector": "Finance", "industry": "Investment"},
    "C": {"name": "Citigroup", "sector": "Finance", "industry": "Banking"},
    "BLK": {"name": "BlackRock", "sector": "Finance", "industry": "Asset Mgmt"},
    "SCHW": {"name": "Charles Schwab", "sector": "Finance", "industry": "Brokerage"},
    "AXP": {"name": "American Express", "sector": "Finance", "industry": "Credit"},
    "V": {"name": "Visa", "sector": "Finance", "industry": "Payments"},
    "MA": {"name": "Mastercard", "sector": "Finance", "industry": "Payments"},
    "PYPL": {"name": "PayPal", "sector": "Finance", "industry": "Payments"},
    "COIN": {"name": "Coinbase", "sector": "Finance", "industry": "Crypto"},
    "MSTR": {"name": "MicroStrategy", "sector": "Finance", "industry": "Crypto"},
    "ICE": {"name": "Intercontinental", "sector": "Finance", "industry": "Exchange"},
    "SPGI": {"name": "S&P Global", "sector": "Finance", "industry": "Ratings"},
    
    # HEALTHCARE
    "LLY": {"name": "Eli Lilly", "sector": "Healthcare", "industry": "Pharma"},
    "JNJ": {"name": "Johnson & Johnson", "sector": "Healthcare", "industry": "Pharma"},
    "UNH": {"name": "UnitedHealth", "sector": "Healthcare", "industry": "Insurance"},
    "PFE": {"name": "Pfizer", "sector": "Healthcare", "industry": "Pharma"},
    "ABBV": {"name": "AbbVie", "sector": "Healthcare", "industry": "Pharma"},
    "MRK": {"name": "Merck", "sector": "Healthcare", "industry": "Pharma"},
    "TMO": {"name": "Thermo Fisher", "sector": "Healthcare", "industry": "Lab"},
    "ABT": {"name": "Abbott", "sector": "Healthcare", "industry": "Medical"},
    "DHR": {"name": "Danaher", "sector": "Healthcare", "industry": "Medical"},
    "AMGN": {"name": "Amgen", "sector": "Healthcare", "industry": "Biotech"},
    "ISRG": {"name": "Intuitive Surgical", "sector": "Healthcare", "industry": "Robotics"},
    "REGN": {"name": "Regeneron", "sector": "Healthcare", "industry": "Biotech"},
    "VRTX": {"name": "Vertex", "sector": "Healthcare", "industry": "Biotech"},
    "MRNA": {"name": "Moderna", "sector": "Healthcare", "industry": "Biotech"},
    "CVS": {"name": "CVS Health", "sector": "Healthcare", "industry": "Retail"},
    "ZTS": {"name": "Zoetis", "sector": "Healthcare", "industry": "Pharma"},
    "DXCM": {"name": "Dexcom", "sector": "Healthcare", "industry": "Medical"},
    "EW": {"name": "Edwards Lifesciences", "sector": "Healthcare", "industry": "Medical"},
    
    # ENERGY
    "XOM": {"name": "Exxon Mobil", "sector": "Energy", "industry": "Oil"},
    "CVX": {"name": "Chevron", "sector": "Energy", "industry": "Oil"},
    "COP": {"name": "ConocoPhillips", "sector": "Energy", "industry": "Oil"},
    "SLB": {"name": "Schlumberger", "sector": "Energy", "industry": "Services"},
    "EOG": {"name": "EOG Resources", "sector": "Energy", "industry": "Oil"},
    "OXY": {"name": "Occidental", "sector": "Energy", "industry": "Oil"},
    "NEE": {"name": "NextEra Energy", "sector": "Utilities", "industry": "Utilities"},
    "ENPH": {"name": "Enphase", "sector": "Energy", "industry": "Solar"},
    "FSLR": {"name": "First Solar", "sector": "Energy", "industry": "Solar"},
    
    # CONSUMER
    "WMT": {"name": "Walmart", "sector": "Retail", "industry": "Retail"},
    "PG": {"name": "Procter & Gamble", "sector": "Consumer", "industry": "Goods"},
    "KO": {"name": "Coca-Cola", "sector": "Consumer", "industry": "Beverages"},
    "PEP": {"name": "PepsiCo", "sector": "Consumer", "industry": "Beverages"},
    "COST": {"name": "Costco", "sector": "Retail", "industry": "Retail"},
    "HD": {"name": "Home Depot", "sector": "Retail", "industry": "Home"},
    "MCD": {"name": "McDonald's", "sector": "Restaurant", "industry": "Fast Food"},
    "SBUX": {"name": "Starbucks", "sector": "Restaurant", "industry": "Coffee"},
    "NKE": {"name": "Nike", "sector": "Consumer", "industry": "Apparel"},
    "LVS": {"name": "Las Vegas Sands", "sector": "Consumer", "industry": "Casinos"},
    "MAR": {"name": "Marriott", "sector": "Consumer", "industry": "Lodging"},
    "GM": {"name": "General Motors", "sector": "Auto", "industry": "Auto"},
    "F": {"name": "Ford", "sector": "Auto", "industry": "Auto"},
    "TM": {"name": "Toyota", "sector": "Auto", "industry": "Auto"},
    "RIVN": {"name": "Rivian", "sector": "Auto", "industry": "EV"},
    
    # INDUSTRIALS
    "CAT": {"name": "Caterpillar", "sector": "Industrial", "industry": "Machinery"},
    "BA": {"name": "Boeing", "sector": "Industrial", "industry": "Aerospace"},
    "HON": {"name": "Honeywell", "sector": "Industrial", "industry": "Conglomerate"},
    "GE": {"name": "GE", "sector": "Industrial", "industry": "Conglomerate"},
    "RTX": {"name": "RTX", "sector": "Industrial", "industry": "Aerospace"},
    "LMT": {"name": "Lockheed Martin", "sector": "Industrial", "industry": "Defense"},
    "NOC": {"name": "Northrop Grumman", "sector": "Industrial", "industry": "Defense"},
    "DE": {"name": "Deere", "sector": "Industrial", "industry": "Machinery"},
    "UPS": {"name": "UPS", "sector": "Industrial", "industry": "Logistics"},
    "FDX": {"name": "FedEx", "sector": "Industrial", "industry": "Logistics"},
    "UBER": {"name": "Uber", "sector": "Tech", "industry": "Rideshare"},
    "ABNB": {"name": "Airbnb", "sector": "Consumer", "industry": "Travel"},
    
    # MEDIA & COMMS
    "DIS": {"name": "Disney", "sector": "Media", "industry": "Entertainment"},
    "NFLX": {"name": "Netflix", "sector": "Media", "industry": "Streaming"},
    "WBD": {"name": "Warner Bros", "sector": "Media", "industry": "Entertainment"},
    "CMCSA": {"name": "Comcast", "sector": "Comms", "industry": "Telecom"},
    "T": {"name": "AT&T", "sector": "Comms", "industry": "Telecom"},
    "VZ": {"name": "Verizon", "sector": "Comms", "industry": "Telecom"},
    "TMUS": {"name": "T-Mobile", "sector": "Comms", "industry": "Telecom"},
    "SPOT": {"name": "Spotify", "sector": "Media", "industry": "Streaming"},
    
    # REAL ESTATE
    "PLD": {"name": "Prologis", "sector": "Real Estate", "industry": "REIT"},
    "AMT": {"name": "American Tower", "sector": "Real Estate", "industry": "REIT"},
    "EQIX": {"name": "Equinix", "sector": "Real Estate", "industry": "REIT"},
    "O": {"name": "Realty Income", "sector": "Real Estate", "industry": "REIT"},
    "WELL": {"name": "Welltower", "sector": "Real Estate", "industry": "REIT"},
    
    # EUROPEAN ADRs
    "ASML": {"name": "ASML", "sector": "Tech", "industry": "Semiconductors"},
    "SAP": {"name": "SAP", "sector": "Tech", "industry": "Software"},
    "BABA": {"name": "Alibaba", "sector": "Tech", "industry": "E-commerce"},
    "TSM": {"name": "TSMC", "sector": "Tech", "industry": "Semiconductors"},
    "NVO": {"name": "Novo Nordisk", "sector": "Healthcare", "industry": "Pharma"},
    "SONY": {"name": "Sony", "sector": "Tech", "industry": "Electronics"},
    "SHEL": {"name": "Shell", "sector": "Energy", "industry": "Oil"},
    "AZN": {"name": "AstraZeneca", "sector": "Healthcare", "industry": "Pharma"},
    "SHOP": {"name": "Shopify", "sector": "Tech", "industry": "E-commerce"},
    "AI": {"name": "C3.ai", "sector": "Tech", "industry": "AI"},
    "PATH": {"name": "UiPath", "sector": "Tech", "industry": "Software"},
    "TTD": {"name": "Trade Desk", "sector": "Tech", "industry": "Software"},
}

ALIASES = {
    "microsoft": "MSFT", "msft": "MSFT",
    "apple": "AAPL", "aapl": "AAPL",
    "google": "GOOGL", "alphabet": "GOOGL",
    "meta": "META", "facebook": "META",
    "amazon": "AMZN", "amzn": "AMZN",
    "nvidia": "NVDA", "nvda": "NVDA",
    "tesla": "TSLA", "tsla": "TSLA",
    "jpmorgan": "JPM", "jpm": "JPM",
    "goldman": "GS", "gs": "GS",
    "visa": "V", "v": "V",
    "mastercard": "MA", "ma": "MA",
    "lilly": "LLY", "ll y": "LLY",
    "pfizer": "PFE", "pfe": "PFE",
    "unitedhealth": "UNH", "unh": "UNH",
    "exxon": "XOM", "xom": "XOM",
    "chevron": "CVX", "cvx": "CVX",
    "walmart": "WMT", "wmt": "WMT",
    "boeing": "BA", "ba": "BA",
    "caterpillar": "CAT", "cat": "CAT",
    "disney": "DIS", "dis": "DIS",
    "netflix": "NFLX", "nflx": "NFLX",
    "adobe": "ADBE", "adbe": "ADBE",
    "oracle": "ORCL", "orcl": "ORCL",
    "salesforce": "CRM", "crm": "CRM",
    "shopify": "SHOP", "shop": "SHOP",
    "snowflake": "SNOW", "snow": "SNOW",
    "crowdstrike": "CRWD", "crwd": "CRWD",
    "servicenow": "NOW", "now": "NOW",
    "palantir": "PLTR", "pltr": "PLTR",
    "uber": "UBER", "uber": "UBER",
    "airbnb": "ABNB", "abnb": "ABNB",
    "coinbase": "COIN", "coin": "COIN",
    "tsmc": "TSM", "taiwan semiconductor": "TSM",
    "asml": "ASML",
    "novo": "NVO", "novo nordisk": "NVO",
    "alibaba": "BABA", "baba": "BABA",
    "home depot": "HD", "hd": "HD",
    "mcdonalds": "MCD", "mcd": "MCD",
    "starbucks": "SBUX", "sbux": "SBUX",
    "nike": "NKE", "nke": "NKE",
    "intel": "INTC", "intc": "INTC",
    "amd": "AMD",
    "paypal": "PYPL", "pypl": "PYPL",
    "spotify": "SPOT", "spot": "SPOT",
}

# ============================================================================
# CLASSE INDICATORS - ANALYSE PRO
# ============================================================================

@dataclass
class Indicators:
    ticker: str
    company_name: str
    current_price: float
    timestamp: datetime = field(default_factory=datetime.now)
    sector: Optional[str] = None
    
    # Prix et capitalisation
    market_cap: Optional[float] = None
    enterprise_value: Optional[float] = None
    week_52_high: Optional[float] = None
    week_52_low: Optional[float] = None
    week_52_change_pct: Optional[float] = None
    avg_volume: Optional[float] = None
    current_volume: Optional[float] = None
    
    # Valorisation
    price_to_earnings: Optional[float] = None
    price_to_earnings_forward: Optional[float] = None
    peg_ratio: Optional[float] = None
    price_to_book: Optional[float] = None
    price_to_sales: Optional[float] = None
    ev_to_revenue: Optional[float] = None
    ev_to_ebitda: Optional[float] = None
    
    # Par action
    earnings_per_share: Optional[float] = None
    eps_trailing: Optional[float] = None
    eps_forward: Optional[float] = None
    eps_growth_5y: Optional[float] = None
    book_value_per_share: Optional[float] = None
    fcf_per_share: Optional[float] = None
    revenue_per_share: Optional[float] = None
    
    # Rentabilité
    profit_margin: Optional[float] = None
    operating_margin: Optional[float] = None
    gross_margin: Optional[float] = None
    roe: Optional[float] = None
    roa: Optional[float] = None
    roic: Optional[float] = None
    
    # Croissance
    revenue: Optional[float] = None
    revenue_growth_yoy: Optional[float] = None
    revenue_growth_3y: Optional[float] = None
    revenue_growth_5y: Optional[float] = None
    earnings_growth: Optional[float] = None
    
    # Endettement
    total_debt: Optional[float] = None
    debt_to_equity: Optional[float] = None
    current_ratio: Optional[float] = None
    quick_ratio: Optional[float] = None
    
    # Cash Flow
    free_cash_flow: Optional[float] = None
    operating_cash_flow: Optional[float] = None
    
    # Dividendes
    dividend_yield: Optional[float] = None
    payout_ratio: Optional[float] = None
    
    # Risque
    beta: Optional[float] = None
    
    # Analystes
    analyst_rating: Optional[str] = None
    target_price: Optional[float] = None
    upside_downside: Optional[float] = None
    number_of_analysts: Optional[int] = None
    
    # Analyse technique
    ma_50: Optional[float] = None
    ma_200: Optional[float] = None
    rsi_14: Optional[float] = None
    support: Optional[float] = None
    resistance: Optional[float] = None
    trend: Optional[str] = None
    
    # News/Sentiment
    news_sentiment: Optional[str] = None
    news_link: Optional[str] = None
    
    # Events
    earnings_date: Optional[str] = None
    next_earnings: Optional[datetime] = None
    
    def fmt_currency(self, v):
        if v is None: return "N/A"
        if abs(v) >= 1e12: return f"${v/1e12:.2f}T"
        if abs(v) >= 1e9: return f"${v/1e9:.2f}B"
        if abs(v) >= 1e6: return f"${v/1e6:.2f}M"
        return f"${v:.2f}"
    
    def fmt_pct(self, v):
        return f"{v:.2f}%" if v is not None else "N/A"
    
    def fmt_ratio(self, v):
        return f"{v:.2f}x" if v is not None else "N/A"
    
    def get_score(self) -> float:
        score = 50
        
        # P/E
        if self.price_to_earnings:
            if 12 <= self.price_to_earnings <= 20: score += 15
            elif self.price_to_earnings < 12: score += 10
            elif self.price_to_earnings > 40: score -= 20
        
        # PEG
        if self.peg_ratio:
            if self.peg_ratio < 1: score += 15
            elif self.peg_ratio > 2: score -= 15
        
        # Marges
        if self.profit_margin:
            if self.profit_margin >= 20: score += 15
            elif self.profit_margin < 5: score -= 15
        
        # ROE
        if self.roe:
            if self.roe >= 20: score += 15
            elif self.roe < 10: score -= 10
        
        # Dette
        if self.debt_to_equity:
            if self.debt_to_equity < 0.5: score += 10
            elif self.debt_to_equity > 2: score -= 15
        
        # Croissance
        if self.revenue_growth_yoy:
            if self.revenue_growth_yoy >= 15: score += 15
            elif self.revenue_growth_yoy < 0: score -= 15
        
        # FCF
        if self.free_cash_flow and self.free_cash_flow < 0: score -= 10
        
        return max(0, min(100, score))
    
    def get_recommendation(self) -> str:
        s = self.get_score()
        if s >= 75: return "⭐⭐⭐⭐ ACHAT FORT"
        if s >= 65: return "⭐⭐⭐ Achat"
        if s >= 55: return "✅ Achat Modéré"
        if s >= 45: return "⚖️ Neutre"
        if s >= 35: return "⚠️ Vente"
        return "❌ Vente Forte"
    
    def get_strategy_bull(self) -> str:
        score = self.get_score()
        if score >= 70 and self.beta and self.beta > 1.2: return "🎯 Croissance agressive"
        elif score >= 60 and self.revenue_growth_yoy and self.revenue_growth_yoy > 15: return "🚀 Forte croissance"
        elif score >= 60: return "✅ Achat - Croissance"
        elif score >= 50: return "⚖️ Neutre - Attendre"
        return "❌ Éviter"
    
    def get_strategy_bear(self) -> str:
        score = self.get_score()
        if score >= 70 and self.dividend_yield and self.dividend_yield > 3: return "🏰 Défensif + Dividende"
        elif score >= 60 and self.beta and self.beta < 0.8: return "🛡️ Basse volatilité"
        elif score >= 55: return "✅ Conserver"
        return "❌ Risqué"
    
    def get_key_number(self) -> tuple:
        score = self.get_score()
        if score >= 70: return score, "EXCELLENT", "#00ff88", "Potentiel haussier important"
        elif score >= 60: return score, "BON", "#88ff88", "Entreprise de qualité"
        elif score >= 50: return score, "NEUTRE", "#ffc107", "Attendre meilleure opportunité"
        elif score >= 35: return score, "RISQUÉ", "#ff8844", "Problèmes identifiés"
        return score, "TRÈS RISQUÉ", "#ff4757", "Ne pas investir"
    
    def get_target_price(self) -> dict:
        current = self.current_price
        results = {}
        
        if self.week_52_low and self.week_52_high:
            results['avg_52w'] = (self.week_52_low + self.week_52_high) / 2
        
        results['correction_20pct'] = current * 0.80
        
        if self.eps_trailing and self.eps_trailing > 0:
            results['fair_pe_20'] = self.eps_trailing * 20
        
        if self.target_price:
            results['analyst_target'] = self.target_price
            results['analyst_buy_zone'] = self.target_price * 0.90
        
        if results.get('analyst_buy_zone'):
            recommended = results['analyst_buy_zone']
        elif results.get('fair_pe_20'):
            recommended = results['fair_pe_20']
        else:
            recommended = current * 0.80
        
        results['recommended_buy'] = recommended
        results['discount_pct'] = ((recommended - current) / current * 100) if current > 0 else 0
        return results
    
    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
    
    @classmethod
    def from_dict(cls, d):
        d.pop('_sa_instance_state', None)
        return cls(**d)

# ============================================================================
# BASE DE DONNÉES SQLITE
# ============================================================================

class Database:
    def __init__(self):
        self.path = Path.home() / ".stock_analyzer" / "analyses.db"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()
    
    def init_db(self):
        try:
            with sqlite3.connect(self.path) as conn:
                conn.execute("CREATE TABLE IF NOT EXISTS analyses (id INTEGER PRIMARY KEY, ticker TEXT, data TEXT, timestamp TEXT)")
                conn.execute("CREATE TABLE IF NOT EXISTS searches (id INTEGER PRIMARY KEY, ticker TEXT, timestamp TEXT)")
                conn.execute("CREATE TABLE IF NOT EXISTS portfolio (id INTEGER PRIMARY KEY, ticker TEXT, shares REAL, avg_price REAL)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_ticker ON analyses(ticker)")
        except: pass
    
    def save(self, ind: Indicators):
        try:
            with sqlite3.connect(self.path) as conn:
                conn.execute("INSERT INTO analyses (ticker, data, timestamp) VALUES (?, ?, ?)",
                    (ind.ticker, json.dumps(ind.to_dict()), ind.timestamp.isoformat()))
                conn.execute("INSERT OR REPLACE INTO searches (ticker, timestamp) VALUES (?, ?)",
                    (ind.ticker, datetime.now().isoformat()))
        except: pass
    
    def get(self, ticker: str) -> Optional[Indicators]:
        try:
            with sqlite3.connect(self.path) as conn:
                conn.row_factory = sqlite3.Row
                row = conn.execute("SELECT * FROM analyses WHERE ticker=? ORDER BY timestamp DESC LIMIT 1", (ticker.upper(),)).fetchone()
                if row and row['data']:
                    return Indicators.from_dict(json.loads(row['data']))
        except: pass
        return None
    
    def get_all(self, limit=100) -> List[Indicators]:
        try:
            with sqlite3.connect(self.path) as conn:
                conn.row_factory = sqlite3.Row
                rows = conn.execute("SELECT * FROM (SELECT * FROM analyses ORDER BY timestamp DESC) GROUP BY ticker LIMIT ?", (limit,)).fetchall()
                return [Indicators.from_dict(json.loads(r['data'])) for r in rows if r['data']]
        except: return []
    
    def get_searches(self, limit=50) -> List[Dict]:
        try:
            with sqlite3.connect(self.path) as conn:
                conn.row_factory = sqlite3.Row
                rows = conn.execute("SELECT * FROM (SELECT * FROM searches ORDER BY timestamp DESC) GROUP BY ticker LIMIT ?", (limit,)).fetchall()
                return [{'ticker': r['ticker'], 'timestamp': r['timestamp']} for r in rows]
        except: return []
    
    def get_stats(self) -> dict:
        try:
            with sqlite3.connect(self.path) as conn:
                total = conn.execute("SELECT COUNT(*) FROM analyses").fetchone()[0]
                companies = conn.execute("SELECT COUNT(DISTINCT ticker) FROM analyses").fetchone()[0]
                searches = conn.execute("SELECT COUNT(DISTINCT ticker) FROM searches").fetchone()[0]
                return {'total': total, 'companies': companies, 'searches': searches}
        except: return {'total': 0, 'companies': 0, 'searches': 0}
    
    def get_portfolio(self) -> List[Dict]:
        try:
            with sqlite3.connect(self.path) as conn:
                conn.row_factory = sqlite3.Row
                return [dict(r) for r in conn.execute("SELECT * FROM portfolio").fetchall()]
        except: return []
    
    def add_to_portfolio(self, ticker: str, shares: float, avg_price: float):
        try:
            with sqlite3.connect(self.path) as conn:
                conn.execute("INSERT OR REPLACE INTO portfolio (ticker, shares, avg_price) VALUES (?, ?, ?)",
                    (ticker.upper(), shares, avg_price))
        except: pass
    
    def remove_from_portfolio(self, ticker: str):
        try:
            with sqlite3.connect(self.path) as conn:
                conn.execute("DELETE FROM portfolio WHERE ticker=?", (ticker.upper(),))
        except: pass
    
    def get_portfolio_value(self) -> tuple:
        total_value = 0
        total_cost = 0
        portfolio = self.get_portfolio()
        results = []
        for item in portfolio:
            ind = self.get(item['ticker'])
            if ind:
                current_value = item['shares'] * ind.current_price
                cost = item['shares'] * item['avg_price']
                gain_loss = current_value - cost
                gain_loss_pct = (gain_loss / cost * 100) if cost > 0 else 0
                total_value += current_value
                total_cost += cost
                results.append({
                    'ticker': item['ticker'],
                    'name': ind.company_name,
                    'shares': item['shares'],
                    'avg_price': item['avg_price'],
                    'current_price': ind.current_price,
                    'current_value': current_value,
                    'gain_loss': gain_loss,
                    'gain_loss_pct': gain_loss_pct
                })
        return total_value, total_cost, results

# ============================================================================
# ANALYSEUR
# ============================================================================

class Analyzer:
    def __init__(self):
        self.db = Database()
    
    def resolve(self, query: str) -> Optional[str]:
        q = query.strip().upper()
        if q in COMPANY_DB: return q
        if q in ALIASES: return ALIASES[q]
        q_lower = query.strip().lower()
        if q_lower in ALIASES: return ALIASES[q_lower]
        for ticker, info in COMPANY_DB.items():
            if q_lower in info['name'].lower():
                return ticker
        return None
    
    def get_sector(self, ticker: str) -> Optional[str]:
        t = self.resolve(ticker)
        if t and t in COMPANY_DB:
            return COMPANY_DB[t].get('sector')
        return None
    
    def analyze(self, ticker: str, use_cache=True) -> Optional[Indicators]:
        resolved = self.resolve(ticker)
        if not resolved:
            return None
        
        if use_cache:
            cached = self.db.get(resolved)
            if cached:
                return cached
        
        try:
            stock = yf.Ticker(resolved)
            info = stock.info
            
            if not info or not info.get('regularMarketPrice'):
                return None
            
            # Récupérer l'historique pour analyse technique
            hist = stock.history(period="1y")
            
            name = info.get('longName') or info.get('shortName') or resolved
            price = info.get('regularMarketPrice') or info.get('currentPrice', 0)
            sector = self.get_sector(resolved)
            
            # Calculs analyse technique
            ma_50 = None
            ma_200 = None
            rsi = None
            support = None
            resistance = None
            trend = "Neutre"
            
            if len(hist) >= 50:
                ma_50 = hist['Close'].tail(50).mean()
                if len(hist) >= 200:
                    ma_200 = hist['Close'].tail(200).mean()
                
                # RSI simplifié
                delta = hist['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                rsi = 100 - (100 / (1 + rs)).iloc[-1] if len(rs) > 0 else None
                
                # Support/Résistance
                support = hist['Low'].tail(50).min()
                resistance = hist['High'].tail(50).max()
                
                # Trend
                if ma_50 and ma_200:
                    if price > ma_50 > ma_200:
                        trend = "📈 Haussier"
                    elif price < ma_50 < ma_200:
                        trend = "📉 Baissier"
                    elif price > ma_50:
                        trend = "📊 Consolidation"
                    else:
                        trend = "⚠️ Weakness"
            
            # Prochain earnings
            earnings_date = None
            next_earnings = None
            try:
                cal = stock.calendar
                if cal is not None and isinstance(cal, pd.DataFrame):
                    if not cal.empty:
                        earnings_date = str(cal.iloc[0, 0]) if len(cal) > 0 else None
            except:
                pass
            
            ind = Indicators(
                ticker=resolved,
                company_name=name,
                current_price=price,
                sector=sector,
                
                market_cap=info.get('marketCap'),
                enterprise_value=info.get('enterpriseValue'),
                week_52_high=info.get('fiftyTwoWeekHigh'),
                week_52_low=info.get('fiftyTwoWeekLow'),
                avg_volume=info.get('averageVolume'),
                current_volume=info.get('volume'),
                
                price_to_earnings=info.get('trailingPE'),
                price_to_earnings_forward=info.get('forwardPE'),
                peg_ratio=info.get('pegRatio'),
                price_to_book=info.get('priceToBook'),
                price_to_sales=(info.get('marketCap') or 0) / (info.get('totalRevenue') or 1),
                ev_to_revenue=info.get('enterpriseToRevenue'),
                ev_to_ebitda=info.get('enterpriseToEbitda'),
                
                earnings_per_share=info.get('trailingEps'),
                eps_trailing=info.get('trailingEps'),
                eps_forward=info.get('forwardEps'),
                eps_growth_5y=(info.get('earningsGrowth') or 0) * 500,
                book_value_per_share=info.get('bookValue'),
                fcf_per_share=(info.get('freeCashflow') or 0) / (info.get('sharesOutstanding') or 1) if info.get('freeCashflow') and info.get('sharesOutstanding') else None,
                revenue_per_share=(info.get('totalRevenue') or 0) / (info.get('sharesOutstanding') or 1) if info.get('sharesOutstanding') else None,
                
                profit_margin=(info.get('profitMargins') or 0) * 100,
                operating_margin=(info.get('operatingMargins') or 0) * 100,
                gross_margin=(info.get('grossMargins') or 0) * 100,
                roe=(info.get('returnOnEquity') or 0) * 100,
                roa=(info.get('returnOnAssets') or 0) * 100,
                roic=(info.get('returnOnInvestedCapital') or 0) * 100,
                
                revenue=info.get('totalRevenue'),
                revenue_growth_yoy=(info.get('revenueGrowth') or 0) * 100,
                revenue_growth_3y=(info.get('revenueGrowth') or 0) * 300,
                revenue_growth_5y=(info.get('revenueGrowth') or 0) * 500,
                earnings_growth=(info.get('earningsGrowth') or 0) * 100,
                
                total_debt=info.get('totalDebt'),
                debt_to_equity=info.get('debtToEquity'),
                current_ratio=info.get('currentRatio'),
                quick_ratio=info.get('quickRatio'),
                
                free_cash_flow=info.get('freeCashflow'),
                operating_cash_flow=info.get('operatingCashflow'),
                
                dividend_yield=(info.get('dividendYield') or 0) * 100,
                payout_ratio=(info.get('payoutRatio') or 0) * 100,
                
                beta=info.get('beta'),
                
                analyst_rating=info.get('recommendationKey', '').title(),
                target_price=info.get('targetMeanPrice'),
                upside_downside=((info.get('targetMeanPrice', 0) - price) / price * 100) if price and info.get('targetMeanPrice') else None,
                number_of_analysts=info.get('numberOfAnalystOpinions'),
                
                # Analyse technique
                ma_50=ma_50,
                ma_200=ma_200,
                rsi_14=rsi,
                support=support,
                resistance=resistance,
                trend=trend,
                
                # News
                news_link=f"https://finance.yahoo.com/quote/{resolved}/news",
                
                # Earnings
                earnings_date=earnings_date,
                next_earnings=next_earnings,
            )
            
            self.db.save(ind)
            return ind
            
        except Exception as e:
            print(f"Erreur: {e}")
            return None

try:
    import pandas as pd
except:
    os.system(f"{sys.executable} -m pip install pandas")
    import pandas as pd

analyzer = Analyzer()

# ============================================================================
# HTML
# ============================================================================

HTML = '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stock Analyzer Pro v2</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', system-ui, sans-serif; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); min-height: 100vh; color: #e0e0e0; }
        .navbar { background: rgba(255,255,255,0.05); padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.1); flex-wrap: wrap; gap: 1rem; }
        .logo { font-size: 1.5rem; font-weight: 700; color: #00d4ff; text-decoration: none; }
        .nav { display: flex; gap: 0.3rem; flex-wrap: wrap; }
        .nav a { color: #aaa; text-decoration: none; padding: 0.5rem 0.8rem; border-radius: 8px; transition: 0.3s; font-size: 0.9rem; }
        .nav a:hover { background: rgba(0,212,255,0.2); color: #00d4ff; }
        .container { max-width: 1400px; margin: 0 auto; padding: 1.5rem; }
        .card { background: rgba(255,255,255,0.05); border-radius: 16px; padding: 1.5rem; margin-bottom: 1.5rem; border: 1px solid rgba(255,255,255,0.1); }
        .hero { text-align: center; padding: 2rem; background: linear-gradient(135deg, rgba(0,212,255,0.1), transparent); border-radius: 24px; margin-bottom: 2rem; }
        .hero h1 { font-size: 2rem; background: linear-gradient(135deg, #00d4ff, #00ff88); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem; }
        .search-box { display: flex; gap: 1rem; max-width: 600px; margin: 1.5rem auto; }
        .search-box input { flex: 1; padding: 0.8rem 1.2rem; border-radius: 12px; border: 2px solid rgba(255,255,255,0.1); background: rgba(255,255,255,0.05); color: #fff; font-size: 1rem; }
        .search-box input:focus { outline: none; border-color: #00d4ff; }
        .btn { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.6rem 1.2rem; border-radius: 8px; border: none; font-weight: 600; cursor: pointer; text-decoration: none; transition: 0.3s; font-size: 0.9rem; }
        .btn-primary { background: linear-gradient(135deg, #00d4ff, #0099cc); color: #1a1a2e; }
        .btn-secondary { background: rgba(255,255,255,0.1); color: #e0e0e0; border: 1px solid rgba(255,255,255,0.2); }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 4px 20px rgba(0,212,255,0.3); }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-bottom: 1.5rem; }
        .stat { background: rgba(0,212,255,0.1); border-radius: 12px; padding: 1rem; text-align: center; border: 1px solid rgba(0,212,255,0.2); }
        .stat-value { font-size: 1.8rem; font-weight: 700; color: #00d4ff; }
        .stat-label { color: #888; margin-top: 0.3rem; font-size: 0.85rem; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 0.75rem; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); font-size: 0.9rem; }
        th { color: #00d4ff; font-weight: 600; }
        tr:hover { background: rgba(0,212,255,0.05); }
        .badge { display: inline-block; padding: 0.2rem 0.6rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600; }
        .badge-buy { background: rgba(0,255,136,0.2); color: #00ff88; }
        .badge-hold { background: rgba(255,193,7,0.2); color: #ffc107; }
        .badge-sell { background: rgba(255,71,87,0.2); color: #ff4757; }
        .quick-links { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 1rem; justify-content: center; }
        .quick-link { padding: 0.3rem 0.6rem; background: rgba(255,255,255,0.05); border-radius: 20px; color: #888; text-decoration: none; font-size: 0.8rem; }
        .quick-link:hover { background: rgba(0,212,255,0.2); color: #00d4ff; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; }
        .indicator { background: rgba(255,255,255,0.03); border-radius: 12px; padding: 1rem; border: 1px solid rgba(255,255,255,0.05); }
        .indicator-label { color: #666; font-size: 0.8rem; margin-bottom: 0.3rem; }
        .indicator-value { font-size: 1.1rem; font-weight: 600; }
        .good { color: #00ff88; }
        .warning { color: #ffc107; }
        .bad { color: #ff4757; }
        h1 { margin-bottom: 1rem; font-size: 1.5rem; }
        h2 { margin-bottom: 0.8rem; color: #00d4ff; font-size: 1.2rem; }
        h3 { margin-bottom: 0.5rem; color: #00d4ff; font-size: 1rem; }
        .sector-tag { display: inline-block; padding: 0.15rem 0.5rem; background: rgba(255,255,255,0.1); border-radius: 4px; font-size: 0.75rem; color: #888; }
        .news-link { color: #00d4ff; text-decoration: none; display: inline-flex; align-items: center; gap: 0.3rem; }
        .news-link:hover { text-decoration: underline; }
        .alert { background: rgba(255,193,7,0.2); border: 1px solid #ffc107; border-radius: 12px; padding: 1rem; margin-bottom: 1rem; }
        .alert-green { background: rgba(0,255,136,0.1); border-color: #00ff88; }
        .alert-red { background: rgba(255,71,87,0.1); border-color: #ff4757; }
        input[type="number"] { padding: 0.5rem; border-radius: 8px; border: 1px solid rgba(255,255,255,0.2); background: rgba(255,255,255,0.05); color: #fff; width: 100px; }
        .portfolio-total { display: flex; justify-content: space-between; padding: 1rem; background: rgba(0,212,255,0.1); border-radius: 12px; margin-bottom: 1rem; }
        @media (max-width: 768px) { .navbar { flex-direction: column; } .search-box { flex-direction: column; } .stats { grid-template-columns: repeat(2, 1fr); } }
    </style>
</head>
<body>
    <nav class="navbar">
        <a href="/" class="logo">📊 Stock Analyzer Pro v2</a>
        <div class="nav">
            <a href="/">Accueil</a>
            <a href="/analyze">Analyser</a>
            <a href="/compare">Comparer</a>
            <a href="/library">Bibliothèque</a>
            <a href="/portfolio">Portfolio</a>
            <a href="/macro">📰 Macro</a>
        </div>
    </nav>
    <div class="container">
        CONTENT
    </div>
</body>
</html>'''

def score_class(score):
    if score >= 60: return "good"
    if score >= 40: return "warning"
    return "bad"

def badge_class(rec):
    if "Achat" in rec: return "badge-buy"
    if "Neutre" in rec: return "badge-hold"
    return "badge-sell"

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def index():
    stats = analyzer.db.get_stats()
    recent = analyzer.db.get_all(10)
    searches = analyzer.db.get_searches(10)
    
    recent_html = ""
    if recent:
        recent_html = "<h2 style='margin-bottom:1rem;'>📈 Analyses Récentes</h2><table><thead><tr><th>Ticker</th><th>Entreprise</th><th>Prix</th><th>Score</th><th>Recommandation</th></tr></thead><tbody>"
        for ind in recent:
            score = ind.get_score()
            rec = ind.get_recommendation()
            recent_html += f"<tr><td><strong>{ind.ticker}</strong></td><td>{ind.company_name[:25]}</td><td>${ind.current_price:.2f}</td><td class='{score_class(score)}'>{score:.0f}</td><td><span class='badge {badge_class(rec)}'>{rec}</span></td></tr>"
        recent_html += "</tbody></table>"
    
    searches_html = ""
    if searches:
        searches_html = "<h3 style='margin-top:1.5rem;'>🔍 Recherches Récentes</h3><div class='quick-links'>"
        for s in searches:
            searches_html += f"<a href='/analyze?ticker={s['ticker']}' class='quick-link'>{s['ticker']}</a>"
        searches_html += "</div>"
    
    content = f'''
<div class="hero">
    <h1>Stock Analyzer Pro v2</h1>
    <p>Analyses Financières + News + Technique + Macro</p>
    <form action="/analyze" method="get" class="search-box">
        <input type="text" name="ticker" placeholder="Ticker ou nom (ex: MSFT, Microsoft)...">
        <button type="submit" class="btn btn-primary">Analyser</button>
    </form>
    <div class="quick-links">
        <a href="/analyze?ticker=MSFT" class="quick-link">Microsoft</a>
        <a href="/analyze?ticker=AAPL" class="quick-link">Apple</a>
        <a href="/analyze?ticker=GOOGL" class="quick-link">Google</a>
        <a href="/analyze?ticker=NVDA" class="quick-link">NVIDIA</a>
        <a href="/analyze?ticker=TSLA" class="quick-link">Tesla</a>
        <a href="/analyze?ticker=META" class="quick-link">Meta</a>
        <a href="/analyze?ticker=JPM" class="quick-link">JPMorgan</a>
        <a href="/analyze?ticker=LLY" class="quick-link">Eli Lilly</a>
    </div>
</div>
<div class="stats">
    <div class="stat"><div class="stat-value">{stats.get("companies", 0)}</div><div class="stat-label">Entreprises</div></div>
    <div class="stat"><div class="stat-value">{stats.get("searches", 0)}</div><div class="stat-label">Recherches</div></div>
    <div class="stat"><div class="stat-value">{stats.get("total", 0)}</div><div class="stat-label">Analyses</div></div>
</div>
{recent_html}
{searches_html}
'''
    return HTML.replace('CONTENT', content)

@app.route('/analyze', methods=['GET', 'POST'])
def analyze_page():
    if request.method == 'POST':
        ticker = request.form.get('ticker', '').strip()
        if ticker:
            ind = analyzer.analyze(ticker)
            if ind:
                return redirect(f"/result/{ind.ticker}")
    
    ticker_param = request.args.get('ticker', '')
    if ticker_param:
        ind = analyzer.analyze(ticker_param)
        if ind:
            return redirect(f"/result/{ind.ticker}")
    
    content = '''
<h1>📊 Analyser une Action</h1>
<div class="card">
    <form method="POST">
        <div class="search-box">
            <input type="text" name="ticker" placeholder="Entrez un ticker ou nom" required>
            <button type="submit" class="btn btn-primary">Analyser</button>
        </div>
    </form>
    <h3>Populaires</h3>
    <div class="quick-links">
        <a href="/analyze?ticker=MSFT" class="quick-link">Microsoft</a>
        <a href="/analyze?ticker=AAPL" class="quick-link">Apple</a>
        <a href="/analyze?ticker=GOOGL" class="quick-link">Google</a>
        <a href="/analyze?ticker=NVDA" class="quick-link">NVIDIA</a>
        <a href="/analyze?ticker=AMZN" class="quick-link">Amazon</a>
        <a href="/analyze?ticker=META" class="quick-link">Meta</a>
        <a href="/analyze?ticker=TSLA" class="quick-link">Tesla</a>
        <a href="/analyze?ticker=AMD" class="quick-link">AMD</a>
    </div>
    <h3 style="margin-top:1rem;">Finance</h3>
    <div class="quick-links">
        <a href="/analyze?ticker=JPM" class="quick-link">JPMorgan</a>
        <a href="/analyze?ticker=BAC" class="quick-link">Bank of America</a>
        <a href="/analyze?ticker=GS" class="quick-link">Goldman</a>
        <a href="/analyze?ticker=V" class="quick-link">Visa</a>
        <a href="/analyze?ticker=MA" class="quick-link">Mastercard</a>
    </div>
    <h3 style="margin-top:1rem;">Healthcare</h3>
    <div class="quick-links">
        <a href="/analyze?ticker=LLY" class="quick-link">Eli Lilly</a>
        <a href="/analyze?ticker=UNH" class="quick-link">UnitedHealth</a>
        <a href="/analyze?ticker=JNJ" class="quick-link">J&J</a>
        <a href="/analyze?ticker=PFE" class="quick-link">Pfizer</a>
    </div>
</div>
'''
    return HTML.replace('CONTENT', content)

@app.route('/result/<ticker>')
def result(ticker):
    ind = analyzer.analyze(ticker)
    if not ind:
        return redirect("/analyze")
    
    score = ind.get_score()
    rec = ind.get_recommendation()
    bull_strat = ind.get_strategy_bull()
    bear_strat = ind.get_strategy_bear()
    key_num, key_label, key_color, key_advice = ind.get_key_number()
    target = ind.get_target_price()
    
    # Prix d'achat
    buy_price = target.get('recommended_buy', 0)
    discount = target.get('discount_pct', 0)
    current_price = ind.current_price
    
    if buy_price < current_price:
        price_section = f'''
<div class="card" style="background: linear-gradient(135deg, #00ff8822, transparent); border: 2px solid #00ff88; text-align: center; padding: 1.5rem;">
    <div style="color:#00ff88;font-size:0.9rem;margin-bottom:0.5rem;">⏳ PRIX D'ACHAT RECOMMANDÉ</div>
    <div style="font-size: 3rem; font-weight: 800; color: #00ff88;">${buy_price:.2f}</div>
    <div style="color: #888; margin-top: 0.5rem;">Prix actuel: ${current_price:.2f} → Attendre {abs(discount):.0f}% de baisse</div>
</div>
'''
    else:
        price_section = f'''
<div class="card" style="background: linear-gradient(135deg, #ffc10722, transparent); border: 2px solid #ffc107; text-align: center; padding: 1.5rem;">
    <div style="color:#ffc107;font-size:0.9rem;margin-bottom:0.5rem;">✅ PRIX INTÉRESSANT</div>
    <div style="font-size: 3rem; font-weight: 800; color: #00ff88;">${current_price:.2f}</div>
    <div style="color: #888; margin-top: 0.5rem;">Déjà en zone d'achat (cible: ${buy_price:.2f})</div>
</div>
'''
    
    # Analyse technique
    trend_color = "#00ff88" if "Haussier" in (ind.trend or "") else "#ff4757" if "Baissier" in (ind.trend or "") else "#ffc107"
    rsi_color = "#00ff88" if ind.rsi_14 and ind.rsi_14 < 30 else "#ff4757" if ind.rsi_14 and ind.rsi_14 > 70 else "#ffc107"
    
    tech_section = f'''
<div class="card">
    <h2>📊 Analyse Technique</h2>
    <div class="grid">
        <div class="indicator">
            <div class="indicator-label">Tendance</div>
            <div class="indicator-value" style="color:{trend_color};">{ind.trend or "N/A"}</div>
        </div>
        <div class="indicator">
            <div class="indicator-label">RSI 14</div>
            <div class="indicator-value" style="color:{rsi_color};">{f"{ind.rsi_14:.1f}" if ind.rsi_14 else "N/A"}</div>
            <div style="font-size:0.7rem;color:#888;">{"Survendu" if ind.rsi_14 and ind.rsi_14 < 30 else "Suracheté" if ind.rsi_14 and ind.rsi_14 > 70 else "Neutre"}</div>
        </div>
        <div class="indicator">
            <div class="indicator-label">MA 50</div>
            <div class="indicator-value">${f"{ind.ma_50:.2f}" if ind.ma_50 else "N/A"}</div>
            <div style="font-size:0.7rem;color:{"#00ff88" if ind.ma_50 and ind.current_price > ind.ma_50 else "#ff4757"};">{"Au-dessus" if ind.ma_50 and ind.current_price > ind.ma_50 else "En-dessous"} du prix</div>
        </div>
        <div class="indicator">
            <div class="indicator-label">MA 200</div>
            <div class="indicator-value">${f"{ind.ma_200:.2f}" if ind.ma_200 else "N/A"}</div>
        </div>
        <div class="indicator">
            <div class="indicator-label">Support</div>
            <div class="indicator-value good">${f"{ind.support:.2f}" if ind.support else "N/A"}</div>
        </div>
        <div class="indicator">
            <div class="indicator-label">Résistance</div>
            <div class="indicator-value bad">${f"{ind.resistance:.2f}" if ind.resistance else "N/A"}</div>
        </div>
    </div>
</div>
'''
    
    # News section
    news_section = f'''
<div class="card">
    <h2>📰 Actualités & Events</h2>
    <div class="grid">
        <div class="indicator">
            <div class="indicator-label">Dernières News</div>
            <a href="{ind.news_link}" target="_blank" class="news-link">📰 Voir sur Yahoo Finance →</a>
        </div>
        <div class="indicator">
            <div class="indicator-label">Calendrier Earnings</div>
            <a href="https://finance.yahoo.com/calendar/earnings/?symbol={ind.ticker}" target="_blank" class="news-link">📅 Voir le calendrier →</a>
        </div>
    </div>
    <div class="alert">
        <strong>💡 Sources recommandées pour suivre l'actualité:</strong><br>
        <a href="https://seekingalpha.com/search?q={ind.ticker}" target="_blank" class="news-link">Seeking Alpha</a> · 
        <a href="https://www.benzinga.com/search?query={ind.ticker}" target="_blank" class="news-link">Benzinga</a> · 
        <a href="https://finviz.com/quote.ashx?t={ind.ticker}" target="_blank" class="news-link">Finviz</a>
    </div>
</div>
'''
    
    content = f'''
<div style="margin-bottom:1rem;"><a href="/analyze" class="btn btn-secondary">← Nouvelle analyse</a></div>

<div class="card" style="background: linear-gradient(135deg, rgba(0,212,255,0.1), transparent);">
    <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:1rem;">
        <div>
            <h1 style="font-size:1.5rem;margin-bottom:0.3rem;">{ind.company_name}</h1>
            <span class="sector-tag">{ind.sector or "N/A"}</span>
            <p style="color:#888;margin-top:0.3rem;">{ind.ticker}</p>
        </div>
        <div style="text-align:right;">
            <div style="font-size:2rem;font-weight:700;color:#00d4ff;">${ind.current_price:.2f}</div>
            <div style="color:#888;">{ind.fmt_currency(ind.market_cap)}</div>
        </div>
    </div>
    <div style="display:flex;gap:2rem;margin-top:1.5rem;flex-wrap:wrap;">
        <div>
            <div class="score-big {score_class(score)}" style="font-size:3rem;font-weight:700;">{score:.0f}</div>
            <div style="color:#888;font-size:0.85rem;">SCORE GLOBAL</div>
        </div>
        <div>
            <span class="badge {badge_class(rec)}" style="font-size:1.2rem;padding:0.5rem 1rem;">{rec}</span>
        </div>
    </div>
</div>

{price_section}

<div class="card" style="background: linear-gradient(135deg, {key_color}22, transparent); border: 1px solid {key_color}; text-align: center; padding: 1rem;">
    <div style="font-size: 1rem; font-weight: 600; color: {key_color};">{key_label} ({key_num:.0f}/100)</div>
    <div style="color: #aaa; font-size: 0.85rem; margin-top: 0.3rem;">{key_advice}</div>
</div>

<div class="grid">
    <div class="indicator"><div class="indicator-label">P/E</div><div class="indicator-value">{ind.fmt_ratio(ind.price_to_earnings)}</div></div>
    <div class="indicator"><div class="indicator-label">PEG</div><div class="indicator-value {score_class(score)}">{ind.fmt_ratio(ind.peg_ratio)}</div></div>
    <div class="indicator"><div class="indicator-label">P/B</div><div class="indicator-value">{ind.fmt_ratio(ind.price_to_book)}</div></div>
    <div class="indicator"><div class="indicator-label">EV/EBITDA</div><div class="indicator-value">{ind.fmt_ratio(ind.ev_to_ebitda)}</div></div>
    <div class="indicator"><div class="indicator-label">Marge Nette</div><div class="indicator-value">{ind.fmt_pct(ind.profit_margin)}</div></div>
    <div class="indicator"><div class="indicator-label">ROE</div><div class="indicator-value">{ind.fmt_pct(ind.roe)}</div></div>
    <div class="indicator"><div class="indicator-label">Croissance CA</div><div class="indicator-value {score_class(score)}">{ind.fmt_pct(ind.revenue_growth_yoy)}</div></div>
    <div class="indicator"><div class="indicator-label">Dette/Equity</div><div class="indicator-value">{ind.fmt_ratio(ind.debt_to_equity)}</div></div>
    <div class="indicator"><div class="indicator-label">FCF</div><div class="indicator-value">{ind.fmt_currency(ind.free_cash_flow)}</div></div>
    <div class="indicator"><div class="indicator-label">Beta</div><div class="indicator-value">{f"{ind.beta:.2f}" if ind.beta else "N/A"}</div></div>
    <div class="indicator"><div class="indicator-label">Dividende</div><div class="indicator-value">{ind.fmt_pct(ind.dividend_yield)}</div></div>
    <div class="indicator"><div class="indicator-label">Target Price</div><div class="indicator-value">${f"{ind.target_price:.2f}" if ind.target_price else "N/A"}</div></div>
</div>

{tech_section}

{news_section}

<div class="card">
    <h2>📋 Stratégies</h2>
    <div class="grid">
        <div class="indicator" style="border-color:rgba(0,255,136,0.3);">
            <div class="indicator-label">🐂 Marché Haussier</div>
            <div class="indicator-value">{bull_strat}</div>
        </div>
        <div class="indicator" style="border-color:rgba(255,193,7,0.3);">
            <div class="indicator-label">🐻 Marché Baissier</div>
            <div class="indicator-value">{bear_strat}</div>
        </div>
    </div>
</div>

<div class="card">
    <h3>💼 Ajouter au Portfolio</h3>
    <form action="/portfolio/add" method="POST" style="display:flex;gap:1rem;align-items:center;flex-wrap:wrap;">
        <input type="hidden" name="ticker" value="{ind.ticker}">
        <label>Actions: <input type="number" name="shares" step="0.01" placeholder="Nombre" required></label>
        <label>Prix moyen: <input type="number" name="avg_price" step="0.01" placeholder="$" required></label>
        <button type="submit" class="btn btn-primary">Ajouter</button>
    </form>
</div>

<div class="card" style="margin-top:1rem;text-align:center;color:#666;font-size:0.85rem;">
    Analyse - {ind.timestamp.strftime("%d/%m/%Y à %H:%M:%S")}
</div>
'''
    return HTML.replace('CONTENT', content)

@app.route('/compare', methods=['GET', 'POST'])
def compare_page():
    results = []
    if request.method == 'POST':
        tickers = [t.strip().upper() for t in request.form.get('tickers', '').split(',') if t.strip()]
        for t in tickers:
            ind = analyzer.analyze(t)
            if ind:
                results.append(ind)
    
    table_html = ""
    if results:
        table_html = "<table><thead><tr><th>Indicateur</th>"
        for r in results:
            table_html += f"<th>{r.ticker}</th>"
        table_html += "</tr></thead><tbody>"
        table_html += "<tr style='background:rgba(0,212,255,0.1);'><td><strong>Prix</strong></td>"
        for r in results:
            table_html += f"<td><strong>${r.current_price:.2f}</strong></td>"
        table_html += "</tr><tr><td>P/E</td>"
        for r in results:
            table_html += f"<td>{r.price_to_earnings:.1f if r.price_to_earnings else 'N/A'}</td>"
        table_html += "</tr><tr><td>PEG</td>"
        for r in results:
            table_html += f"<td>{r.peg_ratio:.2f if r.peg_ratio else 'N/A'}</td>"
        table_html += "</tr><tr><td>Marge Nette</td>"
        for r in results:
            table_html += f"<td>{r.profit_margin:.1f if r.profit_margin else 'N/A'}%</td>"
        table_html += "</tr><tr><td>ROE</td>"
        for r in results:
            table_html += f"<td>{r.roe:.1f if r.roe else 'N/A'}%</td>"
        table_html += "</tr><tr><td>Croissance CA</td>"
        for r in results:
            table_html += f"<td>{r.revenue_growth_yoy:.1f if r.revenue_growth_yoy else 'N/A'}%</td>"
        table_html += "</tr><tr style='background:rgba(0,212,255,0.1);'><td><strong>Score</strong></td>"
        for r in results:
            sc = r.get_score()
            table_html += f"<td><strong class='{score_class(sc)}'>{sc:.0f}</strong></td>"
        table_html += "</tr><tr><td>Recommandation</td>"
        for r in results:
            rc = r.get_recommendation()
            table_html += f"<td><span class='badge {badge_class(rc)}'>{rc}</span></td>"
        table_html += "</tr></tbody></table>"
    
    content = f'''
<h1>⚖️ Comparer des Actions</h1>
<div class="card">
    <form method="POST">
        <label style="display:block;margin-bottom:0.5rem;color:#888;">Tickers séparés par des virgules:</label>
        <div class="search-box">
            <input type="text" name="tickers" placeholder="Ex: MSFT, AAPL, GOOGL, NVDA" required>
            <button type="submit" class="btn btn-primary">Comparer</button>
        </div>
    </form>
    <div class="quick-links">
        <a href="?tickers=MSFT,AAPL,GOOGL,NVDA" class="quick-link">Tech Giants</a>
        <a href="?tickers=JPM,BAC,WFC,GS,MS" class="quick-link">Banques</a>
        <a href="?tickers=NVDA,AMD,INTC,QCOM,AVGO" class="quick-link">Semi-conducteurs</a>
        <a href="?tickers=LLY,JNJ,PFE,UNH,ABBV" class="quick-link">Santé</a>
    </div>
</div>
{"<div class='card'><h2>📊 Comparaison</h2>" + table_html + "</div>" if table_html else ""}
'''
    return HTML.replace('CONTENT', content)

@app.route('/library')
def library():
    stats = analyzer.db.get_stats()
    analyses = analyzer.db.get_all(100)
    searches = analyzer.db.get_searches(50)
    
    analyses_html = ""
    if analyses:
        analyses_html = "<table><thead><tr><th>Ticker</th><th>Entreprise</th><th>Prix</th><th>Score</th><th>Recommandation</th><th></th></tr></thead><tbody>"
        for ind in analyses:
            score = ind.get_score()
            rec = ind.get_recommendation()
            analyses_html += f"<tr><td><strong>{ind.ticker}</strong></td><td>{ind.company_name[:25]}</td><td>${ind.current_price:.2f}</td><td class='{score_class(score)}'>{score:.0f}</td><td><span class='badge {badge_class(rec)}'>{rec}</span></td><td><a href='/result/{ind.ticker}' class='btn btn-secondary' style='padding:0.3rem 0.6rem;font-size:0.75rem;'>Voir</a></td></tr>"
        analyses_html += "</tbody></table>"
    
    searches_html = ""
    if searches:
        searches_html = "<h3>🔍 Recherches</h3><div class='quick-links'>"
        for s in searches:
            searches_html += f"<a href='/result/{s['ticker']}' class='quick-link'>{s['ticker']}</a>"
        searches_html += "</div>"
    
    content = f'''
<h1>📚 Bibliothèque ({stats.get("companies", 0)} entreprises)</h1>
<div class="stats">
    <div class="stat"><div class="stat-value">{stats.get("companies", 0)}</div><div class="stat-label">Entreprises</div></div>
    <div class="stat"><div class="stat-value">{stats.get("searches", 0)}</div><div class="stat-label">Recherches</div></div>
</div>
<div class="card">
    <h2>📈 Analyses</h2>
    <a href="/analyze" class="btn btn-primary" style="margin-bottom:1rem;">+ Nouvelle Analyse</a>
    {analyses_html}
</div>
<div class="card">
    {searches_html}
</div>
'''
    return HTML.replace('CONTENT', content)

@app.route('/portfolio', methods=['GET', 'POST'])
def portfolio_page():
    if request.method == 'POST':
        delete_ticker = request.form.get('delete')
        if delete_ticker:
            analyzer.db.remove_from_portfolio(delete_ticker)
    
    total_value, total_cost, items = analyzer.db.get_portfolio_value()
    gain_loss = total_value - total_cost
    gain_loss_pct = (gain_loss / total_cost * 100) if total_cost > 0 else 0
    
    portfolio_html = ""
    if items:
        portfolio_html = "<table><thead><tr><th>Ticker</th><th>Actions</th><th>Prix Achat</th><th>Prix Actuel</th><th>Valeur</th><th>Gain/Perte</th><th></th></tr></thead><tbody>"
        for item in items:
            color = "#00ff88" if item['gain_loss'] >= 0 else "#ff4757"
            sign = "+" if item['gain_loss'] >= 0 else ""
            portfolio_html += f"<tr><td><strong>{item['ticker']}</strong><br><span style='color:#888;font-size:0.75rem;'>{item['name'][:20]}</span></td><td>{item['shares']:.2f}</td><td>${item['avg_price']:.2f}</td><td>${item['current_price']:.2f}</td><td><strong>${item['current_value']:.2f}</strong></td><td style='color:{color};'>{sign}${item['gain_loss']:.2f} ({sign}{item['gain_loss_pct']:.1f}%)</td><td><form method='POST' style='display:inline;'><input type='hidden' name='delete' value=\"{item['ticker']}\"><button type='submit' class='btn' style='background:rgba(255,71,87,0.2);color:#ff4757;padding:0.3rem 0.6rem;font-size:0.75rem;'>✕</button></form></td></tr>"
        portfolio_html += "</tbody></table>"
    else:
        portfolio_html = "<p style='text-align:center;color:#888;padding:2rem;'>💼 Portfolio vide. Ajoutez des actions depuis la page d'analyse.</p>"
    
    content = f'''
<h1>💼 Mon Portfolio</h1>
<div class="portfolio-total">
    <div>
        <div style="font-size:0.9rem;color:#888;">Valeur Totale</div>
        <div style="font-size:1.8rem;font-weight:700;color:#00d4ff;">${total_value:,.2f}</div>
    </div>
    <div>
        <div style="font-size:0.9rem;color:#888;">Coût Total</div>
        <div style="font-size:1.5rem;">${total_cost:,.2f}</div>
    </div>
    <div>
        <div style="font-size:0.9rem;color:#888;">Gain/Perte</div>
        <div style="font-size:1.5rem;color:{"#00ff88" if gain_loss >= 0 else "#ff4757"};">{"+" if gain_loss >= 0 else ""}${gain_loss:,.2f} ({"+" if gain_loss_pct >= 0 else ""}{gain_loss_pct:.1f}%)</div>
    </div>
</div>
<div class="card">
    <h2>📋 Positions</h2>
    {portfolio_html}
</div>
<div class="card">
    <h3>➕ Ajouter Manuellement</h3>
    <form action="/portfolio/add" method="POST" style="display:flex;gap:1rem;align-items:center;flex-wrap:wrap;">
        <label>Ticker: <input type="text" name="ticker" placeholder="MSFT" required style="width:100px;"></label>
        <label>Actions: <input type="number" name="shares" step="0.01" placeholder="10" required style="width:100px;"></label>
        <label>Prix moyen: <input type="number" name="avg_price" step="0.01" placeholder="350" required style="width:100px;"></label>
        <button type="submit" class="btn btn-primary">Ajouter</button>
    </form>
</div>
'''
    return HTML.replace('CONTENT', content)

@app.route('/portfolio/add', methods=['POST'])
def add_to_portfolio():
    ticker = request.form.get('ticker', '').strip()
    shares = float(request.form.get('shares', 0))
    avg_price = float(request.form.get('avg_price', 0))
    
    if ticker and shares > 0 and avg_price > 0:
        analyzer.analyze(ticker)
        analyzer.db.add_to_portfolio(ticker, shares, avg_price)
    
    return redirect('/portfolio')

@app.route('/macro')
def macro_page():
    content = '''
<h1>🌍 Économie Macro & Events</h1>

<div class="card">
    <h2>📅 Calendrier Économique</h2>
    <div class="alert">
        <strong>Sources fiables pour suivre l'économie:</strong><br>
        <a href="https://www.forexfactory.com/" target="_blank" class="news-link">Forex Factory</a> · 
        <a href="https://www.economiccalendar.com/" target="_blank" class="news-link">Economic Calendar</a> · 
        <a href="https://www.investing.com/economic-calendar/" target="_blank" class="news-link">Investing.com</a>
    </div>
    <h3>📊 Indicateurs Clés à Surveiller</h3>
    <table>
        <thead><tr><th>Indicateur</th><th>Fréquence</th><th>Importance</th><th>Impact</th></tr></thead>
        <tbody>
            <tr><td>Non-Farm Payrolls (NFP)</td><td>Mensuel</td><td>⭐⭐⭐⭐⭐</td><td>Actions, Dollar, Obligations</td></tr>
            <tr><td>Fed Funds Rate</td><td>8x/an</td><td>⭐⭐⭐⭐⭐</td><td>Tous les marchés</td></tr>
            <tr><td>IPC (Inflation)</td><td>Mensuel</td><td>⭐⭐⭐⭐⭐</td><td>Taux, Actions</td></tr>
            <tr><td>PIB US</td><td>Trimestriel</td><td>⭐⭐⭐⭐</td><td>Actions, Dollar</td></tr>
            <tr><td>PMI Manufacturing</td><td>Mensuel</td><td>⭐⭐⭐</td><td>Actions Industrielles</td></tr>
            <tr><td>Consumer Confidence</td><td>Mensuel</td><td>⭐⭐⭐</td><td>Consommation</td></tr>
            <tr><td>Retail Sales</td><td>Mensuel</td><td>⭐⭐⭐</td><td>Retail, Consommation</td></tr>
            <tr><td>Jobless Claims</td><td>Hebdomadaire</td><td>⭐⭐</td><td>Marché du travail</td></tr>
        </tbody>
    </table>
</div>

<div class="card">
    <h2>🏛️ Impact par Secteur</h2>
    <table>
        <thead><tr><th>Secteur</th><th>Sensible à</th><th>Stratégie</th></tr></thead>
        <tbody>
            <tr><td>🏦 Banques</td><td>Taux Fed, Yield Curve, Crédit</td><td>Surveiller taux courts/longs</td></tr>
            <tr><td>🏠 Immobilier</td><td>Taux longs, Hypothécaires</td><td>Watch 10Y Treasury yield</td></tr>
            <tr><td>⛽ Énergie</td><td>Prix Oil, Géopolitique</td><td>Brent, WTI Crude</td></tr>
            <tr><td>💊 Pharma</td><td>FDA, Politique santé</td><td>FDA approvals calendar</td></tr>
            <tr><td>🛒 Consommation</td><td>Consumer spending, Inflation</td><td>Retail sales, Confidence</td></tr>
            <tr><td>💻 Tech</td><td>Taux longs, Sentiment risque</td><td>NASDAQ vs S&P500 ratio</td></tr>
            <tr><td>🏭 Industriels</td><td>PMI, Trade tariffs</td><td>Global trade data</td></tr>
            <tr><td>💰 Finance</td><td>Credit spreads, Volatility</td><td>VIX, HY spreads</td></tr>
        </tbody>
    </table>
</div>

<div class="card">
    <h2>📰 Sources News Finance</h2>
    <div class="quick-links">
        <a href="https://www.wsj.com" target="_blank" class="quick-link">WSJ</a>
        <a href="https://www.ft.com" target="_blank" class="quick-link">Financial Times</a>
        <a href="https://www.bloomberg.com" target="_blank" class="quick-link">Bloomberg</a>
        <a href="https://seekingalpha.com" target="_blank" class="quick-link">Seeking Alpha</a>
        <a href="https://www.benzinga.com" target="_blank" class="quick-link">Benzinga</a>
        <a href="https://finviz.com" target="_blank" class="quick-link">Finviz</a>
        <a href="https://www.marketwatch.com" target="_blank" class="quick-link">MarketWatch</a>
        <a href="https://www.reuters.com" target="_blank" class="quick-link">Reuters</a>
    </div>
</div>

<div class="card">
    <h2>📈 VIX & Volatilité</h2>
    <p style="color:#888;">Surveiller le VIX (indice de peur):</p>
    <div class="quick-links">
        <a href="https://finance.yahoo.com/quote/%5EVIX/" target="_blank" class="quick-link">VIX sur Yahoo Finance</a>
        <a href="https://www.cboe.com/indices/vix/" target="_blank" class="quick-link">CBOE VIX</a>
    </div>
    <div class="alert">
        <strong>💡 Interprétation VIX:</strong><br>
        VIX < 15: Marché confiant (potential overbought)<br>
        VIX 15-25: Volatilité normale<br>
        VIX 25-40: Stress du marché (potential buying opportunity)<br>
        VIX > 40: Panique/crise (buy the dip?)
    </div>
</div>
'''
    return HTML.replace('CONTENT', content)

# ============================================================================
# LANCEMENT
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  [ STOCK ANALYZER PRO v2 ]")
    print("  Analyse + Technique + News + Macro")
    print("=" * 60)
    print("  Open: http://localhost:5000")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)
