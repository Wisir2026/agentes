"""
SETUP & TEST GUIDE - Complete Integration Testing

Este guia cobre todo o processo de setup e testes dos módulos.
"""

# =============================================================================
# PARTE 1: SETUP INICIAL
# =============================================================================

"""
1. CLONE O REPOSITÓRIO
   git clone https://github.com/Wisir2026/agentes.git
   cd agentes

2. CRIE UM AMBIENTE VIRTUAL
   python -m venv venv
   
   Linux/Mac:
   source venv/bin/activate
   
   Windows:
   venv\Scripts\activate

3. INSTALE AS DEPENDÊNCIAS
   pip install -r requirements.txt
   
   Se requirements.txt não existir, instale manualmente:
   pip install openbb pandas numpy python-dotenv pytest
   pip install openai anthropic google-generativeai

4. OBTENHA AS CHAVES DE API

   a) OpenAI API Key:
      - Acesse: https://platform.openai.com/api-keys
      - Crie uma nova chave
      - Copie e guarde em local seguro
      
   b) OpenBB API Key (opcional):
      - Acesse: https://my.openbb.co
      - Crie uma conta ou faça login
      - Gere um token pessoal

5. CONFIGURE AS VARIÁVEIS DE AMBIENTE
   
   Crie um arquivo .env na raiz do projeto:
   
   touch .env  (Linux/Mac)
   type nul > .env  (Windows)
   
   Adicione o conteúdo:
"""

# .env content example
env_example = """
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-your-actual-key-here
OPENAI_ORG_ID=org-xxxxxxxxx  # opcional

# OpenBB Configuration  
OPENBB_PERSONAL_ACCESS_TOKEN=your_token_here

# Google API (opcional)
GOOGLE_API_KEY=your_google_key_here

# Anthropic API (opcional)
ANTHROPIC_API_KEY=your_anthropic_key_here

# xAI API (opcional)
XAI_API_KEY=your_xai_key_here

# Application Configuration
DEBUG=true
LOG_LEVEL=INFO
"""

# =============================================================================
# PARTE 2: TESTES UNITÁRIOS
# =============================================================================

"""
Vamos testar cada módulo individualmente
"""

# TEST 1: Verificar imports
test_imports = """
python -c "
import sys
print('Python version:', sys.version)

try:
    from openbb import obb
    print('✓ OpenBB importado com sucesso')
except ImportError as e:
    print('✗ Erro ao importar OpenBB:', e)

try:
    from tradingagents.graph.trading_graph import TradingAgentsGraph
    print('✓ TradingAgents importado com sucesso')
except ImportError as e:
    print('✗ Erro ao importar TradingAgents:', e)

try:
    from examples.data_integration_example import OpenBBDataClient
    print('✓ data_integration_example importado')
except ImportError as e:
    print('✗ Erro ao importar data_integration_example:', e)

try:
    from examples.analysis_engine_example import AnalysisEngine
    print('✓ analysis_engine_example importado')
except ImportError as e:
    print('✗ Erro ao importar analysis_engine_example:', e)
"
"""

# TEST 2: Verificar variáveis de ambiente
test_env = """
python -c "
import os
from dotenv import load_dotenv

load_dotenv()

keys_to_check = [
    'OPENAI_API_KEY',
    'OPENBB_PERSONAL_ACCESS_TOKEN'
]

for key in keys_to_check:
    value = os.getenv(key)
    if value:
        # Mostrar apenas os primeiros 10 caracteres
        masked = value[:10] + '...' if len(value) > 10 else value
        print(f'✓ {key} = {masked}')
    else:
        print(f'✗ {key} não configurado')
"
"""

# TEST 3: Teste da classe OpenBBDataClient
test_openbb_client = """
python -c "
import logging
from datetime import datetime, timedelta
from examples.data_integration_example import OpenBBDataClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Inicializar cliente
    logger.info('Inicializando OpenBBDataClient...')
    client = OpenBBDataClient()
    
    # Teste 1: Fetch histórico
    logger.info('Teste 1: Buscando dados históricos...')
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    df = client.fetch_historical_data('AAPL', start_date, end_date)
    if df.empty:
        print('✗ Nenhum dado retornado')
    else:
        print(f'✓ Dados históricos obtidos: {len(df)} registros')
        print(f'  Últimas 3 linhas:')
        print(df.tail(3))
    
    # Teste 2: Indicadores técnicos
    logger.info('Teste 2: Calculando indicadores técnicos...')
    indicators = client.fetch_technical_indicators('AAPL', length=20)
    print(f'✓ Indicadores calculados: {list(indicators.keys())}')
    
    # Teste 3: Dados fundamentais
    logger.info('Teste 3: Buscando dados fundamentais...')
    fundamentals = client.fetch_fundamental_data('AAPL')
    print(f'✓ Dados fundamentais obtidos: {list(fundamentals.keys())}')
    
except Exception as e:
    print(f'✗ Erro: {e}')
    import traceback
    traceback.print_exc()
"
"""

# TEST 4: Teste da classe AnalysisEngine
test_analysis_engine = """
python -c "
import logging
from datetime import datetime, timedelta
import pandas as pd
from examples.analysis_engine_example import AnalysisEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Inicializar engine
    logger.info('Inicializando AnalysisEngine...')
    engine = AnalysisEngine(llm_provider='openai', debug=False)
    print('✓ AnalysisEngine inicializado')
    
    # Dados de teste
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    # DataFrame simulado
    dates = pd.date_range(start_date, end_date, freq='D')
    historical_data = pd.DataFrame({
        'open': [150 + i*0.5 for i in range(len(dates))],
        'high': [152 + i*0.5 for i in range(len(dates))],
        'low': [149 + i*0.5 for i in range(len(dates))],
        'close': [151 + i*0.5 for i in range(len(dates))],
        'volume': [1000000] * len(dates)
    }, index=dates)
    
    fundamental_data = {
        'pe_ratio': 28.5,
        'roe': 25.3,
        'roa': 10.2,
        'debt_to_equity': 0.5,
        'current_ratio': 2.1
    }
    
    technical_indicators = {
        'rsi': 65.3,
        'macd': {'value': 2.5, 'signal': 2.0, 'histogram': 0.5},
        'bollinger': {'upper': 155, 'middle': 150, 'lower': 145},
        'sma_20': 151.2,
        'sma_50': 150.1,
        'ema_12': 151.5,
        'ema_26': 150.8
    }
    
    news_sentiment = {
        'sentiment_score': 0.65,
        'sentiment_distribution': {
            'positive': 12,
            'neutral': 8,
            'negative': 5
        },
        'articles': [
            {'title': 'Apple stock rises', 'sentiment': 0.8},
            {'title': 'Market volatility', 'sentiment': 0.5}
        ]
    }
    
    # Teste 1: Análise fundamental
    logger.info('Teste 1: Análise fundamental...')
    fund_analysis = engine.analyze_fundamentals('AAPL', fundamental_data)
    print(f'✓ Análise fundamental: {fund_analysis}')
    
    # Teste 2: Análise técnica
    logger.info('Teste 2: Análise técnica...')
    tech_analysis = engine.analyze_technicals('AAPL', technical_indicators)
    print(f'✓ Análise técnica: RSI={tech_analysis[\"momentum\"][\"rsi\"]}')
    
    # Teste 3: Análise de sentimento
    logger.info('Teste 3: Análise de sentimento...')
    sent_analysis = engine.analyze_sentiment('AAPL', news_sentiment)
    print(f'✓ Análise de sentimento: {sent_analysis[\"overall_sentiment\"]:.2f}')
    
except Exception as e:
    print(f'✗ Erro: {e}')
    import traceback
    traceback.print_exc()
"
"""

# =============================================================================
# PARTE 3: TESTES DE INTEGRAÇÃO
# =============================================================================

test_integration = """
python examples/complete_workflow_example.py
# Escolha: 1 (Workflow completo), 2 (Portfolio), 3 (Backtesting), ou all
"""

# =============================================================================
# PARTE 4: SCRIPT DE TESTE COMPLETO
# =============================================================================

complete_test_script = """
#!/usr/bin/env python
\"\"\"
Script de teste completo - testa todos os módulos
\"\"\"

import sys
import os
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_environment():
    \"\"\"Teste 1: Verificar variáveis de ambiente\"\"\"
    logger.info("=" * 70)
    logger.info("TESTE 1: Variáveis de Ambiente")
    logger.info("=" * 70)
    
    from dotenv import load_dotenv
    load_dotenv()
    
    required_keys = ['OPENAI_API_KEY', 'OPENBB_PERSONAL_ACCESS_TOKEN']
    
    for key in required_keys:
        value = os.getenv(key)
        if value:
            masked = value[:10] + '...' if len(value) > 10 else value
            logger.info(f"✓ {key} configurado: {masked}")
        else:
            logger.warning(f"✗ {key} não configurado")
    
    return True

def test_imports():
    \"\"\"Teste 2: Verificar importações\"\"\"
    logger.info("\\n" + "=" * 70)
    logger.info("TESTE 2: Importações")
    logger.info("=" * 70)
    
    modules = [
        ('openbb', 'OpenBB'),
        ('examples.data_integration_example', 'Data Integration'),
        ('examples.analysis_engine_example', 'Analysis Engine'),
    ]
    
    for module_name, display_name in modules:
        try:
            __import__(module_name)
            logger.info(f"✓ {display_name} importado com sucesso")
        except ImportError as e:
            logger.error(f"✗ Erro ao importar {display_name}: {e}")
            return False
    
    return True

def test_data_integration():
    \"\"\"Teste 3: Integração de dados\"\"\"
    logger.info("\\n" + "=" * 70)
    logger.info("TESTE 3: Integração de Dados (OpenBB)")
    logger.info("=" * 70)
    
    try:
        from examples.data_integration_example import OpenBBDataClient
        
        client = OpenBBDataClient()
        
        # Fetch dados
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        logger.info(f"Buscando dados para AAPL ({start_date} a {end_date})...")
        df = client.fetch_historical_data('AAPL', start_date, end_date)
        
        if df.empty:
            logger.error("✗ Nenhum dado retornado")
            return False
        
        logger.info(f"✓ Dados obtidos: {len(df)} registros")
        logger.info(f"  Preço atual: ${df['close'].iloc[-1]:.2f}")
        
        # Indicadores técnicos
        logger.info("Calculando indicadores técnicos...")
        indicators = client.fetch_technical_indicators('AAPL')
        logger.info(f"✓ Indicadores: {list(indicators.keys())}")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_analysis_engine():
    \"\"\"Teste 4: Motor de análise\"\"\"
    logger.info("\\n" + "=" * 70)
    logger.info("TESTE 4: Motor de Análise")
    logger.info("=" * 70)
    
    try:
        from examples.analysis_engine_example import AnalysisEngine
        import pandas as pd
        
        engine = AnalysisEngine(llm_provider='openai', debug=False)
        logger.info("✓ AnalysisEngine inicializado")
        
        # Dados simulados
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        dates = pd.date_range(start_date, end_date, freq='D')
        historical_data = pd.DataFrame({
            'open': [150 + i*0.5 for i in range(len(dates))],
            'high': [152 + i*0.5 for i in range(len(dates))],
            'low': [149 + i*0.5 for i in range(len(dates))],
            'close': [151 + i*0.5 for i in range(len(dates))],
            'volume': [1000000] * len(dates)
        }, index=dates)
        
        fundamental_data = {'pe_ratio': 28.5, 'roe': 25.3}
        technical_indicators = {'rsi': 65.3}
        news_sentiment = {'sentiment_score': 0.65, 'sentiment_distribution': {}, 'articles': []}
        
        # Teste análises
        fund = engine.analyze_fundamentals('AAPL', fundamental_data)
        logger.info(f"✓ Análise fundamental: valuation={fund['valuation']['score']:.2f}")
        
        tech = engine.analyze_technicals('AAPL', technical_indicators)
        logger.info(f"✓ Análise técnica: momentum={tech['momentum']['score']:.2f}")
        
        sent = engine.analyze_sentiment('AAPL', news_sentiment)
        logger.info(f"✓ Análise de sentimento: {sent['overall_sentiment']:.2f}")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    \"\"\"Executar todos os testes\"\"\"
    logger.info("\\n")
    logger.info("🚀 " * 20)
    logger.info("INICIANDO TESTES DO TRADING AGENTS")
    logger.info("🚀 " * 20)
    
    tests = [
        ("Ambiente", test_environment),
        ("Importações", test_imports),
        ("Integração de Dados", test_data_integration),
        ("Motor de Análise", test_analysis_engine),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"Erro ao executar {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumo
    logger.info("\\n" + "=" * 70)
    logger.info("RESUMO DOS TESTES")
    logger.info("=" * 70)
    
    for test_name, result in results:
        status = "✓ PASSOU" if result else "✗ FALHOU"
        logger.info(f"{test_name}: {status}")
    
    total_passed = sum(1 for _, r in results if r)
    total_tests = len(results)
    
    logger.info(f"\\nTotal: {total_passed}/{total_tests} testes passaram")
    
    if total_passed == total_tests:
        logger.info("\\n✅ TODOS OS TESTES PASSARAM!")
        return 0
    else:
        logger.info(f"\\n❌ {total_tests - total_passed} teste(s) falharam")
        return 1

if __name__ == "__main__":
    sys.exit(main())
"""

print(__doc__)
print("\n" + "=" * 70)
print("GUIA DE SETUP E TESTES")
print("=" * 70)
print(env_example)
print("\n" + "=" * 70)
print("SALVANDO SCRIPT DE TESTE COMPLETO...")
print("=" * 70)

# Salvar o script de teste
with open("test_complete.py", "w") as f:
    f.write(complete_test_script)

print("✓ Script salvo em: test_complete.py")
print("\nPara executar os testes:")
print("  python test_complete.py")
