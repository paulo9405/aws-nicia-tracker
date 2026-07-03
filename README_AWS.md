# Nícia Track — Laboratório de Deploy na AWS

> Este repositório é uma **cópia do projeto Nícia Track** criada exclusivamente
> para estudo de deploy na AWS, construção de portfólio e preparação para
> entrevistas técnicas.
>
> O projeto original não é alterado. Este é o ambiente de experimentação.

---

## O que é este projeto

**Nícia Track** é uma plataforma Django de preparação para concursos públicos:
- 800 questões reais em 13 disciplinas
- Simulados com distribuição proporcional
- Dashboard de desempenho, streak e metas
- Plano de estudos com capítulos e revisão de erros
- Autenticação multiusuário por email

**Stack:** Python 3.12 · Django 4.2 · PostgreSQL · Bootstrap 5 · HTMX · Docker

---

## Objetivo do laboratório

Aprender na prática como fazer deploy de uma aplicação Django real na AWS,
cobrindo os serviços mais usados em produção:

| Serviço | Para quê |
|---|---|
| EC2 | Servidor de aplicação |
| Docker | Containerização e paridade de ambiente |
| RDS | Banco de dados PostgreSQL gerenciado |
| S3 | Arquivos estáticos e uploads de usuário |
| Nginx | Proxy reverso e terminação SSL |
| Let's Encrypt | Certificado HTTPS gratuito |
| IAM | Controle de acesso aos recursos |
| CloudWatch | Logs e monitoramento |

---

## Arquitetura planejada

```
Usuário
    │ HTTPS
    ▼
[DNS / Domínio]
    │
    ▼
[EC2 - Ubuntu 22.04]
    ├── Nginx (porta 443) ← proxy reverso + SSL
    └── Docker Container
            └── Gunicorn (porta 8000)
                    └── Django 4.2
                            ├── RDS PostgreSQL ← banco gerenciado
                            └── S3 ← static + media files
```

---

## Fases do deploy

| Fase | O que cobre | Status |
|---|---|---|
| 0 | Preparação e documentação | Em andamento |
| 1 | EC2 + Docker (aplicação rodando) | Aguardando |
| 2 | RDS PostgreSQL (banco gerenciado) | Aguardando |
| 3 | S3 (static e media files) | Aguardando |
| 4 | Nginx + HTTPS + domínio | Aguardando |
| 5 | Segurança, custos e monitoramento | Aguardando |
| 6 | Documentação final e portfólio | Aguardando |

---

## Documentação AWS

Toda a documentação planejada está em [`docs/aws_deploy/`](docs/aws_deploy/):

| Arquivo | Conteúdo |
|---|---|
| [01_PROJECT_ANALYSIS.md](docs/aws_deploy/01_PROJECT_ANALYSIS.md) | Análise completa do projeto existente |
| [02_AWS_DEPLOY_ROADMAP.md](docs/aws_deploy/02_AWS_DEPLOY_ROADMAP.md) | Plano por fases com riscos e critérios |
| [03_ARCHITECTURE_EXPLAINED.md](docs/aws_deploy/03_ARCHITECTURE_EXPLAINED.md) | Cada componente explicado em detalhe |
| [04_PHASE_01_EC2_DOCKER.md](docs/aws_deploy/04_PHASE_01_EC2_DOCKER.md) | Deploy na EC2 com Docker |
| [05_PHASE_02_RDS_POSTGRESQL.md](docs/aws_deploy/05_PHASE_02_RDS_POSTGRESQL.md) | Migração para RDS |
| [06_PHASE_03_S3_STATIC_MEDIA.md](docs/aws_deploy/06_PHASE_03_S3_STATIC_MEDIA.md) | Static e media no S3 |
| [07_PHASE_04_NGINX_HTTPS_DOMAIN.md](docs/aws_deploy/07_PHASE_04_NGINX_HTTPS_DOMAIN.md) | Nginx, HTTPS e domínio |
| [08_PHASE_05_SECURITY_COSTS_MONITORING.md](docs/aws_deploy/08_PHASE_05_SECURITY_COSTS_MONITORING.md) | Segurança, custos e monitoramento |
| [09_INTERVIEW_STUDY_GUIDE.md](docs/aws_deploy/09_INTERVIEW_STUDY_GUIDE.md) | Guia de entrevista (PT + EN) |
| [10_IMPLEMENTATION_LOG.md](docs/aws_deploy/10_IMPLEMENTATION_LOG.md) | Log vivo de decisões e problemas |
| [AWS_DEPLOY_CHECKLIST.md](docs/aws_deploy/AWS_DEPLOY_CHECKLIST.md) | Checklist por fase |

---

## Como rodar localmente (desenvolvimento)

```bash
# Clonar
git clone <url-do-repo>
cd aws-nicia

# Copiar variáveis de ambiente
cp .env.example .env
# Editar .env conforme necessário

# Opção A: com Docker Compose (PostgreSQL incluso)
docker compose up

# Opção B: sem Docker (SQLite, mais simples)
python -m venv .venv
source .venv/bin/activate
pip install -r requirements/development.txt
python manage.py migrate
python manage.py import_questions docs/15_BANCO_MESTRE_DE_QUESTOES.md
python manage.py create_admin
python manage.py runserver
```

---

## Tecnologias

**Backend:**
- Python 3.12
- Django 4.2 (MTV, CBV, Service Layer)
- PostgreSQL 16 (via psycopg2-binary)
- Gunicorn 22 (servidor WSGI de produção)
- WhiteNoise 6 (static files em produção)

**Frontend:**
- Bootstrap 5 (grid responsivo)
- HTMX (reatividade sem SPA)

**Infraestrutura:**
- Docker + Docker Compose
- AWS EC2, RDS, S3, IAM, CloudWatch
- Nginx (proxy reverso)
- Let's Encrypt (certificado SSL)

**Qualidade:**
- pytest + pytest-django (~3.000 linhas de testes)
- factory-boy, Faker, freezegun
- black, isort

---

## Segurança

- Nunca commitar `.env` (está no `.gitignore`)
- `DEBUG=False` obrigatório em produção
- `SECRET_KEY` única e gerada aleatoriamente para cada ambiente
- Banco acessível apenas pela EC2 (Security Group)
- HTTPS obrigatório (redirect automático)
- CSRF proteção ativa (`CSRF_TRUSTED_ORIGINS` configurado)

---

## Autor

Paulo Gomes — projeto de aprendizado de DevOps e AWS.
