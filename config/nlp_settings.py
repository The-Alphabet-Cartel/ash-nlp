"""
Configuration settings for Enhanced Ash NLP Service - nlp_settings.py
Centralized configuration management for the NLP server
"""

import re

# Server configuration
SERVER_CONFIG = {
    "version": "4.1",
    "architecture": "modular",
    "hardware_info": {
        "cpu": "Ryzen 7 7700x",
        "gpu": "RTX 3050 (8GB VRAM)",
        "ram": "64GB",
        "inference_device": "CPU",
        "models_loaded": 2
    },
    "capabilities": {
        "crisis_analysis": "Original depression + sentiment analysis",
        "phrase_extraction": "Extract crisis keywords using model scoring",
        "pattern_learning": "Learn distinctive crisis patterns from community messages", 
        "semantic_analysis": "Enhanced crisis detection with community context",
        "community_awareness": "LGBTQIA+ specific pattern recognition"
    },
    "performance_targets": {
        "overall_accuracy": "75%+ (vs 61.7% baseline)",
        "high_crisis_detection": "95%+ (with bot's keyword detection)",
        "false_positive_rate": "<8% (vs current 15%)",
        "processing_time": "<80ms for analysis, <200ms for phrase extraction"
    },
    "cost_optimization": {
        "primary_intelligence": "Your existing depression + sentiment models",
        "claude_dependency": "Minimal - only for edge cases in bot",
        "processing_location": "Local on your AI rig - no external API costs",
        "efficiency": "Leverages existing hardware investment"
    },
    "bot_integration": {
        "phrase_extraction": "Bot calls /extract_phrases for keyword discovery",
        "pattern_learning": "Bot sends message batches to /learn_patterns daily", 
        "semantic_analysis": "Bot uses /semantic_analysis for uncertain cases",
        "cost_efficiency": "Reduces bot's Claude API usage by 80-90%"
    }
}

# Crisis level mapping thresholds
CRISIS_THRESHOLDS = {
    "high": 0.50,
    "medium": 0.22,
    "low": 0.12
}

# Context patterns for detection
POSITIVE_CONTEXT_PATTERNS = {
    'humor': ['joke', 'funny', 'hilarious', 'laugh', 'comedy', 'lol', 'haha'],
    'entertainment': ['movie', 'show', 'game', 'book', 'story', 'video'],
    'work_success': ['work', 'job', 'project', 'performance', 'success', 'achievement'],
    'food': ['hungry', 'eat', 'food', 'burger', 'pizza', 'meal'],
    'fatigue': ['tired', 'exhausted', 'sleepy', 'worn out'],
    'frustration': ['traffic', 'homework', 'test', 'exam', 'assignment']
}

IDIOM_PATTERNS = [
    (r'\b(dead|dying) (tired|exhausted)\b', 'fatigue'),
    (r'\bjoke (killed|murdered) me\b', 'humor'),
    (r'\b(that|it) (killed|murdered) me\b', 'humor'),
    (r'\bdying of laughter\b', 'humor'),
    (r'\b(killing|slaying) it\b', 'success'),
    (r'\bmurder (a|some) \w+\b', 'desire'),
    (r'\bdriving me (crazy|insane|nuts)\b', 'frustration'),
    (r'\b(brutal|killer) (test|exam|workout)\b', 'difficulty')
]

# LGBTQIA+ community patterns
LGBTQIA_PATTERNS = {
    # Family rejection patterns (HIGH crisis)
    'family_rejection': {
        'patterns': [
            r'family (rejected|disowned|kicked out|threw out) me',
            r'parents (don\'t|won\'t) (accept|love|support) me',
            r'(mom|dad|mother|father) (rejected|disowned) me',
            r'family (doesn\'t|won\'t) accept (my|me being)',
            r'(religious|conservative) family'
        ],
        'crisis_level': 'high',
        'category': 'family_rejection'
    },
    
    # Identity crisis patterns (MEDIUM)
    'identity_crisis': {
        'patterns': [
            r'(gender|trans|gay|lesbian|bi) (panic|crisis|confusion)',
            r'questioning (my|myself|everything)',
            r'(internalized|religious) (homophobia|shame|guilt)',
            r'(coming out|pride) (anxiety|stress|fear)',
            r'(closet|hiding) (suffocating|exhausting|killing me)'
        ],
        'crisis_level': 'medium',
        'category': 'identity_crisis'
    },
    
    # Dysphoria and transition patterns (MEDIUM)
    'dysphoria_transition': {
        'patterns': [
            r'(gender|body) dysphoria',
            r'(transition|dysphoria) (regret|doubt|scared|anxiety)',
            r'(deadnamed|misgendered) (me|today|again|constantly)',
            r'(passing|voice|body) (anxiety|dysphoria|stress)',
            r'(hormone|surgery) (regret|doubt|scared)'
        ],
        'crisis_level': 'medium',
        'category': 'dysphoria_transition'
    },
    
    # Discrimination and safety patterns (HIGH)
    'discrimination_safety': {
        'patterns': [
            r'(hate crime|discrimination|harassment)',
            r'(conversion therapy|pray away|religious trauma)',
            r'(unsafe|scared) (to be|being) (myself|gay|trans)',
            r'(workplace|school) (discrimination|harassment)',
            r'(violent|aggressive) (homophobia|transphobia)'
        ],
        'crisis_level': 'high',
        'category': 'discrimination_safety'
    },
    
    # Community support patterns (LOW - positive but worth tracking)
    'community_support': {
        'patterns': [
            r'(chosen|found) family',
            r'(pride|community) (support|family|love)',
            r'(lgbtq|queer) (community|support|friends)',
            r'(ally|allies) (support|help|love)'
        ],
        'crisis_level': 'low',
        'category': 'community_support'
    }
}

# Crisis context indicators
CRISIS_CONTEXTS = {
    'temporal_urgency': {
        'indicators': ['right now', 'tonight', 'today', 'immediately', 'urgent'],
        'context_type': 'temporal_urgency',
        'crisis_boost': 'high'
    },
    'intensity_amplifier': {
        'indicators': ['extremely', 'incredibly', 'absolutely', 'completely', 'totally'],
        'context_type': 'intensity_amplifier',
        'crisis_boost': 'medium'
    },
    'social_isolation': {
        'indicators': ['no one', 'nobody', 'alone', 'isolated', 'abandoned'],
        'context_type': 'social_isolation',
        'crisis_boost': 'medium'
    },
    'capability_loss': {
        'indicators': ['can\'t', 'unable', 'impossible', 'won\'t be able'],
        'context_type': 'capability_loss',
        'crisis_boost': 'medium'
    }
}

# Community vocabulary for semantic analysis
COMMUNITY_VOCABULARY = {
    'identity_terms': [
        'trans', 'transgender', 'gay', 'lesbian', 'bisexual', 'pansexual', 
        'asexual', 'queer', 'enby', 'nonbinary', 'genderfluid'
    ],
    'experience_terms': [
        'coming out', 'dysphoria', 'euphoria', 'transition', 'deadname', 
        'chosen name', 'passing', 'binding', 'misgendered'
    ],
    'community_terms': [
        'chosen family', 'found family', 'pride', 'ally', 'safe space', 
        'visibility', 'representation'
    ],
    'struggle_terms': [
        'closeted', 'discrimination', 'homophobia', 'transphobia', 
        'religious trauma', 'internalized shame'
    ]
}

# Temporal patterns for analysis
TEMPORAL_INDICATORS = {
    'immediate': ['right now', 'immediately', 'urgent', 'asap', 'tonight'],
    'recent': ['today', 'yesterday', 'lately', 'recently', 'this week'],
    'ongoing': ['always', 'constantly', 'every day', 'all the time', 'never stops'],
    'future_fear': ['never get better', 'will never', 'hopeless', 'pointless', 'no future']
}

# Context analysis weights
CONTEXT_WEIGHTS = {
    'crisis_context_words': [
        'struggling', 'difficult', 'hard', 'painful', 'scared', 'worried', 
        'anxious', 'depressed', 'rejected', 'alone', 'isolated', 'hate', 'hurt'
    ],
    'positive_context_words': [
        'proud', 'happy', 'celebrating', 'love', 'support', 'accepted', 
        'supported', 'community', 'friends', 'family'
    ]
}

# Default parameters for analysis
DEFAULT_PARAMS = {
    'phrase_extraction': {
        'min_phrase_length': 2,
        'max_phrase_length': 6,
        'crisis_focus': True,
        'community_specific': True,
        'min_confidence': 0.3,
        'max_results': 20
    },
    'pattern_learning': {
        'min_crisis_messages': 10,
        'max_phrases_to_analyze': 200,
        'min_distinctiveness_ratio': 2.0,
        'min_frequency': 3,
        'confidence_thresholds': {
            'high_confidence': 0.7,
            'medium_confidence': 0.4,
            'low_confidence': 0.1
        }
    },
    'semantic_analysis': {
        'context_window': 3,  # Words around community terms
        'boost_weights': {
            'high_relevance': 0.1,
            'medium_relevance': 0.05,
            'family_rejection': 0.15,
            'discrimination_fear': 0.15,
            'support_seeking': -0.05  # Reduces crisis level (positive)
        }
    }
}

# Negation patterns that affect interpretation
NEGATION_PATTERNS = [
    r'\bnot (really|actually|that|very|going to|planning to|trying to)\b',
    r'\bdoesn\'t (really|actually|mean|want to)\b',
    r'\bisn\'t (really|actually|that)\b',
    r'\bwon\'t (really|actually|ever)\b',
    r'\bdon\'t (want to|plan to|intend to)\b'
]

# Burden ideation patterns (often missed by models)
BURDEN_PATTERNS = [
    'better off without me', 'everyone would be better without me',
    'better off if i was gone', 'better off if i wasn\'t here',
    'nobody would miss me', 'wouldn\'t be missed'
]

# Hopelessness patterns that should be HIGH
HOPELESSNESS_PATTERNS = [
    'everything feels pointless', 'life feels pointless',
    'i hate my life', 'hate my life',
    'wish i could disappear', 'want to disappear'
]

# Struggle patterns that should be HIGH
STRUGGLE_PATTERNS = [
    'really struggling', 'struggling so much',
    'can\'t take it anymore', 'can\'t go on'
]

# Enhanced idiom patterns with context requirements
ENHANCED_IDIOM_PATTERNS = [
    {
        'patterns': [r'\b(dead|dying) (tired|exhausted|beat)\b'],
        'required_context': lambda msg: not any(word in msg.lower() for word in ['depressed', 'sad', 'hopeless', 'hate', 'kill myself']),
        'reduction_factor': 0.15,
        'max_score_after': 0.10,
        'name': 'fatigue_idiom'
    },
    {
        'patterns': [r'\b(joke|that|it) (killed|murdered) me\b', r'\bdying of laughter\b'],
        'required_context': lambda msg: any(word in msg.lower() for word in ['funny', 'hilarious', 'laugh', 'lol', 'haha']),
        'reduction_factor': 0.05,
        'max_score_after': 0.08,
        'name': 'humor_idiom'
    },
    {
        'patterns': [r'\b(killing|slaying|crushing) it\b'],
        'required_context': lambda msg: any(word in msg.lower() for word in ['work', 'job', 'performance', 'success']),
        'reduction_factor': 0.10,
        'max_score_after': 0.05,
        'name': 'success_idiom'
    },
    {
        'patterns': [r'\bmurder (a|some) \w+\b', r'\bcould kill for\b'],
        'required_context': lambda msg: any(word in msg.lower() for word in ['food', 'hungry', 'eat', 'burger', 'pizza']),
        'reduction_factor': 0.08,
        'max_score_after': 0.05,
        'name': 'food_craving_idiom'
    },
    {
        'patterns': [r'\bdriving me (crazy|insane|nuts)\b', r'\b(brutal|killer) (test|exam|homework)\b'],
        'required_context': lambda msg: any(word in msg.lower() for word in ['traffic', 'homework', 'test', 'exam', 'work']),
        'reduction_factor': 0.12,
        'max_score_after': 0.08,
        'name': 'frustration_idiom'
    }
]