# 10 — Implementation Log: AWS Deploy

> Log vivo. Atualizar a cada passo implementado.
> Data, decisão tomada, problema encontrado, como foi resolvido.

---

## Fase atual

**Fase 1 — Deploy inicial na EC2 com Docker**
**Status:** Em andamento (EC2 pronta, Docker instalado, deploy pendente)
**Data início da Fase 1:** 2026-07-02

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
| WhiteNoise para static files na Fase 1 | Já está configurado e funciona; S3 fica para Fase 3 |
| Separar media files em S3 antes de static | Media files têm risco real de perda; static é opcional |
| RDS Multi-AZ desativado | Laboratório — custo dobra desnecessariamente |
| t2.micro / db.t3.micro | Free tier — custo zero nos primeiros 12 meses |

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
- [ ] Ajustar `production.py` para tornar `sslmode` configurável via env var
- [ ] Criar `docker-compose.prod.yml` para EC2 (PostgreSQL em container + Django)
- [ ] Criar `.env` na EC2 com variáveis de produção
- [ ] Build da imagem Docker na EC2
- [ ] Subir containers com `docker compose -f docker-compose.prod.yml up -d`
- [ ] Verificar acesso via IP público (porta 80)

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
