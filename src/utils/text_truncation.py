"""
Ash-NLP: Crisis Detection Backend for The Alphabet Cartel Discord Community
CORE PRINCIPLE: Multi-Model Ensemble → Weighted Decision Engine → Crisis Classification
******************  CORE SYSTEM VISION (Never to be violated):  ****************
Ash-NLP is a CRISIS DETECTION BACKEND that:
1. PRIMARY: Uses BART Zero-Shot Classification for semantic crisis detection
2. CONTEXTUAL: Enhances with sentiment, irony, and emotion model signals
3. ENSEMBLE: Combines weighted model outputs through decision engine
4. PURPOSE: Detect crisis messages in Discord community communications
********************************************************************************
Text Truncation Utility for Ash-NLP Service - FE-003
---
FILE VERSION: v5.0-6-2.0-1
LAST MODIFIED: 2026-01-02
PHASE: Phase 6 - Sprint 2 (FE-003: Token Truncation)
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- FE-003: Smart text truncation for long inputs
- Preserve sentence boundaries when truncating
- Support multiple truncation strategies (smart, head, tail)
- Approximate token counting without loading tokenizer
"""

import logging
import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple

# Module version
__version__ = "v5.0-6-2.0-1"

# Initialize logger
logger = logging.getLogger(__name__)


# =============================================================================
# Enums
# =============================================================================

class TruncationStrategy(str, Enum):
    """Truncation strategy options (FE-003)."""
    
    SMART = "smart"      # Preserve sentence boundaries, prioritize recent content
    HEAD = "head"        # Keep beginning, truncate end
    TAIL = "tail"        # Keep end, truncate beginning


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class TruncationResult:
    """
    Result of text truncation (FE-003).
    
    Attributes:
        text: The truncated text
        was_truncated: Whether truncation occurred
        original_tokens: Approximate token count of original
        final_tokens: Approximate token count after truncation
        strategy_used: Which strategy was applied
    """
    text: str
    was_truncated: bool
    original_tokens: int
    final_tokens: int
    strategy_used: TruncationStrategy


# =============================================================================
# Text Truncator
# =============================================================================

class TextTruncator:
    """
    Smart text truncation for model inputs (FE-003).
    
    Handles long text inputs by intelligently truncating
    while preserving semantic meaning and sentence boundaries.
    
    Implements Clean Architecture v5.1 principles:
    - Factory function pattern (create_text_truncator)
    - Configurable via parameters
    - Resilient with safe defaults
    
    Token Estimation:
        Uses approximate 4 characters per token ratio.
        This is conservative for English text and works
        well for most Transformer models without needing
        to load the actual tokenizer.
    """
    
    # Approximate characters per token (conservative estimate)
    CHARS_PER_TOKEN = 4.0
    
    # Sentence boundary patterns
    SENTENCE_ENDINGS = re.compile(r'[.!?]+[\s]+')
    
    def __init__(
        self,
        max_tokens: int = 512,
        strategy: TruncationStrategy = TruncationStrategy.SMART,
        preserve_sentences: bool = True,
    ):
        """
        Initialize TextTruncator.
        
        Args:
            max_tokens: Maximum tokens allowed (default: 512)
            strategy: Truncation strategy (default: smart)
            preserve_sentences: Try to preserve sentence boundaries
            
        Note:
            Use create_text_truncator() factory function instead.
        """
        self.max_tokens = max_tokens
        self.strategy = strategy
        self.preserve_sentences = preserve_sentences
        
        # Calculate max characters based on token limit
        self.max_chars = int(max_tokens * self.CHARS_PER_TOKEN)
        
        logger.debug(
            f"TextTruncator initialized "
            f"(max_tokens={max_tokens}, strategy={strategy.value}, "
            f"max_chars={self.max_chars})"
        )
    
    def truncate(self, text: str) -> TruncationResult:
        """
        Truncate text if it exceeds the token limit.
        
        Args:
            text: Input text to potentially truncate
            
        Returns:
            TruncationResult with truncated text and metadata
        """
        if not text:
            return TruncationResult(
                text="",
                was_truncated=False,
                original_tokens=0,
                final_tokens=0,
                strategy_used=self.strategy,
            )
        
        # Estimate original token count
        original_tokens = self._estimate_tokens(text)
        
        # Check if truncation needed
        if original_tokens <= self.max_tokens:
            return TruncationResult(
                text=text,
                was_truncated=False,
                original_tokens=original_tokens,
                final_tokens=original_tokens,
                strategy_used=self.strategy,
            )
        
        # Apply truncation based on strategy
        if self.strategy == TruncationStrategy.SMART:
            truncated = self._smart_truncate(text)
        elif self.strategy == TruncationStrategy.HEAD:
            truncated = self._head_truncate(text)
        else:  # TAIL
            truncated = self._tail_truncate(text)
        
        final_tokens = self._estimate_tokens(truncated)
        
        logger.debug(
            f"Text truncated: {original_tokens} -> {final_tokens} tokens "
            f"(strategy: {self.strategy.value})"
        )
        
        return TruncationResult(
            text=truncated,
            was_truncated=True,
            original_tokens=original_tokens,
            final_tokens=final_tokens,
            strategy_used=self.strategy,
        )
    
    def _estimate_tokens(self, text: str) -> int:
        """
        Estimate token count based on character length.
        
        Uses a conservative 4 characters per token estimate.
        This works well for English text without needing
        the actual tokenizer.
        
        Args:
            text: Text to estimate tokens for
            
        Returns:
            Estimated token count
        """
        if not text:
            return 0
        return max(1, int(len(text) / self.CHARS_PER_TOKEN))
    
    def _smart_truncate(self, text: str) -> str:
        """
        Smart truncation that preserves sentence boundaries.
        
        Strategy:
        1. Find all sentence boundaries
        2. Keep complete sentences that fit within limit
        3. Prioritize recent content (end of text)
        4. Add ellipsis indicator if truncated
        
        Args:
            text: Text to truncate
            
        Returns:
            Truncated text with preserved sentence boundaries
        """
        if len(text) <= self.max_chars:
            return text
        
        # Split into sentences
        sentences = self._split_sentences(text)
        
        if not sentences:
            # No clear sentence boundaries, fall back to head truncation
            return self._head_truncate(text)
        
        # Build result from end (prioritize recent content)
        result_sentences = []
        current_length = 0
        ellipsis_reserve = 4  # "... " prefix
        
        for sentence in reversed(sentences):
            sentence_len = len(sentence)
            
            if current_length + sentence_len + ellipsis_reserve <= self.max_chars:
                result_sentences.insert(0, sentence)
                current_length += sentence_len
            else:
                break
        
        if not result_sentences:
            # Even one sentence is too long, truncate within sentence
            return self._head_truncate(sentences[-1])
        
        # Add ellipsis if we removed sentences
        if len(result_sentences) < len(sentences):
            return "... " + " ".join(result_sentences)
        
        return " ".join(result_sentences)
    
    def _head_truncate(self, text: str) -> str:
        """
        Simple head truncation: keep beginning, cut end.
        
        Args:
            text: Text to truncate
            
        Returns:
            Truncated text with "..." suffix
        """
        if len(text) <= self.max_chars:
            return text
        
        # Leave room for ellipsis
        cut_point = self.max_chars - 3
        
        # Try to find a word boundary
        if self.preserve_sentences:
            # Look for last space before cut point
            last_space = text[:cut_point].rfind(' ')
            if last_space > cut_point * 0.5:  # Only if we don't lose too much
                cut_point = last_space
        
        return text[:cut_point].rstrip() + "..."
    
    def _tail_truncate(self, text: str) -> str:
        """
        Tail truncation: keep end, cut beginning.
        
        Args:
            text: Text to truncate
            
        Returns:
            Truncated text with "..." prefix
        """
        if len(text) <= self.max_chars:
            return text
        
        # Leave room for ellipsis
        start_point = len(text) - self.max_chars + 3
        
        # Try to find a word boundary
        if self.preserve_sentences:
            # Look for first space after start point
            first_space = text[start_point:].find(' ')
            if first_space > 0 and first_space < len(text) * 0.2:
                start_point += first_space + 1
        
        return "..." + text[start_point:].lstrip()
    
    def _split_sentences(self, text: str) -> list:
        """
        Split text into sentences.
        
        Args:
            text: Text to split
            
        Returns:
            List of sentences
        """
        # Split on sentence endings
        parts = self.SENTENCE_ENDINGS.split(text)
        
        # Clean up and filter empty
        sentences = [s.strip() for s in parts if s.strip()]
        
        return sentences
    
    def needs_truncation(self, text: str) -> bool:
        """
        Check if text needs truncation.
        
        Args:
            text: Text to check
            
        Returns:
            True if text exceeds token limit
        """
        return self._estimate_tokens(text) > self.max_tokens
    
    def get_stats(self, text: str) -> dict:
        """
        Get statistics about text without truncating.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with token/character counts
        """
        return {
            "characters": len(text),
            "estimated_tokens": self._estimate_tokens(text),
            "max_tokens": self.max_tokens,
            "needs_truncation": self.needs_truncation(text),
            "strategy": self.strategy.value,
        }


# =============================================================================
# Factory Function
# =============================================================================

def create_text_truncator(
    max_tokens: int = 512,
    strategy: str = "smart",
    preserve_sentences: bool = True,
) -> TextTruncator:
    """
    Factory function for TextTruncator (Clean Architecture v5.1 Pattern).
    
    Args:
        max_tokens: Maximum tokens allowed (default: 512)
        strategy: Truncation strategy ("smart", "head", "tail")
        preserve_sentences: Try to preserve sentence boundaries
        
    Returns:
        Configured TextTruncator instance
        
    Example:
        >>> truncator = create_text_truncator(max_tokens=512)
        >>> result = truncator.truncate(long_text)
        >>> if result.was_truncated:
        ...     print(f"Truncated from {result.original_tokens} to {result.final_tokens}")
    """
    # Convert string strategy to enum
    strategy_enum = TruncationStrategy(strategy.lower())
    
    logger.info(f"🏭 Creating TextTruncator (max_tokens={max_tokens}, strategy={strategy})")
    
    return TextTruncator(
        max_tokens=max_tokens,
        strategy=strategy_enum,
        preserve_sentences=preserve_sentences,
    )


# =============================================================================
# Convenience Functions
# =============================================================================

def truncate_text(
    text: str,
    max_tokens: int = 512,
    strategy: str = "smart",
) -> str:
    """
    Convenience function to truncate text.
    
    Args:
        text: Text to truncate
        max_tokens: Maximum tokens
        strategy: Truncation strategy
        
    Returns:
        Truncated text (or original if no truncation needed)
    """
    truncator = create_text_truncator(max_tokens=max_tokens, strategy=strategy)
    result = truncator.truncate(text)
    return result.text


def estimate_tokens(text: str) -> int:
    """
    Convenience function to estimate token count.
    
    Args:
        text: Text to estimate
        
    Returns:
        Estimated token count
    """
    if not text:
        return 0
    return max(1, int(len(text) / TextTruncator.CHARS_PER_TOKEN))


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "TruncationStrategy",
    "TruncationResult",
    "TextTruncator",
    "create_text_truncator",
    "truncate_text",
    "estimate_tokens",
]
