"""
Module de base de données pour stocker et récupérer les analyses d'actions
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Optional, Dict
from pathlib import Path

from indicators import FinancialIndicators


class AnalysisDatabase:
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = Path.home() / ".stock_analyzer" / "analyses.db"
            db_path.parent.mkdir(parents=True, exist_ok=True)
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS analyses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticker TEXT NOT NULL,
                    company_name TEXT,
                    analysis_data TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    score REAL,
                    recommendation TEXT,
                    UNIQUE(ticker, timestamp)
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS companies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticker TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    sector TEXT,
                    industry TEXT,
                    last_updated TEXT
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS comparisons (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    comparison_name TEXT,
                    tickers TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_ticker ON analyses(ticker)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp ON analyses(timestamp)
            """)
    
    def save_analysis(self, indicators: FinancialIndicators) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO analyses (ticker, company_name, analysis_data, timestamp, score, recommendation)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                indicators.ticker.upper(),
                indicators.company_name,
                json.dumps(indicators.to_dict()),
                indicators.timestamp.isoformat(),
                indicators.get_overall_score(),
                indicators.get_recommendation()
            ))
            return cursor.lastrowid
    
    def get_analysis(self, ticker: str, latest: bool = True) -> Optional[FinancialIndicators]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            if latest:
                cursor = conn.execute("""
                    SELECT * FROM analyses 
                    WHERE ticker = ? 
                    ORDER BY timestamp DESC 
                    LIMIT 1
                """, (ticker.upper(),))
            else:
                cursor = conn.execute("""
                    SELECT * FROM analyses 
                    WHERE ticker = ? 
                    ORDER BY timestamp ASC
                """, (ticker.upper(),))
            
            row = cursor.fetchone()
            if row:
                data = json.loads(row['analysis_data'])
                return FinancialIndicators.from_dict(data)
        return None
    
    def get_all_analyses(self, ticker: str) -> List[FinancialIndicators]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM analyses 
                WHERE ticker = ? 
                ORDER BY timestamp DESC
            """, (ticker.upper(),))
            
            analyses = []
            for row in cursor.fetchall():
                data = json.loads(row['analysis_data'])
                analyses.append(FinancialIndicators.from_dict(data))
            return analyses
    
    def get_latest_analyses(self, limit: int = 50) -> List[FinancialIndicators]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM (
                    SELECT *, MAX(timestamp) as max_ts 
                    FROM analyses 
                    GROUP BY ticker
                )
                ORDER BY max_ts DESC
                LIMIT ?
            """, (limit,))
            
            analyses = []
            for row in cursor.fetchall():
                data = json.loads(row['analysis_data'])
                analyses.append(FinancialIndicators.from_dict(data))
            return analyses
    
    def get_all_tickers(self) -> List[str]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT DISTINCT ticker FROM analyses ORDER BY ticker
            """)
            return [row[0] for row in cursor.fetchall()]
    
    def delete_analysis(self, ticker: str, keep_latest: bool = True):
        with sqlite3.connect(self.db_path) as conn:
            if keep_latest:
                conn.execute("""
                    DELETE FROM analyses 
                    WHERE ticker = ? 
                    AND id NOT IN (
                        SELECT MAX(id) FROM analyses 
                        WHERE ticker = ? 
                        GROUP BY ticker
                    )
                """, (ticker.upper(), ticker.upper()))
            else:
                conn.execute("DELETE FROM analyses WHERE ticker = ?", (ticker.upper(),))
    
    def save_company(self, ticker: str, name: str, sector: str = None, industry: str = None):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO companies (ticker, name, sector, industry, last_updated)
                VALUES (?, ?, ?, ?, ?)
            """, (ticker.upper(), name, sector, industry, datetime.now().isoformat()))
    
    def get_company(self, ticker: str) -> Optional[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM companies WHERE ticker = ?
            """, (ticker.upper(),))
            row = cursor.fetchone()
            if row:
                return dict(row)
        return None
    
    def search_companies(self, query: str) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM companies 
                WHERE UPPER(ticker) LIKE ? OR UPPER(name) LIKE ?
                ORDER BY ticker
                LIMIT 20
            """, (f"%{query.upper()}%", f"%{query.upper()}%"))
            return [dict(row) for row in cursor.fetchall()]
    
    def save_comparison(self, name: str, tickers: List[str]) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO comparisons (comparison_name, tickers, created_at)
                VALUES (?, ?, ?)
            """, (name, ",".join(tickers), datetime.now().isoformat()))
            return cursor.lastrowid
    
    def get_comparisons(self) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM comparisons ORDER BY created_at DESC
            """)
            comparisons = []
            for row in cursor.fetchall():
                comp = dict(row)
                comp['tickers'] = comp['tickers'].split(",")
                comparisons.append(comp)
            return comparisons
    
    def get_statistics(self) -> Dict:
        with sqlite3.connect(self.db_path) as conn:
            stats = {}
            
            cursor = conn.execute("SELECT COUNT(DISTINCT ticker) as count FROM analyses")
            stats['total_companies'] = cursor.fetchone()[0]
            
            cursor = conn.execute("SELECT COUNT(*) as count FROM analyses")
            stats['total_analyses'] = cursor.fetchone()[0]
            
            cursor = conn.execute("""
                SELECT recommendation, COUNT(*) as count 
                FROM (
                    SELECT ticker, recommendation, MAX(timestamp) as ts
                    FROM analyses GROUP BY ticker
                )
                GROUP BY recommendation
            """)
            stats['recommendations'] = {row[0]: row[1] for row in cursor.fetchall()}
            
            return stats
