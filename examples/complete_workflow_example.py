"""
complete_workflow_example.py - Complete Trading Workflow

This example demonstrates the full integration of:
1. wisir (OpenBB) - Data collection
2. agentes (TradingAgents) - AI-powered analysis
3. Risk management - Portfolio risk assessment
4. Trading decisions - Final recommendations
"""

import logging
from datetime import datetime, timedelta
import sys
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def example_complete_workflow():
    """Run complete trading workflow with all integrations"""
    logger.info("=" * 70)
    logger.info("COMPLETE TRADING WORKFLOW")
    logger.info("wisir + agentes Integration")
    logger.info("=" * 70)
    
    try:
        # Step 1: Import modules
        logger.info("\n[STEP 1] Import Required Modules")
        logger.info("-" * 70)
        
        from examples.data_integration_example import OpenBBDataClient, DataValidator
        from examples.analysis_engine_example import AnalysisEngine
        
        data_client = OpenBBDataClient()
        validator = DataValidator()
        logger.info("✓ Modules imported successfully")
        
        # Step 2: Fetch market data
        logger.info("\n[STEP 2] Fetch Market Data from OpenBB")
        logger.info("-" * 70)
        
        ticker = "AAPL"
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
        
        logger.info(f"Ticker: {ticker}")
        logger.info(f"Period: {start_date} to {end_date}")
        
        # Fetch historical data
        logger.info(f"\nFetching historical data...")
        historical_data = data_client.fetch_historical_data(
            ticker,
            start_date,
            end_date
        )
        
        if historical_data.empty:
            logger.error("No historical data retrieved")
            return
        
        logger.info(f"✓ Historical data: {len(historical_data)} records")
        logger.info(f"  Date range: {historical_data.index[0]} to {historical_data.index[-1]}")
        logger.info(f"  Price range: ${historical_data['close'].min():.2f} - ${historical_data['close'].max():.2f}")
        
        # Validate data
        if not validator.validate_historical_data(historical_data):
            logger.warning("Historical data validation issues detected")
        else:
            logger.info("✓ Historical data validation passed")
        
        # Fetch technical indicators
        logger.info(f"\nFetching technical indicators...")
        technical_indicators = data_client.fetch_technical_indicators(
            ticker,
            length=20,
            indicator_type="all"
        )
        logger.info(f"✓ Technical indicators: {', '.join(technical_indicators.keys())}")
        
        if "rsi" in technical_indicators:
            logger.info(f"  RSI: {technical_indicators['rsi']:.2f}")
        
        # Fetch fundamental data
        logger.info(f"\nFetching fundamental data...")
        fundamental_data = data_client.fetch_fundamental_data(ticker)
        logger.info(f"✓ Fundamental metrics: {', '.join(fundamental_data.keys())}")
        
        if fundamental_data:
            if "pe_ratio" in fundamental_data and fundamental_data["pe_ratio"]:
                logger.info(f"  P/E Ratio: {fundamental_data['pe_ratio']:.2f}")
            if "roe" in fundamental_data and fundamental_data["roe"]:
                logger.info(f"  ROE: {fundamental_data['roe']:.2f}%")
        
        # Fetch news and sentiment
        logger.info(f"\nFetching news and sentiment...")
        news_sentiment = data_client.fetch_news_sentiment(ticker, days=7, limit=50)
        logger.info(f"✓ News articles: {len(news_sentiment['articles'])}")
        logger.info(f"  Sentiment score: {news_sentiment['sentiment_score']:.2f}")
        logger.info(f"  Distribution: Positive {news_sentiment['sentiment_distribution']['positive']} | " +
                   f"Negative {news_sentiment['sentiment_distribution']['negative']} | " +
                   f"Neutral {news_sentiment['sentiment_distribution']['neutral']}")
        
        # Step 3: Initialize Analysis Engine
        logger.info("\n[STEP 3] Initialize AI Analysis Engine")
        logger.info("-" * 70)
        
        engine = AnalysisEngine(
            llm_provider="openai",
            debug=False
        )
        logger.info("✓ Analysis engine initialized with OpenAI")
        
        # Step 4: Run comprehensive analysis
        logger.info("\n[STEP 4] Run Trading Analysis")
        logger.info("-" * 70)
        
        analysis_date = end_date
        logger.info(f"Analyzing {ticker} on {analysis_date}...")
        
        result = engine.analyze(
            ticker=ticker,
            date=analysis_date,
            historical_data=historical_data,
            fundamental_data=fundamental_data,
            technical_indicators=technical_indicators,
            news_sentiment=news_sentiment
        )
        
        logger.info("✓ Analysis complete")
        
        # Step 5: Display trading decision
        logger.info("\n[STEP 5] Trading Decision")
        logger.info("-" * 70)
        
        print(f"\n{'=' * 70}")
        print(f"📊 TRADING RECOMMENDATION FOR {ticker}")
        print(f"{'=' * 70}")
        print(f"\nAnalysis Date: {analysis_date}")
        print(f"\n🎯 DECISION: {result.decision}")
        print(f"📈 CONFIDENCE: {result.confidence:.1%}")
        print(f"\n💬 REASONING:\n{result.reasoning}")
        
        # Step 6: Detailed component analysis
        logger.info("\n[STEP 6] Component Analysis Breakdown")
        logger.info("-" * 70)
        
        # Fundamental analysis
        print(f"\n{'=' * 70}")
        print(f"📊 FUNDAMENTAL ANALYSIS")
        print(f"{'=' * 70}")
        
        fund_analysis = engine.analyze_fundamentals(ticker, fundamental_data)
        print(f"\nValuation:")
        for key, value in fund_analysis['valuation'].items():
            print(f"  • {key.replace('_', ' ').title()}: {value}")
        
        print(f"\nProfitability:")
        for key, value in fund_analysis['profitability'].items():
            print(f"  • {key.replace('_', ' ').title()}: {value}")
        
        print(f"\nFinancial Health:")
        for key, value in fund_analysis['financial_health'].items():
            print(f"  • {key.replace('_', ' ').title()}: {value}")
        
        # Technical analysis
        print(f"\n{'=' * 70}")
        print(f"📈 TECHNICAL ANALYSIS")
        print(f"{'=' * 70}")
        
        tech_analysis = engine.analyze_technicals(ticker, technical_indicators)
        print(f"\nMomentum:")
        for key, value in tech_analysis['momentum'].items():
            print(f"  • {key.replace('_', ' ').title()}: {value}")
        
        print(f"\nTrend:")
        for key, value in tech_analysis['trend'].items():
            print(f"  • {key.replace('_', ' ').title()}: {value}")
        
        print(f"\nSupport & Resistance:")
        for key, value in tech_analysis['support_resistance'].items():
            print(f"  • {key.replace('_', ' ').title()}: {value}")
        
        # Sentiment analysis
        print(f"\n{'=' * 70}")
        print(f"💬 SENTIMENT ANALYSIS")
        print(f"{'=' * 70}")
        
        sent_analysis = engine.analyze_sentiment(ticker, news_sentiment)
        print(f"\nOverall Sentiment: {sent_analysis['overall_sentiment']:.2f}")
        print(f"Article Count: {sent_analysis['article_count']}")
        print(f"Sentiment Trend: {sent_analysis['sentiment_trend']}")
        print(f"Distribution:")
        for sentiment_type, count in sent_analysis['distribution'].items():
            print(f"  • {sentiment_type.title()}: {count}")
        
        # Step 7: Summary and Action Items
        logger.info("\n[STEP 7] Summary & Recommendations")
        logger.info("-" * 70)
        
        print(f"\n{'=' * 70}")
        print(f"✅ ANALYSIS COMPLETE")
        print(f"{'=' * 70}")
        print(f"\nTicker: {ticker}")
        print(f"Analysis Date: {analysis_date}")
        print(f"\nFINAL RECOMMENDATION: {result.decision}")
        print(f"CONFIDENCE LEVEL: {result.confidence:.1%}")
        
        if result.decision == "BUY":
            print("\n🟢 Action: Consider buying this stock")
            print("   - Review your risk tolerance")
            print("   - Set stop-loss and take-profit levels")
            print("   - Consider position size")
        elif result.decision == "SELL":
            print("\n🔴 Action: Consider selling this stock")
            print("   - Evaluate your current position")
            print("   - Plan exit strategy")
            print("   - Consider tax implications")
        else:
            print("\n🟡 Action: Hold current position")
            print("   - Monitor for changes")
            print("   - Wait for clearer signals")
            print("   - Review at next analysis date")
        
        logger.info("=" * 70)
        logger.info("✅ WORKFLOW COMPLETED SUCCESSFULLY")
        logger.info("=" * 70)
        
    except ImportError as e:
        logger.error(f"❌ Missing dependency: {e}")
        logger.info("\nInstall missing packages:")
        logger.info("  pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Workflow error: {e}", exc_info=True)
        sys.exit(1)


def example_multiple_tickers():
    """Analyze multiple tickers and compare"""
    logger.info("\n" + "=" * 70)
    logger.info("PORTFOLIO ANALYSIS - Multiple Tickers")
    logger.info("=" * 70)
    
    try:
        from examples.data_integration_example import OpenBBDataClient
        from examples.analysis_engine_example import AnalysisEngine
        
        data_client = OpenBBDataClient()
        engine = AnalysisEngine(llm_provider="openai")
        
        tickers = ["AAPL", "MSFT", "GOOGL"]
        analysis_date = datetime.now().strftime("%Y-%m-%d")
        
        results = {}
        
        print(f"\nAnalyzing portfolio: {', '.join(tickers)}")
        print(f"Analysis Date: {analysis_date}\n")
        
        for ticker in tickers:
            try:
                logger.info(f"Analyzing {ticker}...")
                
                # Fetch data
                start_date = (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d")
                
                historical = data_client.fetch_historical_data(
                    ticker,
                    start_date,
                    analysis_date
                )
                
                technical = data_client.fetch_technical_indicators(ticker)
                fundamental = data_client.fetch_fundamental_data(ticker)
                news = data_client.fetch_news_sentiment(ticker)
                
                # Analyze
                result = engine.analyze(
                    ticker,
                    analysis_date,
                    historical,
                    fundamental,
                    technical,
                    news
                )
                
                results[ticker] = result
                
            except Exception as e:
                logger.error(f"Error analyzing {ticker}: {e}")
                continue
        
        # Print portfolio summary
        print(f"{'=' * 70}")
        print(f"PORTFOLIO SUMMARY")
        print(f"{'=' * 70}\n")
        
        print(f"{'Ticker':<10} {'Decision':<10} {'Confidence':<15} {'Action':<20}")
        print("-" * 55)
        
        for ticker in tickers:
            if ticker in results:
                result = results[ticker]
                action = "🟢 BUY" if result.decision == "BUY" else "🔴 SELL" if result.decision == "SELL" else "🟡 HOLD"
                print(
                    f"{ticker:<10} "
                    f"{result.decision:<10} "
                    f"{result.confidence:.1%}            "
                    f"{action:<20}"
                )
        
    except Exception as e:
        logger.error(f"Error in portfolio analysis: {e}", exc_info=True)


def example_backtesting_strategy():
    """Backtest strategy over multiple weeks"""
    logger.info("\n" + "=" * 70)
    logger.info("STRATEGY BACKTESTING")
    logger.info("=" * 70)
    
    try:
        from examples.data_integration_example import OpenBBDataClient
        from examples.analysis_engine_example import AnalysisEngine
        
        data_client = OpenBBDataClient()
        engine = AnalysisEngine(llm_provider="openai")
        
        ticker = "AAPL"
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)
        
        logger.info(f"Backtesting {ticker} from {start_date.date()} to {end_date.date()}")
        
        # Fetch all historical data
        all_data = data_client.fetch_historical_data(
            ticker,
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d")
        )
        
        if all_data.empty:
            logger.error("No data for backtesting")
            return
        
        # Backtest weekly
        backtest_results = []
        current_date = start_date
        buy_count = sell_count = hold_count = 0
        
        print(f"\nBacktesting {ticker}:")
        print(f"{'Date':<15} {'Decision':<10} {'Confidence':<15}")
        print("-" * 40)
        
        while current_date <= end_date:
            test_date = current_date.strftime("%Y-%m-%d")
            
            try:
                # Get data up to current date
                cutoff_data = all_data[all_data.index <= test_date]
                
                if len(cutoff_data) > 0:
                    # Run analysis
                    technical = data_client.fetch_technical_indicators(ticker)
                    fundamental = data_client.fetch_fundamental_data(ticker)
                    news = data_client.fetch_news_sentiment(ticker)
                    
                    result = engine.analyze(
                        ticker,
                        test_date,
                        cutoff_data,
                        fundamental,
                        technical,
                        news
                    )
                    
                    backtest_results.append({
                        "date": test_date,
                        "decision": result.decision,
                        "confidence": result.confidence
                    })
                    
                    print(
                        f"{test_date:<15} "
                        f"{result.decision:<10} "
                        f"{result.confidence:.1%}"
                    )
                    
                    # Count decisions
                    if result.decision == "BUY":
                        buy_count += 1
                    elif result.decision == "SELL":
                        sell_count += 1
                    else:
                        hold_count += 1
                    
            except Exception as e:
                logger.debug(f"Error on {test_date}: {e}")
            
            current_date += timedelta(weeks=1)
        
        # Print backtest summary
        print(f"\n{'=' * 70}")
        print(f"BACKTEST SUMMARY")
        print(f"{'=' * 70}")
        print(f"Total periods analyzed: {len(backtest_results)}")
        print(f"BUY signals: {buy_count}")
        print(f"SELL signals: {sell_count}")
        print(f"HOLD signals: {hold_count}")
        
    except Exception as e:
        logger.error(f"Error in backtesting: {e}", exc_info=True)


if __name__ == "__main__":
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    # Verify API keys
    if not os.getenv("OPENAI_API_KEY"):
        logger.warning("⚠️  OPENAI_API_KEY not set in .env file")
        logger.info("Please add: OPENAI_API_KEY=your_key_here")
    
    print("\n" + "🚀 " * 15)
    print("TRADING AGENTS - Complete Integration Examples")
    print("wisir + agentes Framework")
    print("🚀 " * 15 + "\n")
    
    # Run examples
    choice = input("Select example (1=Complete Workflow, 2=Multiple Tickers, 3=Backtesting, or 'all'): ").strip()
    
    if choice == "1" or choice.lower() == "all":
        try:
            example_complete_workflow()
        except Exception as e:
            logger.error(f"Example 1 failed: {e}")
    
    if choice == "2" or choice.lower() == "all":
        try:
            example_multiple_tickers()
        except Exception as e:
            logger.error(f"Example 2 failed: {e}")
    
    if choice == "3" or choice.lower() == "all":
        try:
            example_backtesting_strategy()
        except Exception as e:
            logger.error(f"Example 3 failed: {e}")
    
    logger.info("\n✅ Examples completed!\n")
