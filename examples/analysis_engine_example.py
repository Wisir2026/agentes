"""
analysis_engine.py - TradingAgents Analysis Engine

This module integrates with the TradingAgents Framework (agentes)
to provide AI-powered trading analysis using multiple LLM providers.
"""

from typing import Dict, Any, Optional, Tuple
import logging
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class LLMProvider(Enum):
    """Supported LLM providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    XAI = "xai"
    OPENROUTER = "openrouter"
    OLLAMA = "ollama"


@dataclass
class AnalysisResult:
    """Result of trading analysis"""
    ticker: str
    date: str
    decision: str  # "BUY", "SELL", "HOLD"
    confidence: float  # 0.0 to 1.0
    reasoning: str
    analyst_reports: Dict[str, Any]
    researcher_insights: Dict[str, Any]
    risk_assessment: Dict[str, Any]


class AnalysisEngine:
    """
    Main analysis engine that orchestrates TradingAgents framework
    
    This engine coordinates:
    1. Multiple analyst agents (fundamental, technical, sentiment, news)
    2. Researcher agents (bullish/bearish debate)
    3. Trader agent (decision making)
    4. Risk manager (risk assessment)
    
    Example:
        >>> engine = AnalysisEngine(llm_provider="openai")
        >>> result = engine.analyze("AAPL", "2026-06-08", historical_data)
        >>> print(result.decision)
        >>> print(result.confidence)
    """

    def __init__(
        self,
        config: Optional[Dict] = None,
        llm_provider: str = "openai",
        debug: bool = False
    ):
        """
        Initialize Analysis Engine
        
        Args:
            config: Configuration dictionary with:
                   - llm_provider: Which LLM to use
                   - deep_think_llm: Model for complex reasoning
                   - quick_think_llm: Model for quick tasks
                   - max_debate_rounds: Number of debate rounds
                   - temperature: LLM temperature (0.0-1.0)
            llm_provider: Default LLM provider
            debug: Enable debug logging
        """
        self.config = config or self._get_default_config()
        self.config["llm_provider"] = llm_provider
        self.llm_provider = llm_provider
        self.debug = debug
        
        self.ta_graph = None
        self._initialize_trading_agents()
        
        logger.info(
            f"AnalysisEngine initialized with provider: {llm_provider}, "
            f"debug={debug}"
        )

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "llm_provider": "openai",
            "deep_think_llm": "gpt-4",
            "quick_think_llm": "gpt-3.5-turbo",
            "max_debate_rounds": 2,
            "temperature": 0.7,
            "max_tokens": 2000,
            "timeout": 60
        }

    def _initialize_trading_agents(self) -> None:
        """Initialize TradingAgents Framework"""
        try:
            from tradingagents.graph.trading_graph import TradingAgentsGraph
            from tradingagents.default_config import DEFAULT_CONFIG
            
            # Merge configurations
            merged_config = DEFAULT_CONFIG.copy()
            merged_config.update(self.config)
            
            # Initialize graph
            self.ta_graph = TradingAgentsGraph(
                debug=self.debug,
                config=merged_config
            )
            
            logger.info("TradingAgents Framework initialized successfully")
            
        except ImportError as e:
            logger.error(
                "Failed to import TradingAgents. "
                "Make sure agentes repo is in PYTHONPATH"
            )
            raise ImportError("TradingAgents Framework not available") from e
        except Exception as e:
            logger.error(f"Error initializing TradingAgents: {e}")
            raise

    def analyze(
        self,
        ticker: str,
        date: str,
        historical_data: Dict[str, Any],
        fundamental_data: Optional[Dict[str, Any]] = None,
        technical_indicators: Optional[Dict[str, Any]] = None,
        news_sentiment: Optional[Dict[str, Any]] = None
    ) -> AnalysisResult:
        """
        Perform complete trading analysis
        
        Args:
            ticker: Stock ticker symbol
            date: Analysis date (YYYY-MM-DD)
            historical_data: Historical OHLCV data
            fundamental_data: Fundamental metrics (P/E, earnings, etc.)
            technical_indicators: Technical indicators (RSI, MACD, etc.)
            news_sentiment: News and sentiment data
            
        Returns:
            AnalysisResult with decision and reasoning
            
        Raises:
            ValueError: If inputs are invalid
            Exception: If analysis fails
            
        Example:
            >>> data = {
            ...     "ticker": "AAPL",
            ...     "date": "2026-06-08",
            ...     "close": 150.25,
            ...     "volume": 1000000
            ... }
            >>> result = engine.analyze("AAPL", "2026-06-08", data)
            >>> print(f"Decision: {result.decision}")
            >>> print(f"Confidence: {result.confidence}")
        """
        if not self.ta_graph:
            raise RuntimeError("TradingAgents not initialized")
        
        if not ticker or not isinstance(ticker, str):
            raise ValueError(f"Invalid ticker: {ticker}")
        
        try:
            logger.info(f"Starting analysis for {ticker} on {date}")
            
            # Prepare analysis data
            analysis_data = self._prepare_analysis_data(
                ticker,
                date,
                historical_data,
                fundamental_data,
                technical_indicators,
                news_sentiment
            )
            
            # Run TradingAgents propagation
            logger.info("Running TradingAgents framework propagation...")
            state, decision_text = self.ta_graph.propagate(ticker, date)
            
            # Parse results
            result = self._parse_trading_agents_result(
                ticker,
                date,
                decision_text,
                state,
                analysis_data
            )
            
            logger.info(
                f"Analysis complete for {ticker}: "
                f"Decision={result.decision}, "
                f"Confidence={result.confidence:.2f}"
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing {ticker}: {e}")
            raise

    def analyze_fundamentals(
        self,
        ticker: str,
        fundamental_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Deep analysis of fundamental data
        
        Args:
            ticker: Stock ticker
            fundamental_data: Fundamental metrics
            
        Returns:
            Dictionary with fundamental analysis
        """
        logger.info(f"Analyzing fundamentals for {ticker}")
        
        analysis = {
            "valuation": self._analyze_valuation(fundamental_data),
            "profitability": self._analyze_profitability(fundamental_data),
            "financial_health": self._analyze_financial_health(fundamental_data)
        }
        
        return analysis

    def analyze_technicals(
        self,
        ticker: str,
        technical_indicators: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Deep analysis of technical indicators
        
        Args:
            ticker: Stock ticker
            technical_indicators: Technical indicators
            
        Returns:
            Dictionary with technical analysis
        """
        logger.info(f"Analyzing technicals for {ticker}")
        
        analysis = {
            "momentum": self._analyze_momentum(technical_indicators),
            "trend": self._analyze_trend(technical_indicators),
            "support_resistance": self._analyze_support_resistance(technical_indicators)
        }
        
        return analysis

    def analyze_sentiment(
        self,
        ticker: str,
        news_sentiment: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Deep analysis of sentiment data
        
        Args:
            ticker: Stock ticker
            news_sentiment: News and sentiment data
            
        Returns:
            Dictionary with sentiment analysis
        """
        logger.info(f"Analyzing sentiment for {ticker}")
        
        analysis = {
            "overall_sentiment": news_sentiment.get("sentiment_score", 0.5),
            "distribution": news_sentiment.get("sentiment_distribution", {}),
            "article_count": len(news_sentiment.get("articles", [])),
            "sentiment_trend": self._analyze_sentiment_trend(news_sentiment)
        }
        
        return analysis

    # Helper Methods
    
    def _prepare_analysis_data(
        self,
        ticker: str,
        date: str,
        historical_data: Dict[str, Any],
        fundamental_data: Optional[Dict[str, Any]],
        technical_indicators: Optional[Dict[str, Any]],
        news_sentiment: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Prepare and validate analysis data"""
        data = {
            "ticker": ticker,
            "date": date,
            "historical": historical_data or {},
            "fundamentals": fundamental_data or {},
            "technicals": technical_indicators or {},
            "sentiment": news_sentiment or {}
        }
        
        logger.debug(f"Analysis data prepared: {len(data)} components")
        return data

    def _parse_trading_agents_result(
        self,
        ticker: str,
        date: str,
        decision_text: str,
        state: Dict[str, Any],
        analysis_data: Dict[str, Any]
    ) -> AnalysisResult:
        """Parse TradingAgents result into AnalysisResult"""
        
        # Extract decision and confidence
        decision, confidence = self._extract_decision(decision_text)
        
        # Extract reports
        analyst_reports = state.get("analyst_reports", {})
        researcher_insights = state.get("researcher_insights", {})
        risk_assessment = state.get("risk_assessment", {})
        
        return AnalysisResult(
            ticker=ticker,
            date=date,
            decision=decision,
            confidence=confidence,
            reasoning=decision_text,
            analyst_reports=analyst_reports,
            researcher_insights=researcher_insights,
            risk_assessment=risk_assessment
        )

    @staticmethod
    def _extract_decision(decision_text: str) -> Tuple[str, float]:
        """Extract decision and confidence from TradingAgents output"""
        decision_text_upper = decision_text.upper()
        
        # Extract decision
        if "BUY" in decision_text_upper or "BULLISH" in decision_text_upper:
            decision = "BUY"
        elif "SELL" in decision_text_upper or "BEARISH" in decision_text_upper:
            decision = "SELL"
        else:
            decision = "HOLD"
        
        # Extract confidence
        confidence = 0.5
        import re
        confidence_match = re.search(r"(\d+(?:\.\d+)?)\s*%?", decision_text)
        if confidence_match:
            conf_value = float(confidence_match.group(1))
            if 0 <= conf_value <= 100:
                confidence = conf_value / 100 if conf_value > 1 else conf_value
        
        return decision, confidence

    @staticmethod
    def _analyze_valuation(fundamental_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze valuation metrics"""
        pe_ratio = fundamental_data.get("pe_ratio", 0)
        
        return {
            "undervalued": pe_ratio < 15 if pe_ratio > 0 else None,
            "pe_score": min(max(20 - pe_ratio, 0) / 10, 1.0) if pe_ratio > 0 else 0.5,
            "score": 0.5
        }

    @staticmethod
    def _analyze_profitability(fundamental_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze profitability metrics"""
        roe = fundamental_data.get("roe", 0)
        roa = fundamental_data.get("roa", 0)
        
        strong = (roe or 0) > 15 and (roa or 0) > 5
        
        return {
            "strong": strong,
            "roe": roe or 0,
            "roa": roa or 0
        }

    @staticmethod
    def _analyze_financial_health(fundamental_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze financial health metrics"""
        debt_to_equity = fundamental_data.get("debt_to_equity", 0)
        current_ratio = fundamental_data.get("current_ratio", 1)
        
        stable = (debt_to_equity or 0) < 2 and (current_ratio or 1) > 1
        
        return {
            "stable": stable,
            "debt_ratio": debt_to_equity or 0,
            "score": 0.5
        }

    @staticmethod
    def _analyze_momentum(technical_indicators: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze momentum indicators"""
        rsi = technical_indicators.get("rsi", 50)
        
        strong = rsi > 60 or rsi < 40
        
        return {
            "strong": strong,
            "rsi": rsi,
            "score": (rsi - 30) / 40 if rsi else 0.5
        }

    @staticmethod
    def _analyze_trend(technical_indicators: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze trend indicators"""
        macd = technical_indicators.get("macd", {})
        sma_20 = technical_indicators.get("sma_20", 0)
        sma_50 = technical_indicators.get("sma_50", 0)
        
        direction = "UP" if (sma_20 or 0) > (sma_50 or 0) else "DOWN"
        strength = abs(macd.get("histogram", 0)) if macd else 0
        
        return {
            "direction": direction,
            "strength": strength,
            "score": 0.5
        }

    @staticmethod
    def _analyze_support_resistance(
        technical_indicators: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze support and resistance levels"""
        bollinger = technical_indicators.get("bollinger", {})
        
        return {
            "upper": bollinger.get("upper", 0),
            "lower": bollinger.get("lower", 0),
            "score": 0.5
        }

    @staticmethod
    def _analyze_sentiment_trend(news_sentiment: Dict[str, Any]) -> str:
        """Analyze sentiment trend"""
        distribution = news_sentiment.get("sentiment_distribution", {})
        positive = distribution.get("positive", 0)
        negative = distribution.get("negative", 0)
        
        if positive > negative * 1.5:
            return "IMPROVING"
        elif negative > positive * 1.5:
            return "DETERIORATING"
        else:
            return "NEUTRAL"
