<!-- ash-nlp/docs/tech/managers/logging_manager.md -->
<!--
Logging Config Manager Documentation for Ash-NLP Service
FILE VERSION: v5.0
LAST MODIFIED: 2025-12-30
CLEAN ARCHITECTURE: Compliant
-->
# Logging Config Manager Documentation

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp
**Project**: Ash-NLP v5.0
**Community**: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
**FILE VERSION**: v5.0
**LAST UPDATED**: 2025-12-30
**CLEAN ARCHITECTURE**: Compliant

---

# LoggingConfigManager Documentation

The LoggingConfigManager handles comprehensive logging configuration for the Ash-NLP crisis detection system, ensuring proper audit trails and debugging capabilities for life-saving mental health support operations.

---

## Overview

LoggingConfigManager provides centralized logging configuration management, supporting detailed crisis analysis logging, performance monitoring, and comprehensive audit trails for community safety operations.

### Core Responsibilities
- **Logging level management** - Dynamic control of system-wide logging verbosity
- **Output destination configuration** - File, console, and remote logging setup
- **Crisis analysis logging** - Specialized logging for mental health crisis detection
- **Performance logging** - Monitoring and optimization support logging
- **Security and privacy compliance** - Ensures LGBTQIA+ community privacy protection

### Phase 3e Consolidation Impact
- **Configuration pattern standardization** - Now uses `get_config_section()` for all configuration access
- **Integration with SharedUtilitiesManager** - Leverages shared logging utilities and validation
- **Performance optimization compatibility** - Logging optimized for 74% performance improvement with minimal overhead

---

## Manager Interface

### Factory Function
```python
def create_logging_config_manager(unified_config: UnifiedConfigManager) -> LoggingConfigManager
```

### Core Methods
- `get_logging_config()` - Retrieves current logging configuration
- `configure_logger(logger_name: str)` - Sets up logger with current configuration
- `get_log_level(component: str)` - Gets logging level for specific component
- `update_logging_level(component: str, level: str)` - Runtime logging level updates
- `get_crisis_logging_config()` - Specialized crisis detection logging configuration

---

## Configuration Structure

### JSON Configuration (`config/logging_settings.json`)
```json
{
    "default_level": "INFO",
    "component_levels": {
        "crisis_analyzer": "DEBUG",
        "model_coordination": "INFO",
        "pattern_detection": "INFO",
        "shared_utilities": "WARNING",
        "performance": "INFO"
    },
    "handlers": {
        "console": {
            "enabled": true,
            "level": "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
        "file": {
            "enabled": true,
            "level": "DEBUG",
            "filename": "logs/ash-nlp.log",
            "max_bytes": 10485760,
            "backup_count": 5
        }
    },
    "privacy_settings": {
        "sanitize_user_content": true,
        "log_message_ids_only": true,
        "exclude_personal_info": true
    }
}
```

### Environment Variable Overrides
- `ASH_LOG_LEVEL` - Override default logging level
- `ASH_LOG_CRISIS_LEVEL` - Override crisis analysis logging level
- `ASH_LOG_CONSOLE_ENABLED` - Enable/disable console logging
- `ASH_LOG_FILE_ENABLED` - Enable/disable file logging
- `ASH_LOG_PRIVACY_SANITIZE` - Enable/disable content sanitization

---

## Integration Points

### Dependencies
- **UnifiedConfigManager** - Primary configuration access and environment variable integration
- **SharedUtilitiesManager** - Logging utilities and privacy protection methods

### Used By
- **CrisisAnalyzer** - Detailed crisis detection and analysis logging
- **ModelCoordinationManager** - AI model interaction and performance logging
- **PatternDetectionManager** - Pattern matching and community safety logging
- **All System Components** - Centralized logging configuration for consistent behavior

---

## Privacy and Security Features

### LGBTQIA+ Community Protection
- **Content sanitization** - Automatically removes personally identifiable information from logs
- **Message ID logging** - Logs message identifiers without content for audit trails
- **Privacy-first defaults** - Conservative logging settings protect community members
- **Configurable privacy levels** - Adjustable privacy protection based on deployment needs

### Crisis Response Logging
- **Detailed analysis trails** - Comprehensive logging for crisis detection decision-making
- **Performance monitoring** - Tracks response times and system performance for life-saving operations
- **Error tracking** - Captures and logs system errors that could impact crisis response
- **Audit compliance** - Maintains logs suitable for community safety auditing

---

## Error Handling and Resilience

### Graceful Degradation
- **Invalid logging configuration** - Falls back to basic console logging with INFO level
- **File system errors** - Continues with console logging if file logging fails
- **Configuration parsing errors** - Uses hardcoded safe defaults for all logging

### Production Safety
- **Non-blocking logging** - Logging errors never interrupt crisis detection operations
- **Automatic log rotation** - Prevents disk space issues in production environments
- **Memory-efficient logging** - Optimized for long-running crisis detection service

---

## Performance Optimization

### Phase 3e Performance Integration
- **Lazy log message formatting** - Only formats log messages when actually logged
- **Efficient privacy sanitization** - Optimized content cleaning for minimal overhead
- **Conditional debug logging** - Debug-level logging optimized to minimize production impact
- **Log level caching** - Caches logging level decisions for frequently accessed components

### Resource Management
- **Log file rotation** - Automatic cleanup of old log files to manage disk space
- **Memory-conscious logging** - Efficient logging patterns that don't impact crisis detection performance
- **Network logging optimization** - Efficient remote logging when configured

---

## Testing and Validation

### Configuration Testing
- **Logging level validation** - Ensures all logging levels are properly configured
- **Handler configuration testing** - Validates file and console handler setup
- **Privacy sanitization testing** - Confirms personal information is properly protected

### Integration Testing
- **Manager interaction testing** - Validates logging integration across all managers
- **Performance impact testing** - Ensures logging doesn't degrade crisis detection performance
- **Privacy compliance testing** - Validates LGBTQIA+ community privacy protection
---

*Logging Manager Guide for Ash-NLP v5.0*

**Built with care for chosen family** 🏳️‍🌈
