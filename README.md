# Stock Analyzer - Analyse d'Actions Professionnelle

Application d'analyse d'actions avec indicateurs financiers complets, bibliothèque d'analyses et comparateur.

## Installation

```bash
pip install -e .
```

Ou directement:

```bash
pip install yfinance rich tabulate
python -m stock_analyzer.cli
```

## Utilisation

### Mode Interactif

```bash
stock-analyzer
# ou
python -m stock_analyzer.cli
```

### Mode Commande

```bash
# Analyser une action
stock-analyzer analyze MSFT
stock-analyzer analyze microsoft
stock-analyzer analyze Apple

# Comparer plusieurs actions
stock-analyzer compare MSFT GOOGL NVDA

# Afficher la bibliothèque
stock-analyzer library

# Rechercher une entreprise
stock-analyzer search apple
```

## Fonctionnalités

### Indicateurs Financiers Complets

- **Valorisation**: P/E, PEG, P/B, EV/Revenue, EV/EBITDA, Prix/52w High
- **Rentabilité**: Marges (Brute, Opérationnelle, Nette), ROE, ROA, ROIC, EPS
- **Croissance**: Croissance CA YoY, 3Y annualized, CA/Action
- **Endettement**: Dette/Equity, Dette/Actifs, Current Ratio, Quick Ratio
- **Cash Flow**: FCF, FCF/Action, OCF
- **Risque**: Bêta, 52w High/Low, Rating Analystes, Target Price
- **Dividendes**: Rendement, Payout Ratio

### Bibliothèque d'Analyses

- Sauvegarde automatique de toutes les analyses
- Consultation rapide des analyses précédentes
- Statistiques globales

### Comparateur

- Comparez plusieurs actions côte à côte
- Tableaux comparatifs détaillés

### Recherche d'Entreprises

- Recherche par nom (microsoft, apple, etc.)
- Recherche par ticker (MSFT, AAPL, etc.)
- Base de données de 100+ entreprises majeures

## Entreprises Supportées

L'application inclut une base de données complète incluant:

- **Tech**: Microsoft, Apple, Google, Meta, Amazon, NVIDIA, Tesla, etc.
- **Finance**: JPMorgan, Goldman Sachs, Morgan Stanley, Visa, Mastercard, etc.
- **Healthcare**: UnitedHealth, Eli Lilly, Johnson & Johnson, Pfizer, etc.
- **Energy**: Exxon, Chevron, NextEra Energy, etc.
- **Consumer**: Walmart, Coca-Cola, PepsiCo, McDonald's, Nike, etc.
- **Et beaucoup plus...**

## Structure du Projet

```
stock_analyzer/
├── __init__.py          # Point d'entrée du package
├── analyzer.py         # Module principal d'analyse
├── cli.py              # Interface CLI interactive
├── comparator.py       # Module de comparaison
├── database.py         # Base de données SQLite
├── indicators.py       # Classe des indicateurs financiers
├── search.py           # Recherche d'entreprises
├── requirements.txt    # Dépendances
├── setup.py            # Configuration installation
└── README.md           # Ce fichier
```

## Exemples d'Utilisation

```python
from stock_analyzer import StockAnalyzer, AnalysisDatabase

# Analyser une action
analyzer = StockAnalyzer()
indicators = analyzer.analyze("MSFT")

print(f"Score: {indicators.get_overall_score()}")
print(f"Recommandation: {indicators.get_recommendation()}")

# Sauvegarder l'analyse
db = AnalysisDatabase()
db.save_analysis(indicators)

# Récupérer une analyse précédente
cached = db.get_analysis("MSFT")

# Comparer des actions
from stock_analyzer import StockComparator
comparator = StockComparator()
results = comparator.compare(["MSFT", "AAPL", "GOOGL"])
```

## Score Global

Le score global est calculé à partir de 5 composantes:

- **Valorisation (25%)**: P/E, PEG, P/B, EV/Revenue
- **Solvabilité (20%)**: Dette/Equity, Current/Quick Ratio
- **Profitabilité (25%)**: Marges, ROE, ROA
- **Croissance (15%)**: Croissance CA YoY, 3Y
- **Cash Flow (15%)**: FCF, FCF/Action

## Licence

MIT License
