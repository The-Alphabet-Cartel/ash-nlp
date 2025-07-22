"""
ML Model Management for Enhanced Ash NLP Service
Handles loading, caching, and access to ML models
"""

import logging
from transformers import pipeline
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class ModelManager:
    """Centralized management of ML models"""
    
    def __init__(self):
        self.depression_model = None
        self.sentiment_model = None
        self._models_loaded = False
    
    async def load_models(self):
        """Load both depression and sentiment analysis models"""
        
        logger.info("=" * 50)
        logger.info("STARTING ENHANCED MODEL LOADING PROCESS")
        logger.info("=" * 50)
        
        try:
            # Primary depression model
            logger.info("Loading Depression Detection model...")
            self.depression_model = pipeline(
                "text-classification",
                model="rafalposwiata/deproberta-large-depression",
                device=-1,  # CPU inference
                top_k=None
            )
            
            # Secondary sentiment model for context
            logger.info("Loading Sentiment Analysis model...")
            self.sentiment_model = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                device=-1,
                top_k=None
            )
            
            self._models_loaded = True
            logger.info("✅ Both models loaded successfully!")
            
            # Quick test
            test_message = "I want to kill myself"
            dep_result = self.depression_model(test_message)
            sent_result = self.sentiment_model(test_message)
            
            logger.info(f"✅ Depression test: {dep_result}")
            logger.info(f"✅ Sentiment test: {sent_result}")
            logger.info("✅ Enhanced multi-model system ready for keyword discovery")
            logger.info("=" * 50)
            
        except Exception as e:
            self._models_loaded = False
            logger.error(f"❌ Failed to load models: {e}")
            logger.exception("Full traceback:")
            raise
    
    def models_loaded(self) -> bool:
        """Check if all models are loaded"""
        return (self._models_loaded and 
                self.depression_model is not None and 
                self.sentiment_model is not None)
    
    def get_depression_model(self):
        """Get the depression detection model"""
        if not self.models_loaded():
            raise RuntimeError("Models not loaded")
        return self.depression_model
    
    def get_sentiment_model(self):
        """Get the sentiment analysis model"""
        if not self.models_loaded():
            raise RuntimeError("Models not loaded")
        return self.sentiment_model
    
    def get_model_status(self) -> Dict[str, bool]:
        """Get status of all models"""
        return {
            "depression": self.depression_model is not None,
            "sentiment": self.sentiment_model is not None,
            "all_loaded": self.models_loaded()
        }
    
    def analyze_with_depression_model(self, text: str) -> Optional[Any]:
        """Analyze text with depression model"""
        if not self.depression_model:
            return None
        try:
            return self.depression_model(text)
        except Exception as e:
            logger.error(f"Error in depression model analysis: {e}")
            return None
    
    def analyze_with_sentiment_model(self, text: str) -> Optional[Any]:
        """Analyze text with sentiment model"""
        if not self.sentiment_model:
            return None
        try:
            return self.sentiment_model(text)
        except Exception as e:
            logger.error(f"Error in sentiment model analysis: {e}")
            return None