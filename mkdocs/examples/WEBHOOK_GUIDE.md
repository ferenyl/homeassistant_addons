# MkDocs Webhook Integration Guide

Detta dokument beskriver hur du konfigurerar webhooks för automatisk ombyggnad av din MkDocs-dokumentation.

## GitHub Webhook Setup

1. Gå till ditt GitHub repository
2. Klicka på "Settings" → "Webhooks"
3. Klicka "Add webhook"
4. Konfigurera:
   - **Payload URL**: `http://din-homeassistant-ip:8081/webhook`
   - **Content type**: `application/json`
   - **Which events**: "Just the push event"
   - **Active**: ✓

## GitLab Webhook Setup

1. Gå till ditt GitLab projekt
2. Gå till "Settings" → "Webhooks"
3. Lägg till webhook:
   - **URL**: `http://din-homeassistant-ip:8081/webhook`
   - **Trigger**: "Push events"
   - **Enable SSL verification**: Av (om du inte har SSL)

## Port Forwarding

För att webhooks ska fungera från internet måste du:

1. Öppna port 8081 i din router
2. Vidarebefordra port 8081 till din Home Assistant-server
3. Använd din publika IP-adress i webhook-URL:en

## Säkerhet

**Viktigt**: Att exponera API:et på internet kan vara en säkerhetsrisk. Överväg dessa alternativ:

### Alternativ 1: VPN
- Använd VPN för att komma åt ditt hemmanätverk
- Konfigurera webhooks att använda din VPN-IP

### Alternativ 2: Cloudflare Tunnel
- Använd Cloudflare Tunnel för säker exponering
- Konfigurera tunnel som pekar på port 8081

### Alternativ 3: Reverse Proxy med autentisering
- Använd nginx eller traefik med basic auth
- Lägg till autentisering framför API:et

## Testning

Testa din webhook-konfiguration:

```bash
# Testa lokalt
curl -X POST http://localhost:8081/webhook

# Testa från internet (ersätt med din IP)
curl -X POST http://din-publika-ip:8081/webhook
```

## Felsökning

### Webhook fungerar inte
1. Kontrollera att port 8081 är öppen
2. Kolla add-on-loggarna för fel
3. Verifiera att `enable_api: true` i konfigurationen

### Onödiga ombyggnader
- Konfigurera Git-triggrar att endast trigga på ändringar i docs-filer
- Använd GitHub Actions/GitLab CI för mer avancerad logik

### Säkerhetsproblem
- Begränsa webhook-IP:s (whitelist GitHub/GitLab IP-ranges)
- Implementera webhook-signaturer för verifiering
- Använd HTTPS om möjligt

## Avancerad konfiguration

### Conditional Webhooks
Modifiera API-servern för att acceptera villkorliga rebuilds baserat på ändrade filer:

```python
# Exempel: Endast rebuild om docs/-filer ändrats
if 'docs/' in modified_files:
    trigger_rebuild()
```

### Rate Limiting
Implementera rate limiting för att förhindra spam:

```python
# Exempel: Max 1 rebuild per minut
if time.time() - last_rebuild < 60:
    return "Rate limited"
```