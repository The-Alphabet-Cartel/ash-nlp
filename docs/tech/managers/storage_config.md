<!-- ash-nlp/docs/tech/managers/storage_config.md -->
<!--
Storage Config Manager Documentation for Ash-NLP Service
FILE VERSION: v3.1-1
LAST MODIFIED: 2025-08-26
PHASE: 3e
CLEAN ARCHITECTURE: v3.1 Compliant
-->
# Storage Config Manager Documentation

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp
**Project**: Ash-NLP v3.1
**Community**: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
**FILE VERSION**: v3.1-1
**LAST UPDATED**: 2025-08-26
**CLEAN ARCHITECTURE**: v3.1 Compliant

---

# StorageConfigManager Documentation

The StorageConfigManager handles storage and file system configuration for the Ash-NLP crisis detection system, managing data storage, backup systems, and file organization across the Debian 12 Linux server infrastructure.

---

## Overview

StorageConfigManager provides centralized configuration for all storage-related operations including data persistence, backup management, cache storage, and file system organization, ensuring reliable data management for the life-saving crisis detection service.

### Core Responsibilities
- **Storage path management** - Directory structure and file path configuration
- **Data persistence configuration** - Database and file-based storage settings
- **Backup and recovery settings** - Automated backup and disaster recovery configuration
- **Cache storage management** - Analysis result and model cache storage settings
- **File system security** - Storage permissions and access control settings

### Phase 3e Consolidation Impact
- **Configuration pattern standardization** - Now uses `get_config_section()` for all configuration access
- **Integration with SharedUtilitiesManager** - Leverages shared file system utilities and validation
- **Performance optimization compatibility** - Storage configuration optimized for 74% performance improvement with efficient caching

---

## Manager Interface

### Factory Function
```python
def create_storage_config_manager(unified_config: UnifiedConfigManager) -> StorageConfigManager
```

### Core Methods
- `get_storage_config()` - Retrieves current storage configuration
- `get_storage_path(path_type: str)` - Gets specific storage directory path
- `get_backup_config()` - Retrieves backup and recovery configuration
- `get_cache_config()` - Gets cache storage settings and limits
- `validate_storage_paths()` - Validates storage directory accessibility and permissions
- `ensure_directory_structure()` - Creates required directory structure if missing

---

## Configuration Structure

### JSON Configuration (`config/storage_settings.json`)
```json
{
    "base_paths": {
        "data_directory": "data/",
        "cache_directory": "cache/",
        "backup_directory": "backups/",
        "logs_directory": "logs/",
        "models_directory": "models/"
    },
    "data_storage": {
        "analysis_results": {
            "path": "data/analysis/",
            "format": "json",
            "compression": true,
            "retention_days": 90
        },
        "learning_data": {
            "path": "data/learning/",
            "format": "json",
            "compression": true,
            "retention_days": 365
        },
        "community_patterns": {
            "path": "data/patterns/",
            "format": "json",
            "compression": false,
            "retention_days": -1
        }
    },
    "cache_storage": {
        "analysis_cache": {
            "path": "cache/analysis/",
            "max_size_mb": 1024,
            "cleanup_interval_hours": 6
        },
        "model_cache": {
            "path": "cache/models/",
            "max_size_mb": 4096,
            "cleanup_interval_hours": 24
        },
        "pattern_cache": {
            "path": "cache/patterns/",
            "max_size_mb": 512,
            "cleanup_interval_hours": 12
        }
    },
    "backup": {
        "enabled": true,
        "interval_hours": 24,
        "retention_days": 30,
        "compression": true,
        "remote_backup": false
    }
}
```

### Environment Variable Overrides
- `ASH_DATA_DIRECTORY` - Override base data directory path
- `ASH_CACHE_DIRECTORY` - Override cache directory path
- `ASH_BACKUP_ENABLED` - Override backup system enablement
- `ASH_BACKUP_INTERVAL_HOURS` - Override backup frequency
- `ASH_CACHE_MAX_SIZE_MB` - Override cache size limits

---

## Storage Architecture

### Directory Structure
```
ash-nlp/
├── data/                     # Primary data storage
│   ├── analysis/            # Crisis analysis results
│   ├── learning/            # Learning system data
│   └── patterns/            # Community pattern data
├── cache/                   # Performance caching
│   ├── analysis/            # Analysis result cache
│   ├── models/              # AI model cache
│   └── patterns/            # Pattern matching cache
├── backups/                 # Automated backups
│   ├── daily/               # Daily backup snapshots
│   └── weekly/              # Weekly backup archives
├── logs/                    # System and analysis logs
└── models/                  # AI model storage
    ├── zero_shot/           # Zero-shot classification models
    └── embeddings/          # Text embedding models
```

### File System Integration
- **Docker volume mounting** - Container-to-host file system mapping
- **Permission management** - Appropriate file and directory permissions
- **Cross-platform compatibility** - Path handling for different operating systems
- **Symbolic link support** - Support for symbolic links in storage paths

---

## Data Management

### Analysis Data Storage
- **Crisis analysis results** - Persistent storage of crisis detection analyses
- **Community interaction logs** - LGBTQIA+ Discord community interaction data
- **Performance metrics** - Storage of system performance and response time data
- **Error and incident data** - Storage of system errors and crisis response incidents

### Learning System Data
- **Training data** - Storage of learning system training and validation data
- **Model improvement data** - Data used for continuous model improvement
- **Community feedback** - Storage of community feedback for system enhancement
- **Pattern evolution** - Historical data showing pattern recognition improvements

### Privacy and Security
- **Data encryption** - Encryption of sensitive community data at rest
- **Access control** - File system permissions protecting community privacy
- **Data retention policies** - Automatic cleanup of expired sensitive data
- **GDPR compliance** - Data storage policies compliant with privacy regulations

---

## Backup and Recovery

### Automated Backup System
- **Scheduled backups** - Regular automated backup of critical data
- **Incremental backups** - Efficient incremental backup strategies
- **Backup verification** - Automatic validation of backup integrity
- **Recovery testing** - Regular testing of backup recovery procedures

### Disaster Recovery
- **Data recovery procedures** - Step-by-step recovery from various failure scenarios
- **Backup restoration** - Automated and manual backup restoration procedures
- **System continuity** - Ensure crisis detection system availability during recovery
- **Community service continuity** - Minimize impact on LGBTQIA+ community crisis support

---

## Performance Optimization

### Cache Management
- **Analysis result caching** - Fast retrieval of previous analysis results
- **Model output caching** - Caching of AI model outputs for similar inputs
- **Pattern matching caching** - Efficient caching of community pattern detection results
- **Configuration caching** - Storage configuration caching for reduced I/O overhead

### Storage Performance
- **SSD optimization** - Configuration optimized for SSD storage performance
- **I/O scheduling** - Efficient file I/O scheduling for better performance
- **Memory-mapped files** - Using memory mapping for large file access
- **Parallel I/O** - Concurrent file operations where appropriate

---

## Integration Points

### Dependencies
- **UnifiedConfigManager** - Primary configuration access and environment variable integration
- **SharedUtilitiesManager** - File system utilities, path validation, and storage management

### Used By
- **CrisisAnalyzer** - Analysis result storage and retrieval
- **LearningSystemManager** - Learning data storage and management
- **ModelCoordinationManager** - AI model storage and caching
- **All System Components** - Logging, caching, and data persistence

---

## Error Handling and Resilience

### Graceful Degradation
- **Storage path failures** - Fallback to alternative storage paths if primary paths fail
- **Disk space exhaustion** - Graceful handling of disk space issues with cleanup
- **Permission errors** - Automatic permission correction where possible
- **File system corruption** - Recovery procedures for file system issues

### Production Safety
- **Storage validation** - Automatic validation of storage configuration before use
- **Disk space monitoring** - Proactive monitoring of available storage space
- **Automatic cleanup** - Scheduled cleanup of temporary files and expired data
- **Error logging** - Comprehensive logging of storage-related errors

---

## Testing and Validation

### Configuration Testing
- **Path validation testing** - Ensures all configured paths are valid and accessible
- **Permission testing** - Validates file system permissions are appropriate
- **Backup system testing** - Regular testing of backup and recovery procedures
- **Cache management testing** - Validates cache size limits and cleanup procedures

### Integration Testing
- **Storage integration testing** - Tests integration with all system components
- **Performance testing** - Validates storage performance under load
- **Recovery testing** - Tests disaster recovery procedures and data integrity
- **Cross-platform testing** - Ensures storage works across different environments