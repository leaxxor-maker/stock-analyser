"""
Module principal d'analyse d'actions
Récupère les données financières et calcule tous les indicateurs
"""

import yfinance as yf
from typing import Optional, Dict, List
from datetime import datetime

from indicators import FinancialIndicators
from search import CompanySearch


class StockAnalyzer:
    def __init__(self):
        self.search = CompanySearch()
    
    def analyze(self, ticker: str, fetch_fresh: bool = False) -> Optional[FinancialIndicators]:
        resolved_ticker = self.search.resolve(ticker)
        if not resolved_ticker:
            print(f"Ticker '{ticker}' non reconnu. Utilisez le nom complet ou vérifiez l'orthographe.")
            return None
        
        try:
            stock = yf.Ticker(resolved_ticker)
            info = stock.info
            
            if not info or info.get('regularMarketPrice') is None:
                print(f"Impossible de récupérer les données pour {resolved_ticker}")
                return None
            
            company_name = info.get('longName') or info.get('shortName') or resolved_ticker
            current_price = info.get('regularMarketPrice') or info.get('currentPrice') or 0
            
            indicators = FinancialIndicators(
                ticker=resolved_ticker,
                company_name=company_name,
                current_price=current_price,
                
                price_to_earnings=info.get('trailingPE'),
                peg_ratio=info.get('pegRatio'),
                price_to_book=info.get('priceToBook'),
                
                earnings_per_share=info.get('trailingEps'),
                book_value_per_share=info.get('bookValue'),
                dividend_yield=info.get('dividendYield'),
                payout_ratio=info.get('payoutRatio'),
                
                free_cash_flow=info.get('freeCashflow'),
                operating_cash_flow=info.get('operatingCashflow'),
                fcf_per_share=info.get('freeCashflow') / info.get('sharesOutstanding') if info.get('freeCashflow') and info.get('sharesOutstanding') else None,
                
                total_debt=info.get('totalDebt'),
                debt_to_equity=info.get('debtToEquity'),
                debt_to_assets=info.get('totalAssets') and info.get('totalDebt') and (info.get('totalDebt') / info.get('totalAssets')) if info.get('totalDebt') and info.get('totalAssets') else None,
                current_ratio=info.get('currentRatio'),
                quick_ratio=info.get('quickRatio'),
                
                revenue=info.get('totalRevenue'),
                revenue_growth_yoy=info.get('revenueGrowth') * 100 if info.get('revenueGrowth') else None,
                revenue_growth_3y=info.get('revenueGrowth') * 36 if info.get('revenueGrowth') else None,
                revenue_per_share=info.get('totalRevenue') / info.get('sharesOutstanding') if info.get('totalRevenue') and info.get('sharesOutstanding') else None,
                
                net_income=info.get('netIncomeToCommon'),
                profit_margin=info.get('profitMargins') * 100 if info.get('profitMargins') else None,
                operating_margin=info.get('operatingMargins') * 100 if info.get('operatingMargins') else None,
                gross_margin=info.get('grossMargins') * 100 if info.get('grossMargins') else None,
                
                roe=info.get('returnOnEquity') * 100 if info.get('returnOnEquity') else None,
                roa=info.get('returnOnAssets') * 100 if info.get('returnOnAssets') else None,
                roic=info.get('netIncome') and info.get('totalCapital') and (info.get('netIncome') / info.get('totalCapital') * 100) if info.get('netIncome') and info.get('totalCapital') else None,
                
                beta=info.get('beta'),
                market_cap=info.get('marketCap'),
                enterprise_value=info.get('enterpriseValue'),
                ev_to_revenue=info.get('enterpriseToRevenue'),
                ev_to_ebitda=info.get('enterpriseToEbitda'),
                
                shares_outstanding=info.get('sharesOutstanding'),
                institutional_ownership=info.get('heldByInsiders') and (1 - info.get('heldByInsiders')) * 100 or None,
                
                week_52_high=info.get('fiftyTwoWeekHigh'),
                week_52_low=info.get('fiftyTwoWeekLow'),
                price_to_52w_high=current_price / info.get('fiftyTwoWeekHigh') * 100 if info.get('fiftyTwoWeekHigh') else None,
                
                analyst_rating=info.get('recommendationKey', '').title(),
                target_price=info.get('targetMeanPrice'),
                upside_downside=((info.get('targetMeanPrice') - current_price) / current_price * 100) if info.get('targetMeanPrice') and current_price else None,
                
                timestamp=datetime.now()
            )
            
            return indicators
            
        except Exception as e:
            print(f"Erreur lors de l'analyse de {ticker}: {e}")
            return None
    
    def analyze_batch(self, tickers: List[str]) -> Dict[str, FinancialIndicators]:
        results = {}
        for ticker in tickers:
            indicator = self.analyze(ticker)
            if indicator:
                results[indicator.ticker] = indicator
        return results
    
    def quick_compare(self, tickers: List[str]) -> List[Dict]:
        results = []
        for ticker in tickers:
            ind = self.analyze(ticker)
            if ind:
                results.append({
                    "ticker": ind.ticker,
                    "name": ind.company_name,
                    "price": ind.current_price,
                    "pe": ind.price_to_earnings,
                    "peg": ind.peg_ratio,
                    "pb": ind.price_to_book,
                    "div_yield": ind.dividend_yield,
                    "roe": ind.roe,
                    "debt_eq": ind.debt_to_equity,
                    "rev_growth": ind.revenue_growth_yoy,
                    "score": ind.get_overall_score(),
                    "recommendation": ind.get_recommendation()
                })
        return results
