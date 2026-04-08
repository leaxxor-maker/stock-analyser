from setuptools import setup, find_packages

setup(
    name="stock-analyzer",
    version="1.0.0",
    description="Application complete d'analyse d'actions avec indicateurs financiers",
    author="Stock Analyzer AI",
    packages=find_packages(),
    install_requires=[
        "yfinance>=0.2.28",
        "rich>=13.7.0",
        "tabulate>=0.9.0",
    ],
    entry_points={
        'console_scripts': [
            'stock-analyzer=stock_analyzer.cli:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
)
