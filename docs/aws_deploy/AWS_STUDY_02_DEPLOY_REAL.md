# AWS STUDY 02 — O Deploy Real (Nícia Track na AWS)

> Explicação de ponta a ponta da implementação que eu **realmente** fiz.
> Foco em entender cada decisão e como as peças se conectam.
>
> **Fatos reais deste deploy (memorize):**
> - **SO:** Amazon Linux 2023 (não Ubuntu) → `dnf`, usuário `ec2-user`
> - **Instância:** t3.micro, região **us-east-2 (Ohio)**
> - **Elastic IP:** `3.148.15.93`
> - **Domínio:** `https://nicia.paulodev.net` via **Cloudflare** (não Route 53)
> - **Banco:** PostgreSQL em **container Docker** na EC2 (não RDS)
> - **Migração real:** dados vieram do **Neon PostgreSQL 18** (que rodava com o Render)
> - **HTTPS:** Let's Encrypt + Certbot
> - **Planejado (não feito):** RDS, S3, CloudWatch, CI/CD

---

## Visão geral da arquitetura

```
Usuário (navegador)
      │  HTTPS (443)
      ▼
  Cloudflare  ── DNS de nicia.paulodev.net → aponta para o Elastic IP
      │
      ▼
  DNS resolve → 3.148.15.93 (Elastic IP da EC2)
      │
      ▼
┌──────────────────────────────────────────────────┐
│  EC2  (Amazon Linux 2023, t3.micro, us-east-2)    │
│                                                    │
│  Nginx (80/443)                                    │
│   ├── redireciona HTTP → HTTPS                      │
│   ├── termina SSL (certificado Let's Encrypt)      │
│   └── proxy_pass → 127.0.0.1:8000                   │
│                                                    │
│  Docker Compose (docker-compose.prod.yml)          │
│   ├── web:  Gunicorn → Django (porta 8000, local)  │
│   └── db:   PostgreSQL 16 (container)              │
└──────────────────────────────────────────────────┘
```

### O papel de cada componente

| Componente | Papel | Por que existe |
|---|---|---|
| **Cloudflare** | DNS + CDN + proteção DDoS | Traduz o domínio para o IP; protege e acelera a borda |
| **DNS (registro A)** | Aponta `nicia.paulodev.net` → `3.148.15.93` | Sem ele, o usuário teria que digitar o IP |
| **Elastic IP** | IP público fixo da EC2 | Reinício da EC2 não quebra o DNS |
| **EC2** | Servidor onde tudo roda | Controle total do ambiente |
| **Nginx** | Proxy reverso + terminação SSL | Gunicorn não deve ficar exposto direto à internet |
| **Gunicorn** | Servidor WSGI (workers paralelos) | Roda o Django em produção (runserver não serve) |
| **Django** | Lógica da aplicação (views→services→ORM) | O produto em si |
| **PostgreSQL (container)** | Banco relacional | Guarda usuários, questões, progresso |

### Sequência de uma requisição (o que acontece ao abrir o site)

```
1. Usuário digita https://nicia.paulodev.net
2. Cloudflare/DNS resolve o domínio → 3.148.15.93
3. Nginx recebe na 443, valida o certificado SSL, desencripta
4. Nginx repassa como HTTP para 127.0.0.1:8000 com header X-Forwarded-Proto: https
5. Gunicorn recebe e chama config.wsgi:application
6. Django: middleware → router → view → service → ORM
7. ORM consulta o PostgreSQL (container) → retorna dados
8. View renderiza o template (Bootstrap 5 + HTMX) → HTML
9. Gunicorn devolve ao Nginx → Nginx encripta → browser
```

---

## Timeline da implementação

> Ordem cronológica real, agrupada por fase. Cada etapa: **o que fiz · o que é ·
> por que · como conecta · erros possíveis · fala de entrevista.**

### Fase 0 — Conta AWS e segurança (2026-07-02)

#### 1. Criação da conta AWS
- **O que fiz:** ativei a conta com cartão de crédito e verifiquei o email.
- **O que é:** o container de tudo (recursos, identidades, faturamento).
- **Por quê:** ponto de partida obrigatório.
- **Conecta:** toda a infra vive dentro dela.
- **Entrevista:** "Antes de criar recurso, configurei segurança e custo."

#### 2. MFA na conta Root
- **O que fiz:** habilitei MFA no Root via authenticator app.
- **O que é:** segundo fator (senha + código do celular).
- **Por quê:** Root tem poder total; se vazar, perde-se tudo.
- **Erro possível:** habilitar MFA só depois de já ter usado o Root para tudo.
- **Entrevista:** "Root é chave-mestra: MFA e uso só em emergência."

#### 3. IAM User (`paulo-aws-admin`)
- **O que fiz:** criei o usuário com senha e troca obrigatória no 1º login.
- **O que é:** identidade para uso diário (substitui o Root).
- **Por quê:** princípio de não usar Root no dia a dia.
- **Conecta:** é com esse usuário que administro EC2, Security Groups etc.

#### 4. Grupo + Policy + MFA no usuário
- **O que fiz:** criei o grupo `Administrators` com `AdministratorAccess`, coloquei o usuário
  no grupo e habilitei MFA nele.
- **Erro real que cometi:** criei usuário, grupo e policy, mas **esqueci de adicionar o usuário
  ao grupo** → `Access Denied` e MFA inacessível. O campo "Grupo" mostrava `0`. Corrigi
  adicionando ao grupo; permissões vieram por herança `User → Group → Policy`.
- **Entrevista:** "Todo Access Denied começa no IAM: verifico usuário, grupo, policy e herança."

#### 5. Budget de custo
- **O que fiz:** Budget de **US$ 15/mês** com alertas em 85%, 100% e previsão de 100%.
- **Por quê:** na AWS o erro nº 1 é financeiro (esquecer recurso ligado).
- **Entrevista:** "Budget com alertas antes de qualquer infraestrutura."

### Fase 1 — EC2, Docker e deploy (2026-07-02 → 2026-07-03)

#### 6. Criação da EC2
- **O que fiz:** instância **Amazon Linux 2023, t3.micro, us-east-2**.
- **Desvios conscientes do plano:** era Ubuntu 22.04/t2.micro/us-east-1. Impacto: `dnf` no
  lugar de `apt`, usuário `ec2-user` no lugar de `ubuntu`, e Nginx/Certbot/Compose instalados
  de forma diferente.
- **Entrevista:** "Escolhi Amazon Linux 2023; isso muda o gerenciador para `dnf` e o usuário SSH."

#### 7. Key Pair e SSH
- **O que fiz:** gerei `nicia-track-key.pem`, apliquei `chmod 400`, conectei com
  `ssh -i nicia-track-key.pem ec2-user@3.148.15.93`.
- **O que é:** autenticação por par de chaves (pública na EC2, privada comigo).
- **Erro possível:** usar `ubuntu@` (é `ec2-user@`); chave com permissão aberta → SSH recusa.

#### 8. Security Group
- **O que fiz:** 22 → meu IP (`177.36.193.61/32`), 80 e 443 → `0.0.0.0/0`.
  Porta 8000 **nunca aberta**.
- **O que é:** firewall virtual stateful.
- **Por quê:** menor exposição — SSH só pra mim, Gunicorn nunca direto na internet.

#### 9. Elastic IP
- **O que fiz:** aloquei `3.148.15.93` e associei à EC2.
- **Por quê:** IP fixo para o DNS não quebrar em reinícios.

#### 10. Docker
- **O que fiz:** instalei Docker 25.0.14, iniciei via `systemctl`, habilitei no boot e
  adicionei `ec2-user` ao grupo `docker` (para rodar sem `sudo`).
- **Por quê:** empacotar a app com todas as dependências, paridade dev/prod.

#### 11. Docker Compose
- **O que fiz:** instalei Docker Compose **v5.3.0**.
- **Erro real:** o plugin `docker-compose-plugin` **não existe nos repos do Amazon Linux 2023**.
  Solução: baixar o binário oficial do GitHub para `/usr/local/lib/docker/cli-plugins/`.
- **O que é:** orquestra múltiplos containers (web + db) com um comando.

#### 12. Variáveis de ambiente (`.env`)
- **O que fiz:** criei `.env` na EC2 com `chmod 600` contendo `SECRET_KEY` forte, `DEBUG=False`,
  `DJANGO_SETTINGS_MODULE=config.settings.production`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`,
  variáveis `PG*` e `DB_SSLMODE`.
- **Por quê:** secrets fora do código; configuração muda por ambiente sem mexer no código.
- **Erro real:** `sslmode=require` do `production.py` era **incompatível** com o PostgreSQL do
  container (sem SSL). Solução: tornar o `sslmode` configurável via `DB_SSLMODE` (`disable` no
  container, `require` no futuro RDS).
- **Erro real:** `docker compose restart` **não recarrega** o `.env`. Solução: `down && up -d`.

#### 13. Deploy do Django
- **O que fiz:** criei `docker-compose.prod.yml` usando **imagem pré-construída**, fiz o build,
  subi os containers (Gunicorn + PostgreSQL `healthy`), e validei com
  `curl http://localhost:8000/conta/login/` → **HTTP 200**.
- **Erro real (HTTPS prematuro):** `SECURE_SSL_REDIRECT=True` causava **301** para um HTTPS que
  ainda não existia. Solução: desativar temporariamente HSTS/secure cookies/redirect e reativar
  só depois do Nginx+HTTPS prontos.

### Fase 2 — Nginx, Cloudflare, HTTPS e migração (2026-07-03)

#### 14. Nginx (proxy reverso)
- **O que fiz:** instalei e configurei o Nginx como proxy reverso na porta 80 → `127.0.0.1:8000`.
  Validei acesso externo em `http://3.148.15.93/conta/login/`.
- **Por quê:** Gunicorn não deve ficar exposto direto (sem TLS, rate limiting, proteção slowloris).
- **Erro real:** `curl http://localhost/` retornava a **página padrão do Nginx** — porque
  `server_name localhost` não bate com o virtual host do IP. Lição: testar sempre com o **IP real**.

#### 15. Cloudflare (DNS)
- **O que fiz:** configurei o Cloudflare como DNS de `nicia.paulodev.net` com registro **A** →
  `3.148.15.93`.
- **Por que Cloudflare e não Route 53:** já tinha conta; Cloudflare dá proteção DDoS e CDN grátis.

#### 16. HTTPS (Let's Encrypt + Certbot)
- **O que fiz:** obtive certificado SSL para `nicia.paulodev.net`, configurei o Nginx para 443 com
  redirect automático HTTP → HTTPS, e configurei renovação automática (validada com
  `certbot renew --dry-run`).
- **Reativei no Django:** `SECURE_SSL_REDIRECT`, HSTS e secure cookies; atualizei `ALLOWED_HOSTS`
  e `CSRF_TRUSTED_ORIGINS` com o domínio.
- **Detalhe crítico:** `SECURE_PROXY_SSL_HEADER` (já no `production.py`) faz o Django confiar no
  header `X-Forwarded-Proto: https` do Nginx — sem isso, loop infinito de redirect.
- **Resultado:** `https://nicia.paulodev.net` com cadeado verde; `curl -I` mostra HSTS.

#### 17. Migração do banco Neon → EC2
- **O que fiz:** migrei todos os dados de produção do **Neon PostgreSQL 18** (que servia o Render)
  para o **PostgreSQL 16 em container** na EC2.
- **Passos:** backup preventivo do banco AWS → validar acesso ao Neon (`psql`, 25 tabelas) →
  `pg_dump` → comparar contagens → `DROP SCHEMA public CASCADE` → `pg_restore` → validar.
- **Problema real de versão:** `pg_dump`/`pg_restore` v16 **não** lidam com o PostgreSQL 18 do Neon
  (`server version mismatch` / `unsupported version 1.16`). **Solução elegante:** usar um container
  temporário `postgres:18` para dump **e** restore. No restore, conectei o container temporário na
  **mesma rede Docker** do container de banco (`--network`) e usei `--no-owner` (o `neon_superuser`
  não existe no Postgres local).
- **Descoberta importante:** a estrutura (tabelas) já estava na AWS, mas os **dados de progresso**
  não — `lessonprogress` (16) e `useranswer` (85) só existiam no Neon. Contar registros **antes e
  depois** revelou isso. Estrutura correta ≠ dados migrados.
- **Avisos normais:** `transaction_timeout`, `cloud_admin`, `ALTER DEFAULT PRIVILEGES` são
  infraestrutura específica do Neon — não indicam falha.

#### 18. Hardening básico
- **O que fiz:** confirmei `DEBUG=False`, `SECRET_KEY` forte, `.env` fora do git e com `chmod 600`,
  SSH restrito ao meu IP, porta 8000 fechada, MFA no Root e no IAM User.
- **Ainda pendente (planejado):** desabilitar SSH por senha, `fail2ban`, IAM Role/usuário mínimo
  para S3.

---

## Decisões arquiteturais

> Para cada decisão: **contexto · alternativas · motivo · vantagens · desvantagens.**

### Por que EC2?
- **Contexto:** preciso hospedar a app e aprender infra de verdade.
- **Alternativas:** Render/Heroku (PaaS), ECS/Fargate, Lambda.
- **Motivo:** controle total e aprendizado — a EC2 expõe o que o PaaS esconde.
- **Vantagens:** controle, portfólio, base para RDS/S3/Nginx.
- **Desvantagens:** mais trabalho manual (patches, processos, firewall).

### Por que Docker?
- **Contexto:** o projeto já tinha Dockerfile funcional.
- **Alternativas:** instalar Python/Django direto na EC2 (venv).
- **Motivo:** paridade dev/prod e reprodutibilidade.
- **Vantagens:** "funciona na minha máquina" deixa de ser problema; isolamento.
- **Desvantagens:** curva de aprendizado; cold start mais lento (CMD roda migrations).

### Por que PostgreSQL?
- **Contexto:** app multiusuário com dados relacionais (usuários, questões, progresso).
- **Alternativas:** SQLite (dev), MySQL.
- **Motivo:** concorrência real, robustez, é o padrão do projeto (dev com Docker e prod).
- **Vantagens:** confiável, recursos avançados, integra nativo com Django.
- **Desvantagens:** exige gerenciamento (backup, versão) — sentido na dor da migração 18→16.

### Por que PostgreSQL em container (e ainda NÃO RDS)?
- **Contexto:** validar o stack completo antes de adicionar custo/complexidade.
- **Alternativas:** RDS gerenciado já de início.
- **Motivo:** simplicidade e custo zero; RDS cobra por hora mesmo parado.
- **Vantagens:** barato, rápido de subir, tudo num compose.
- **Desvantagens:** sem backup automático/failover; dados atrelados à EC2 → faço `pg_dump` manual.

### Por que Nginx?
- **Contexto:** preciso de HTTPS e de não expor o Gunicorn.
- **Alternativas:** expor Gunicorn direto; Caddy; ALB da AWS.
- **Motivo:** proxy reverso maduro + terminação SSL + headers de segurança.
- **Vantagens:** TLS, gzip, rate limiting, absorve conexões lentas.
- **Desvantagens:** mais uma peça para configurar e manter.

### Por que Gunicorn (e não runserver)?
- **Motivo:** `runserver` é single-thread, de desenvolvimento, inseguro na internet. Gunicorn
  tem workers paralelos e é o padrão WSGI de produção.

### Por que Cloudflare (e não Route 53)?
- **Contexto:** já tinha conta no Cloudflare.
- **Alternativas:** AWS Route 53.
- **Motivo:** DNS grátis + CDN + proteção DDoS sem custo adicional.
- **Vantagens:** custo zero, proteção na borda.
- **Desvantagens:** DNS fora da AWS (menos "tudo integrado"); menos alinhado a uma stack 100% AWS.

### Por que variáveis de ambiente?
- **Motivo:** separar configuração de código (12-factor). Secrets fora do git, config muda por
  ambiente sem rebuild.
- **Vantagens:** seguro, portável.
- **Desvantagens:** `.env` manual na EC2 pode divergir; para escala, usar SSM/Secrets Manager.

### Por que não deixar a porta 8000 aberta?
- **Motivo:** o Gunicorn não é feito para exposição direta (sem TLS, rate limiting, proteção
  slowloris). Só o Nginx (local) fala com ele. Menor superfície de ataque.

### Por que HTTPS?
- **Motivo:** sem TLS, senhas trafegam em texto puro; browsers marcam como "não seguro"; HSTS
  força HTTPS. Obrigatório em produção.

### Por que ainda não migrar para RDS?
- **Motivo:** custo por hora contínuo e complexidade adicional. Primeiro validei todo o stack.
  A migração é barata em esforço depois — só trocar variáveis `PG*` e `DB_SSLMODE=require`.

---

## O que aprendi na prática

> Aprendizados reais, tirados dos logs e da implementação — não teoria genérica.

1. **Conta Root não é para o dia a dia.** Usei só no setup, com MFA, e migrei para um IAM User.
2. **`User → Group → Policy` é literal.** Esqueci de pôr o usuário no grupo e tomei `Access Denied`
   com MFA inacessível. O campo "Grupo = 0" foi o diagnóstico.
3. **Security Group é firewall.** SSH só do meu IP; porta 8000 nunca aberta; só Nginx fala com
   Gunicorn.
4. **Elastic IP evita quebra de DNS.** IP fixo (3.148.15.93) para o registro A do Cloudflare.
5. **Amazon Linux ≠ Ubuntu.** `dnf` em vez de `apt`, `ec2-user` em vez de `ubuntu`, e o
   `docker-compose-plugin` não estava nos repos (instalei o binário manualmente).
6. **HTTPS exige configuração em dois lugares:** no Nginx (certificado, 443, redirect) **e** no
   Django (`SECURE_SSL_REDIRECT`, HSTS, `SECURE_PROXY_SSL_HEADER`, `CSRF_TRUSTED_ORIGINS`).
7. **Ligar `SECURE_SSL_REDIRECT` cedo demais quebra tudo.** Antes do HTTPS existir, dava 301 em
   loop. Desativei temporariamente e reativei depois.
8. **`docker compose restart` NÃO recarrega o `.env`.** Precisa de `down && up -d`.
9. **PostgreSQL tem incompatibilidade de versão.** `pg_dump`/`pg_restore` v16 não lidam com dump
   do servidor 18. Container temporário `postgres:18` resolveu dump e restore.
10. **Estrutura correta não garante dados migrados.** As tabelas existiam na AWS, mas o progresso
    dos alunos (16 lessonprogress, 85 useranswer) só estava no Neon. **Sempre contar registros
    antes e depois.**
11. **`sslmode` precisa ser configurável.** `require` quebra com Postgres em container (sem SSL);
    tornei `DB_SSLMODE` uma env var.
12. **Testar com o IP/host real.** `curl localhost` pegava a página padrão do Nginx por causa do
    `server_name`; só o IP real batia no virtual host certo.
13. **Backup antes de qualquer operação destrutiva.** Fiz `pg_dump` do banco AWS antes do
    `DROP SCHEMA`.

---

## Próximas fases

### ✅ Já implementado
- Conta AWS, MFA (Root + IAM User), IAM Group/Policy, Budget
- EC2 (Amazon Linux 2023, t3.micro, us-east-2), Key Pair, SSH
- Security Group (22/80/443; 8000 fechada), Elastic IP `3.148.15.93`
- Docker + Docker Compose + **PostgreSQL em container**
- Deploy do Django com Gunicorn, `.env` seguro
- Nginx (proxy reverso), Cloudflare DNS, HTTPS (Let's Encrypt)
- Migração de dados Neon 18 → EC2 16
- Hardening básico (DEBUG=False, SECRET_KEY forte, SSH restrito, 8000 fechada)

### 🔲 Planejado (ainda NÃO implementado)
- **RDS:** mover o PostgreSQL do container para banco gerenciado → backups automáticos, failover,
  ciclo de vida separado da EC2. Migração = trocar `PGHOST`/`DB_SSLMODE`, sem mexer no código.
- **S3:** mover media files (avatares) para bucket → resolve o problema do disco efêmero do
  container; static pode ir junto ou seguir no WhiteNoise. Requer `django-storages` + `boto3` e
  IAM com permissão mínima de S3.
- **CloudWatch:** alarme de CPU alta, logs centralizados (Nginx/Gunicorn), complementado com Sentry.
- **CI/CD (GitHub Actions):** push na `main` → build e deploy automáticos, separando as migrations
  do CMD do container (evita condição de corrida com múltiplas réplicas).
- **Hardening extra:** desabilitar SSH por senha, `fail2ban`, IAM Role na EC2 em vez de chaves.
