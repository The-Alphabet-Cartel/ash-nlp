# Ash NLP Server - GitHub Release Guide v2.1

**Release Management for the Advanced Crisis Detection NLP Processing Engine**

Part of The Alphabet Cartel's [Ash Crisis Detection & Community Support Ecosystem](https://github.com/the-alphabet-cartel/ash)

---

## 🎯 Release Overview

This guide covers release management for the Ash NLP Server, including versioning, testing, deployment, and ecosystem coordination.

### Release Philosophy
- **Stability First**: Production deployments must be rock-solid
- **Ecosystem Coordination**: Releases coordinate with ash-bot, ash-dash, and ash-thrash
- **Community Impact**: Every release improves crisis detection for our community
- **Documentation**: Comprehensive release notes for technical and crisis response teams

## 📋 Release Process

### 1. Pre-Release Preparation

**Version Planning:**
```bash
# Semantic versioning: MAJOR.MINOR.PATCH
# v2.1.0 = Major feature release
# v2.1.1 = Bug fixes and improvements
# v2.1.2 = Security patches and minor fixes
```

**Feature Branch Preparation:**
```powershell
# Create release branch
git checkout -b release/v2.1.1

# Update version numbers in key files
# Update nlp_main.py
# Update docker-compose.yml image tags
# Update README.md badges and version references
```

**Documentation Updates:**
```powershell
# Ensure all documentation is current
# docs/deployment_v2_1.md
# docs/team/team_guide_v2_1.md
# docs/tech/API_v2_1.md
# docs/tech/troubleshooting_v2_1.md
# README.md

# Update CHANGELOG.md with new features and fixes
```

### 2. Testing & Validation

**Comprehensive Testing Protocol:**
```powershell
# 1. Unit tests (if available)
python -m pytest tests/ -v

# 2. Integration testing with ash-thrash
# Run from testing server (10.20.30.253)
curl http://10.20.30.16:8884/test_nlp_integration

# 3. Performance validation
# Verify GPU utilization and response times
nvidia-smi
Measure-Command { Invoke-RestMethod -Uri "http://10.20.30.16:8881/analyze" -Method POST -Body $testPayload }

# 4. Learning system validation
curl http://10.20.30.16:8881/learning_statistics

# 5. Full ecosystem testing
# Test integration with ash-bot, ash-dash, and ash-thrash
```

**Quality Gates:**
- ✅ All critical tests passing
- ✅ Performance within acceptable thresholds (< 200ms analysis)
- ✅ Learning system functional
- ✅ Integration tests with all ecosystem components passing
- ✅ Documentation updated and reviewed
- ✅ Security review completed

### 3. Release Creation

**GitHub Release Process:**
```bash
# 1. Merge release branch to main
git checkout main
git merge release/v2.1.1

# 2. Create annotated tag
git tag -a v2.1.1 -m "Release v2.1.1: Enhanced crisis detection and performance improvements"

# 3. Push tag to trigger release automation
git push origin main --tags
```

**Release Automation (GitHub Actions):**
```yaml
# .github/workflows/release.yml
name: Create Release
on:
  push:
    tags:
      - 'v*'

jobs:
  build-and-release:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Build Docker Image
        run: |
          docker build -t ghcr.io/the-alphabet-cartel/ash-nlp:${{ github.ref_name }} .
          docker push ghcr.io/the-alphabet-cartel/ash-nlp:${{ github.ref_name }}
      
      - name: Create GitHub Release
        uses: actions/create-release@v1
        with:
          tag_name: ${{ github.ref_name }}
          release_name: Ash NLP Server ${{ github.ref_name }}
          body_path: RELEASE_NOTES.md
          draft: false
          prerelease: false
```

## 📦 Release Assets

### Docker Images

**Multi-Platform Images:**
```bash
# Build for production deployment
docker buildx build --platform linux/amd64,windows/amd64 \
  -t ghcr.io/the-alphabet-cartel/ash-nlp:v2.1.1 \
  -t ghcr.io/the-alphabet-cartel/ash-nlp:latest \
  --push .
```

**Image Variants:**
- `ash-nlp:v2.1.1` - Specific version tag
- `ash-nlp:latest` - Latest stable release
- `ash-nlp:v2.1.1-gpu` - GPU-optimized variant
- `ash-nlp:v2.1.1-dev` - Development variant with debugging tools

### Release Artifacts

**Documentation Package:**
```powershell
# Create release documentation package
$releaseDir = "release-artifacts-v2.1.1"
New-Item -Path $releaseDir -ItemType Directory

# Copy essential documentation
Copy-Item "README.md" "$releaseDir/"
Copy-Item "docs/" "$releaseDir/docs/" -Recurse
Copy-Item ".env.template" "$releaseDir/"
Copy-Item "docker-compose.yml" "$releaseDir/"

# Create deployment quick-start guide
@"
# Ash NLP Server v2.1.1 - Quick Deployment

## Requirements
- Windows 11 Pro with Docker Desktop
- NVIDIA RTX 3050 or better
- 8GB+ RAM available for container

## Deployment
1. Extract this package to C:\Deployments\ash-nlp
2. Copy .env.template to .env and configure
3. Run: docker-compose up -d
4. Verify: curl http://10.20.30.16:8881/health

## Documentation
- README.md - Complete overview
- docs/deployment_v2_1.md - Detailed deployment guide
- docs/tech/API_v2_1.md - API reference
"@ | Out-File "$releaseDir/QUICK_START.md"

# Create release package
Compress-Archive -Path "$releaseDir\*" -DestinationPath "ash-nlp-v2.1.1-release-package.zip"
```

## 📝 Release Notes Template

### v2.1.1 Release Notes

**Release Date:** [Date]  
**Docker Image:** `ghcr.io/the-alphabet-cartel/ash-nlp:v2.1.1`  
**Compatibility:** Ash Bot v2.1.x, Ash Dashboard v2.1.x, Ash Testing v2.1.x

#### 🚀 New Features

**Enhanced Crisis Detection:**
- Improved contextual understanding for LGBTQIA+ terminology
- Better detection of gaming-related stress vs. actual crisis indicators
- Enhanced ensemble scoring algorithm for more accurate classifications

**Performance Improvements:**
- 15% faster analysis response times (now averaging 145ms)
- Optimized GPU memory usage for RTX 3050 deployment
- Improved batch processing for concurrent requests

**Learning System Enhancements:**
- Real-time learning from false positive/negative feedback
- Adaptive threshold adjustment based on community patterns
- Enhanced learning persistence and backup mechanisms

#### 🐛 Bug Fixes

- Fixed memory leak in model loading process
- Resolved GPU initialization timeout on cold starts
- Fixed learning system corruption during high-load periods
- Corrected analytics webhook delivery failures

#### 🔧 Technical Improvements

- Updated to latest PyTorch and Transformers libraries
- Enhanced Docker GPU resource allocation
- Improved logging and monitoring capabilities
- Better error handling and recovery mechanisms

#### 📚 Documentation Updates

- Updated deployment guide for Windows 11 dedicated server
- Enhanced API documentation with more examples
- New troubleshooting section for GPU-related issues
- Updated team guide with new features and workflows

#### ⚡ Performance Metrics

```json
{
    "response_time": {
        "average": "145ms",
        "p95": "280ms",
        "improvement": "15% faster vs v2.1.0"
    },
    "accuracy": {
        "overall": "87%",
        "high_crisis_detection": "96%",
        "false_positive_rate": "6.2%"
    },
    "resource_usage": {
        "gpu_memory": "3.2GB / 8GB RTX 3050",
        "system_memory": "4.1GB average",
        "cpu_usage": "25% average (6 cores)"
    }
}
```

#### 🔄 Migration Guide

**From v2.1.0 to v2.1.1:**
```powershell
# 1. Backup current deployment
& "C:\Deployments\ash-nlp\scripts\backup_ash_nlp.ps1"

# 2. Update image
docker-compose pull

# 3. Restart with new version
docker-compose down
docker-compose up -d

# 4. Verify deployment
curl http://10.20.30.16:8881/health
```

**Breaking Changes:** None - fully backward compatible

**Configuration Changes:**
- New optional setting: `ADAPTIVE_THRESHOLD_ENABLED=true`
- Enhanced GPU settings: `GPU_MEMORY_FRACTION=0.8`

#### 🎯 Ecosystem Integration

**Ash Bot (v2.1.x):**
- Enhanced NLP integration with new confidence scoring
- Improved fallback mechanisms for NLP server unavailability
- Better error handling for analysis timeouts

**Ash Dashboard (v2.1.x):**
- Real-time learning system metrics
- Enhanced performance monitoring charts
- New NLP server health indicators

**Ash Testing (v2.1.x):**
- Updated test phrases for new detection capabilities
- Enhanced performance validation tests
- Improved integration testing protocols

#### 🚨 Known Issues

- **GPU Memory**: Occasional GPU memory warnings on very high loads (monitoring)
- **Learning System**: Learning adjustments may take 10-15 minutes to fully propagate
- **Windows Docker**: Some users may need to restart Docker Desktop after Windows updates

#### 🛣️ What's Next

**v2.2.0 Preview (Q4 2025):**
- Multi-language support (Spanish, French)
- Advanced context tracking across multiple messages
- Integration with professional mental health APIs
- Voice channel analysis capabilities

#### 🙏 Acknowledgments

- **Crisis Response Team** for feedback and testing
- **Community Members** for providing real-world validation
- **Development Team** for code contributions and reviews
- **The Alphabet Cartel Community** for continued support

## 🔄 Post-Release Process

### 1. Deployment Coordination

**Production Deployment:**
```powershell
# Deploy to production server (10.20.30.16)
Set-Location C:\Deployments\ash-nlp

# Update production environment
docker-compose pull
docker-compose down
docker-compose up -d

# Verify deployment health
Start-Sleep 60
$health = Invoke-RestMethod -Uri "http://10.20.30.16:8881/health"
Write-Host "Production deployment status: $($health.status)"
```

**Integration Testing:**
```bash
# Test integration with ash-bot
curl http://10.20.30.253:8882/test_nlp_integration

# Test dashboard integration
curl http://10.20.30.253:8883/health

# Run comprehensive testing suite
curl http://10.20.30.253:8884/run_comprehensive_test
```

### 2. Ecosystem Updates

**Update Main Repository:**
```bash
# Update main ash repository with new submodule version
cd ash
git submodule update --remote ash-nlp
git add ash-nlp
git commit -m "Update ash-nlp to v2.1.1"
git tag v2.1.1-ecosystem
git push origin main --tags
```

**Component Compatibility:**
```bash
# Verify all components work with new NLP version
# This may require coordinated releases of:
# - ash-bot (if API changes)
# - ash-dash (if metrics changes)
# - ash-thrash (if testing updates needed)
```

### 3. Communication

**Release Announcement:**
```markdown
# 🚀 Ash NLP Server v2.1.1 Released!

We're excited to announce the release of Ash NLP Server v2.1.1, bringing enhanced crisis detection capabilities and improved performance to our community support system.

## Key Highlights
- 15% faster analysis (145ms average)
- Improved LGBTQIA+ terminology detection
- Enhanced learning system with real-time adaptation
- Better GPU optimization for our RTX 3050 deployment

## What This Means for Our Community
- More accurate crisis detection
- Faster response times for support interventions
- Better understanding of gaming vs. crisis language
- Continuous improvement through learning feedback

## For Crisis Response Teams
Please review the updated [Team Guide](docs/team/team_guide_v2_1.md) for new features and workflows.

## Technical Details
Full release notes and deployment instructions available in our [GitHub repository](https://github.com/the-alphabet-cartel/ash-nlp/releases/tag/v2.1.1).

Questions? Join us in #tech-support on Discord!
```

**Team Notifications:**
- **Discord Announcements**: #announcements channel
- **Crisis Response Team**: Direct notification in #crisis-response
- **Development Team**: #development channel update
- **Documentation Team**: Update requests for any user-facing changes

### 4. Monitoring & Feedback

**Post-Release Monitoring:**
```powershell
# Monitor key metrics for first 48 hours
# - Response times
# - Accuracy rates
# - Error rates
# - Integration health
# - User feedback

# Set up enhanced monitoring script
& "C:\Deployments\ash-nlp\scripts\post_release_monitoring.ps1"
```

**Feedback Collection:**
- Monitor GitHub issues for bug reports
- Collect performance feedback from crisis response teams
- Track user-reported accuracy issues
- Document any integration problems

## 📞 Release Support

### Support Channels
- **GitHub Issues**: Technical problems and bug reports
- **Discord #tech-support**: General technical assistance  
- **Discord #crisis-response**: Team-specific questions
- **Discord #development**: Developer discussions

### Escalation Process
1. **Community Support**: Discord channels and GitHub issues
2. **Technical Issues**: GitHub issues with detailed reproduction steps
3. **Critical Production Issues**: Direct Discord contact with development team
4. **Emergency**: Use emergency contact procedures for system-down situations

---

## 🔗 Related Documentation

- **[Deployment Guide](deployment_v2_1.md)** - Production deployment procedures
- **[API Documentation](tech/API_v2_1.md)** - Complete API reference
- **[Team Guide](team/team_guide_v2_1.md)** - Crisis response team procedures
- **[Main Repository](https://github.com/the-alphabet-cartel/ash)** - Ecosystem overview

---

**The Alphabet Cartel** - Building inclusive gaming communities through technology.

**Discord:** https://discord.gg/alphabetcartel | **Website:** https://alphabetcartel.org

*Every release brings us closer to a safer, more supportive community for everyone.*