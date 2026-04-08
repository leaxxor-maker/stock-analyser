"""
Interface CLI interactive pour l'analyse d'actions
"""

import sys
import os
from typing import Optional, List
from datetime import datetime

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

from analyzer import StockAnalyzer
from database import AnalysisDatabase
from comparator import StockComparator
from search import CompanySearch


class CLI:
    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.analyzer = StockAnalyzer()
        self.db = AnalysisDatabase()
        self.comparator = StockComparator(self.db)
        self.search = CompanySearch()
    
    def print(self, *args, **kwargs):
        if self.console:
            self.console.print(*args, **kwargs)
        else:
            print(*args, **kwargs)
    
    def print_header(self, text: str):
        if self.console:
            self.console.print(Panel(f"[bold cyan]{text}[/bold cyan]", box=box.ROUNDED))
        else:
            print(f"\n{'='*60}\n{text}\n{'='*60}")
    
    def print_success(self, text: str):
        if self.console:
            self.console.print(f"[green]✓[/green] {text}")
        else:
            print(f"✓ {text}")
    
    def print_error(self, text: str):
        if self.console:
            self.console.print(f"[red]✗[/red] {text}")
        else:
            print(f"✗ {text}")
    
    def print_warning(self, text: str):
        if self.console:
            self.console.print(f"[yellow]![/yellow] {text}")
        else:
            print(f"! {text}")
    
    def analyze_command(self, ticker: str, save: bool = True):
        self.print(f"\n📊 Analyse de {ticker} en cours...")
        
        indicator = self.analyzer.analyze(ticker)
        if not indicator:
            self.print_error(f"Impossible d'analyser {ticker}")
            return
        
        if save:
            self.db.save_analysis(indicator)
            self.db.save_company(indicator.ticker, indicator.company_name)
            self.print_success(f"Analyse sauvegardée pour {indicator.ticker}")
        
        self._display_analysis(indicator)
    
    def _display_analysis(self, ind):
        if self.console:
            self._display_analysis_rich(ind)
        else:
            self._display_analysis_plain(ind)
    
    def _display_analysis_rich(self, ind):
        score = ind.get_overall_score()
        recommendation = ind.get_recommendation()
        
        score_color = "green" if score >= 60 else "yellow" if score >= 40 else "red"
        
        header = Panel(
            f"[bold]{ind.company_name}[/bold] ({ind.ticker})\n"
            f"Prix: [green]${ind.current_price:.2f}[/green]\n"
            f"Capitalisation: {ind.format_currency(ind.market_cap)}\n"
            f"Score: [{score_color}]{score:.1f}/100[/{score_color}] | {recommendation}",
            box=box.ROUNDED,
            title="Analyse Complète"
        )
        self.print(header)
        
        valuation_table = Table(title="📈 Valorisation", box=box.SIMPLE)
        valuation_table.add_column("Indicateur", style="cyan")
        valuation_table.add_column("Valeur", style="green")
        valuation_table.add_column("Interprétation", style="yellow")
        
        if ind.price_to_earnings:
            pe_val = f"{ind.price_to_earnings:.2f}x"
            pe_interp = "✓ Bon" if 10 <= ind.price_to_earnings <= 25 else "⚠ Élevé" if ind.price_to_earnings > 25 else "⚠ Faible"
        else:
            pe_val = "N/A"
            pe_interp = "⚠ Indisponible"
        
        valuation_table.add_row("P/E (Price/Earnings)", pe_val, pe_interp)
        valuation_table.add_row("PEG Ratio", ind.format_ratio(ind.peg_ratio), 
                               "✓ Bon" if ind.peg_ratio and ind.peg_ratio <= 1 else "⚠ À vérifier" if ind.peg_ratio else "⚠ Indisponible")
        valuation_table.add_row("P/B (Price/Book)", ind.format_ratio(ind.price_to_book),
                               "✓ Bon" if ind.price_to_book and ind.price_to_book <= 5 else "⚠ Élevé" if ind.price_to_book and ind.price_to_book > 5 else "⚠ Indisponible")
        valuation_table.add_row("EV/Revenue", ind.format_ratio(ind.ev_to_revenue),
                               "✓ Bon" if ind.ev_to_revenue and ind.ev_to_revenue <= 3 else "⚠ Élevé" if ind.ev_to_revenue and ind.ev_to_revenue > 3 else "⚠ Indisponible")
        valuation_table.add_row("Prix vs 52w High", ind.format_percentage(ind.price_to_52w_high),
                               "✓ Proche du high" if ind.price_to_52w_high and ind.price_to_52w_high >= 90 else "⚠ En baisse")
        valuation_table.add_row("Target Price", f"${ind.target_price:.2f}" if ind.target_price else "N/A",
                               f"{ind.format_percentage(ind.upside_downside)} upside" if ind.upside_downside else "⚠ Indisponible")
        self.print(valuation_table)
        
        profitability_table = Table(title="💰 Rentabilité", box=box.SIMPLE)
        profitability_table.add_column("Indicateur", style="cyan")
        profitability_table.add_column("Valeur", style="green")
        profitability_table.add_column("Benchmark", style="yellow")
        
        profitability_table.add_row("Marge Brute", ind.format_percentage(ind.gross_margin), "≥ 40% est excellent")
        profitability_table.add_row("Marge Opérationnelle", ind.format_percentage(ind.operating_margin), "≥ 20% est excellent")
        profitability_table.add_row("Marge Nette", ind.format_percentage(ind.profit_margin), "≥ 15% est excellent")
        profitability_table.add_row("ROE", ind.format_percentage(ind.roe), "≥ 15% est excellent")
        profitability_table.add_row("ROA", ind.format_percentage(ind.roa), "≥ 5% est acceptable")
        profitability_table.add_row("EPS", f"${ind.earnings_per_share:.2f}" if ind.earnings_per_share else "N/A", "")
        self.print(profitability_table)
        
        growth_table = Table(title="📊 Croissance", box=box.SIMPLE)
        growth_table.add_column("Indicateur", style="cyan")
        growth_table.add_column("Valeur", style="green")
        growth_table.add_column("Benchmark", style="yellow")
        
        growth_table.add_row("Croissance CA (YoY)", ind.format_percentage(ind.revenue_growth_yoy), "≥ 10% est excellent")
        growth_table.add_row("Croissance CA (3Y annualized)", ind.format_percentage(ind.revenue_growth_3y), "≥ 15% est excellent")
        growth_table.add_row("CA Total", ind.format_currency(ind.revenue), "")
        self.print(growth_table)
        
        debt_table = Table(title="🏦 Endettement", box=box.SIMPLE)
        debt_table.add_column("Indicateur", style="cyan")
        debt_table.add_column("Valeur", style="green")
        debt_table.add_column("Interprétation", style="yellow")
        
        if ind.debt_to_equity:
            debt_interp = "✓ Faible" if ind.debt_to_equity < 0.5 else "✓ Modéré" if ind.debt_to_equity < 1 else "⚠ Élevé" if ind.debt_to_equity < 2 else "❌ Très élevé"
        else:
            debt_interp = "⚠ Indisponible"
        
        debt_table.add_row("Dette/Equity", ind.format_ratio(ind.debt_to_equity), debt_interp)
        debt_table.add_row("Dette Totale", ind.format_currency(ind.total_debt), "")
        debt_table.add_row("Dette/Actifs", ind.format_percentage(ind.debt_to_assets), "✓ < 50% recommandé")
        debt_table.add_row("Current Ratio", ind.format_ratio(ind.current_ratio), "✓ ≥ 1.5 recommandé")
        debt_table.add_row("Quick Ratio", ind.format_ratio(ind.quick_ratio), "✓ ≥ 1 recommandé")
        self.print(debt_table)
        
        cashflow_table = Table(title="💵 Cash Flow", box=box.SIMPLE)
        cashflow_table.add_column("Indicateur", style="cyan")
        cashflow_table.add_column("Valeur", style="green")
        cashflow_table.add_column("Interprétation", style="yellow")
        
        fcf_interp = "✓ Positif" if ind.free_cash_flow and ind.free_cash_flow > 0 else "⚠ Négatif"
        cashflow_table.add_row("Free Cash Flow", ind.format_currency(ind.free_cash_flow), fcf_interp)
        cashflow_table.add_row("FCF/Action", f"${ind.fcf_per_share:.2f}" if ind.fcf_per_share else "N/A", "✓ FCF ≥ EPS recommandé")
        cashflow_table.add_row("Operating CF", ind.format_currency(ind.operating_cash_flow), "")
        self.print(cashflow_table)
        
        risk_table = Table(title="⚠️ Risque", box=box.SIMPLE)
        risk_table.add_column("Indicateur", style="cyan")
        risk_table.add_column("Valeur", style="green")
        risk_table.add_column("Interprétation", style="yellow")
        
        if ind.beta:
            beta_interp = "✓ Défensif" if ind.beta < 0.8 else "⚠ Neutre" if ind.beta < 1.2 else "⚠ Agressif"
        else:
            beta_interp = "⚠ Indisponible"
        
        risk_table.add_row("Bêta", f"{ind.beta:.2f}" if ind.beta else "N/A", beta_interp)
        risk_table.add_row("52w High", f"${ind.week_52_high:.2f}" if ind.week_52_high else "N/A", "")
        risk_table.add_row("52w Low", f"${ind.week_52_low:.2f}" if ind.week_52_low else "N/A", "")
        risk_table.add_row("Rating Analystes", ind.analyst_rating or "N/A", "")
        self.print(risk_table)
        
        dividend_table = Table(title="💰 Dividendes", box=box.SIMPLE)
        dividend_table.add_column("Indicateur", style="cyan")
        dividend_table.add_column("Valeur", style="green")
        dividend_table.add_column("Benchmark", style="yellow")
        
        div_yield = ind.dividend_yield * 100 if ind.dividend_yield else None
        dividend_table.add_row("Rendement", ind.format_percentage(div_yield), "≥ 2% est intéressant")
        dividend_table.add_row("Payout Ratio", ind.format_percentage(ind.payout_ratio), "≤ 60% est durable")
        self.print(dividend_table)
        
        score_breakdown = Panel(
            f"Valorisation: [cyan]{ind.get_valuation_score():.1f}/100[cyan]\n"
            f"Solvabilité: [cyan]{ind.get_solvency_score():.1f}/100[cyan]\n"
            f"Profitabilité: [cyan]{ind.get_profitability_score():.1f}/100[cyan]\n"
            f"Croissance: [cyan]{ind.get_growth_score():.1f}/100[cyan]\n"
            f"Cash Flow: [cyan]{ind.get_cash_flow_score():.1f}/100[cyan]",
            title="📊 Détails du Score"
        )
        self.print(score_breakdown)
        
        self.print(f"\n⏰ Analyse du {ind.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def _display_analysis_plain(self, ind):
        print(f"\n{'='*70}")
        print(f"ANALYSE DE {ind.ticker} - {ind.company_name}")
        print(f"{'='*70}")
        print(f"\nPrix: ${ind.current_price:.2f}")
        print(f"Capitalisation: {ind.format_currency(ind.market_cap)}")
        print(f"Score Global: {ind.get_overall_score():.1f}/100")
        print(f"Recommandation: {ind.get_recommendation()}")
        
        print(f"\n--- VALORISATION ---")
        print(f"P/E: {ind.format_ratio(ind.price_to_earnings)}")
        print(f"PEG: {ind.format_ratio(ind.peg_ratio)}")
        print(f"P/B: {ind.format_ratio(ind.price_to_book)}")
        print(f"EV/Revenue: {ind.format_ratio(ind.ev_to_revenue)}")
        print(f"EV/EBITDA: {ind.format_ratio(ind.ev_to_ebitda)}")
        
        print(f"\n--- RENTABILITÉ ---")
        print(f"Marge Nette: {ind.format_percentage(ind.profit_margin)}")
        print(f"ROE: {ind.format_percentage(ind.roe)}")
        print(f"ROA: {ind.format_percentage(ind.roa)}")
        print(f"EPS: ${ind.earnings_per_share:.2f}" if ind.earnings_per_share else "EPS: N/A")
        
        print(f"\n--- CROISSANCE ---")
        print(f"Croissance CA (YoY): {ind.format_percentage(ind.revenue_growth_yoy)}")
        print(f"CA Total: {ind.format_currency(ind.revenue)}")
        
        print(f"\n--- ENDETTEMENT ---")
        print(f"Dette/Equity: {ind.format_ratio(ind.debt_to_equity)}")
        print(f"Current Ratio: {ind.format_ratio(ind.current_ratio)}")
        print(f"Quick Ratio: {ind.format_ratio(ind.quick_ratio)}")
        
        print(f"\n--- CASH FLOW ---")
        print(f"FCF: {ind.format_currency(ind.free_cash_flow)}")
        print(f"FCF/Action: ${ind.fcf_per_share:.2f}" if ind.fcf_per_share else "FCF/Action: N/A")
        
        print(f"\n--- RISQUE ---")
        print(f"Bêta: {ind.beta:.2f}" if ind.beta else "Bêta: N/A")
        print(f"52w High: ${ind.week_52_high:.2f}" if ind.week_52_high else "52w High: N/A")
        print(f"52w Low: ${ind.week_52_low:.2f}" if ind.week_52_low else "52w Low: N/A")
        print(f"Rating Analystes: {ind.analyst_rating or 'N/A'}")
        
        print(f"\n--- DIVIDENDES ---")
        div_yield = ind.dividend_yield * 100 if ind.dividend_yield else None
        print(f"Rendement: {ind.format_percentage(div_yield)}")
        print(f"Payout Ratio: {ind.format_percentage(ind.payout_ratio)}")
        
        print(f"\n{'='*70}")
        print(f"Analyse du {ind.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def compare_command(self, tickers: List[str]):
        if len(tickers) < 2:
            self.print_error("Veuillez fournir au moins 2 tickers à comparer")
            return
        
        self.print(f"\n🔄 Comparaison de {', '.join(tickers)} en cours...")
        
        indicators_list = self.comparator.compare(tickers)
        if not indicators_list:
            self.print_error("Impossible de récupérer les données")
            return
        
        for ind in indicators_list:
            self.db.save_analysis(ind)
        
        table = self.comparator.format_comparison_table(indicators_list)
        self.print(Panel(table, title="📊 Tableau Comparatif", box=box.ROUNDED))
    
    def library_command(self, show_all: bool = False):
        stats = self.db.get_statistics()
        
        self.print_header("📚 Bibliothèque d'Analyses")
        self.print(f"Entreprises analysées: {stats['total_companies']}")
        self.print(f"Total des analyses: {stats['total_analyses']}")
        
        if stats.get('recommendations'):
            self.print("\nRépartition des recommandations:")
            for rec, count in stats['recommendations'].items():
                self.print(f"  {rec}: {count}")
        
        analyses = self.db.get_latest_analyses(limit=20)
        
        if analyses:
            table = Table(title="Dernières Analyses", box=box.SIMPLE)
            table.add_column("Ticker", style="cyan")
            table.add_column("Entreprise", style="white")
            table.add_column("Prix", style="green")
            table.add_column("P/E", style="yellow")
            table.add_column("Score", style="magenta")
            table.add_column("Recommandation", style="white")
            table.add_column("Date", style="dim")
            
            for ind in analyses:
                score = ind.get_overall_score()
                score_color = "green" if score >= 60 else "yellow" if score >= 40 else "red"
                table.add_row(
                    ind.ticker,
                    ind.company_name[:30],
                    f"${ind.current_price:.2f}",
                    ind.format_ratio(ind.price_to_earnings),
                    f"[{score_color}]{score:.1f}[/{score_color}]",
                    ind.get_recommendation(),
                    ind.timestamp.strftime('%Y-%m-%d')
                )
            
            self.print(table)
        else:
            self.print_warning("Aucune analyse en bibliothèque. Lancez une analyse d'abord!")
    
    def search_command(self, query: str):
        results = self.search.search(query)
        
        if not results:
            self.print_warning(f"Aucun résultat pour '{query}'")
            return
        
        table = Table(title=f"Résultats pour '{query}'", box=box.SIMPLE)
        table.add_column("Ticker", style="cyan")
        table.add_column("Entreprise", style="white")
        table.add_column("Secteur", style="yellow")
        table.add_column("Industrie", style="dim")
        
        for r in results:
            table.add_row(r['ticker'], r['name'], r.get('sector', 'N/A'), r.get('industry', 'N/A'))
        
        self.print(table)
    
    def sectors_command(self):
        sectors = self.search.get_sectors()
        
        table = Table(title="Secteurs Disponibles", box=box.SIMPLE)
        table.add_column("#", style="dim")
        table.add_column("Secteur", style="cyan")
        table.add_column("Entreprises", style="green")
        
        for i, sector in enumerate(sectors, 1):
            companies = self.search.get_by_sector(sector)
            table.add_row(str(i), sector, str(len(companies)))
        
        self.print(table)
    
    def help_command(self):
        help_text = """
╔══════════════════════════════════════════════════════════════════════╗
║                    STOCK ANALYZER - GUIDE D'UTILISATION               ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  COMMANDES PRINCIPALES:                                                ║
║                                                                        ║
║  analyze <ticker>     Analyser une action (ex: analyze MSFT)         ║
║                       Accepte: MSFT, microsoft, Apple, etc.           ║
║                                                                        ║
║  compare <t1> <t2>... Comparer plusieurs actions (ex: compare AAPL MSFT)║
║                                                                        ║
║  library              Afficher la bibliothèque d'analyses            ║
║                                                                        ║
║  search <query>       Rechercher une entreprise par nom              ║
║                                                                        ║
║  sectors              Lister tous les secteurs disponibles           ║
║                                                                        ║
║  help                 Afficher cette aide                            ║
║  exit / quit          Quitter                                         ║
║                                                                        ║
╠══════════════════════════════════════════════════════════════════════╣
║  INDICATEURS UTILISÉS:                                                 ║
║                                                                        ║
║  VALORISATION:    P/E, PEG, P/B, EV/Revenue, EV/EBITDA, Prix/52w High ║
║  RENTABILITÉ:     Marges (Brute, Op, Nette), ROE, ROA, EPS           ║
║  CROISSANCE:      Croissance CA YoY, 3Y, CA/Action                   ║
║  ENDETTEMENT:     Dette/Equity, Dette/Actifs, Current/Quick Ratio     ║
║  CASH FLOW:       FCF, FCF/Action, OCF                                ║
║  RISQUE:          Bêta, 52w High/Low, Rating Analystes               ║
║  DIVIDENDES:      Rendement, Payout Ratio                             ║
║                                                                        ║
╠══════════════════════════════════════════════════════════════════════╣
║  EXEMPLES:                                                             ║
║                                                                        ║
║  > analyze microsoft                                                   ║
║  > analyze AAPL                                                        ║
║  > compare MSFT GOOGL NVDA                                             ║
║  > search apple                                                         ║
║  > library                                                             ║
║                                                                        ║
╚══════════════════════════════════════════════════════════════════════╝
        """
        self.print(help_text)
    
    def run_interactive(self):
        self.print("[bold cyan]🏛️  STOCK ANALYZER - Analyse d'Actions[/bold cyan]")
        self.print("[dim]Tapez 'help' pour la liste des commandes[/dim]\n")
        
        while True:
            try:
                user_input = input("stock-analyzer> ").strip()
                
                if not user_input:
                    continue
                
                parts = user_input.split()
                command = parts[0].lower()
                args = parts[1:]
                
                if command in ['exit', 'quit', 'q']:
                    self.print("Au revoir! 👋")
                    break
                
                elif command == 'help':
                    self.help_command()
                
                elif command == 'analyze':
                    if not args:
                        self.print_error("Usage: analyze <ticker>")
                    else:
                        self.analyze_command(' '.join(args))
                
                elif command == 'compare':
                    if len(args) < 2:
                        self.print_error("Usage: compare <ticker1> <ticker2> ...")
                    else:
                        self.compare_command(args)
                
                elif command == 'library':
                    self.library_command()
                
                elif command == 'search':
                    if not args:
                        self.print_error("Usage: search <nom>")
                    else:
                        self.search_command(' '.join(args))
                
                elif command == 'sectors':
                    self.sectors_command()
                
                else:
                    ticker = self.search.resolve(command)
                    if ticker:
                        self.analyze_command(command)
                    else:
                        self.print_error(f"Commande '{command}' non reconnue. Tapez 'help'.")
                
            except KeyboardInterrupt:
                self.print("\n\nAu revoir! 👋")
                break
            except Exception as e:
                self.print_error(f"Erreur: {e}")


def main():
    cli = CLI()
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        args = sys.argv[2:]
        
        if command == 'analyze' and args:
            cli.analyze_command(' '.join(args))
        elif command == 'compare' and len(args) >= 2:
            cli.compare_command(args)
        elif command == 'library':
            cli.library_command()
        elif command == 'search' and args:
            cli.search_command(' '.join(args))
        elif command == 'sectors':
            cli.sectors_command()
        elif command == 'help':
            cli.help_command()
        else:
            cli.help_command()
    else:
        cli.run_interactive()


if __name__ == "__main__":
    main()
