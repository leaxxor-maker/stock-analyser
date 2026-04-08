"""
Module de comparaison d'actions
Permet de comparer plusieurs actions côte à côte
"""

from typing import List, Dict, Optional
from tabulate import tabulate

from analyzer import StockAnalyzer
from indicators import FinancialIndicators
from database import AnalysisDatabase


class StockComparator:
    def __init__(self, db: AnalysisDatabase = None):
        self.analyzer = StockAnalyzer()
        self.db = db or AnalysisDatabase()
    
    def compare(self, tickers: List[str], use_cache: bool = True) -> List[FinancialIndicators]:
        indicators_list = []
        
        for ticker in tickers:
            if use_cache:
                cached = self.db.get_analysis(ticker, latest=True)
                if cached:
                    indicators_list.append(cached)
                    continue
            
            ind = self.analyzer.analyze(ticker)
            if ind:
                indicators_list.append(ind)
                if use_cache:
                    self.db.save_analysis(ind)
        
        return indicators_list
    
    def format_comparison_table(self, indicators_list: List[FinancialIndicators]) -> str:
        if not indicators_list:
            return "Aucune donnée à afficher"
        
        headers = ["Indicateur"] + [ind.ticker for ind in indicators_list]
        rows = []
        
        def format_val(val, fmt="float"):
            if val is None:
                return "N/A"
            if fmt == "pct":
                return f"{val:.2f}%"
            elif fmt == "currency":
                if abs(val) >= 1e12:
                    return f"${val/1e12:.2f}T"
                elif abs(val) >= 1e9:
                    return f"${val/1e9:.2f}B"
                elif abs(val) >= 1e6:
                    return f"${val/1e6:.2f}M"
                else:
                    return f"${val:.2f}"
            elif fmt == "ratio":
                return f"{val:.2f}x"
            else:
                if abs(val) >= 1e9:
                    return f"{val/1e9:.2f}B"
                elif abs(val) >= 1e6:
                    return f"{val/1e6:.2f}M"
                else:
                    return f"{val:.2f}"
        
        rows.append(["Prix", *[f"${ind.current_price:.2f}" for ind in indicators_list]])
        rows.append(["Capitalisation", *[format_val(ind.market_cap, "currency") for ind in indicators_list]])
        rows.append(["", [""]])
        
        rows.append(["--- Valorisation ---", *["" for _ in indicators_list]])
        rows.append(["P/E", *[format_val(ind.price_to_earnings, "ratio") for ind in indicators_list]])
        rows.append(["PEG", *[format_val(ind.peg_ratio, "ratio") for ind in indicators_list]])
        rows.append(["P/B", *[format_val(ind.price_to_book, "ratio") for ind in indicators_list]])
        rows.append(["EV/Revenue", *[format_val(ind.ev_to_revenue, "ratio") for ind in indicators_list]])
        rows.append(["EV/EBITDA", *[format_val(ind.ev_to_ebitda, "ratio") for ind in indicators_list]])
        rows.append(["Prix/52w High", *[f"{format_val(ind.price_to_52w_high, 'pct')}" for ind in indicators_list]])
        rows.append(["", [""]])
        
        rows.append(["--- Rentabilité ---", *["" for _ in indicators_list]])
        rows.append(["Marge Brute", *[format_val(ind.gross_margin, "pct") for ind in indicators_list]])
        rows.append(["Marge Opérationnelle", *[format_val(ind.operating_margin, "pct") for ind in indicators_list]])
        rows.append(["Marge Nette", *[format_val(ind.profit_margin, "pct") for ind in indicators_list]])
        rows.append(["ROE", *[format_val(ind.roe, "pct") for ind in indicators_list]])
        rows.append(["ROA", *[format_val(ind.roa, "pct") for ind in indicators_list]])
        rows.append(["ROIC", *[format_val(ind.roic, "pct") for ind in indicators_list]])
        rows.append(["", [""]])
        
        rows.append(["--- Croissance ---", *["" for _ in indicators_list]])
        rows.append(["Croissance CA (YoY)", *[format_val(ind.revenue_growth_yoy, "pct") for ind in indicators_list]])
        rows.append(["Croissance CA (3Y)", *[format_val(ind.revenue_growth_3y, "pct") for ind in indicators_list]])
        rows.append(["", [""]])
        
        rows.append(["--- Endettement ---", *["" for _ in indicators_list]])
        rows.append(["Dette Totale", *[format_val(ind.total_debt, "currency") for ind in indicators_list]])
        rows.append(["Dette/Equity", *[format_val(ind.debt_to_equity, "ratio") for ind in indicators_list]])
        rows.append(["Dette/Actifs", *[format_val(ind.debt_to_assets, "pct") for ind in indicators_list]])
        rows.append(["Current Ratio", *[format_val(ind.current_ratio, "ratio") for ind in indicators_list]])
        rows.append(["Quick Ratio", *[format_val(ind.quick_ratio, "ratio") for ind in indicators_list]])
        rows.append(["", [""]])
        
        rows.append(["--- Cash Flow ---", *["" for _ in indicators_list]])
        rows.append(["FCF", *[format_val(ind.free_cash_flow, "currency") for ind in indicators_list]])
        rows.append(["FCF/Action", *[format_val(ind.fcf_per_share, "float") for ind in indicators_list]])
        rows.append(["OCF", *[format_val(ind.operating_cash_flow, "currency") for ind in indicators_list]])
        rows.append(["", [""]])
        
        rows.append(["--- Dividendes ---", *["" for _ in indicators_list]])
        rows.append(["Rendement", *[format_val(ind.dividend_yield * 100 if ind.dividend_yield else None, "pct") for ind in indicators_list]])
        rows.append(["Payout Ratio", *[format_val(ind.payout_ratio * 100 if ind.payout_ratio else None, "pct") for ind in indicators_list]])
        rows.append(["", [""]])
        
        rows.append(["--- Risque ---", *["" for _ in indicators_list]])
        rows.append(["Bêta", *[format_val(ind.beta, "float") for ind in indicators_list]])
        rows.append(["52w High", *[f"${ind.week_52_high:.2f}" if ind.week_52_high else "N/A" for ind in indicators_list]])
        rows.append(["52w Low", *[f"${ind.week_52_low:.2f}" if ind.week_52_low else "N/A" for ind in indicators_list]])
        rows.append(["", [""]])
        
        rows.append(["--- Score Global ---", *["" for _ in indicators_list]])
        rows.append(["Score", *[f"{ind.get_overall_score():.1f}/100" for ind in indicators_list]])
        rows.append(["Recommandation", *[ind.get_recommendation() for ind in indicators_list]])
        rows.append(["Upside/Downside", *[f"{ind.upside_downside:.1f}%" if ind.upside_downside else "N/A" for ind in indicators_list]])
        rows.append(["Rating Analystes", *[ind.analyst_rating or "N/A" for ind in indicators_list]])
        
        clean_rows = []
        for row in rows:
            if row[0] != "" or not all(v == "" for v in row[1:]):
                if row[0] == "":
                    clean_rows.append(["", *[v if v else "" for v in row[1:]]])
                else:
                    clean_rows.append(row)
        
        return tabulate(clean_rows, headers=headers, tablefmt="grid")
    
    def compare_scores(self, tickers: List[str]) -> Dict[str, float]:
        indicators_list = self.compare(tickers)
        return {
            ind.ticker: {
                "score": ind.get_overall_score(),
                "valuation": ind.get_valuation_score(),
                "solvency": ind.get_solvency_score(),
                "profitability": ind.get_profitability_score(),
                "growth": ind.get_growth_score(),
                "cash_flow": ind.get_cash_flow_score()
            }
            for ind in indicators_list
        }
    
    def rank_by_metric(self, tickers: List[str], metric: str) -> List[Dict]:
        indicators_list = self.compare(tickers)
        
        if metric == "pe":
            sorted_inds = sorted([i for i in indicators_list if i.price_to_earnings], 
                                key=lambda x: x.price_to_earnings)
        elif metric == "peg":
            sorted_inds = sorted([i for i in indicators_list if i.peg_ratio], 
                                key=lambda x: x.peg_ratio)
        elif metric == "pb":
            sorted_inds = sorted([i for i in indicators_list if i.price_to_book], 
                                key=lambda x: x.price_to_book)
        elif metric == "roe":
            sorted_inds = sorted([i for i in indicators_list if i.roe], 
                                key=lambda x: x.roe, reverse=True)
        elif metric == "growth":
            sorted_inds = sorted([i for i in indicators_list if i.revenue_growth_yoy], 
                                key=lambda x: x.revenue_growth_yoy, reverse=True)
        elif metric == "score":
            sorted_inds = sorted(indicators_list, 
                                key=lambda x: x.get_overall_score(), reverse=True)
        elif metric == "debt":
            sorted_inds = sorted([i for i in indicators_list if i.debt_to_equity], 
                                key=lambda x: x.debt_to_equity)
        elif metric == "fcf":
            sorted_inds = sorted([i for i in indicators_list if i.free_cash_flow], 
                                key=lambda x: x.free_cash_flow, reverse=True)
        else:
            sorted_inds = indicators_list
        
        return [
            {
                "rank": i + 1,
                "ticker": ind.ticker,
                "name": ind.company_name,
                "value": getattr(ind, f"price_to_earnings" if metric == "pe" else f"peg_ratio" if metric == "peg" else f"price_to_book" if metric == "pb" else f"roe" if metric == "roe" else f"revenue_growth_yoy" if metric == "growth" else f"get_overall_score" if metric == "score" else f"debt_to_equity" if metric == "debt" else f"free_cash_flow" if metric == "fcf" else None, None)
            }
            for i, ind in enumerate(sorted_inds)
        ]
