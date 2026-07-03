# 10 — Implementation Log: AWS Deploy

> Log vivo. Atualizar a cada passo implementado.
> Data, decisão tomada, problema encontrado, como foi resolvido.

---

## Fase atual

**Fase 3 — RDS, S3, CI/CD e monitoramento**
**Status:** Não iniciada
**Data início da Fase 3:** —

**Fase 2 — Domínio, HTTPS e segurança**
**Status:** Concluída
**Data início:** 2026-07-03
**Data conclusão:** 2026-07-03

**Fase 1 — Deploy inicial na EC2 com Docker**
**Status:** Concluída
**Data início:** 2026-07-02
**Data conclusão:** 2026-07-03

**Fase 0 — Preparação e documentação inicial**
**Status:** Concluída
**Data início:** 2026-07-01
**Data conclusão:** 2026-07-02

---

## Histórico de alterações

### 2026-07-01 — Análise e documentação inicial

**O que foi feito:**
- Leitura completa do projeto: Dockerfile, docker-compose.yml, settings/,
  requirements/, apps/, tests/, docs/, render.yaml, DEPLOY.md
- Criação da pasta `docs/aws_deploy/`
- Geração de 11 documentos de planejamento e referência

**Principais descobertas:**
- Projeto está bem estruturado com Dockerfile funcional e pronto para produção
- `settings/production.py` já espera variáveis `PG*` para PostgreSQL
- `SECURE_PROXY_SSL_HEADER` já está configurado (necessário para Nginx)
- WhiteNoise já serve static files — S3 é opcional para static, mas obrigatório para media
- CMD do Dockerfile roda migrations a cada startup (idempotente, mas lento em cold start)
- Nenhum secret está versionado (.env está no .gitignore)
- `sentry-sdk` já está em production.txt mas pode precisar de inicialização explícita

**Arquivos criados:**
- `docs/aws_deploy/01_PROJECT_ANALYSIS.md`
- `docs/aws_deploy/02_AWS_DEPLOY_ROADMAP.md`
- `docs/aws_deploy/03_ARCHITECTURE_EXPLAINED.md`
- `docs/aws_deploy/04_PHASE_01_EC2_DOCKER.md`
- `docs/aws_deploy/05_PHASE_02_RDS_POSTGRESQL.md`
- `docs/aws_deploy/06_PHASE_03_S3_STATIC_MEDIA.md`
- `docs/aws_deploy/07_PHASE_04_NGINX_HTTPS_DOMAIN.md`
- `docs/aws_deploy/08_PHASE_05_SECURITY_COSTS_MONITORING.md`
- `docs/aws_deploy/09_INTERVIEW_STUDY_GUIDE.md`
- `docs/aws_deploy/10_IMPLEMENTATION_LOG.md`
- `docs/aws_deploy/AWS_DEPLOY_CHECKLIST.md`
- `README_AWS.md`

### 2026-07-03 — Migração de dados: Neon PostgreSQL → EC2 PostgreSQL

**Fase:** 2

**O que foi feito:**
- Backup preventivo do banco AWS antes de qualquer alteração
- Validação de acesso ao Neon via `psql` (25 tabelas encontradas)
- Dump gerado com container temporário `postgres:18` (incompatibilidade de versão impediu uso do `pg_dump` local)
- Comparação de contagens: progresso dos alunos (`lessonprogress`: 16, `useranswer`: 85) existia no Neon mas não na AWS
- Schema limpo (`DROP SCHEMA public CASCADE`) para evitar conflitos
- Restore executado também com container `postgres:18` na rede Docker do container de destino
- Validação pós-restore: 25 tabelas, 16 lessonprogress, 85 useranswer, 3 usuários (incluindo niciadijkinga@hotmail.com)

**Problemas encontrados:**
- `pg_dump` local (v16) não aceita exportar banco PostgreSQL 18 do Neon
- `pg_restore` local (v16) não consegue ler dump gerado pelo pg_dump 18 (`unsupported version 1.16`)

**Como foi resolvido:**
- Container temporário `postgres:18` para ambos dump e restore
- Para o restore: descobrir a rede Docker do container de banco e conectar o container temporário na mesma rede via `--network`

**Decisões técnicas:**
- `--no-owner` no pg_restore (objetos do Neon como `neon_superuser` não existem no PostgreSQL local)
- Avisos sobre `transaction_timeout`, `cloud_admin` e `ALTER DEFAULT PRIVILEGES` são normais — infraestrutura Neon-específica

**Arquivos alterados:**
- `docs/aws_deploy/11_DATABASE_MIGRATION_NEON_TO_EC2.md` (criado)

**Próximo passo:**
- Considerar migração para RDS quando houver necessidade de backups automáticos e maior resiliência

---

### 2026-07-03 — Domínio, HTTPS, Nginx e hardening de produção concluídos

**Fase:** 2

**O que foi feito:**
- Cloudflare configurado como DNS para o domínio `nicia.paulodev.net`
- Registro DNS tipo A apontando para Elastic IP `3.148.15.93`
- Let's Encrypt + Certbot: certificado SSL obtido para `nicia.paulodev.net`
- Nginx configurado para HTTPS (porta 443) com redirect automático HTTP → HTTPS
- `ALLOWED_HOSTS` atualizado com o domínio real
- `CSRF_TRUSTED_ORIGINS` atualizado com `https://nicia.paulodev.net`
- `SECURE_SSL_REDIRECT`, HSTS e secure cookies reativados em `production.py`
- Renovação automática do certificado configurada (certbot)
- Porta 8000 confirmada como fechada no Security Group (nunca foi aberta — já estava correta)
- Validação final: `https://nicia.paulodev.net` acessível com cadeado verde
- Testes: `curl -I https://nicia.paulodev.net` e `sudo certbot renew --dry-run` executados com sucesso

**Arquitetura final confirmada:**
```
Internet → 80/443 → Nginx → localhost:8000 → Gunicorn → Django → PostgreSQL (container)
```

**Security Group da EC2 (estado final):**
```
22/TCP  (SSH)   → 177.36.193.61/32 (IP próprio)
80/TCP  (HTTP)  → 0.0.0.0/0
443/TCP (HTTPS) → 0.0.0.0/0
```
Porta 8000 não exposta externamente.

**Problemas encontrados:**
- Nenhum nesta etapa.

**Próximo passo:**
- Fase 3: backup automático do PostgreSQL, migração para RDS, S3 para media files,
  CloudWatch, CI/CD com GitHub Actions.

---

### 2026-07-02 — EC2 criada, Elastic IP, SSH e Docker instalado

**Fase:** 1

**O que foi feito:**
- Instância EC2 criada na região us-east-2 (Ohio)
- Chave SSH `nicia-track-key.pem` gerada e permissões configuradas (`chmod 400`)
- Security Group configurado: porta 22 (SSH) → IP próprio, porta 80 (HTTP) → 0.0.0.0/0
- Elastic IP `3.148.15.93` alocado e associado à EC2
- Acesso SSH validado: `ssh -i nicia-track-key.pem ec2-user@3.148.15.93`
- Sistema atualizado: `sudo dnf update -y`
- Git instalado: versão 2.50.1
- Docker instalado: versão 25.0.14
- Docker iniciado via systemctl e habilitado no boot
- `ec2-user` adicionado ao grupo `docker` (sem necessidade de sudo)
- Docker validado: `docker ps` funciona sem permissão negada

**Desvios em relação ao plano original:**

| Item | Planejado | Executado | Impacto |
|---|---|---|---|
| Região | us-east-1 | us-east-2 (Ohio) | Nenhum — mesma latência para BR |
| SO | Ubuntu 22.04 LTS | Amazon Linux 2023 | Gerenciador de pacotes é `dnf` (não `apt`); usuário SSH é `ec2-user` (não `ubuntu`) |
| Tipo da instância | t2.micro | t3.micro | Melhor performance (geração mais nova), também free tier |
| Porta 443 no SG | Abrir agora | Não aberta ainda | Abrir antes de configurar Nginx/HTTPS |

> **Atenção futura:** Certbot e Nginx têm instalação diferente no Amazon Linux 2023
> (não usar `apt install certbot python3-certbot-nginx` — usar `dnf` ou instalação via snap/pip).

**Problemas encontrados:**
- Nenhum. Todos os passos executados sem erros.

**Próximo passo:**
- Clonar o repositório na EC2
- Criar `.env` com variáveis de produção
- Executar `docker build` e subir o container

---

### 2026-07-02 — Configuração inicial da conta AWS

**Fase:** 0

**O que foi feito:**
- Criação e ativação da conta AWS com cadastro de cartão de crédito
- Ativação de MFA na conta Root via authenticator app
- Criação do AWS Budget: US$ 15/mês com alertas em 85%, 100% e previsão de 100%
- Criação do IAM User `paulo-aws-admin` com senha e troca obrigatória na primeira entrada
- Criação do grupo IAM `Administrators` com a policy gerenciada `AdministratorAccess`
- Adição do `paulo-aws-admin` ao grupo `Administrators`
- Ativação de MFA no `paulo-aws-admin` via authenticator app
- Validação: login com `paulo-aws-admin` + acesso ao EC2 confirmado sem Access Denied

**Problemas encontrados:**
- Usuário `paulo-aws-admin` criado mas não adicionado ao grupo `Administrators`
  → Resultado: Access Denied e MFA inacessível

**Como foi resolvido:**
- Identificado na lista de usuários IAM que o campo "Grupo" mostrava 0
- Adicionado manualmente o usuário ao grupo `Administrators`
- Permissões aplicadas imediatamente via herança `User → Group → Policy`

**Decisões técnicas:**
- `paulo-aws-admin` com `AdministratorAccess` é para uso humano no console — correto
- IAM User específico para a aplicação Django (permissões mínimas em S3) será criado na Fase 3

**Arquivos alterados:**
- `docs/aws_deploy/conta-aws-criada.md` (criado pelo usuário, documenta os passos)

**Próximo passo:**
- Iniciar Fase 1: criar instância EC2 (Ubuntu 22.04, t2.micro)

---

## Alterações realizadas no código

Nenhuma alteração de código até o momento.
O objetivo desta fase é documentação, análise e configuração da conta AWS.

---

## Problemas encontrados

| Data | Problema | Solução |
|---|---|---|
| 2026-07-02 | IAM User criado sem estar no grupo → Access Denied | Adicionado ao grupo `Administrators`; permissões aplicadas via herança `User → Group → Policy` |

---

## Decisões técnicas registradas

| Decisão | Motivo |
|---|---|
| Manter Dockerfile original | Não alterar código sem necessidade — funciona para Render, adaptação mínima para AWS |
| WhiteNoise para static files na Fase 1 | Já está configurado e funciona; S3 fica para fase posterior |
| Separar media files em S3 antes de static | Media files têm risco real de perda; static é opcional |
| RDS Multi-AZ desativado | Laboratório — custo dobra desnecessariamente |
| t2.micro / db.t3.micro | Free tier — custo zero nos primeiros 12 meses |
| Cloudflare como DNS (em vez de Route 53) | Já tinha conta; Cloudflare oferece proteção DDoS e CDN gratuitos |
| PostgreSQL em container (não RDS) nas Fases 1-2 | Validar o stack completo antes de adicionar complexidade do RDS |

---

## Próximos passos

- [x] Criar conta AWS e habilitar MFA na conta root *(2026-07-02)*
- [x] Criar IAM User com permissões de administrador para uso diário *(2026-07-02)*
- [x] Configurar Budget com alertas de custo *(2026-07-02)*
- [x] Verificar secrets no histórico git — nenhum encontrado *(2026-07-02)*
- [x] Criar instância EC2 — Amazon Linux 2023, t3.micro, us-east-2 *(2026-07-02)*
- [x] Configurar Security Group (portas 22 e 80) *(2026-07-02)*
- [x] Criar e associar Elastic IP `3.148.15.93` à EC2 *(2026-07-02)*
- [x] Instalar Git e Docker na EC2 *(2026-07-02)*
- [x] Docker funcionando sem sudo (`ec2-user` no grupo docker) *(2026-07-02)*
- [x] Abrir porta 443 no Security Group *(2026-07-02)*
- [x] Instalar Docker Compose v5.3.0 na EC2 (manual — plugin não disponível nos repos do AL2023) *(2026-07-02)*
- [x] Clonar repositório na EC2 *(2026-07-02)*
- [x] Analisar Dockerfile, docker-compose.yml e production.py *(2026-07-02)*
- [x] Ajustar `production.py`: `DB_SSLMODE` configurável e HTTPS desativado temporariamente *(2026-07-03)*
- [x] Criar `docker-compose.prod.yml` para EC2 com imagem pré-construída *(2026-07-03)*
- [x] Criar `.env` na EC2 com variáveis de produção *(2026-07-03)*
- [x] Build da imagem Docker na EC2 *(2026-07-03)*
- [x] Containers rodando: Gunicorn + PostgreSQL healthy *(2026-07-03)*
- [x] `curl http://localhost:8000/conta/login/` retorna HTTP 200 *(2026-07-03)*
- [x] Nginx instalado e configurado como proxy reverso (porta 80 → 8000) *(2026-07-03)*
- [x] `http://3.148.15.93/conta/login/` acessível externamente via porta 80 *(2026-07-03)*
- [x] Porta 8000 confirmada como fechada no Security Group *(2026-07-03)*
- [x] Domínio `nicia.paulodev.net` registrado e apontado via Cloudflare para `3.148.15.93` *(2026-07-03)*
- [x] Certbot instalado e certificado SSL obtido (Let's Encrypt) *(2026-07-03)*
- [x] Nginx configurado para HTTPS (porta 443) e redirect HTTP → HTTPS *(2026-07-03)*
- [x] `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS` atualizados com o domínio *(2026-07-03)*
- [x] `SECURE_SSL_REDIRECT`, HSTS e secure cookies reativados em `production.py` *(2026-07-03)*
- [x] Renovação automática do certificado configurada *(2026-07-03)*
- [x] `https://nicia.paulodev.net` acessível com cadeado verde *(2026-07-03)*
- [ ] Migrar PostgreSQL do container para RDS
- [ ] Configurar backup automático do banco
- [ ] S3 para media files (avatares)
- [ ] CloudWatch: logs centralizados e alarme de CPU
- [ ] CI/CD com GitHub Actions

---

## Template para próximas entradas

```markdown
### YYYY-MM-DD — [Descrição da atividade]

**Fase:** X

**O que foi feito:**
-

**Problemas encontrados:**
-

**Como foi resolvido:**
-

**Decisões técnicas:**
-

**Arquivos alterados:**
-

**Próximo passo:**
-
```

---

## Registro de erros e soluções

| Data | Erro | Solução |
|---|---|---|
| 2026-07-02 | IAM User `paulo-aws-admin` sem grupo → Access Denied | Adicionado ao grupo `Administrators`; permissões herdadas imediatamente |
| 2026-07-02 | SO escolhido (Amazon Linux 2023) difere do plano (Ubuntu 22.04) | Sem erro — decisão consciente; impacta comandos futuros de Nginx e Certbot (usar `dnf` em vez de `apt`) |
| 2026-07-02 | `docker-compose-plugin` não disponível nos repositórios do Amazon Linux 2023 | Instalação manual do binário oficial do GitHub em `/usr/local/lib/docker/cli-plugins/` |
| 2026-07-02 | `sslmode=require` em `production.py` incompatível com PostgreSQL em container (sem SSL) | Tornar `sslmode` configurável via env var `DB_SSLMODE`; usar `disable` no container, `require` no RDS |
| 2026-07-03 | `SECURE_SSL_REDIRECT=True` causava 301 para HTTPS inexistente | Desativado temporariamente junto com HSTS e secure cookies; reativar na Fase 4 (Nginx + HTTPS) |
| 2026-07-03 | `docker compose restart` não recarrega variáveis do `.env` | Usar `docker compose down && up -d` para recarregar env vars |
| 2026-07-03 | `curl http://localhost/` retorna página padrão do Nginx | Normal — `server_name localhost` não corresponde ao virtual host `3.148.15.93`; testar sempre com o IP real |

---

## Recursos e referências úteis

| Recurso | Link / Localização |
|---|---|
| Documentação oficial Django | https://docs.djangoproject.com/en/4.2/ |
| AWS EC2 User Guide | https://docs.aws.amazon.com/ec2/ |
| AWS RDS PostgreSQL | https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/ |
| AWS S3 | https://docs.aws.amazon.com/s3/ |
| django-storages S3 | https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html |
| Let's Encrypt / Certbot | https://certbot.eff.org/ |
| Gunicorn configuration | https://docs.gunicorn.org/en/stable/settings.html |
| Nginx documentation | https://nginx.org/en/docs/ |
