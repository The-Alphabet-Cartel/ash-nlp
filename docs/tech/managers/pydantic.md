<!-- ash-nlp/docs/tech/managers/pydantic.md -->
<!--
Pydantic Manager Documentation for Ash-NLP Service
FILE VERSION: v3.1-1
LAST MODIFIED: 2025-08-26
PHASE: 3e
CLEAN ARCHITECTURE: v3.1 Compliant
-->
# Pydantic Manager Documentation

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp
**Project**: Ash-NLP v3.1
**Community**: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
**FILE VERSION**: v3.1-1
**LAST UPDATED**: 2025-08-26
**CLEAN ARCHITECTURE**: v3.1 Compliant

---

# PydanticManager Documentation

The PydanticManager handles Pydantic model management, data validation, and schema enforcement for the Ash-NLP crisis detection system, ensuring robust data validation and type safety across all system components.

---

## Overview

PydanticManager provides centralized management of Pydantic models, data validation schemas, and type enforcement, ensuring data integrity and consistency throughout the crisis detection pipeline with special attention to LGBTQIA+ community safety data validation.

### Core Responsibilities
- **Pydantic model registration** - Centralized registration and management of all Pydantic models
- **Data validation orchestration** - Coordination of data validation across system components
- **Schema enforcement** - Ensuring consistent data schemas throughout the system
- **Type safety management** - Runtime type checking and validation for critical data structures
- **API data validation** - Request/response validation for all API endpoints

### Phase 3e Consolidation Impact
- **Configuration pattern standardization** - Now uses `get_config_section()` for all configuration access
- **Integration with SharedUtilitiesManager** - Leverages shared validation utilities and data processing
- **Performance optimization compatibility** - Validation optimized for 74% performance improvement with efficient schema caching

---

## Manager Interface

### Factory Function
```python
def create_pydantic_manager(unified_config: UnifiedConfigManager) -> PydanticManager
```

### Core Methods
- `get_model(model_name: str)` - Retrieves registered Pydantic model by name
- `register_model(model_name: str, model_class: BaseModel)` - Registers new Pydantic model
- `validate_data(data: dict, model_name: str)` - Validates data against specified model
- `get_validation_config()` - Retrieves validation configuration settings
- `create_dynamic_model(schema: dict)` - Creates dynamic Pydantic model from schema
- `validate_api_request(data: dict, endpoint: str)` - Validates API request data

---

## Pydantic Model Registry

### Crisis Detection Models
```python
class CrisisAnalysisRequest(BaseModel):
    message_content: str
    message_id: str = None
    user_context: dict = None
    analysis_options: dict = None

class CrisisAnalysisResponse(BaseModel):
    is_crisis: bool
    confidence_score: float
    crisis_type: str
    severity_level: str
    ai_model_details: dict
    pattern_matches: list
    recommended_actions: list
    analysis_timestamp: datetime

class CommunityContext(BaseModel):
    user_pronouns: str = None
    user_identity: str = None
    community_role: str = None
    previous_interactions: int = 0
    support_history: list = []
```

### Configuration Models
```python
class ManagerConfig(BaseModel):
    manager_name: str
    enabled: bool = True
    configuration: dict
    dependencies: list = []

class APIEndpointConfig(BaseModel):
    path: str
    method: str
    requires_auth: bool = False
    rate_limit: int = 60
    validation_schema: str
```

### Learning System Models
```python
class LearningDataPoint(BaseModel):
    input_text: str
    expected_output: dict
    context: dict = None
    community_feedback: str = None
    timestamp: datetime

class ModelPerformanceMetrics(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    false_positive_rate: float
    false_negative_rate: float
```

---

## Configuration Structure

### JSON Configuration (`config/pydantic_config.json`)
```json
{
    "validation": {
        "strict_mode": true,
        "allow_extra_fields": false,
        "validate_default": true,
        "use_enum_values": true
    },
    "schema_caching": {
        "enabled": true,
        "cache_ttl_seconds": 3600,
        "max_cached_schemas": 100
    },
    "error_handling": {
        "detailed_errors": true,
        "include_field_path": true,
        "custom_error_messages": true
    },
    "performance": {
        "lazy_model_creation": true,
        "schema_precompilation": true,
        "validation_caching": true
    },
    "community_validation": {
        "pronoun_validation": true,
        "identity_awareness": true,
        "privacy_protection": true,
        "sensitive_data_masking": true
    }
}
```

### Environment Variable Overrides
- `ASH_PYDANTIC_STRICT_MODE` - Override strict validation mode
- `ASH_PYDANTIC_CACHE_ENABLED` - Override schema caching
- `ASH_PYDANTIC_DETAILED_ERRORS` - Override detailed error reporting
- `ASH_COMMUNITY_VALIDATION_ENABLED` - Override community-specific validation

---

## Data Validation Features

### Crisis Detection Validation
- **Message content validation** - Ensures crisis analysis input is properly formatted
- **Response schema validation** - Validates crisis analysis output consistency
- **Confidence score validation** - Ensures confidence scores are within valid ranges
- **Community context validation** - Validates LGBTQIA+ community-specific data fields

### API Data Validation
- **Request validation** - Comprehensive validation of all API request data
- **Response validation** - Ensures API responses meet expected schemas
- **Parameter validation** - Query parameter and path parameter validation
- **Authentication data validation** - Validates authentication and authorization data

### Community Safety Validation
- **Pronoun validation** - Validates and respects community member pronouns
- **Identity field validation** - Validates LGBTQIA+ identity fields with respect and accuracy
- **Privacy protection** - Validates that sensitive data is properly protected
- **Consent validation** - Ensures proper consent is obtained for data processing

---

## Performance Optimization

### Schema Caching
- **Compiled schema caching** - Caches compiled Pydantic schemas for faster validation
- **Model instance caching** - Caches frequently used model instances
- **Validation result caching** - Caches validation results for repeated data patterns
- **Dynamic model caching** - Caches dynamically generated models

### Validation Performance
- **Lazy validation** - Defers validation until actually needed
- **Partial validation** - Validates only changed fields when possible
- **Batch validation** - Efficient validation of multiple items
- **Async validation** - Asynchronous validation for non-blocking operations

---

## Integration Points

### Dependencies
- **UnifiedConfigManager** - Primary configuration access and environment variable integration
- **SharedUtilitiesManager** - Data processing utilities and validation helpers

### Used By
- **API Endpoints** - Request/response validation for all API operations
- **CrisisAnalyzer** - Crisis analysis data validation and schema enforcement
- **LearningSystemManager** - Learning data validation and model performance tracking
- **All System Components** - Type safety and data validation throughout system

---

## Error Handling and Resilience

### Validation Error Handling
- **Detailed error messages** - Clear, helpful validation error messages
- **Field-level error reporting** - Specific field validation error information
- **Custom error formatting** - Community-friendly error message formatting
- **Error aggregation** - Comprehensive error reporting for multiple validation failures

### Production Safety
- **Graceful validation failures** - System continues operating with validation warnings
- **Default value fallbacks** - Safe defaults when validation fails on optional fields
- **Schema evolution support** - Handles schema changes gracefully
- **Backward compatibility** - Maintains compatibility with older data formats

---

## Community Features

### LGBTQIA+ Community Support
- **Inclusive data validation** - Validation that respects diverse identities and expressions
- **Pronoun validation** - Proper validation and handling of community member pronouns
- **Identity-aware validation** - Validation that understands LGBTQIA+ identity contexts
- **Privacy-first validation** - Validation that prioritizes community member privacy

### Community Safety Features
- **Sensitive data protection** - Automatic masking of sensitive community member data
- **Consent validation** - Ensures proper consent for data collection and processing
- **Community feedback validation** - Validates community feedback and improvement suggestions
- **Crisis context validation** - Specialized validation for crisis-related community data

---

## Testing and Validation

### Schema Testing
- **Model schema validation** - Ensures all Pydantic models have correct schemas
- **Data type testing** - Validates data type enforcement across all models
- **Constraint testing** - Tests field constraints and validation rules
- **Schema evolution testing** - Tests handling of schema changes over time

### Integration Testing
- **API integration testing** - Tests validation integration with all API endpoints
- **Manager integration testing** - Tests validation integration across all managers
- **Performance testing** - Validates that validation doesn't impact system performance
- **Community feature testing** - Tests LGBTQIA+ community-specific validation features