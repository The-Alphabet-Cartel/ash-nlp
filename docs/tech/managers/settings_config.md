<!-- ash-nlp/docs/tech/managers/settings_config.md -->
<!--
Settings Manager Documentation for Ash-NLP Service
FILE VERSION: v5.0
LAST MODIFIED: 2025-12-30
CLEAN ARCHITECTURE: Compliant
-->
# Settings Manager Documentation

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp
**Project**: Ash-NLP v5.0
**Community**: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
**FILE VERSION**: v5.0
**LAST UPDATED**: 2025-12-30
**CLEAN ARCHITECTURE**: Compliant

---

# SettingsConfigManager Documentation

The SettingsConfigManager handles general application settings and system-wide configuration for the Ash-NLP crisis detection system, providing centralized management of core operational parameters.

---

## Overview

SettingsConfigManager provides centralized management of application-wide settings, system defaults, and operational parameters that don't fit into specialized configuration managers, ensuring consistent system behavior across all components.

### Core Responsibilities
- **Application-wide settings management** - Core system settings and operational defaults
- **System behavior configuration** - General system operation parameters and preferences
- **Cross-component settings** - Settings that affect multiple system components
- **Default value management** - System-wide default values and fallback settings
- **Runtime setting updates** - Dynamic configuration updates for operational flexibility

### Phase 3e Consolidation Impact
- **Configuration pattern standardization** - Now uses `get_config_section()` for all configuration access
- **Integration with SharedUtilitiesManager** - Leverages shared validation and configuration utilities
- **Performance optimization compatibility** - Settings optimized for 74% performance improvement architecture

---

## Manager Interface

### Factory Function
```python
def create_settings_config_manager(unified_config: UnifiedConfigManager) -> SettingsConfigManager
```

### Core Methods
- `get_settings()` - Retrieves current application settings
- `get_setting(key: str, default: any = None)` - Gets individual setting with optional default
- `update_setting(key: str, value: any)` - Runtime setting updates
- `get_system_defaults()` - Retrieves system-wide default values
- `validate_settings()` - Validates settings consistency and correctness
- `reset_setting(key: str)` - Resets setting to default value

---

## Configuration Structure

### JSON Configuration (`config/setting_config.json`)
```json
{
    "application": {
        "name": "Ash-NLP",
        "version": "3.1",
        "description": "Crisis Detection Natural Language Processor",
        "community": "The Alphabet Cartel",
        "debug_mode": false
    },
    "system": {
        "timezone": "UTC",
        "date_format": "ISO8601",
        "encoding": "utf-8",
        "locale": "en_US"
    },
    "operational": {
        "max_retries": 3,
        "retry_delay_seconds": 1,
        "default_timeout_seconds": 30,
        "batch_size": 100,
        "concurrent_limit": 10
    },
    "community": {
        "discord_integration": true,
        "lgbtqia_patterns": true,
        "community_safety_mode": true,
        "crisis_escalation_enabled": true
    },
    "development": {
        "verbose_logging": false,
        "performance_monitoring": true,
        "error_reporting": true,
        "testing_mode": false
    }
}
```

### Environment Variable Overrides
- `ASH_DEBUG_MODE` - Override application debug mode
- `ASH_TIMEZONE` - Override system timezone setting
- `ASH_MAX_RETRIES` - Override maximum retry attempts
- `ASH_CONCURRENT_LIMIT` - Override concurrent operation limit
- `ASH_COMMUNITY_SAFETY_MODE` - Override community safety mode

---

## Setting Categories

### Application Settings
- **Basic application information** - Name, version, and description
- **Runtime behavior** - Debug mode and operational parameters
- **Feature enablement** - Core feature toggles and system capabilities
- **Community integration** - LGBTQIA+ Discord community specific settings

### System Configuration
- **Internationalization** - Timezone, locale, and encoding settings
- **Data formatting** - Date formats and text encoding preferences
- **Resource management** - System resource allocation and limits
- **Error handling** - Retry policies and timeout configurations

### Community Safety Settings
- **LGBTQIA+ pattern recognition** - Community-specific crisis detection patterns
- **Discord integration** - Discord bot integration settings and capabilities
- **Crisis escalation** - Automated crisis response and escalation settings
- **Privacy protection** - Community member privacy and safety settings

---

## Integration Points

### Dependencies
- **UnifiedConfigManager** - Primary configuration access and environment variable integration
- **SharedUtilitiesManager** - Setting validation utilities and common configuration patterns

### Used By
- **All System Components** - Centralized settings for consistent behavior across managers
- **CrisisAnalyzer** - Community safety and operational settings
- **API Endpoints** - Application information and operational parameters
- **Discord Integration** - Community-specific settings and preferences

---

## Dynamic Configuration

### Runtime Updates
- **Hot configuration reloading** - Update settings without system restart
- **Setting validation** - Ensures runtime updates maintain system consistency
- **Change notifications** - Notify components when relevant settings change
- **Rollback capability** - Ability to revert setting changes if issues occur

### Configuration Persistence
- **Setting persistence** - Save runtime changes to configuration files
- **Default restoration** - Ability to restore settings to default values
- **Configuration backup** - Backup and restore setting configurations
- **Version control** - Track setting changes over time

---

## Error Handling and Resilience

### Graceful Degradation
- **Invalid settings** - Falls back to safe default values with logging
- **Missing configuration sections** - Uses hardcoded fallback values
- **Type conversion errors** - Handles setting type mismatches gracefully
- **Configuration file corruption** - Reconstructs settings from defaults

### Production Safety
- **Conservative defaults** - Safe operational defaults for all settings
- **Validation before application** - All setting changes validated before use
- **Error logging** - Clear error messages for setting configuration issues
- **System stability** - Setting errors never crash the crisis detection system

---

## Community Features

### LGBTQIA+ Community Support
- **Inclusive pattern recognition** - Settings for community-specific crisis indicators
- **Identity-aware processing** - Settings for identity-sensitive crisis detection
- **Community safety prioritization** - Settings that prioritize community member safety
- **Discord integration optimization** - Settings optimized for Discord community interaction

### Crisis Response Configuration
- **Escalation thresholds** - Settings for crisis severity escalation
- **Response coordination** - Settings for automated crisis response coordination
- **Community notification** - Settings for community staff notification preferences
- **Privacy protection** - Settings ensuring community member privacy during crisis response

---

*Settings Configuration Manager Guide for Ash-NLP v5.0*

**Built with care for chosen family** 🏳️‍🌈
