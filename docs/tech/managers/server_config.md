<!-- ash-nlp/docs/tech/managers/server_config.md -->
<!--
Server Config Manager Documentation for Ash-NLP Service
FILE VERSION: v5.0
LAST MODIFIED: 2025-12-30
CLEAN ARCHITECTURE: Compliant
-->
# Server Config Manager Documentation

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp
**Project**: Ash-NLP v5.0
**Community**: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
**FILE VERSION**: v5.0
**LAST UPDATED**: 2025-12-30
**CLEAN ARCHITECTURE**: Compliant

---

# ServerConfigManager Documentation

The ServerConfigManager handles server configuration and deployment settings for the Ash-NLP crisis detection system, managing the production deployment on the Debian Linux server infrastructure.

---

## Overview

ServerConfigManager provides centralized configuration for server infrastructure, API endpoints, security settings, and deployment parameters, ensuring reliable production operation of the life-saving crisis detection service.

### Core Responsibilities
- **Server infrastructure configuration** - Port assignments, host settings, and network configuration
- **API endpoint management** - REST API configuration and security settings
- **Production deployment settings** - Docker container configuration and resource allocation
- **Security and access control** - Authentication, rate limiting, and access management
- **Health monitoring configuration** - Server health checks and monitoring endpoints

### Phase 3e Consolidation Impact
- **Configuration pattern standardization** - Now uses `get_config_section()` for all configuration access
- **Integration with SharedUtilitiesManager** - Leverages shared validation and configuration utilities
- **Performance optimization compatibility** - Server configuration optimized for 74% performance improvement architecture

---

## Manager Interface

### Factory Function
```python
def create_server_config_manager(unified_config: UnifiedConfigManager) -> ServerConfigManager
```

### Core Methods
- `get_server_config()` - Retrieves current server configuration
- `get_api_config()` - Gets API endpoint and security configuration
- `get_host_settings()` - Retrieves host, port, and network settings
- `get_security_config()` - Gets authentication and security settings
- `get_deployment_config()` - Retrieves Docker and deployment configuration
- `validate_server_config()` - Validates server configuration consistency

---

## Configuration Structure

### JSON Configuration (`config/server_config.json`)
```json
{
    "server": {
        "host": "0.0.0.0",
        "port": 8881,
        "debug": false,
        "workers": 4,
        "timeout_seconds": 30
    },
    "api": {
        "base_path": "/",
        "cors_enabled": true,
        "cors_origins": ["http://localhost:3000"],
        "rate_limiting": {
            "enabled": true,
            "requests_per_minute": 60,
            "burst_limit": 10
        }
    },
    "security": {
        "require_auth": false,
        "api_key_validation": false,
        "ssl_enabled": false,
        "trusted_proxies": ["127.0.0.1"]
    },
    "health": {
        "health_check_enabled": true,
        "health_check_path": "/health",
        "metrics_enabled": true,
        "metrics_path": "/metrics"
    },
    "deployment": {
        "docker_enabled": true,
        "container_name": "ash-nlp",
        "restart_policy": "unless-stopped",
        "environment": "production"
    }
}
```

### Environment Variable Overrides
- `ASH_SERVER_HOST` - Override server host binding
- `ASH_SERVER_PORT` - Override server port (default: 8881)
- `ASH_SERVER_DEBUG` - Override debug mode setting
- `ASH_API_CORS_ENABLED` - Override CORS enablement
- `ASH_SECURITY_REQUIRE_AUTH` - Override authentication requirement
- `ASH_DEPLOYMENT_ENVIRONMENT` - Override deployment environment

---

## Infrastructure Integration

### Debian 12 Linux Server
- **AMD Ryzen 7 5800x CPU** - Multi-worker configuration optimized for 8-core CPU
- **NVIDIA RTX 3060 12GB GPU** - GPU memory management and CUDA configuration
- **64GB RAM** - Memory allocation and management for AI model loading
- **Docker deployment** - Container-first deployment philosophy
- **Network configuration** - Server IP 10.20.30.253 with port 8881

### Docker Integration
- **Container management** - Docker container configuration and resource allocation
- **Environment variable injection** - Secure injection of configuration into containers
- **Health checks** - Docker health check configuration for container monitoring
- **Resource limits** - CPU and memory limits for production stability

---

## API Configuration

### RESTful API Endpoints
- **Crisis analysis endpoint** - `/analyze` for primary crisis detection
- **Health monitoring** - `/health` for system status checks
- **Metrics endpoint** - `/metrics` for performance monitoring
- **Administrative endpoints** - Admin-only endpoints for system management

### Security Features
- **Rate limiting** - Configurable request rate limiting to prevent abuse
- **CORS management** - Cross-origin resource sharing configuration
- **Authentication integration** - Pluggable authentication system support
- **Trusted proxy handling** - Support for reverse proxy deployments

---

## Integration Points

### Dependencies
- **UnifiedConfigManager** - Primary configuration access and environment variable integration
- **SharedUtilitiesManager** - Server utilities and validation methods

### Used By
- **FastAPI Application** - Primary web framework configuration
- **Crisis Detection API** - API endpoint configuration and security
- **Health Monitoring Systems** - Health check and metrics configuration
- **Docker Deployment** - Container configuration and resource management

---

## Production Deployment

### Server Architecture
- **Single-server deployment** - Production deployment on dedicated Debian 12 server
- **Docker containerization** - All services deployed as Docker containers
- **Service discovery** - Container networking and service communication
- **Resource monitoring** - CPU, memory, and GPU resource monitoring

### Performance Optimization
- **Worker process configuration** - Multi-worker setup for concurrent request handling
- **Connection pooling** - Efficient database and external service connection management
- **Request timeout management** - Appropriate timeouts for crisis detection response times
- **Static resource serving** - Efficient serving of documentation and static assets

---

## Error Handling and Resilience

### Graceful Degradation
- **Invalid server configuration** - Falls back to safe default server settings
- **Port binding errors** - Automatic port selection if default port unavailable
- **Resource exhaustion** - Graceful handling of server resource limits
- **Network configuration errors** - Fallback network settings for reliable operation

### Production Safety
- **Health check endpoints** - Kubernetes/Docker health check support
- **Graceful shutdown** - Proper cleanup and shutdown procedures
- **Error logging** - Comprehensive error logging for production debugging
- **Automatic restart** - Docker restart policies for service continuity

---

## Monitoring and Observability

### Health Monitoring
- **System health checks** - Endpoint health and dependency checks
- **Performance metrics** - Response time, throughput, and error rate monitoring
- **Resource utilization** - CPU, memory, and GPU usage monitoring
- **Service availability** - Uptime and availability tracking

### Logging Integration
- **Access logging** - HTTP request and response logging
- **Error tracking** - Server error and exception tracking
- **Security logging** - Authentication and authorization attempt logging
- **Performance logging** - Request timing and resource usage logging

---

*Server Configuration Manager Guide for Ash-NLP v5.0*

**Built with care for chosen family** 🏳️‍🌈
