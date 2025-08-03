{
  "models_configuration": {
    "depression_model": "${NLP_DEPRESSION_MODEL}",
    "sentiment_model": "${NLP_SENTIMENT_MODEL}",
    "emotional_distress_model": "${NLP_EMOTIONAL_DISTRESS_MODEL}",
    "cache_dir": "${NLP_MODEL_CACHE_DIR}",
    "huggingface_token": "${GLOBAL_HUGGINGFACE_TOKEN}",
    "ensemble_mode": "${NLP_ENSEMBLE_MODE}",
    "depression_weight": "${NLP_DEPRESSION_MODEL_WEIGHT}",
    "sentiment_weight": "${NLP_SENTIMENT_MODEL_WEIGHT}",
    "emotional_distress_weight": "${NLP_EMOTIONAL_DISTRESS_MODEL_WEIGHT}",
    "gap_detection_enabled": "${NLP_GAP_DETECTION_ENABLED}",
    "disagreement_threshold": "${NLP_DISAGREEMENT_THRESHOLD}"
  },
  "hardware_configuration": {
    "device": "${NLP_DEVICE}",
    "precision": "${NLP_MODEL_PRECISION}",
    "max_batch_size": "${NLP_MAX_BATCH_SIZE}",
    "use_fast_tokenizer": "${NLP_USE_FAST_TOKENIZER}",
    "trust_remote_code": "${NLP_TRUST_REMOTE_CODE}",
    "model_revision": "${NLP_MODEL_REVISION}"
  },
  "model_defaults": {
    "depression_model": "MoritzLaurer/deberta-v3-base-zeroshot-v2.0",
    "sentiment_model": "MoritzLaurer/mDeBERTa-v3-base-mnli-xnli",
    "emotional_distress_model": "Lowerated/lm6-deberta-v3-topic-sentiment",
    "cache_dir": "./models/cache",
    "ensemble_mode": "majority",
    "depression_weight": 0.5,
    "sentiment_weight": 0.2,
    "emotional_distress_weight": 0.3,
    "gap_detection_enabled": true,
    "disagreement_threshold": 2,
    "device": "auto",
    "precision": "float16",
    "max_batch_size": 32,
    "use_fast_tokenizer": true,
    "trust_remote_code": false,
    "model_revision": "main"
  },
  "model_metadata": {
    "ensemble_architecture": "three_model_consensus",
    "version": "3.1",
    "migration_phase": "phase_2",
    "models": {
      "depression": {
        "type": "DeBERTa-based classification",
        "labels": ["crisis", "mild_crisis", "negative", "neutral", "positive"],
        "purpose": "Primary crisis classification",
        "specialization": "Depression and suicidal ideation detection"
      },
      "sentiment": {
        "type": "mDeBERTa-based sentiment analysis", 
        "labels": ["very_negative", "negative", "neutral", "positive", "very_positive"],
        "purpose": "Contextual validation and enhancement",
        "specialization": "Emotional tone and context analysis"
      },
      "emotional_distress": {
        "type": "DistilBERT-based emotional classification",
        "labels": ["high_distress", "medium_distress", "low_distress", "minimal_distress"],
        "purpose": "Emotional distress and stress detection",
        "specialization": "General emotional distress and mental strain"
      }
    },
    "ensemble_features": {
      "gap_detection": "Identifies disagreements between models for manual review",
      "consensus_building": "Combines predictions using configurable ensemble modes",
      "confidence_spreading": "Analyzes confidence distribution across models",
      "disagreement_flagging": "Auto-flags cases requiring staff review"
    }
  }
}