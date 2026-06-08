"""
data_integration.py - OpenBB Data Integration Module

This module handles all data fetching from OpenBB Platform (wisir).
It provides a unified interface for accessing historical prices,
technical indicators, fundamental data, and news sentiment.
"""

from typing import Dict, Any, Optional, List
import logging
from datetime import datetime, timedelta
import pandas as pd

logger = logging.getLogger(__name__)


class OpenBBDataClient:
    """
    Client for fetching data from OpenBB Platform (wisir)
    
    This class interfaces with the OpenBB data platform to collect
    historical prices, technical indicators, and fundamental data.
    
    Example:
        >>> client = OpenBBDataClient()
        >>> df = client.fetch_historical_data("AAPL", "2026-01-01", "2026-06-08")
        >>> print(df.head())
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize OpenBB data client
        
        Args:
            config: Configuration with API credentials and settings
                   Expected keys: 'openbb_token', 'timeout', 'retry_count'
        """
        self.config = config or {}
        self.obb = None
        self._connect()
        logger.info("OpenBBDataClient initialized successfully")

    def _connect(self) -> None:
        """
        Establish connection to OpenBB Platform
        
        Raises:
            ImportError: If openbb package is not installed
            Exception: If connection fails
        """
        try:
            from openbb import obb
            self.obb = obb
            logger.info("Successfully connected to OpenBB Platform")
        except ImportError as e:
            logger.error("OpenBB not installed. Run: pip install openbb")
            raise ImportError("OpenBB package required") from e
        except Exception as e:
            logger.error(f"Error connecting to OpenBB: {e}")
            raise

    def fetch_historical_data(
        self,
        ticker: str,
        start_date: str,
        end_date: str,
        interval: str = "1d"
    ) -> pd.DataFrame:
        """
        Fetch historical price data from OpenBB
        
        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL')
            start_date: Start date in format YYYY-MM-DD
            end_date: End date in format YYYY-MM-DD
            interval: Data interval - '1d' (daily), '1h' (hourly), '15m' (15min)
            
        Returns:
            DataFrame with columns: Date, Open, High, Low, Close, Volume
            
        Raises:
            ValueError: If ticker is invalid or dates are malformed
            Exception: If API call fails
            
        Example:
            >>> df = client.fetch_historical_data("AAPL", "2026-01-01", "2026-06-08")
            >>> print(df)
            >>> print(df.describe())
        """
        if not self.obb:
            raise RuntimeError("Not connected to OpenBB")
        
        if not ticker or not isinstance(ticker, str):
            raise ValueError(f"Invalid ticker: {ticker}")
        
        try:
            logger.info(
                f"Fetching historical data for {ticker} "
                f"({start_date} to {end_date}, interval={interval})"
            )
            
            # Validate dates
            self._validate_dates(start_date, end_date)
            
            # Fetch data from OpenBB
            historical = self.obb.equity.price.historical(
                symbol=ticker.upper(),
                start_date=start_date,
                end_date=end_date,
                interval=interval
            )
            
            # Convert to DataFrame
            df = historical.to_dataframe()
            
            # Validate returned data
            if df.empty:
                logger.warning(f"No data returned for {ticker}")
                return df
            
            # Clean and prepare data
            df = self._clean_historical_data(df)
            
            logger.info(f"Retrieved {len(df)} data points for {ticker}")
            return df
            
        except ValueError as e:
            logger.error(f"Validation error: {e}")
            raise
        except Exception as e:
            logger.error(f"Error fetching historical data for {ticker}: {e}")
            raise

    def fetch_technical_indicators(
        self,
        ticker: str,
        length: int = 20,
        indicator_type: str = "all"
    ) -> Dict[str, Any]:
        """
        Fetch technical indicators (MACD, RSI, Bollinger Bands, etc.)
        
        Args:
            ticker: Stock ticker symbol
            length: Period for calculation (default: 20 days)
            indicator_type: 'all', 'macd', 'rsi', 'bollinger', 'sma', 'ema'
            
        Returns:
            Dictionary with technical indicators:
            {
                'macd': {'value': float, 'signal': float, 'histogram': float},
                'rsi': float,
                'bollinger': {'upper': float, 'lower': float, 'middle': float},
                'sma_20': float,
                'sma_50': float,
                'ema_12': float,
                'ema_26': float
            }
            
        Raises:
            ValueError: If ticker or parameters are invalid
            Exception: If API call fails
            
        Example:
            >>> indicators = client.fetch_technical_indicators("AAPL", length=20)
            >>> print(f"RSI: {indicators['rsi']}")
            >>> print(f"MACD: {indicators['macd']}")
        """
        if not self.obb:
            raise RuntimeError("Not connected to OpenBB")
        
        if not ticker or not isinstance(ticker, str):
            raise ValueError(f"Invalid ticker: {ticker}")
        
        if length < 5 or length > 200:
            raise ValueError("Length must be between 5 and 200")
        
        try:
            logger.info(
                f"Fetching technical indicators for {ticker} "
                f"(length={length}, type={indicator_type})"
            )
            
            indicators = {}
            
            # Fetch historical data for calculations
            df = self.fetch_historical_data(
                ticker,
                (datetime.now() - timedelta(days=length * 2)).strftime("%Y-%m-%d"),
                datetime.now().strftime("%Y-%m-%d")
            )
            
            if df.empty:
                logger.warning(f"No data for technical indicators: {ticker}")
                return indicators
            
            # Calculate indicators
            if indicator_type in ["all", "rsi"]:
                indicators["rsi"] = self._calculate_rsi(df["close"], length)
            
            if indicator_type in ["all", "macd"]:
                indicators["macd"] = self._calculate_macd(df["close"])
            
            if indicator_type in ["all", "bollinger"]:
                indicators["bollinger"] = self._calculate_bollinger(df["close"], length)
            
            if indicator_type in ["all", "sma"]:
                indicators["sma_20"] = self._calculate_sma(df["close"], 20)
                indicators["sma_50"] = self._calculate_sma(df["close"], 50)
            
            if indicator_type in ["all", "ema"]:
                indicators["ema_12"] = self._calculate_ema(df["close"], 12)
                indicators["ema_26"] = self._calculate_ema(df["close"], 26)
            
            logger.info(f"Successfully calculated {len(indicators)} indicators")
            return indicators
            
        except Exception as e:
            logger.error(f"Error fetching technical indicators for {ticker}: {e}")
            raise

    def fetch_fundamental_data(self, ticker: str) -> Dict[str, Any]:
        """
        Fetch fundamental data (P/E, earnings, revenue, etc.)
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Dictionary with fundamental data:
            {
                'pe_ratio': float,
                'eps': float,
                'revenue': float,
                'net_income': float,
                'debt_to_equity': float,
                'roe': float,
                'roa': float,
                'current_ratio': float
            }
            
        Raises:
            ValueError: If ticker is invalid
            Exception: If API call fails
            
        Example:
            >>> fundamentals = client.fetch_fundamental_data("AAPL")
            >>> print(f"P/E Ratio: {fundamentals['pe_ratio']}")
            >>> print(f"ROE: {fundamentals['roe']}")
        """
        if not self.obb:
            raise RuntimeError("Not connected to OpenBB")
        
        if not ticker or not isinstance(ticker, str):
            raise ValueError(f"Invalid ticker: {ticker}")
        
        try:
            logger.info(f"Fetching fundamental data for {ticker}")
            
            fundamentals = {}
            
            # Fetch income statement data
            try:
                income = self.obb.equity.fundamental.income(symbol=ticker.upper())
                if income:
                    fundamentals["revenue"] = income.get("revenue", None)
                    fundamentals["net_income"] = income.get("net_income", None)
                    fundamentals["eps"] = income.get("eps", None)
            except Exception as e:
                logger.warning(f"Could not fetch income data for {ticker}: {e}")
            
            # Fetch balance sheet data
            try:
                balance = self.obb.equity.fundamental.balance(symbol=ticker.upper())
                if balance:
                    fundamentals["debt_to_equity"] = balance.get("debt_to_equity", None)
                    fundamentals["current_ratio"] = balance.get("current_ratio", None)
            except Exception as e:
                logger.warning(f"Could not fetch balance data for {ticker}: {e}")
            
            # Fetch ratios
            try:
                ratios = self.obb.equity.fundamental.ratios(symbol=ticker.upper())
                if ratios:
                    fundamentals["pe_ratio"] = ratios.get("pe_ratio", None)
                    fundamentals["roe"] = ratios.get("roe", None)
                    fundamentals["roa"] = ratios.get("roa", None)
            except Exception as e:
                logger.warning(f"Could not fetch ratios for {ticker}: {e}")
            
            logger.info(f"Retrieved {len(fundamentals)} fundamental metrics for {ticker}")
            return fundamentals
            
        except Exception as e:
            logger.error(f"Error fetching fundamental data for {ticker}: {e}")
            raise

    def fetch_news_sentiment(
        self,
        ticker: str,
        days: int = 7,
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        Fetch news and sentiment data
        
        Args:
            ticker: Stock ticker symbol
            days: Number of days to look back
            limit: Maximum number of news articles to fetch
            
        Returns:
            Dictionary with news and sentiment:
            {
                'articles': [
                    {
                        'title': str,
                        'url': str,
                        'date': str,
                        'source': str,
                        'sentiment': float (0-1)
                    }
                ],
                'sentiment_score': float (-1 to 1),
                'sentiment_distribution': {
                    'positive': int,
                    'neutral': int,
                    'negative': int
                }
            }
            
        Raises:
            ValueError: If parameters are invalid
            Exception: If API call fails
            
        Example:
            >>> news = client.fetch_news_sentiment("AAPL", days=7)
            >>> print(f"Sentiment Score: {news['sentiment_score']}")
            >>> print(f"Articles: {len(news['articles'])}")
        """
        if not self.obb:
            raise RuntimeError("Not connected to OpenBB")
        
        if not ticker or not isinstance(ticker, str):
            raise ValueError(f"Invalid ticker: {ticker}")
        
        if days < 1 or days > 365:
            raise ValueError("Days must be between 1 and 365")
        
        try:
            logger.info(f"Fetching news sentiment for {ticker} (last {days} days)")
            
            news_data = {
                "articles": [],
                "sentiment_score": 0.0,
                "sentiment_distribution": {
                    "positive": 0,
                    "neutral": 0,
                    "negative": 0
                }
            }
            
            # Fetch news from OpenBB
            try:
                news = self.obb.news.world(
                    query=ticker.upper(),
                    limit=limit
                )
                
                if news:
                    articles = news if isinstance(news, list) else [news]
                    
                    for article in articles[:limit]:
                        news_data["articles"].append({
                            "title": article.get("title", ""),
                            "url": article.get("url", ""),
                            "date": article.get("date", ""),
                            "source": article.get("source", ""),
                            "sentiment": self._analyze_sentiment(article.get("title", ""))
                        })
                    
                    # Calculate sentiment distribution
                    sentiments = [
                        article["sentiment"] for article in news_data["articles"]
                    ]
                    
                    if sentiments:
                        positive = sum(1 for s in sentiments if s > 0.6)
                        negative = sum(1 for s in sentiments if s < 0.4)
                        neutral = len(sentiments) - positive - negative
                        
                        news_data["sentiment_distribution"]["positive"] = positive
                        news_data["sentiment_distribution"]["negative"] = negative
                        news_data["sentiment_distribution"]["neutral"] = neutral
                        
                        # Calculate overall sentiment score
                        news_data["sentiment_score"] = sum(sentiments) / len(sentiments)
                    
            except Exception as e:
                logger.warning(f"Could not fetch news for {ticker}: {e}")
            
            logger.info(
                f"Retrieved {len(news_data['articles'])} articles for {ticker} "
                f"(sentiment: {news_data['sentiment_score']:.2f})"
            )
            return news_data
            
        except Exception as e:
            logger.error(f"Error fetching news sentiment for {ticker}: {e}")
            raise

    # Helper Methods
    
    @staticmethod
    def _validate_dates(start_date: str, end_date: str) -> None:
        """Validate date format and logic"""
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            
            if start > end:
                raise ValueError("Start date must be before end date")
            
            if end > datetime.now():
                raise ValueError("End date cannot be in the future")
                
        except ValueError as e:
            logger.error(f"Date validation error: {e}")
            raise

    @staticmethod
    def _clean_historical_data(df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize historical data"""
        # Rename columns to lowercase
        df.columns = df.columns.str.lower()
        
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Sort by date
        if "date" in df.columns:
            df = df.sort_values("date")
        
        # Remove rows with null prices
        df = df.dropna(subset=["close"])
        
        return df

    @staticmethod
    def _calculate_rsi(prices: pd.Series, period: int = 14) -> float:
        """Calculate Relative Strength Index (RSI)"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return float(rsi.iloc[-1]) if not rsi.empty else 50.0

    @staticmethod
    def _calculate_macd(prices: pd.Series) -> Dict[str, float]:
        """Calculate MACD (Moving Average Convergence Divergence)"""
        exp1 = prices.ewm(span=12, adjust=False).mean()
        exp2 = prices.ewm(span=26, adjust=False).mean()
        
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        histogram = macd - signal
        
        return {
            "value": float(macd.iloc[-1]) if not macd.empty else 0.0,
            "signal": float(signal.iloc[-1]) if not signal.empty else 0.0,
            "histogram": float(histogram.iloc[-1]) if not histogram.empty else 0.0
        }

    @staticmethod
    def _calculate_bollinger(prices: pd.Series, period: int = 20) -> Dict[str, float]:
        """Calculate Bollinger Bands"""
        sma = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        
        upper = sma + (std * 2)
        lower = sma - (std * 2)
        
        return {
            "upper": float(upper.iloc[-1]) if not upper.empty else 0.0,
            "middle": float(sma.iloc[-1]) if not sma.empty else 0.0,
            "lower": float(lower.iloc[-1]) if not lower.empty else 0.0
        }

    @staticmethod
    def _calculate_sma(prices: pd.Series, period: int) -> float:
        """Calculate Simple Moving Average (SMA)"""
        sma = prices.rolling(window=period).mean()
        return float(sma.iloc[-1]) if not sma.empty else 0.0

    @staticmethod
    def _calculate_ema(prices: pd.Series, period: int) -> float:
        """Calculate Exponential Moving Average (EMA)"""
        ema = prices.ewm(span=period, adjust=False).mean()
        return float(ema.iloc[-1]) if not ema.empty else 0.0

    @staticmethod
    def _analyze_sentiment(text: str) -> float:
        """
        Simple sentiment analysis on text (0-1 scale)
        In production, use a proper NLP library like TextBlob or transformers
        """
        # Placeholder implementation
        # In production, use: from textblob import TextBlob
        # sentiment = TextBlob(text).sentiment.polarity
        
        positive_words = ["bullish", "up", "gain", "profit", "strong", "buy"]
        negative_words = ["bearish", "down", "loss", "weak", "sell", "drop"]
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count + negative_count == 0:
            return 0.5
        
        score = positive_count / (positive_count + negative_count)
        return score


class DataValidator:
    """Validate and clean data from OpenBB"""
    
    @staticmethod
    def validate_historical_data(data: pd.DataFrame) -> bool:
        """
        Validate historical data integrity
        
        Args:
            data: DataFrame with historical data
            
        Returns:
            True if data is valid, False otherwise
        """
        logger.debug("Validating historical data...")
        
        if data is None or data.empty:
            logger.error("Data is empty")
            return False
        
        required_columns = ["open", "high", "low", "close", "volume"]
        for col in required_columns:
            if col not in data.columns:
                logger.error(f"Missing required column: {col}")
                return False
        
        # Check for negative prices
        if (data[["open", "high", "low", "close"]] < 0).any().any():
            logger.error("Negative prices detected")
            return False
        
        # Check for null values
        if data[required_columns].isnull().any().any():
            logger.warning("Null values detected in data")
        
        logger.info("Historical data validation passed")
        return True

    @staticmethod
    def validate_indicators(indicators: Dict[str, Any]) -> bool:
        """
        Validate technical indicators
        
        Args:
            indicators: Dictionary with indicators
            
        Returns:
            True if indicators are valid, False otherwise
        """
        logger.debug("Validating indicators...")
        
        if not isinstance(indicators, dict):
            logger.error("Indicators must be a dictionary")
            return False
        
        # RSI should be 0-100
        if "rsi" in indicators:
            if not 0 <= indicators["rsi"] <= 100:
                logger.error(f"Invalid RSI value: {indicators['rsi']}")
                return False
        
        # Sentiment should be 0-1
        if "sentiment" in indicators:
            if not 0 <= indicators["sentiment"] <= 1:
                logger.error(f"Invalid sentiment value: {indicators['sentiment']}")
                return False
        
        logger.info("Indicators validation passed")
        return True
