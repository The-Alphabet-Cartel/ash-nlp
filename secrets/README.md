# Ash-NLP Secrets

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp  
**Community**: [The Alphabet Cartel](https://discord.gg/alphabetcartel) | [alphabetcartel.org](https://alphabetcartel.org)

---

## Overview

This directory contains sensitive credentials used by Ash-NLP. These files are:
- **NOT** committed to Git (via `.gitignore`)
- Mounted into Docker containers via Docker Secrets
- Read by the `SecretsManager` at runtime

---

## Secret Files

| File | Description | Required |
|------|-------------|----------|
| `huggingface` | HuggingFace API token | Optional* |
| `discord_alert_webhook` | Discord webhook for system alerts | Optional |
| `discord_token` | Discord bot token | Future |
| `webhook_secret` | Webhook signing key | Future |

*HuggingFace token is optional for public models but required for:
- Private/gated models
- Higher API rate limits
- Enterprise features

---

## Setup Instructions

### 1. Create the secrets directory

```bash
mkdir -p secrets
```

### 2. Add HuggingFace Token

Get your token from: https://huggingface.co/settings/tokens

```bash
# Create the secret file (no file extension)
echo "hf_your_token_here" > secrets/huggingface

# Set secure permissions
chmod 600 secrets/huggingface
```

### 3. Add Discord Alert Webhook (Optional)

For system alerts (model failures, startup notifications):

1. In Discord: Server Settings → Integrations → Webhooks → New Webhook
2. Copy the webhook URL
3. Create the secret:

```bash
# Create the webhook secret
echo "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN" > secrets/discord_alert_webhook

# Set secure permissions
chmod 600 secrets/discord_alert_webhook
```

**Important**: 
- The file should contain ONLY the token, no quotes or extra whitespace
- Do NOT add a file extension (not `.txt`, not `.token`)

### 3. Verify Setup

```bash
# Check file exists and has content
cat secrets/huggingface

# Verify permissions (should be 600 or rw-------)
ls -la secrets/
```

---

## How It Works

### Docker Secrets (Production)

When running with Docker Compose, secrets are:
1. Defined in `docker-compose.yml`
2. Mounted to `/run/secrets/<name>` inside the container
3. Read by `SecretsManager` at startup

```yaml
# docker-compose.yml
secrets:
  huggingface:
    file: ./secrets/huggingface

services:
  ash-nlp:
    secrets:
      - huggingface
```

Inside the container, the secret is available at:
```
/run/secrets/huggingface
```

### Local Development

For local development without Docker:
1. `SecretsManager` checks `/run/secrets/` first
2. Falls back to `./secrets/` directory
3. Finally checks environment variables

```python
from src.managers import get_secret

token = get_secret("huggingface")
```

### Environment Variable Fallback

Secrets can also be set via environment variables:

```bash
# Option 1: Our naming convention
export NLP_SECRET_HUGGINGFACE="hf_your_token"

# Option 2: Standard HuggingFace variable
export HF_TOKEN="hf_your_token"
```

---

## Security Best Practices

### DO ✅

- Use `chmod 600` for secret files
- Keep secrets out of Git (check `.gitignore`)
- Rotate tokens periodically
- Use Docker Secrets in production
- Delete tokens you no longer use

### DON'T ❌

- Commit secrets to Git
- Log or print secret values
- Share secrets in chat/email
- Use the same token for dev and prod
- Store secrets in environment files committed to Git

---

## File Format

Secret files should contain **only** the secret value:

**Correct** ✅
```
hf_abcdef123456789
```

**Wrong** ❌
```
HF_TOKEN=hf_abcdef123456789
```

**Wrong** ❌
```
"hf_abcdef123456789"
```

**Wrong** ❌
```
hf_abcdef123456789

```
(trailing newline can cause issues)

---

## Troubleshooting

### Secret Not Found

```
DEBUG: Secret 'huggingface' not found
```

Check:
1. File exists: `ls -la secrets/huggingface`
2. File has content: `cat secrets/huggingface`
3. No extra whitespace: `cat -A secrets/huggingface`

### Permission Denied

```
WARNING: Failed to read Docker secret 'huggingface': Permission denied
```

Fix permissions:
```bash
chmod 600 secrets/huggingface
```

### Token Not Working

1. Verify token at https://huggingface.co/settings/tokens
2. Check token has correct permissions (read access)
3. Token may have expired - generate a new one

### Docker Secrets Not Mounting

Verify in docker-compose.yml:
```yaml
secrets:
  huggingface:
    file: ./secrets/huggingface  # Path relative to docker-compose.yml

services:
  ash-nlp:
    secrets:
      - huggingface  # Must be listed here
```

Check inside container:
```bash
docker exec ash-nlp ls -la /run/secrets/
docker exec ash-nlp cat /run/secrets/huggingface
```

---

## Testing Secrets

### Verify SecretsManager

```python
from src.managers import create_secrets_manager

secrets = create_secrets_manager()
print(secrets.get_status())
# Shows which secrets are available

token = secrets.get_huggingface_token()
if token:
    print(f"Token loaded: {token[:10]}...")  # Only show prefix!
else:
    print("No token found")
```

### Verify in Docker

```bash
# Check secrets are mounted
docker exec ash-nlp ls -la /run/secrets/

# Check SecretsManager can read them
docker exec ash-nlp python -c "
from src.managers import create_secrets_manager
s = create_secrets_manager()
print(s.get_status())
"
```

---

## Adding New Secrets

1. Create the secret file in `secrets/`
2. Add to `docker-compose.yml`:
   ```yaml
   secrets:
     new_secret:
       file: ./secrets/new_secret
   
   services:
     ash-nlp:
       secrets:
         - new_secret
   ```
3. Add to `KNOWN_SECRETS` in `src/managers/secrets_manager.py`
4. Access in code:
   ```python
   from src.managers import get_secret
   value = get_secret("new_secret")
   ```

---

## Support

- **Discord**: [discord.gg/alphabetcartel](https://discord.gg/alphabetcartel)
- **GitHub Issues**: [github.com/the-alphabet-cartel/ash-nlp/issues](https://github.com/the-alphabet-cartel/ash-nlp/issues)

---

**Built with care for chosen family** 🏳️‍🌈
