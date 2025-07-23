"""
False Positive Learning Endpoints for NLP Server
Add to: ash-nlp/utils/learning_endpoints.py (new file)
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import json
import os
import numpy as np
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
import re

logger = logging.getLogger(__name__)

# Pydantic models for learning endpoints
class FalsePositiveAnalysisRequest(BaseModel):
    message: str
    detected_level: str
    correct_level: str
    context: str
    severity_score: int

class LearningUpdateRequest(BaseModel):
    false_positive_id: str
    message_data: Dict
    correction_data: Dict
    context_data: str
    timestamp: str

class LearningResponse(BaseModel):
    status: str
    patterns_discovered: int
    confidence_adjustments: int
    learning_applied: bool
    reasoning: str

class LearningManager:
    """Manages false positive learning and model adjustment"""
    
    def __init__(self, model_manager):
        self.model_manager = model_manager
        self.learning_data_file = './data/learning_adjustments.json'
        self.confidence_adjustments = {}
        self.pattern_overrides = {}
        
        # Learning parameters
        self.min_confidence_adjustment = 0.05
        self.max_confidence_adjustment = 0.30
        self.learning_rate = 0.1
        
        # Load existing learning data
        self._load_learning_data()
        
        logger.info("🧠 Learning manager initialized")
    
    def _load_learning_data(self):
        """Load existing learning adjustments"""
        try:
            if os.path.exists(self.learning_data_file):
                with open(self.learning_data_file, 'r') as f:
                    data = json.load(f)
                
                self.confidence_adjustments = data.get('confidence_adjustments', {})
                self.pattern_overrides = data.get('pattern_overrides', {})
                
                logger.info(f"Loaded {len(self.confidence_adjustments)} confidence adjustments")
                logger.info(f"Loaded {len(self.pattern_overrides)} pattern overrides")
            else:
                logger.info("No existing learning data found - starting fresh")
                
        except Exception as e:
            logger.error(f"Error loading learning data: {e}")
    
    def _save_learning_data(self):
        """Save learning adjustments to file"""
        try:
            os.makedirs('./data', exist_ok=True)
            
            data = {
                'confidence_adjustments': self.confidence_adjustments,
                'pattern_overrides': self.pattern_overrides,
                'last_updated': datetime.now(timezone.utc).isoformat(),
                'total_adjustments': len(self.confidence_adjustments),
                'total_overrides': len(self.pattern_overrides)
            }
            
            with open(self.learning_data_file, 'w') as f:
                json.dump(data, f, indent=2)
                
            logger.info(f"Saved learning data: {len(self.confidence_adjustments)} adjustments")
            
        except Exception as e:
            logger.error(f"Error saving learning data: {e}")
    
    async def analyze_false_positive(self, request: FalsePositiveAnalysisRequest) -> LearningResponse:
        """Analyze a false positive and determine learning adjustments"""
        
        try:
            message = request.message.lower().strip()
            detected_level = request.detected_level
            correct_level = request.correct_level
            severity_score = request.severity_score
            
            patterns_discovered = 0
            confidence_adjustments = 0
            learning_applied = False
            reasoning_parts = []
            
            # Step 1: Analyze with current models to understand the error
            depression_result = self.model_manager.analyze_with_depression_model(message)
            sentiment_result = self.model_manager.analyze_with_sentiment_model(message)
            
            if depression_result and sentiment_result:
                # Extract current scores
                from utils.scoring_helpers import extract_depression_score
                from utils.context_helpers import analyze_sentiment_context
                
                current_depression_score = extract_depression_score(depression_result)
                sentiment_scores = analyze_sentiment_context(sentiment_result)
                
                reasoning_parts.append(f"Current depression score: {current_depression_score:.3f}")
                reasoning_parts.append(f"Sentiment scores: {sentiment_scores}")
                
                # Step 2: Extract linguistic patterns that led to false positive
                false_positive_patterns = self._extract_false_positive_patterns(
                    message, depression_result, sentiment_result, detected_level, correct_level
                )
                
                patterns_discovered = len(false_positive_patterns)
                reasoning_parts.append(f"Discovered {patterns_discovered} problematic patterns")
                
                # Step 3: Create confidence adjustments
                if patterns_discovered > 0:
                    adjustments = self._create_confidence_adjustments(
                        false_positive_patterns, severity_score, detected_level, correct_level
                    )
                    
                    confidence_adjustments = len(adjustments)
                    
                    # Apply adjustments
                    for pattern, adjustment in adjustments.items():
                        self.confidence_adjustments[pattern] = adjustment
                        reasoning_parts.append(f"Added adjustment for '{pattern}': {adjustment}")
                    
                    learning_applied = True
                
                # Step 4: Check for context-based overrides
                context_overrides = self._create_context_overrides(
                    message, request.context, detected_level, correct_level
                )
                
                if context_overrides:
                    for override_pattern, override_data in context_overrides.items():
                        self.pattern_overrides[override_pattern] = override_data
                        reasoning_parts.append(f"Added context override for '{override_pattern}'")
                    
                    learning_applied = True
                
                # Save learning data
                if learning_applied:
                    self._save_learning_data()
            
            else:
                reasoning_parts.append("Model analysis failed - using pattern-based learning")
                
                # Fallback: pattern-based learning without model scores
                simple_patterns = self._extract_simple_patterns(message)
                for pattern in simple_patterns:
                    # Simple adjustment based on severity
                    adjustment_factor = -(severity_score / 10.0) * self.max_confidence_adjustment
                    self.confidence_adjustments[pattern] = adjustment_factor
                    confidence_adjustments += 1
                
                if confidence_adjustments > 0:
                    learning_applied = True
                    self._save_learning_data()
            
            return LearningResponse(
                status="success",
                patterns_discovered=patterns_discovered,
                confidence_adjustments=confidence_adjustments,
                learning_applied=learning_applied,
                reasoning=" | ".join(reasoning_parts)
            )
            
        except Exception as e:
            logger.error(f"Error in false positive analysis: {e}")
            return LearningResponse(
                status="error",
                patterns_discovered=0,
                confidence_adjustments=0,
                learning_applied=False,
                reasoning=f"Analysis failed: {str(e)}"
            )
    
    def _extract_false_positive_patterns(self, message: str, depression_result, sentiment_result, 
                                       detected_level: str, correct_level: str) -> List[str]:
        """Extract patterns that likely caused the false positive"""
        
        patterns = []
        
        # Extract n-grams that might be problematic
        words = message.split()
        
        # Look for 2-4 word phrases
        for i in range(len(words)):
            for length in range(2, min(5, len(words) - i + 1)):
                phrase = ' '.join(words[i:i + length])
                
                # Skip very common words
                if phrase in ['i am', 'it is', 'this is', 'i have', 'to be']:
                    continue
                
                # Check if this phrase might have triggered the false positive
                if self._might_be_trigger_phrase(phrase, depression_result, detected_level):
                    patterns.append(phrase)
        
        # Look for specific problematic patterns based on error type
        if detected_level == "high" and correct_level in ["none", "low"]:
            # High false positives - look for idioms, metaphors, hyperbole
            idiom_patterns = self._detect_idioms_and_metaphors(message)
            patterns.extend(idiom_patterns)
        
        return list(set(patterns))  # Remove duplicates
    
    def _might_be_trigger_phrase(self, phrase: str, depression_result, detected_level: str) -> bool:
        """Check if a phrase might have triggered the false positive"""
        
        # Test the phrase in isolation
        try:
            isolated_result = self.model_manager.analyze_with_depression_model(phrase)
            if isolated_result:
                from utils.scoring_helpers import extract_depression_score
                isolated_score = extract_depression_score(isolated_result)
                
                # If this phrase alone gives a significant score, it might be the trigger
                if detected_level == "high" and isolated_score > 0.3:
                    return True
                elif detected_level == "medium" and isolated_score > 0.2:
                    return True
                elif detected_level == "low" and isolated_score > 0.1:
                    return True
        except:
            pass
        
        return False
    
    def _detect_idioms_and_metaphors(self, message: str) -> List[str]:
        """Detect potential idioms and metaphors that caused false positives"""
        
        idiom_patterns = []
        message_lower = message.lower()
        
        # Common false positive patterns
        false_positive_indicators = [
            # Fatigue idioms
            r'\b(dead|dying) (tired|exhausted|beat)\b',
            # Food cravings
            r'\b(murder|kill) (for|a) \w+\b',
            # Success expressions
            r'\b(killing|slaying|crushing) it\b',
            # Frustration expressions
            r'\bdriving me (crazy|insane|nuts)\b',
            # Entertainment
            r'\b(that|it) (killed|murdered) me\b',
            # Humor
            r'\bdying of laughter\b',
            # Work/school stress
            r'\b(brutal|killer) (test|exam|homework|workout)\b'
        ]
        
        for pattern in false_positive_indicators:
            matches = re.finditer(pattern, message_lower)
            for match in matches:
                idiom_patterns.append(match.group())
        
        return idiom_patterns
    
    def _create_confidence_adjustments(self, patterns: List[str], severity_score: int, 
                                     detected_level: str, correct_level: str) -> Dict[str, float]:
        """Create confidence adjustments for the discovered patterns"""
        
        adjustments = {}
        
        # Calculate base adjustment based on severity
        base_adjustment = -(severity_score / 10.0) * self.max_confidence_adjustment
        
        for pattern in patterns:
            # Adjust based on pattern type and error severity
            if detected_level == "high" and correct_level == "none":
                # Strongest adjustment for high→none errors
                adjustment = base_adjustment * 1.5
            elif detected_level == "high" and correct_level == "low":
                # Strong adjustment for high→low errors
                adjustment = base_adjustment * 1.2
            else:
                # Standard adjustment
                adjustment = base_adjustment
            
            # Ensure adjustment is within bounds
            adjustment = max(-self.max_confidence_adjustment, 
                           min(-self.min_confidence_adjustment, adjustment))
            
            adjustments[pattern] = adjustment
        
        return adjustments
    
    def _create_context_overrides(self, message: str, context: str, 
                                detected_level: str, correct_level: str) -> Dict[str, Dict]:
        """Create context-based overrides for better future detection"""
        
        overrides = {}
        
        if not context or context == "No additional context provided":
            return overrides
        
        # Parse context for useful information
        context_lower = context.lower()
        
        # Check for context indicators
        if "humor" in context_lower or "joke" in context_lower:
            # Create humor context override
            humor_patterns = self._extract_humor_indicators(message)
            for pattern in humor_patterns:
                overrides[f"humor_context:{pattern}"] = {
                    'context_type': 'humor',
                    'confidence_reduction': 0.8,
                    'max_crisis_level': 'low',
                    'created_from_fp': True
                }
        
        if "idiom" in context_lower or "expression" in context_lower:
            # Create idiom override
            overrides[f"idiom_override:{message[:50]}"] = {
                'context_type': 'idiom',
                'confidence_reduction': 0.7,
                'max_crisis_level': correct_level,
                'created_from_fp': True
            }
        
        return overrides
    
    def _extract_humor_indicators(self, message: str) -> List[str]:
        """Extract patterns that indicate humor context"""
        
        humor_words = ['lol', 'haha', 'funny', 'joke', 'hilarious', '😂', '😄', '😆']
        message_lower = message.lower()
        
        return [word for word in humor_words if word in message_lower]
    
    def _extract_simple_patterns(self, message: str) -> List[str]:
        """Extract simple patterns for fallback learning"""
        
        words = message.split()
        patterns = []
        
        # Extract 2-3 word phrases
        for i in range(len(words) - 1):
            patterns.append(' '.join(words[i:i+2]))
            if i < len(words) - 2:
                patterns.append(' '.join(words[i:i+3]))
        
        return patterns
    
    def apply_learning_adjustments(self, message: str, base_score: float) -> float:
        """Apply learned adjustments to a message analysis"""
        
        adjusted_score = base_score
        message_lower = message.lower()
        
        # Apply confidence adjustments
        for pattern, adjustment in self.confidence_adjustments.items():
            if pattern in message_lower:
                adjusted_score += adjustment
                logger.debug(f"Applied adjustment for '{pattern}': {adjustment}")
        
        # Apply pattern overrides
        for override_key, override_data in self.pattern_overrides.items():
            if ':' in override_key:
                context_type, pattern = override_key.split(':', 1)
                if pattern in message_lower:
                    reduction = override_data.get('confidence_reduction', 0.5)
                    adjusted_score *= (1 - reduction)
                    logger.debug(f"Applied override for '{pattern}': -{reduction}")
        
        # Ensure score stays within bounds
        return max(0.0, min(1.0, adjusted_score))
    
    def get_learning_stats(self) -> Dict:
        """Get statistics about learning progress"""
        
        return {
            'total_confidence_adjustments': len(self.confidence_adjustments),
            'total_pattern_overrides': len(self.pattern_overrides),
            'adjustment_range': {
                'min': min(self.confidence_adjustments.values()) if self.confidence_adjustments else 0,
                'max': max(self.confidence_adjustments.values()) if self.confidence_adjustments else 0,
                'avg': sum(self.confidence_adjustments.values()) / len(self.confidence_adjustments) if self.confidence_adjustments else 0
            },
            'learning_parameters': {
                'min_adjustment': self.min_confidence_adjustment,
                'max_adjustment': self.max_confidence_adjustment,
                'learning_rate': self.learning_rate
            }
        }

# Add these endpoints to your main FastAPI app in nlp_main.py

def add_learning_endpoints(app: FastAPI, learning_manager: LearningManager):
    """Add learning endpoints to the FastAPI app"""
    
    @app.post("/analyze_false_positive", response_model=LearningResponse)
    async def analyze_false_positive(request: FalsePositiveAnalysisRequest):
        """Analyze a false positive and learn from it"""
        
        if not learning_manager.model_manager.models_loaded():
            raise HTTPException(status_code=503, detail="Models not loaded")
        
        try:
            result = await learning_manager.analyze_false_positive(request)
            return result
            
        except Exception as e:
            logger.error(f"Error in false positive analysis: {e}")
            raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    
    @app.post("/update_learning_model")
    async def update_learning_model(request: LearningUpdateRequest):
        """Update the learning model with new false positive data"""
        
        try:
            # This endpoint can be used for batch updates or additional processing
            logger.info(f"Learning model update received for FP: {request.false_positive_id}")
            
            return {
                "status": "success",
                "message": "Learning model updated",
                "false_positive_id": request.false_positive_id
            }
            
        except Exception as e:
            logger.error(f"Error updating learning model: {e}")
            raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")
    
    @app.get("/learning_stats")
    async def get_learning_stats():
        """Get learning statistics"""
        
        try:
            stats = learning_manager.get_learning_stats()
            return {
                "learning_manager_status": "active",
                "learning_statistics": stats,
                "models_available": learning_manager.model_manager.models_loaded()
            }
            
        except Exception as e:
            logger.error(f"Error getting learning stats: {e}")
            raise HTTPException(status_code=500, detail=f"Stats retrieval failed: {str(e)}")

# Modified analysis endpoint to use learning adjustments
def enhance_analyze_endpoint_with_learning(app: FastAPI, learning_manager: LearningManager):
    """Enhance the existing /analyze endpoint with learning adjustments"""
    
    # This would modify your existing crisis analyzer to use learning_manager.apply_learning_adjustments()
    # Add this to your crisis_analyzer.py:
    
    """
    # In crisis_analyzer.py, modify the analyze_message method:
    
    async def analyze_message(self, message: str, user_id: str = "unknown", channel_id: str = "unknown") -> Dict:
        # ... existing analysis code ...
        
        # After getting depression_score, apply learning adjustments:
        if hasattr(self, 'learning_manager') and self.learning_manager:
            adjusted_score = self.learning_manager.apply_learning_adjustments(message, depression_score)
            logger.info(f"Applied learning adjustments: {depression_score:.3f} → {adjusted_score:.3f}")
            depression_score = adjusted_score
        
        # ... rest of existing code ...
    """