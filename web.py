"""
Stock Analyzer Web - Interface Visuelle
Flask web application pour l'analyse d'actions
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from datetime import datetime

from analyzer import StockAnalyzer
from database import AnalysisDatabase
from comparator import StockComparator
from search import CompanySearch

app = Flask(__name__)
app.config['SECRET_KEY'] = 'stock-analyzer-secret-key'

analyzer = StockAnalyzer()
db = AnalysisDatabase()
comparator = StockComparator(db)
search_engine = CompanySearch()

ETF_CATEGORIES = {
    "US Market": ["SPY", "VOO", "IVV", "VTI", "QQQ", "QQQM", "IWM", "DIA"],
    "International": ["VXUS", "IXUS", "EFA", "EEM", "VWO"],
    "Sectors": ["XLK", "XLF", "XLE", "XLV", "XLC", "XLY", "XLP", "XLB", "XLI", "XLRE", "XLU"],
    "Growth/Value": ["VUG", "VTV", "IWF", "IWD", "SCHG", "SCHD", "VYM"],
    "Bonds": ["BND", "AGG", "TLT", "IEF", "LQD", "HYG"],
    "Thematic": ["ARKK", "SOXX", "SMH", "KWEB", "FXI", "GDX", "GLD", "SLV", "USO", "UNG"],
}


@app.route('/')
def index():
    stats = db.get_statistics()
    recent = db.get_latest_analyses(limit=10)
    return render_template('index.html', stats=stats, recent=recent)


@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        ticker = request.form.get('ticker', '').strip()
        if ticker:
            result = analyzer.analyze(ticker)
            if result:
                db.save_analysis(result)
                return redirect(url_for('result', ticker=result.ticker))
            else:
                return render_template('analyze.html', error=f"Impossible d'analyser '{ticker}'")
    return render_template('analyze.html')


@app.route('/result/<ticker>')
def result(ticker):
    ind = db.get_analysis(ticker, latest=True)
    if not ind:
        ind = analyzer.analyze(ticker)
        if ind:
            db.save_analysis(ind)
    
    if ind:
        return render_template('result.html', ind=ind)
    return redirect(url_for('analyze'))


@app.route('/compare', methods=['GET', 'POST'])
def compare():
    if request.method == 'POST':
        tickers = request.form.get('tickers', '').strip()
        if tickers:
            ticker_list = [t.strip().upper() for t in tickers.split(',') if t.strip()]
            if len(ticker_list) >= 2:
                indicators = comparator.compare(ticker_list)
                table = comparator.format_comparison_table(indicators)
                scores = comparator.compare_scores(ticker_list)
                return render_template('compare.html', indicators=indicators, table=table, scores=scores, tickers=tickers)
            return render_template('compare.html', error="Entrez au moins 2 tickers séparés par des virgules")
    return render_template('compare.html')


@app.route('/library')
def library():
    stats = db.get_statistics()
    analyses = db.get_latest_analyses(limit=50)
    return render_template('library.html', stats=stats, analyses=analyses)


@app.route('/etf')
def etf():
    etfs_by_category = {}
    for category, tickers in ETF_CATEGORIES.items():
        etfs = []
        for ticker in tickers:
            info = search_engine.get_company_info(ticker)
            if info:
                etfs.append(info)
        etfs_by_category[category] = etfs
    return render_template('etf.html', etfs_by_category=etfs_by_category)


@app.route('/search')
def search():
    query = request.args.get('q', '')
    results = []
    if query:
        results = search_engine.search(query)
    sectors = search_engine.get_sectors()
    return render_template('search.html', results=results, query=query, sectors=sectors)


@app.route('/api/search')
def api_search():
    query = request.args.get('q', '')
    if query:
        ticker = search_engine.resolve(query)
        if ticker:
            return jsonify({'ticker': ticker, 'found': True})
        results = search_engine.search(query)
        return jsonify({'results': results[:5], 'found': False})
    return jsonify({'results': [], 'found': False})


@app.route('/api/analyze/<ticker>')
def api_analyze(ticker):
    ind = analyzer.analyze(ticker)
    if ind:
        db.save_analysis(ind)
        return jsonify(ind.to_dict())
    return jsonify({'error': 'Not found'}), 404


if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
