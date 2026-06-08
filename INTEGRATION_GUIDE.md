# Guia de Integração: wisir + agentes + TradingAgents

## 📊 Visão Geral da Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                   TradingAgents (Orquestrador)          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────┐ │
│  │  wisir       │    │  agentes     │    │ Analysis │ │
│  │  (Dados)     │───▶│  (Framework) │───▶│ Engine   │ │
│  └──────────────┘    └──────────────┘    └──────────┘ │
│         ▲                                        │      │
│         │                                        │      │
│         └────────────────────────────────────────┘      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 🔗 Integração wisir (OpenBB)

```python
# 1. Instalação
pip install openbb

# 2. Uso básico
from openbb import obb

# Fetch dados históricos
historical = obb.equity.price.historical("AAPL", limit=100)
df = historical.to_dataframe()

# Fetch notícias
news = obb.news.world(query="AAPL", limit=10)

# Fetch dados fundamentais  
fundamentals = obb.equity.fundamental.balance(symbol="AAPL")
```

## 🤖 Integração agentes (TradingAgents)

```python
# 1. Instalação
git clone https://github.com/Wisir2026/agentes.git

# 2. Uso básico
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Initialize
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "openai"
ta = TradingAgentsGraph(debug=True, config=config)

# Análise
_, decision = ta.propagate("AAPL", "2026-06-08")
```

## 🎯 Implementação em TradingAgents

### Arquivo: `src/data_integration.py`

```python
from openbb import obb
import pandas as pd

class OpenBBDataClient:
    def fetch_historical_data(self, ticker: str, start_date: str, end_date: str):
        historical = obb.equity.price.historical(
            ticker,
            start_date=start_date,
            end_date=end_date
        )
        return historical.to_dataframe()
    
    def fetch_technical_indicators(self, ticker: str):
        # Implementar indicadores técnicos
        pass
    
    def fetch_fundamental_data(self, ticker: str):
        fundamentals = obb.equity.fundamental.balance(symbol=ticker)
        return fundamentals
    
    def fetch_news_sentiment(self, ticker: str, days: int = 7):
        news = obb.news.world(query=ticker, limit=100)
        return news
```

### Arquivo: `src/analysis_engine.py`

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph

class AnalysisEngine:
    def __init__(self, config=None):
        from tradingagents.default_config import DEFAULT_CONFIG
        self.config = config or DEFAULT_CONFIG.copy()
        self.ta = TradingAgentsGraph(debug=True, config=self.config)
    
    def analyze(self, ticker: str, date: str, data: dict):
        """Run TradingAgents analysis"""
        _, decision = self.ta.propagate(ticker, date)
        return decision
```

### Arquivo: `src/trading_system.py`

```python
from src.data_integration import OpenBBDataClient
from src.analysis_engine import AnalysisEngine

class TradingSystem:
    def __init__(self, config=None):
        self.config = config or {}
        self.data_client = OpenBBDataClient()
        self.analysis_engine = AnalysisEngine(config)
    
    def analyze(self, ticker: str, date: str):
        """Complete trading analysis workflow"""
        # 1. Fetch data from wisir
        historical = self.data_client.fetch_historical_data(
            ticker, 
            date, 
            date
        )
        fundamentals = self.data_client.fetch_fundamental_data(ticker)
        news = self.data_client.fetch_news_sentiment(ticker)
        
        # 2. Run TradingAgents analysis
        data = {
            "historical": historical,
            "fundamentals": fundamentals,
            "news": news
        }
        decision = self.analysis_engine.analyze(ticker, date, data)
        
        return decision
```

## 🧪 Testes

### `tests/test_integration.py`

```python
import pytest
from src.trading_system import TradingSystem

class TestIntegration:
    def test_full_workflow(self):
        system = TradingSystem()
        result = system.analyze("AAPL", "2026-06-08")
        assert result is not None
    
    def test_data_integration(self):
        from src.data_integration import OpenBBDataClient
        client = OpenBBDataClient()
        data = client.fetch_historical_data("AAPL", "2026-01-01", "2026-06-08")
        assert len(data) > 0
```

## 🔧 Configuração

### `.env`

```bash
# OpenBB
OPENBB_PERSONAL_ACCESS_TOKEN=your_token

# LLM
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key

# Trading
TRADING_PAIR=AAPL
ANALYSIS_DATE=2026-06-08
```

## 📦 Dependencies

```
requirements.txt:
openbb>=4.0.0
tradingagents[all]>=0.2.0
python-dotenv
pandas
numpy
pytest
```

## 🚀 Execução

```bash
# 1. Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Edit .env with your API keys

# 3. Run
python examples/basic_analysis.py

# 4. Tests
pytest tests/
```

## 📊 Próximos Passos

- [ ] Implementar `data_integration.py`
- [ ] Implementar `analysis_engine.py`
- [ ] Implementar `risk_manager.py`
- [ ] Criar testes de integração
- [ ] Setup CI/CD
- [ ] Criar documentação da API
- [ ] Deploy inicial

---

**Recursos:**
- [OpenBB Docs](https://docs.openbb.co)
- [TradingAgents GitHub](https://github.com/Wisir2026/agentes)
- [LangGraph Docs](https://python.langchain.com/docs/langgraph)
