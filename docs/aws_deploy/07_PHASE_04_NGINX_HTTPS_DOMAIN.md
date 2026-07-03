# 07 — Fase 4: Nginx, HTTPS e Domínio

> Configuração do proxy reverso, certificado SSL e domínio personalizado.
> Esta fase transforma o serviço de "funciona em HTTP" para "pronto para produção".

---

## O que é Nginx

Nginx (pronuncia-se "engine-x") é um servidor web de alta performance.
Originalmente criado para resolver o problema C10k (10.000 conexões simultâneas),
hoje é amplamente usado como:

1. **Servidor web** (serve arquivos estáticos diretamente)
2. **Proxy reverso** (recebe requisições e passa para outro servidor)
3. **Load balancer** (distribui requisições entre múltiplos backends)
4. **Terminador SSL** (cuida do HTTPS, passa HTTP para o backend)

**Neste projeto:** Nginx atuará como **proxy reverso** e **terminador SSL**.

---

## O que é proxy reverso

```
SEM proxy reverso:
Browser → Gunicorn (porta 8000) ← exposto diretamente na internet

COM proxy reverso:
Browser → Nginx (porta 443) → Gunicorn (porta 8000, apenas localhost)
```

**Por que o Gunicorn não deve ser exposto diretamente:**

| Recurso | Nginx | Gunicorn |
|---|---|---|
| TLS/HTTPS | Sim | Não |
| Compressão gzip | Sim | Não |
| Rate limiting | Sim | Não |
| Static files | Sim (nativo) | Via Django (mais lento) |
| Conexões simultâneas | Milhares | Dezenas |
| Proteção DDoS | Básica | Não |

O Gunicorn é excelente em executar Python — mas não foi feito para estar diretamente
exposto à internet.

---

## Como Nginx atua como proxy reverso

Fluxo completo de uma requisição HTTPS:

```
1. Browser envia: GET https://nicia-track.com/questoes/ HTTP/2

2. Nginx recebe na porta 443:
   - Verifica se o domínio é um dos seus server_name
   - Apresenta o certificado SSL (Let's Encrypt)
   - Faz o handshake TLS (negociação de criptografia)
   - Desencripta a requisição

3. Nginx adiciona headers ao passar para o Gunicorn:
   - X-Forwarded-Proto: https   ← Django usa isso para saber que é HTTPS
   - X-Forwarded-For: <IP-do-browser>
   - X-Real-IP: <IP-do-browser>

4. Nginx passa para: http://localhost:8000/questoes/

5. Gunicorn processa via Django → retorna HTML

6. Nginx encripta a resposta e devolve ao browser
```

---

## Por que não expor Django diretamente

Além dos motivos técnicos listados acima, há questões de segurança:

- **Stack traces expostos:** se `DEBUG=True` (acidentalmente), o Nginx pode
  ter um timeout antes de deixar o erro Django ser exibido ao usuário
- **Slow client attacks:** um cliente que lê a resposta muito devagar não bloqueia
  o worker do Gunicorn — o Nginx absorve essa lentidão
- **Cabeçalhos de segurança:** o Nginx pode adicionar `X-Frame-Options`,
  `Content-Security-Policy` etc. sem alterar o código Django

---

## O que é HTTPS

HTTPS = HTTP + TLS (Transport Layer Security).

**Por que é obrigatório em produção:**
- Sem HTTPS, senhas e dados são transmitidos em texto puro na rede
- Qualquer roteador entre o usuário e o servidor pode interceptar o tráfego
- Browsers modernos marcam sites HTTP como "Não seguros"
- Django em produção (`settings/production.py`) já redireciona HTTP → HTTPS
  (`SECURE_SSL_REDIRECT = True`)
- HSTS (`SECURE_HSTS_SECONDS = 31536000`) força o browser a usar HTTPS por 1 ano

**Certificado SSL:**
Um arquivo criptográfico que prova que o servidor é realmente quem diz ser.
- Emitido por uma CA (Certificate Authority)
- Let's Encrypt emite de graça, renovação automática a cada 90 dias
- Certbot é a ferramenta que instala e renova automaticamente

---

## Como o domínio aponta para a EC2

```
1. Você registra um domínio (ex.: nicia-track.com) num registrador
   (Namecheap, GoDaddy, Registro.br, Google Domains, ou AWS Route 53)

2. No painel do registrador, configura um registro DNS tipo A:
   - Host: @  (raiz do domínio) ou nicia-track.com
   - Value: <IP público da EC2>
   - TTL: 300 (5 minutos)

3. Propagação DNS leva até 48h, mas geralmente < 5 minutos

4. Após propagação:
   nslookup nicia-track.com → deve mostrar o IP da EC2
```

**Elastic IP:**
O IP público de uma EC2 padrão muda quando você para e reinicia a instância.
Configure um **Elastic IP** (IP fixo gratuito enquanto associado a uma EC2 rodando)
para que o DNS continue funcionando após reinicializações.

---

## Como SSL seria configurado (Let's Encrypt + Certbot)

```bash
# Na EC2 (após Nginx instalado):

# 1. Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# 2. Obter certificado
# (o domínio já deve estar apontando para esta EC2)
sudo certbot --nginx -d nicia-track.com -d www.nicia-track.com

# Certbot vai:
# - Criar um desafio HTTP em /.well-known/acme-challenge/
# - Let's Encrypt verifica que você controla o domínio
# - Emite o certificado
# - Configura o Nginx automaticamente (edita o arquivo de configuração)

# 3. Renovação automática (já configurada pelo certbot)
sudo crontab -l
# 0 0,12 * * * /usr/bin/certbot renew --quiet
```

**Certificado expira em 90 dias.** A renovação automática garante que nunca expira.

---

## Configuração Nginx (arquivo de configuração)

Arquivo: `/etc/nginx/sites-available/nicia-track`

```nginx
# Redireciona HTTP para HTTPS
server {
    listen 80;
    server_name nicia-track.com www.nicia-track.com;
    return 301 https://$host$request_uri;
}

# Serve HTTPS
server {
    listen 443 ssl http2;
    server_name nicia-track.com www.nicia-track.com;

    # Certificados (gerados pelo Certbot)
    ssl_certificate /etc/letsencrypt/live/nicia-track.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/nicia-track.com/privkey.pem;

    # Segurança SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;

    # Cabeçalhos de segurança
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;

    # Proxy para Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120;
    }

    # Opcional: Nginx serve static files (mais rápido que Django/WhiteNoise)
    # Só necessário se tirar o WhiteNoise ou se o volume justificar
    # location /static/ {
    #     alias /home/ubuntu/aws-nicia/staticfiles/;
    #     expires 1y;
    #     add_header Cache-Control "public, immutable";
    # }
}
```

---

## O papel de ALLOWED_HOSTS e CSRF_TRUSTED_ORIGINS

### ALLOWED_HOSTS

```python
# settings/base.py
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="").split(",")
```

**O que faz:** o Django verifica se o header `Host` da requisição está nesta lista.
Se não estiver, retorna 400 Bad Request.

**Por que existe:** protege contra ataques de "Host header injection".

**Configuração para produção:**
```bash
# .env
ALLOWED_HOSTS=nicia-track.com,www.nicia-track.com
```

### CSRF_TRUSTED_ORIGINS

```python
# settings/production.py
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in config("CSRF_TRUSTED_ORIGINS", default="").split(",")
    if origin.strip()
]
```

**O que faz:** o Django verifica se a origem de requisições POST está nesta lista.
Sem isso, qualquer formulário em HTTPS retorna 403 (CSRF token missing or incorrect).

**Por que existe:** proteção CSRF (Cross-Site Request Forgery). O Django exige
que requisições POST venham de origens confiáveis. Em HTTPS, a verificação é mais
rigorosa — deve incluir o esquema (https://).

**Configuração para produção:**
```bash
# .env
CSRF_TRUSTED_ORIGINS=https://nicia-track.com,https://www.nicia-track.com
```

### Por que SECURE_PROXY_SSL_HEADER é necessário

O Django tem `SECURE_SSL_REDIRECT = True` — redireciona HTTP para HTTPS.
Mas a requisição que chega ao Django (via Nginx) **já é HTTP** (o Nginx desencriptou).
Se o Django não souber que a requisição original era HTTPS, ele vai redirecionar
de HTTPS para HTTPS — loop infinito de redirecionamentos!

`SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")` resolve isso:
o Django lê o header `X-Forwarded-Proto: https` que o Nginx adicionou e entende
que a requisição original era HTTPS — sem redirecionar.

**Este setting já está configurado no `settings/production.py`.**

---

## Checklist da Fase 4

```
[ ] Elastic IP associado à EC2
[ ] Domínio registrado e apontando para o Elastic IP
[ ] Nginx instalado na EC2
[ ] Arquivo de configuração Nginx criado
[ ] nginx -t (teste de configuração) passa sem erros
[ ] Certbot instalado e certificado obtido
[ ] HTTPS funcionando: https://nicia-track.com
[ ] HTTP redireciona para HTTPS automaticamente
[ ] ALLOWED_HOSTS atualizado com o domínio
[ ] CSRF_TRUSTED_ORIGINS atualizado com https://
[ ] Formulários funcionam (sem 403)
[ ] curl -I https://nicia-track.com mostra Strict-Transport-Security
[ ] Renovação automática do certificado configurada
```
