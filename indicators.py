"""
Module d'indicateurs financiers complets pour l'analyse d'actions
"""

from dataclasses import dataclass
from typing import Dict, Optional
from datetime import datetime


@dataclass
class FinancialIndicators:
    ticker: str
    company_name: str
    current_price: float
    
    price_to_earnings: Optional[float] = None
    peg_ratio: Optional[float] = None
    price_to_book: Optional[float] = None
    
    earnings_per_share: Optional[float] = None
    book_value_per_share: Optional[float] = None
    dividend_yield: Optional[float] = None
    payout_ratio: Optional[float] = None
    
    free_cash_flow: Optional[float] = None
    operating_cash_flow: Optional[float] = None
    fcf_per_share: Optional[float] = None
    
    total_debt: Optional[float] = None
    debt_to_equity: Optional[float] = None
    debt_to_assets: Optional[float] = None
    current_ratio: Optional[float] = None
    quick_ratio: Optional[float] = None
    
    revenue: Optional[float] = None
    revenue_growth_yoy: Optional[float] = None
    revenue_growth_3y: Optional[float] = None
    revenue_per_share: Optional[float] = None
    
    net_income: Optional[float] = None
    profit_margin: Optional[float] = None
    operating_margin: Optional[float] = None
    gross_margin: Optional[float] = None
    
    roe: Optional[float] = None
    roa: Optional[float] = None
    roic: Optional[float] = None
    
    beta: Optional[float] = None
    market_cap: Optional[float] = None
    enterprise_value: Optional[float] = None
    ev_to_revenue: Optional[float] = None
    ev_to_ebitda: Optional[float] = None
    
    shares_outstanding: Optional[float] = None
    institutional_ownership: Optional[float] = None
    
    week_52_high: Optional[float] = None
    week_52_low: Optional[float] = None
    price_to_52w_high: Optional[float] = None
    
    analyst_rating: Optional[str] = None
    target_price: Optional[float] = None
    upside_downside: Optional[float] = None
    
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict:
        return {
            "ticker": self.ticker,
            "company_name": self.company_name,
            "current_price": self.current_price,
            "price_to_earnings": self.price_to_earnings,
            "peg_ratio": self.peg_ratio,
            "price_to_book": self.price_to_book,
            "earnings_per_share": self.earnings_per_share,
            "book_value_per_share": self.book_value_per_share,
            "dividend_yield": self.dividend_yield,
            "payout_ratio": self.payout_ratio,
            "free_cash_flow": self.free_cash_flow,
            "operating_cash_flow": self.operating_cash_flow,
            "fcf_per_share": self.fcf_per_share,
            "total_debt": self.total_debt,
            "debt_to_equity": self.debt_to_equity,
            "debt_to_assets": self.debt_to_assets,
            "current_ratio": self.current_ratio,
            "quick_ratio": self.quick_ratio,
            "revenue": self.revenue,
            "revenue_growth_yoy": self.revenue_growth_yoy,
            "revenue_growth_3y": self.revenue_growth_3y,
            "revenue_per_share": self.revenue_per_share,
            "net_income": self.net_income,
            "profit_margin": self.profit_margin,
            "operating_margin": self.operating_margin,
            "gross_margin": self.gross_margin,
            "roe": self.roe,
            "roac": self.roa,
            "roic": self.roic,
            "beta": self.beta,
            "market_cap": self.market_cap,
            "enterprise_value": self.enterprise_value,
            "ev_to_revenue": self.ev_to_revenue,
            "ev_to_ebitda": self.ev_to_ebitda,
            "shares_outstanding": self.shares_outstanding,
            "institutional_ownership": self.institutional_ownership,
            "week_52_high": self.week_52_high,
            "week_52_low": self.week_52_low,
            "price_to_52w_high": self.price_to_52w_high,
            "analyst_rating": self.analyst_rating,
            "target_price": self.target_price,
            "upside_downside": self.upside_downside,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'FinancialIndicators':
        if isinstance(data.get('timestamp'), str):
            data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
    
    def get_valuation_score(self) -> float:
        scores = []
        weights = []
        
        if self.price_to_earnings:
            if 10 <= self.price_to_earnings <= 25:
                scores.append(100 - abs(self.price_to_earnings - 17.5) * 4)
                weights.append(1)
            elif self.price_to_earnings < 10:
                scores.append(90)
                weights.append(1)
            else:
                scores.append(max(0, 50 - (self.price_to_earnings - 25) * 2))
                weights.append(1)
        
        if self.peg_ratio:
            if self.peg_ratio <= 1:
                scores.append(100 - self.peg_ratio * 50)
                weights.append(1.5)
            else:
                scores.append(max(0, 50 - (self.peg_ratio - 1) * 30))
                weights.append(1.5)
        
        if self.price_to_book:
            if 1 <= self.price_to_book <= 5:
                scores.append(100 - abs(self.price_to_book - 3) * 15)
                weights.append(1)
            elif self.price_to_book < 1:
                scores.append(90)
                weights.append(1)
            else:
                scores.append(max(0, 70 - (self.price_to_book - 5) * 10))
                weights.append(1)
        
        if self.ev_to_revenue:
            if self.ev_to_revenue <= 3:
                scores.append(100 - self.ev_to_revenue * 20)
                weights.append(1)
            else:
                scores.append(max(0, 40 - (self.ev_to_revenue - 3) * 10))
                weights.append(1)
        
        if scores and weights:
            return sum(s * w for s, w in zip(scores, weights)) / sum(weights)
        return 50.0
    
    def get_solvency_score(self) -> float:
        scores = []
        weights = []
        
        if self.debt_to_equity:
            if self.debt_to_equity <= 0.5:
                scores.append(100)
                weights.append(2)
            elif self.debt_to_equity <= 1:
                scores.append(100 - (self.debt_to_equity - 0.5) * 40)
                weights.append(2)
            elif self.debt_to_equity <= 2:
                scores.append(80 - (self.debt_to_equity - 1) * 30)
                weights.append(2)
            else:
                scores.append(max(0, 50 - (self.debt_to_equity - 2) * 15))
                weights.append(2)
        
        if self.current_ratio:
            if self.current_ratio >= 1.5:
                scores.append(100)
                weights.append(1)
            elif self.current_ratio >= 1:
                scores.append(70 + (self.current_ratio - 1) * 30)
                weights.append(1)
            else:
                scores.append(max(0, self.current_ratio * 70))
                weights.append(1)
        
        if self.quick_ratio:
            if self.quick_ratio >= 1:
                scores.append(100)
                weights.append(1)
            else:
                scores.append(self.quick_ratio * 100)
                weights.append(1)
        
        if scores and weights:
            return sum(s * w for s, w in zip(scores, weights)) / sum(weights)
        return 50.0
    
    def get_profitability_score(self) -> float:
        scores = []
        weights = []
        
        if self.profit_margin:
            if self.profit_margin >= 20:
                scores.append(100)
                weights.append(2)
            elif self.profit_margin >= 10:
                scores.append(50 + (self.profit_margin - 10) * 5)
                weights.append(2)
            elif self.profit_margin > 0:
                scores.append(self.profit_margin * 5)
                weights.append(2)
            else:
                scores.append(0)
                weights.append(2)
        
        if self.roe:
            if self.roe >= 20:
                scores.append(100)
                weights.append(2)
            elif self.roe >= 10:
                scores.append(50 + (self.roe - 10) * 5)
                weights.append(2)
            elif self.roe > 0:
                scores.append(self.roe * 5)
                weights.append(2)
            else:
                scores.append(0)
                weights.append(2)
        
        if self.roa:
            if self.roa >= 10:
                scores.append(100)
                weights.append(1)
            elif self.roa >= 5:
                scores.append(50 + (self.roa - 5) * 10)
                weights.append(1)
            else:
                scores.append(max(0, self.roa * 10))
                weights.append(1)
        
        if self.operating_margin:
            if self.operating_margin >= 25:
                scores.append(100)
                weights.append(1)
            elif self.operating_margin >= 15:
                scores.append(60 + (self.operating_margin - 15) * 4)
                weights.append(1)
            else:
                scores.append(max(0, 40 + self.operating_margin * 2))
                weights.append(1)
        
        if scores and weights:
            return sum(s * w for s, w in zip(scores, weights)) / sum(weights)
        return 50.0
    
    def get_growth_score(self) -> float:
        scores = []
        weights = []
        
        if self.revenue_growth_yoy:
            if self.revenue_growth_yoy >= 20:
                scores.append(100)
                weights.append(2)
            elif self.revenue_growth_yoy >= 10:
                scores.append(50 + self.revenue_growth_yoy * 2.5)
                weights.append(2)
            elif self.revenue_growth_yoy >= 0:
                scores.append(30 + self.revenue_growth_yoy * 2)
                weights.append(2)
            else:
                scores.append(max(0, 30 + self.revenue_growth_yoy))
                weights.append(2)
        
        if self.revenue_growth_3y:
            if self.revenue_growth_3y >= 15:
                scores.append(100)
                weights.append(1.5)
            elif self.revenue_growth_3y >= 5:
                scores.append(50 + self.revenue_growth_3y * 3.3)
                weights.append(1.5)
            else:
                scores.append(max(0, 40 + self.revenue_growth_3y * 2))
                weights.append(1.5)
        
        if self.fcf_per_share and self.earnings_per_share:
            if self.fcf_per_share >= self.earnings_per_share:
                scores.append(100)
                weights.append(1)
            else:
                scores.append(max(0, (self.fcf_per_share / self.earnings_per_share) * 100 if self.earnings_per_share > 0 else 50))
                weights.append(1)
        
        if scores and weights:
            return sum(s * w for s, w in zip(scores, weights)) / sum(weights)
        return 50.0
    
    def get_cash_flow_score(self) -> float:
        scores = []
        weights = []
        
        if self.free_cash_flow and self.free_cash_flow > 0:
            scores.append(min(100, 50 + self.free_cash_flow / 1e9 * 10))
            weights.append(2)
        elif self.free_cash_flow is not None:
            scores.append(0)
            weights.append(2)
        
        if self.fcf_per_share and self.earnings_per_share:
            if self.earnings_per_share > 0:
                ratio = self.fcf_per_share / self.earnings_per_share
                if ratio >= 1:
                    scores.append(100)
                    weights.append(2)
                else:
                    scores.append(ratio * 100)
                    weights.append(2)
        
        if self.operating_cash_flow and self.net_income:
            if self.net_income > 0:
                ratio = self.operating_cash_flow / self.net_income
                if ratio >= 1:
                    scores.append(100)
                    weights.append(1)
                else:
                    scores.append(ratio * 100)
                    weights.append(1)
        
        if scores and weights:
            return sum(s * w for s, w in zip(scores, weights)) / sum(weights)
        return 50.0
    
    def get_overall_score(self) -> float:
        valuation = self.get_valuation_score()
        solvency = self.get_solvency_score()
        profitability = self.get_profitability_score()
        growth = self.get_growth_score()
        cash_flow = self.get_cash_flow_score()
        
        return (valuation * 0.25 + solvency * 0.20 + profitability * 0.25 + growth * 0.15 + cash_flow * 0.15)
    
    def get_recommendation(self) -> str:
        score = self.get_overall_score()
        if score >= 75:
            return "Achat Fort ⭐⭐⭐"
        elif score >= 60:
            return "Achat"
        elif score >= 45:
            return "Neutre"
        elif score >= 30:
            return "Vente"
        else:
            return "Vente Forte"
    
    def format_currency(self, value: float, prefix: str = "$") -> str:
        if value is None:
            return "N/A"
        if abs(value) >= 1e12:
            return f"{prefix}{value/1e12:.2f}T"
        elif abs(value) >= 1e9:
            return f"{prefix}{value/1e9:.2f}B"
        elif abs(value) >= 1e6:
            return f"{prefix}{value/1e6:.2f}M"
        elif abs(value) >= 1e3:
            return f"{prefix}{value/1e3:.2f}K"
        else:
            return f"{prefix}{value:.2f}"
    
    def format_percentage(self, value: float) -> str:
        if value is None:
            return "N/A"
        return f"{value:.2f}%"
    
    def format_ratio(self, value: float) -> str:
        if value is None:
            return "N/A"
        return f"{value:.2f}x"
