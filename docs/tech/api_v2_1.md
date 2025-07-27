# 🔌 API Documentation - Ash NLP Server v2.1

> *Complete REST API reference for the enhanced learning-enabled AI crisis detection system*

[![API Documentation](https://img.shields.io/badge/API-REST-blue)](https://github.com/the-alphabet-cartel/ash-nlp)
[![Version](https://img.shields.io/badge/version-2.1-blue)](https://github.com/the-alphabet-cartel/ash-nlp/releases/tag/v2.1)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.0-green)](http://10.20.30.16:8881/docs)

**Base URL:** `http://10.20.30.16:8881`  
**Interactive Documentation:** `http://10.20.30.16:8881/docs`  
**ReDoc Documentation:** `http://10.20.30.16:8881/redoc`

---

## 📋 Table of Contents

1. [Authentication](#-authentication)
2. [Core Analysis Endpoints](#-core-analysis-endpoints)
3. [Learning System Endpoints](#-learning-system-endpoints)
4. [Health and Monitoring](#-health-and-monitoring)
5. [Analytics Endpoints](#-analytics-endpoints)
6. [Configuration Endpoints](#-configuration-endpoints)
7. [Error Handling](#-error-handling)
8. [Rate Limiting](#-rate-limiting)
9. [Integration Examples](#-integration-examples)

---

## 🔐 Authentication

### API Key Authentication (Optional)

If `API_KEY_ENABLED=true` in environment configuration:

```http
Authorization: Bearer your_api_key_here
```

### No Authentication (Default)

For internal network use, authentication is disabled by default. The API relies on network-level security within The Alphabet Cartel infrastructure.

---

## 🧠 Core Analysis Endpoints

### Analyze Message for Crisis Detection

**Primary endpoint for crisis detection with learning-enhanced AI analysis**

```http
POST /analyze
Content-Type: application/json
```

#### Request Body

```json
{
    "message": "feeling really down today",
    "user_id": "discord_user_123456789",
    "channel_id": "discord_channel_987654321",
    "context": {
        "previous_messages": ["optional", "context", "messages"],
        "user_recent_activity": "optional recent activity info",
        "channel_type": "general|support|private"
    },
    "options": {
        "include_reasoning": true,
        "include_learning_info": true,
        "confidence_threshold": 0.5
    }
}
```

#### Response (Success - 200)

```json
{
    "needs_response": true,
    "crisis_level": "medium",
    "confidence_score": 0.73,
    "original_confidence": 0.68,
    "learning_adjustment": 0.05,
    "detected_categories": [
        "moderate_depression",
        "emotional_distress"
    ],
    "method": "enhanced_ml_analysis",
    "models_used": [
        "DeBERTa-depression",
        "RoBERTa-sentiment"
    ],
    "processing_time_ms": 89.3,
    "reasoning": "Moderate distress detected with community-learned adjustment applied for subtle expression patterns",
    "learning_info": {
        "patterns_applied": 2,
        "adjustment_confidence": 0.82,
        "community_adaptation": true
    },
    "context_analysis": {
        "detected_context": "personal_expression",
        "context_confidence": 0.76,
        "filtered_contexts": ["gaming", "entertainment"]
    },
    "recommendations": {
        "response_urgency": "moderate",
        "suggested_resources": ["community_support", "mental_health_resources"],
        "follow_up_timeframe": "2-4 hours"
    },
    "metadata": {
        "analysis_id": "analysis_uuid_12345",
        "timestamp": "2025-07-27T15:30:45.123Z",
        "server_version": "2.1.0",
        "learning_system_active": true
    }
}
```

#### Response (No Crisis Detected - 200)

```json
{
    "needs_response": false,
    "crisis_level": "none",
    "confidence_score": 0.15,
    "detected_categories": [],
    "method": "enhanced_ml_analysis",
    "processing_time_ms": 67.8,
    "reasoning": "No crisis indicators detected. Message appears to be casual conversation",
    "context_analysis": {
        "detected_context": "casual_conversation",
        "context_confidence": 0.89
    }
}
```

#### Request Examples

**Basic Analysis:**
```bash
curl -X POST http://10.20.30.16:8881/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "message": "having a really tough day",
    "user_id": "123456789",
    "channel_id": "987654321"
  }'
```

**With Context:**
```bash
curl -X POST http://10.20.30.16:8881/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "message": "feeling off lately",
    "user_id": "123456789", 
    "channel_id": "987654321",
    "context": {
      "previous_messages": ["been stressed about work", "deadline tomorrow"],
      "channel_type": "general"
    },
    "options": {
      "include_reasoning": true,
      "include_learning_info": true
    }
  }'
```

### Batch Analysis

**Analyze multiple messages efficiently**

```http
POST /analyze_batch
Content-Type: application/json
```

#### Request Body

```json
{
    "messages": [
        {
            "id": "msg_1",
            "message": "feeling really down today",
            "user_id": "user_123",
            "channel_id": "channel_456"
        },
        {
            "id": "msg_2", 
            "message": "this game is killing me",
            "user_id": "user_789",
            "channel_id": "channel_456"
        }
    ],
    "options": {
        "parallel_processing": true,
        "include_reasoning": false
    }
}
```

#### Response (200)

```json
{
    "results": [
        {
            "id": "msg_1",
            "needs_response": true,
            "crisis_level": "medium",
            "confidence_score": 0.73,
            "processing_time_ms": 89.3
        },
        {
            "id": "msg_2",
            "needs_response": false,
            "crisis_level": "none", 
            "confidence_score": 0.12,
            "processing_time_ms": 67.8,
            "context_analysis": {
                "detected_context": "gaming",
                "context_confidence": 0.91
            }
        }
    ],
    "batch_stats": {
        "total_messages": 2,
        "crisis_detected": 1,
        "total_processing_time_ms": 157.1,
        "average_processing_time_ms": 78.55
    }
}
```

---

## 🧠 Learning System Endpoints

### Report False Positive

**Report when AI incorrectly flagged non-crisis content as crisis**

```http
POST /analyze_false_positive
Content-Type: application/json
```

#### Request Body

```json
{
    "message": "that boss fight totally killed me",
    "detected_level": "high",
    "correct_level": "none",
    "context": "gaming",
    "severity": 8,
    "reporter_id": "crisis_team_member_123",
    "notes": "Gaming context, player expressing frustration with difficult boss fight",
    "additional_context": {
        "channel_type": "gaming",
        "time_of_day": "evening",
        "user_gaming_activity": "active"
    }
}
```

#### Response (200)

```json
{
    "status": "success",
    "learning_applied": true,
    "pattern_id": "fp_pattern_456789",
    "adjustment_magnitude": 0.18,
    "estimated_impact": "15-20% reduction in similar false positives",
    "processing_time_ms": 45.2,
    "learned_patterns": [
        {
            "pattern_type": "context_filter",
            "pattern": "gaming_death_expressions",
            "confidence": 0.89,
            "adjustment": "reduce_sensitivity"
        }
    ],
    "conflicts_resolved": 1,
    "learning_stats": {
        "total_false_positive_reports": 824,
        "gaming_context_reports": 67,
        "accuracy_improvement": "+2.3%"
    }
}
```

### Report False Negative

**Report when AI missed actual crisis indicators**

```http
POST /analyze_false_negative
Content-Type: application/json
```

#### Request Body

```json
{
    "message": "not doing so great tbh",
    "should_detect_level": "medium",
    "currently_detected": "none",
    "context": "subtle_distress",
    "severity": 6,
    "reporter_id": "crisis_team_member_456",
    "notes": "Community member expressing subtle distress using understated language",
    "additional_context": {
        "user_recent_behavior": "withdrawn",
        "previous_interactions": "concerning",
        "community_context": "supportive"
    }
}
```

#### Response (200)

```json
{
    "status": "success",
    "learning_applied": true,
    "pattern_id": "fn_pattern_789012",
    "sensitivity_increase": 0.12,
    "estimated_impact": "10-15% improvement in similar detections",
    "processing_time_ms": 52.7,
    "learned_patterns": [
        {
            "pattern_type": "subtle_crisis",
            "pattern": "understated_distress_expressions",
            "confidence": 0.76,
            "adjustment": "increase_sensitivity"
        }
    ],
    "conflicts_checked": 3,
    "validation_passed": true,
    "learning_stats": {
        "total_false_negative_reports": 425,
        "subtle_distress_reports": 89,
        "detection_improvement": "+1.8%"
    }
}
```

### Learning Statistics

**Get comprehensive learning system statistics and performance metrics**

```http
GET /learning_statistics
```

#### Response (200)

```json
{
    "system_status": "active",
    "learning_enabled": true,
    "last_update": "2025-07-27T15:45:30.123Z",
    "total_adjustments": 1247,
    "adjustment_breakdown": {
        "false_positive_reductions": 823,
        "false_negative_improvements": 424,
        "pattern_refinements": 156
    },
    "accuracy_metrics": {
        "overall_accuracy": 0.91,
        "accuracy_improvement": "+23.4%",
        "false_positive_rate": 0.041,
        "false_negative_rate": 0.052,
        "baseline_comparison": {
            "accuracy_before": 0.74,
            "accuracy_after": 0.91,
            "improvement": "+17 percentage points"
        }
    },
    "learning_rate_info": {
        "current_rate": 0.1,
        "adaptive_adjustments": 12,
        "performance_trend": "improving"
    },
    "daily_limits": {
        "max_adjustments": 100,
        "used_today": 23,
        "remaining": 77,
        "reset_time": "2025-07-28T00:00:00Z"
    },
    "pattern_statistics": {
        "total_patterns": 1089,
        "effective_patterns": 967,
        "ineffective_patterns": 122,
        "effectiveness_rate": 0.888,
        "most_effective_categories": [
            "gaming_context_filters",
            "subtle_lgbtq_distress",
            "work_stress_indicators"
        ]
    },
    "community_adaptation": {
        "adaptation_score": 0.87,
        "new_terminology_learned": 23,
        "context_understanding": 0.92,
        "cultural_sensitivity": 0.89
    },
    "recent_learning": [
        {
            "pattern_id": "recent_123",
            "type": "false_positive",
            "impact": "gaming context learning",
            "applied_at": "2025-07-27T14:30:00Z",
            "effectiveness": 0.83
        },
        {
            "pattern_id": "recent_124",
            "type": "false_negative",
            "impact": "subtle distress detection",
            "applied_at": "2025-07-27T13:15:00Z",
            "effectiveness": 0.76
        }
    ]
}
```

### Learning Effectiveness Report

**Get detailed analysis of learning system effectiveness over time**

```http
GET /learning_effectiveness_report?period={period}&include_details={boolean}
```

#### Parameters

- `period`: `7days`, `30days`, `90days`, `6months`, `1year`
- `include_details`: `true` or `false` (default: `false`)

#### Response (200)

```json
{
    "report_period": "2025-06-27 to 2025-07-27",
    "generated_at": "2025-07-27T16:00:00Z",
    "executive_summary": {
        "overall_performance": "excellent",
        "key_achievements": [
            "18% reduction in false positives",
            "12% improvement in subtle crisis detection", 
            "Successfully learned 23 new community patterns"
        ],
        "areas_for_improvement": [
            "Academic stress context still generating some false positives",
            "Need more training on generational language differences"
        ],
        "recommendation_priority": "high"
    },
    "detailed_metrics": {
        "accuracy_trend": {
            "period_start": 0.87,
            "period_end": 0.91,
            "peak_accuracy": 0.93,
            "average_accuracy": 0.89,
            "improvement_percentage": "+4.6%",
            "trend_direction": "improving",
            "weekly_data": [0.87, 0.88, 0.90, 0.91]
        },
        "learning_activity": {
            "total_feedback_reports": 156,
            "false_positive_reports": 98,
            "false_negative_reports": 58,
            "patterns_learned": 34,
            "patterns_refined": 23,
            "patterns_deprecated": 7
        },
        "community_adaptation": {
            "new_terminology_learned": 12,
            "context_improvements": 28,
            "language_evolution_tracking": "active",
            "cultural_sensitivity_score": 0.89
        },
        "performance_impact": {
            "crisis_response_time_reduction": "23%",
            "team_workload_reduction": "18%",
            "community_satisfaction": "increased",
            "false_alert_fatigue": "significantly_reduced"
        }
    },
    "pattern_analysis": {
        "most_effective_patterns": [
            {
                "pattern_id": "gaming_context_filter",
                "type": "false_positive_reduction",
                "impact_percentage": 32,
                "applications": 87,
                "effectiveness_score": 0.91,
                "description": "Filters gaming death/violence expressions"
            },
            {
                "pattern_id": "subtle_lgbtq_distress",
                "type": "false_negative_improvement",
                "impact_percentage": 28,
                "applications": 23,
                "effectiveness_score": 0.84,
                "description": "Detects identity-related crisis expressions"
            }
        ],
        "emerging_patterns": [
            "academic_stress_with_identity_context",
            "social_media_comparison_distress", 
            "weather_metaphor_depression",
            "pandemic_fatigue_expressions"
        ],
        "pattern_conflicts_resolved": 12,
        "deprecated_patterns": [
            {
                "pattern_id": "outdated_slang_filter",
                "reason": "language_evolution",
                "deprecated_at": "2025-07-20T10:00:00Z"
            }
        ]
    },
    "recommendations": [
        {
            "priority": "high",
            "category": "accuracy_improvement",
            "recommendation": "Increase gaming context pattern weights by 10%",
            "expected_impact": "+2-3% accuracy",
            "implementation_effort": "low"
        },
        {
            "priority": "medium", 
            "category": "new_patterns",
            "recommendation": "Add specific patterns for academic deadline stress",
            "expected_impact": "+1-2% accuracy",
            "implementation_effort": "medium"
        }
    ]
}
```

---

## 🏥 Health and Monitoring

### Health Check

**Basic health status of the NLP server**

```http
GET /health
```

#### Response (200 - Healthy)

```json
{
    "status": "healthy",
    "timestamp": "2025-07-27T16:00:00.123Z",
    "version": "2.1.0",
    "uptime_seconds": 2847639,
    "services": {
        "ai_models": "loaded",
        "learning_system": "active",
        "database": "connected",
        "analytics": "running"
    },
    "quick_stats": {
        "requests_processed": 15847,
        "average_response_time_ms": 87.3,
        "learning_adjustments_today": 23
    }
}
```

#### Response (503 - Unhealthy)

```json
{
    "status": "unhealthy",
    "timestamp": "2025-07-27T16:00:00.123Z",
    "version": "2.1.0",
    "issues": [
        "AI models not loaded",
        "Learning system inactive"
    ],
    "services": {
        "ai_models": "error",
        "learning_system": "inactive",
        "database": "connected",
        "analytics": "running"
    }
}
```

### Detailed System Status

**Comprehensive system health and performance information**

```http
GET /system_status
```

#### Response (200)

```json
{
    "system_info": {
        "version": "2.1.0",
        "build_date": "2025-07-25T12:00:00Z",
        "python_version": "3.11.5",
        "platform": "Linux-6.2.0-docker",
        "container_id": "ash_nlp_server"
    },
    "hardware_status": {
        "cpu_usage": 24.7,
        "memory_usage": {
            "used_gb": 4.2,
            "total_gb": 8.0,
            "percentage": 52.5
        },
        "gpu_status": {
            "available": true,
            "device": "NVIDIA RTX 3050",
            "memory_used_gb": 2.1,
            "memory_total_gb": 8.0,
            "utilization_percentage": 26.3
        },
        "disk_usage": {
            "models_cache_gb": 3.8,
            "learning_data_gb": 0.3,
            "logs_gb": 0.1,
            "total_used_gb": 4.2
        }
    },
    "ai_models": {
        "depression_model": {
            "name": "rafalposwiata/deproberta-large-depression",
            "status": "loaded",
            "load_time_ms": 3247,
            "memory_usage_gb": 1.8,
            "device": "cuda"
        },
        "sentiment_model": {
            "name": "cardiffnlp/twitter-roberta-base-sentiment-latest",
            "status": "loaded",
            "load_time_ms": 1856,
            "memory_usage_gb": 1.2,
            "device": "cuda"
        }
    },
    "learning_system": {
        "status": "active",
        "patterns_loaded": 1089,
        "adjustments_today": 23,
        "last_learning_event": "2025-07-27T15:45:30Z",
        "effectiveness_score": 0.91,
        "memory_usage_mb": 287
    },
    "performance_metrics": {
        "requests_per_minute": 45.2,
        "average_response_time_ms": 87.3,
        "p95_response_time_ms": 156.8,
        "error_rate_percentage": 0.12,
        "cache_hit_rate_percentage": 78.4
    },
    "database_status": {
        "learning_patterns": "connected",
        "analytics_data": "connected",
        "backup_status": "current",
        "last_backup": "2025-07-27T01:00:00Z"
    }
}
```

### Performance Metrics

**Real-time performance and usage statistics**

```http
GET /performance_metrics?period={period}
```

#### Parameters

- `period`: `1hour`, `24hours`, `7days`, `30days`

#### Response (200)

```json
{
    "metrics_period": "24hours",
    "collected_at": "2025-07-27T16:00:00Z",
    "request_metrics": {
        "total_requests": 2847,
        "successful_requests": 2834,
        "failed_requests": 13,
        "success_rate": 0.9954,
        "requests_per_hour": [
            {"hour": "2025-07-27T15:00:00Z", "count": 124},
            {"hour": "2025-07-27T14:00:00Z", "count": 118},
            {"hour": "2025-07-27T13:00:00Z", "count": 142}
        ]
    },
    "response_time_metrics": {
        "average_ms": 87.3,
        "median_ms": 76.8,
        "p95_ms": 156.8,
        "p99_ms": 234.5,
        "max_ms": 456.2,
        "min_ms": 23.1
    },
    "crisis_detection_metrics": {
        "total_analyses": 2847,
        "crisis_detected": 234,
        "crisis_rate": 0.082,
        "breakdown": {
            "high_crisis": 23,
            "medium_crisis": 89,
            "low_crisis": 122,
            "no_crisis": 2613
        }
    },
    "learning_metrics": {
        "learning_events": 23,
        "false_positive_reports": 15,
        "false_negative_reports": 8,
        "accuracy_improvement": "+0.7%",
        "patterns_updated": 19
    },
    "resource_usage": {
        "cpu_average": 24.7,
        "cpu_peak": 67.3,
        "memory_average_gb": 4.2,
        "memory_peak_gb": 5.1,
        "gpu_utilization_average": 26.3,
        "gpu_memory_usage_gb": 2.1
    }
}
```

---

## 📊 Analytics Endpoints

### Community Language Analysis

**Analyze community language patterns and evolution**

```http
GET /community_language_analysis?period={period}
```

#### Parameters

- `period`: `7days`, `30days`, `90days`

#### Response (200)

```json
{
    "analysis_period": "30days",
    "generated_at": "2025-07-27T16:00:00Z",
    "language_evolution": {
        "new_patterns_detected": 23,
        "evolving_terminology": [
            {
                "term": "feeling sus",
                "frequency_change": "+147%",
                "context": "anxiety/uncertainty",
                "first_detected": "2025-07-05T00:00:00Z"
            },
            {
                "term": "not vibing",
                "frequency_change": "+89%", 
                "context": "mild_distress",
                "first_detected": "2025-07-12T00:00:00Z"
            },
            {
                "term": "struggling fr",
                "frequency_change": "+67%",
                "context": "moderate_crisis",
                "first_detected": "2025-07-18T00:00:00Z"
            }
        ],
        "context_shifts": [
            {
                "term": "dead",
                "previous_contexts": ["fatigue: 60%", "gaming: 30%", "humor: 10%"],
                "current_contexts": ["gaming: 45%", "humor: 30%", "fatigue: 25%"],
                "shift_significance": "moderate"
            },
            {
                "term": "killed",
                "previous_contexts": ["gaming: 70%", "humor: 20%", "work: 10%"],
                "current_contexts": ["gaming: 75%", "humor: 15%", "work: 10%"],
                "shift_significance": "minor"
            }
        ]
    },
    "community_adaptation": {
        "lgbtqia_terminology": {
            "adaptation_score": 0.89,
            "recognition_rate": 0.94,
            "new_terms_learned": 7,
            "cultural_sensitivity": "high"
        },
        "generational_language": {
            "adaptation_score": 0.76,
            "recognition_rate": 0.82,
            "emerging_slang_tracking": "active",
            "learning_velocity": "moderate"
        },
        "server_specific_slang": {
            "adaptation_score": 0.91,
            "unique_expressions": 34,
            "community_phrases": 18,
            "inside_jokes_filter": "effective"
        }
    },
    "sentiment_trends": {
        "overall_community_sentiment": "stable_positive",
        "crisis_indicator_trends": "stable",
        "support_seeking_patterns": "healthy",
        "community_resilience": "high"
    },
    "recommendations": [
        {
            "priority": "high",
            "type": "pattern_addition",
            "recommendation": "Add pattern for 'sus' in anxiety/uncertainty contexts",
            "rationale": "147% increase in usage, becoming standard anxiety expression",
            "implementation": "create_context_pattern"
        },
        {
            "priority": "medium",
            "type": "pattern_refinement", 
            "recommendation": "Monitor 'fr' (for real) usage in distress expressions",
            "rationale": "Emerging as intensity modifier for genuine distress",
            "implementation": "track_modifier_patterns"
        }
    ]
}
```

### Crisis Trend Analysis

**Analyze crisis detection trends and community mental health patterns**

```http
GET /crisis_trend_analysis?period={period}&anonymized={boolean}
```

#### Parameters

- `period`: `7days`, `30days`, `90days`, `6months`
- `anonymized`: `true` or `false` (default: `true`)

#### Response (200)

```json
{
    "analysis_period": "30days",
    "anonymized": true,
    "generated_at": "2025-07-27T16:00:00Z",
    "overall_trends": {
        "total_messages_analyzed": 15847,
        "crisis_detection_rate": 0.082,
        "trend_direction": "stable",
        "severity_distribution": {
            "high_crisis": 0.014,
            "medium_crisis": 0.032,
            "low_crisis": 0.036,
            "no_crisis": 0.918
        }
    },
    "temporal_patterns": {
        "daily_patterns": {
            "peak_hours": ["20:00-22:00", "14:00-16:00"],
            "low_hours": ["04:00-08:00"],
            "weekend_vs_weekday": {
                "weekend_rate": 0.089,
                "weekday_rate": 0.078,
                "difference": "+14% higher on weekends"
            }
        },
        "weekly_trends": [
            {"week": "2025-07-21", "crisis_rate": 0.084},
            {"week": "2025-07-14", "crisis_rate": 0.079},
            {"week": "2025-07-07", "crisis_rate": 0.081},
            {"week": "2025-06-30", "crisis_rate": 0.083}
        ],
        "seasonal_factors": {
            "current_season_impact": "mild_summer_stability",
            "expected_seasonal_changes": "academic_year_preparation_stress"
        }
    },
    "category_trends": {
        "depression_indicators": {
            "trend": "stable",
            "rate": 0.047,
            "change": "-2.1% from previous period"
        },
        "anxiety_indicators": {
            "trend": "slight_increase",
            "rate": 0.039,
            "change": "+5.4% from previous period"
        },
        "identity_crisis": {
            "trend": "stable",
            "rate": 0.018,
            "change": "+1.2% from previous period"
        },
        "relationship_distress": {
            "trend": "decreasing",
            "rate": 0.023,
            "change": "-7.8% from previous period"
        }
    },
    "community_health_indicators": {
        "support_engagement": "high",
        "peer_support_activity": "active",
        "resource_utilization": "healthy",
        "early_intervention_success": "effective",
        "community_resilience_score": 0.87
    },
    "risk_factors": {
        "identified_risk_periods": [
            {
                "period": "Sunday evenings",
                "risk_level": "moderate",
                "pattern": "Sunday scaries + social anxiety"
            }
        ],
        "protective_factors": [
            "active peer support network",
            "responsive crisis team",
            "accessible mental health resources"
        ]
    },
    "recommendations": [
        {
            "category": "preventive_care",
            "recommendation": "Increase peer support outreach on Sunday evenings",
            "rationale": "14% higher crisis detection on weekend nights",
            "implementation": "schedule_proactive_check_ins"
        },
        {
            "category": "resource_allocation",
            "recommendation": "Maintain current crisis response capacity",
            "rationale": "Crisis rates stable, intervention effectiveness high",
            "implementation": "status_quo_with_monitoring"
        }
    ]
}
```

---

## ⚙️ Configuration Endpoints

### Get Current Configuration

**Retrieve current learning system configuration (admin only)**

```http
GET /configuration
```

#### Response (200)

```json
{
    "learning_system": {
        "enabled": true,
        "learning_rate": 0.1,
        "max_adjustments_per_day": 100,
        "max_adjustments_per_hour": 10,
        "min_confidence_adjustment": 0.02,
        "max_confidence_adjustment": 0.20,
        "min_severity_for_learning": 4,
        "require_feedback_validation": true,
        "adaptive_threshold_enabled": true
    },
    "crisis_thresholds": {
        "high": 0.50,
        "medium": 0.22,
        "low": 0.12
    },
    "performance_settings": {
        "max_concurrent_requests": 20,
        "request_timeout": 30,
        "batch_processing_enabled": true,
        "async_processing": true
    },
    "ai_models": {
        "depression_model": "rafalposwiata/deproberta-large-depression",
        "sentiment_model": "cardiffnlp/twitter-roberta-base-sentiment-latest",
        "device": "auto",
        "precision": "float16"
    },
    "data_retention": {
        "learning_data_days": 365,
        "analytics_data_days": 180,
        "logs_retention_days": 30
    }
}
```

### Update Configuration

**Update learning system configuration (admin only)**

```http
PUT /configuration
Content-Type: application/json
```

#### Request Body

```json
{
    "learning_system": {
        "learning_rate": 0.12,
        "max_adjustments_per_day": 120
    },
    "crisis_thresholds": {
        "medium": 0.25
    }
}
```

#### Response (200)

```json
{
    "status": "success",
    "updated_settings": [
        "learning_system.learning_rate",
        "learning_system.max_adjustments_per_day",
        "crisis_thresholds.medium"
    ],
    "requires_restart": false,
    "applied_at": "2025-07-27T16:30:00Z"
}
```

---

## ⚠️ Error Handling

### Standard Error Response Format

All errors follow a consistent format:

```json
{
    "error": {
        "code": "ERROR_CODE",
        "message": "Human readable error message",
        "details": "Additional technical details",
        "timestamp": "2025-07-27T16:00:00Z",
        "request_id": "req_12345"
    }
}
```

### Common Error Codes

#### 400 Bad Request

```json
{
    "error": {
        "code": "INVALID_REQUEST",
        "message": "Message field is required",
        "details": "The 'message' field must be provided and cannot be empty",
        "timestamp": "2025-07-27T16:00:00Z",
        "request_id": "req_12345"
    }
}
```

#### 422 Unprocessable Entity

```json
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Severity must be between 1 and 10",
        "details": "Received severity value: 15. Valid range is 1-10",
        "timestamp": "2025-07-27T16:00:00Z",
        "request_id": "req_12346"
    }
}
```

#### 429 Too Many Requests

```json
{
    "error": {
        "code": "RATE_LIMIT_EXCEEDED",
        "message": "Learning adjustment limit exceeded",
        "details": "Daily limit of 100 learning adjustments reached. Resets at midnight UTC",
        "timestamp": "2025-07-27T16:00:00Z",
        "request_id": "req_12347",
        "retry_after": "2025-07-28T00:00:00Z"
    }
}
```

#### 500 Internal Server Error

```json
{
    "error": {
        "code": "AI_MODEL_ERROR",
        "message": "AI model analysis failed",
        "details": "Depression model returned invalid output. Check model status",
        "timestamp": "2025-07-27T16:00:00Z",
        "request_id": "req_12348"
    }
}
```

#### 503 Service Unavailable

```json
{
    "error": {
        "code": "LEARNING_SYSTEM_UNAVAILABLE",
        "message": "Learning system is temporarily unavailable",
        "details": "Learning system is performing maintenance. Crisis detection still available",
        "timestamp": "2025-07-27T16:00:00Z",
        "request_id": "req_12349",
        "estimated_recovery": "2025-07-27T16:15:00Z"
    }
}
```

---

## 🚦 Rate Limiting

### Default Rate Limits

- **Analysis requests**: 60 per minute per IP
- **Learning feedback**: 10 per minute per reporter
- **Batch analysis**: 5 per minute per IP
- **Analytics requests**: 20 per minute per IP

### Rate Limit Headers

```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1690464000
X-RateLimit-Retry-After: 15
```

### Rate Limit Configuration

Can be adjusted via environment variables:

```bash
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS_PER_MINUTE=60
RATE_LIMIT_BURST_SIZE=10
RATE_LIMIT_LEARNING_REQUESTS=10
```

---

## 🔗 Integration Examples

### Ash Bot Integration

```python
# Example integration from Ash Discord bot
import aiohttp
import asyncio
from typing import Optional, Dict, Any

class NLPClient:
    def __init__(self, base_url: str = "http://10.20.30.16:8881"):
        self.base_url = base_url
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def analyze_message(
        self, 
        message: str, 
        user_id: str, 
        channel_id: str,
        include_reasoning: bool = True
    ) -> Dict[str, Any]:
        """Analyze message for crisis detection"""
        
        payload = {
            "message": message,
            "user_id": user_id,
            "channel_id": channel_id,
            "options": {
                "include_reasoning": include_reasoning,
                "include_learning_info": True
            }
        }
        
        try:
            async with self.session.post(
                f"{self.base_url}/analyze",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_data = await response.json()
                    raise Exception(f"NLP API Error: {error_data}")
                    
        except asyncio.TimeoutError:
            # Fallback to keyword detection
            return self.fallback_analysis(message)
        except Exception as e:
            # Log error and use fallback
            print(f"NLP service error: {e}")
            return self.fallback_analysis(message)
    
    async def report_false_positive(
        self, 
        message: str, 
        detected_level: str,
        context: str,
        severity: int,
        reporter_id: str
    ) -> Dict[str, Any]:
        """Report false positive for learning"""
        
        payload = {
            "message": message,
            "detected_level": detected_level,
            "correct_level": "none",
            "context": context,
            "severity": severity,
            "reporter_id": reporter_id,
            "notes": f"False positive reported by Crisis Response team"
        }
        
        async with self.session.post(
            f"{self.base_url}/analyze_false_positive",
            json=payload
        ) as response:
            return await response.json()
    
    def fallback_analysis(self, message: str) -> Dict[str, Any]:
        """Fallback keyword-based analysis when NLP unavailable"""
        # Implement basic keyword detection as fallback
        return {
            "needs_response": False,
            "crisis_level": "none", 
            "confidence_score": 0.0,
            "method": "keyword_fallback",
            "reasoning": "NLP service unavailable, using keyword fallback"
        }

# Usage in Discord bot
async def on_message(message):
    if message.author.bot:
        return
    
    async with NLPClient() as nlp:
        result = await nlp.analyze_message(
            message=message.content,
            user_id=str(message.author.id),
            channel_id=str(message.channel.id)
        )
        
        if result["needs_response"] and result["crisis_level"] in ["medium", "high"]:
            # Alert Crisis Response team
            await alert_crisis_team(message, result)
```

### Analytics Dashboard Integration

```javascript
// Example integration for ash-dash analytics dashboard
class NLPAnalyticsClient {
    constructor(baseUrl = 'http://10.20.30.16:8881') {
        this.baseUrl = baseUrl;
    }
    
    async getLearningStatistics() {
        const response = await fetch(`${this.baseUrl}/learning_statistics`);
        return await response.json();
    }
    
    async getCrisisTrends(period = '30days') {
        const response = await fetch(
            `${this.baseUrl}/crisis_trend_analysis?period=${period}&anonymized=true`
        );
        return await response.json();
    }
    
    async getPerformanceMetrics(period = '24hours') {
        const response = await fetch(
            `${this.baseUrl}/performance_metrics?period=${period}`
        );
        return await response.json();
    }
    
    async getSystemHealth() {
        const response = await fetch(`${this.baseUrl}/system_status`);
        return await response.json();
    }
    
    // Real-time dashboard updates
    async updateDashboard() {
        try {
            const [stats, trends, performance, health] = await Promise.all([
                this.getLearningStatistics(),
                this.getCrisisTrends(),
                this.getPerformanceMetrics(),
                this.getSystemHealth()
            ]);
            
            // Update dashboard components
            this.updateLearningStats(stats);
            this.updateCrisisTrends(trends);
            this.updatePerformanceCharts(performance);
            this.updateHealthIndicators(health);
            
        } catch (error) {
            console.error('Dashboard update failed:', error);
            this.showError('Unable to update dashboard data');
        }
    }
    
    // Schedule automatic updates
    startAutoUpdate(intervalMs = 30000) {
        setInterval(() => this.updateDashboard(), intervalMs);
    }
}

// Usage in dashboard
const nlpClient = new NLPAnalyticsClient();
nlpClient.startAutoUpdate(30000); // Update every 30 seconds
```

### Testing Suite Integration

```python
# Example integration for ash-thrash testing suite
import requests
import time
from typing import List, Dict, Any

class NLPTestClient:
    def __init__(self, base_url: str = "http://10.20.30.16:8881"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def test_crisis_detection_accuracy(self, test_cases: List[Dict]) -> Dict[str, Any]:
        """Test crisis detection accuracy with known test cases"""
        
        results = {
            "total_tests": len(test_cases),
            "correct_predictions": 0,
            "false_positives": 0,
            "false_negatives": 0,
            "test_results": []
        }
        
        for test_case in test_cases:
            try:
                response = self.session.post(
                    f"{self.base_url}/analyze",
                    json={
                        "message": test_case["message"],
                        "user_id": "test_user",
                        "channel_id": "test_channel"
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    predicted_level = result["crisis_level"]
                    expected_level = test_case["expected_level"]
                    
                    test_result = {
                        "message": test_case["message"],
                        "expected": expected_level,
                        "predicted": predicted_level,
                        "confidence": result["confidence_score"],
                        "correct": predicted_level == expected_level,
                        "processing_time_ms": result.get("processing_time_ms", 0)
                    }
                    
                    if predicted_level == expected_level:
                        results["correct_predictions"] += 1
                    elif predicted_level != "none" and expected_level == "none":
                        results["false_positives"] += 1
                    elif predicted_level == "none" and expected_level != "none":
                        results["false_negatives"] += 1
                    
                    results["test_results"].append(test_result)
                    
                else:
                    print(f"API Error: {response.status_code}")
                    
            except Exception as e:
                print(f"Test error for '{test_case['message']}': {e}")
        
        results["accuracy"] = results["correct_predictions"] / results["total_tests"]
        results["false_positive_rate"] = results["false_positives"] / results["total_tests"]
        results["false_negative_rate"] = results["false_negatives"] / results["total_tests"]
        
        return results
    
    def test_learning_system(self) -> Dict[str, Any]:
        """Test learning system functionality"""
        
        # Test false positive reporting
        fp_response = self.session.post(
            f"{self.base_url}/analyze_false_positive",
            json={
                "message": "this test is killing me",
                "detected_level": "high",
                "correct_level": "none",
                "context": "testing",
                "severity": 5,
                "reporter_id": "test_suite"
            }
        )
        
        # Test learning statistics
        stats_response = self.session.get(f"{self.base_url}/learning_statistics")
        
        return {
            "false_positive_reporting": fp_response.status_code == 200,
            "learning_statistics": stats_response.status_code == 200,
            "learning_system_active": stats_response.json().get("system_status") == "active" if stats_response.status_code == 200 else False
        }

# Usage in test suite
def run_comprehensive_nlp_test():
    client = NLPTestClient()
    
    # Define test cases
    test_cases = [
        {"message": "I want to end it all", "expected_level": "high"},
        {"message": "this game is killing me", "expected_level": "none"},
        {"message": "feeling really down lately", "expected_level": "medium"},
        {"message": "having a great day!", "expected_level": "none"}
    ]
    
    # Run accuracy test
    accuracy_results = client.test_crisis_detection_accuracy(test_cases)
    
    # Test learning system
    learning_results = client.test_learning_system()
    
    # Generate report
    report = {
        "test_timestamp": time.time(),
        "accuracy_results": accuracy_results,
        "learning_system_results": learning_results,
        "overall_health": "healthy" if accuracy_results["accuracy"] > 0.85 else "needs_attention"
    }
    
    return report
```

---

## 📞 Support and Resources

### API Support

**Getting Help:**
- **Interactive Documentation:** `http://10.20.30.16:8881/docs` - Test endpoints directly
- **GitHub Issues:** [Report API bugs and request features](https://github.com/the-alphabet-cartel/ash-nlp/issues)
- **Discord Support:** [The Alphabet Cartel Server](https://discord.gg/alphabetcartel) #tech-support
- **Email Support:** For urgent API integration issues

**Community Resources:**
- **Integration Examples:** Complete code samples in repository
- **Best Practices:** Community-developed integration patterns
- **Performance Optimization:** Hardware-specific tuning guides
- **Troubleshooting:** Common integration issues and solutions

### Related Documentation

**Technical Guides:**
- **[Implementation Guide](implementation_guide.md)** - Complete deployment and setup
- **[Learning System Guide](learning_system.md)** - Advanced learning features
- **[Team Guide](team_guide.md)** - Crisis Response team procedures
- **[Troubleshooting Guide](troubleshooting.md)** - Common issues and solutions

**System Integration:**
- **[Main Ash Bot](https://github.com/the-alphabet-cartel/ash)** - Discord bot integration
- **[Analytics Dashboard](https://github.com/the-alphabet-cartel/ash-dash)** - Metrics visualization
- **[Testing Suite](https://github.com/the-alphabet-cartel/ash-thrash)** - Automated testing

---

**🌟 The API is designed for high availability, low latency, and seamless integration with The Alphabet Cartel ecosystem. All endpoints are optimized for real-time crisis detection while providing comprehensive learning and analytics capabilities.**

**💜 Thank you for using the Ash NLP API to help keep our community safe and supported!**

---

*For technical questions about this API documentation, create a GitHub issue or contact the technical team via Discord.*

**Last Updated:** July 27, 2025 | **API Version:** 2.1 | **Documentation Status:** Active