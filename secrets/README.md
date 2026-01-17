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
| `ash_nlp_discord_alert_token` | Discord Webhook for Ash-NLP Alerts | ✅ Required |
| `huggingface_token` | HuggingFace API Token | ✅ Required |

> **Note**: Each Ash module now uses its own Discord alert webhook for independent routing.
> The legacy shared `discord_alert_token` is deprecated.

---

## Setup Instructions

### 1. Create the secrets directory

```bash
mkdir -p secrets
```

### 2. Add Ash-NLP Discord Alert Webhook (Required for Ash-NLP Alerts)

For model conflict alerts and system notifications from Ash-NLP:

1. In Discord: Server Settings → Integrations → Webhooks → New Webhook
2. Name it something like "Ash-NLP Alerts"
3. Select the channel for alerts (e.g., #ash-nlp-alerts)
4. Copy the webhook URL
5. Create the secret:

```bash
# Create the webhook secret for Ash-NLP
echo "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN" > secrets/ash_nlp_discord_alert_token

# Set secure permissions
chown nas:nas secrets/ash_nlp_discord_alert_token
chmod 600 secrets/ash_nlp_discord_alert_token
```

### 3. Add HuggingFace API Token (Required for Ash-NLP)

Get your token from: [HuggingFace API Token](https://huggingface.co/settings/tokens)

```bash
# Create the secret file (no file extension)
echo "your_huggingface_api_token_here" > secrets/huggingface_token

# Set secure permissions
chown nas:nas secrets/huggingface_token
chmod 600 secrets/huggingface_token
```

### 4. Verify Setup

```bash
# Check files exist and have content
ls -la secrets/

# Verify permissions (should be 600 or -rw-------)
# Verify no trailing whitespace
cat -A secrets/ash_nlp_discord_alert_token
cat -A secrets/huggingface_token
```

---

## How It Works

### Docker Secrets (Production)

When running with Docker Compose, secrets are:
1. Defined in `docker-compose.yml`
2. Mounted to `/run/secrets/<n>` inside the container
3. Read by `SecretsManager` at startup

```yaml
# docker-compose.yml
secrets:
  ash_nlp_discord_alert_token:
    file: ./secrets/ash_nlp_discord_alert_token
  huggingface_token:
    file: ./secrets/huggingface_token

services:
  ash-nlp:
    secrets:
      - ash_nlp_discord_alert_token
      - huggingface_token
```

Inside the container, the secrets are available at:
```
/run/secrets/ash_nlp_discord_alert_token
/run/secrets/huggingface_token
```

### Local Development

For local development without Docker:
1. `SecretsManager` checks `/run/secrets/` first
2. Falls back to `./secrets/` directory
3. Finally checks environment variables

```python
from src.managers import create_secrets_manager

secrets = create_secrets_manager()
discord_alert_token = secrets.get_discord_alert_token()  # Returns ash_nlp_discord_alert_token
huggingface_token = secrets.get_huggingface_token()
```

---

## Security Best Practices

### DO ✅

- Use `chmod 600` for secret files
- Keep secrets out of Git (check `.gitignore`)
- Rotate tokens periodically
- Use Docker Secrets in production

### DON'T ❌

- Commit secrets to Git
- Log or print secret values
- Share secrets in chat/email
- Include quotes or extra whitespace in secret files

---

## Troubleshooting

### Secret Not Found

Check:
1. File exists: `ls -la secrets/huggingface_token`
2. File has content: `cat secrets/huggingface_token`
3. No extra whitespace: `cat -A secrets/huggingface_token`

### Permission Denied

Fix permissions:
```bash
chmod 600 secrets/huggingface_token
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

## Support

- **Discord**: [discord.gg/alphabetcartel](https://discord.gg/alphabetcartel)
- **GitHub Issues**: [github.com/the-alphabet-cartel/ash-nlp/issues](https://github.com/the-alphabet-cartel/ash-nlp/issues)

---

**Built with care for chosen family** 🏳️‍🌈
