# Checklist de Deploy AWS — Nícia Track

> Marque cada item conforme for concluído.
> Siga a ordem: cada fase depende da anterior.

---

## Fase 0 — Preparação local e repositório

```
[x] Projeto clonado em diretório separado (aws-nicia ≠ projeto original)
[x] git log --all -S "PASSWORD" não retorna nada
[x] git log --all -S "SECRET_KEY" não retorna nada
[x] .env está no .gitignore (verificado com: git check-ignore .env)
[x] db.sqlite3 está no .gitignore
[x] media/ está no .gitignore
[x] .env.example está completo com todas as variáveis necessárias para AWS
[x] README_AWS.md criado na raiz explicando o propósito do repositório
[x] docs/aws_deploy/ criada com todos os documentos de planejamento
[x] Conta AWS criada
[x] MFA habilitado na conta root AWS
[x] IAM User criado para uso diário (paulo-aws-admin)
[x] Billing alert configurado (USD 15/mês — alertas em 85%, 100% e previsão)
```

---

## Fase 1 — EC2 e Docker

### Criação da EC2
```
[x] Região AWS selecionada (us-east-2 — Ohio)
[x] AMI selecionada (Amazon Linux 2023 — em vez de Ubuntu 22.04; usar dnf, não apt)
[x] Tipo de instância: t3.micro (free tier — geração mais nova que t2.micro)
[x] Key pair criado e baixado (nicia-track-key.pem) para SSH
[x] Security Group criado com regras:
    [x] SSH (22) → IP próprio apenas (177.36.193.61/32)
    [x] HTTP (80) → 0.0.0.0/0
    [x] HTTPS (443) → 0.0.0.0/0
[ ] EBS: 20GB gp3
[x] EC2 criada e rodando
[x] Elastic IP criado (3.148.15.93) e associado à EC2
[x] Acesso SSH testado: ssh -i nicia-track-key.pem ec2-user@3.148.15.93
```

### Instalação de dependências na EC2
```
[x] Docker Engine instalado (v25.0.14)
[x] Docker Compose instalado (v5.3.0 — instalação manual; plugin não disponível nos repos AL2023)
[x] Git instalado (v2.50.1)
[x] docker ps funciona sem sudo (ec2-user no grupo docker)
```

### Deploy da aplicação
```
[x] Repositório clonado na EC2
[x] .env criado na EC2 com permissão 600
[x] .env contém SECRET_KEY forte (50+ chars)
[x] .env contém DEBUG=False
[x] .env contém DJANGO_SETTINGS_MODULE=config.settings.production
[x] .env contém ALLOWED_HOSTS
[x] .env contém CSRF_TRUSTED_ORIGINS
[x] docker build -t nicia-track:latest . (sem erros)
[x] Containers rodando: Gunicorn + PostgreSQL healthy (docker compose ps)
[x] docker logs não mostra erros fatais
[x] Gunicorn booting confirmado nos logs
[x] curl http://localhost:8000/conta/login/ retorna 200
[x] Acesso via browser: http://3.148.15.93/ funciona
[x] Login com admin funciona
[x] Questões aparecem no sistema
```

---

## Fase 2 — RDS PostgreSQL

### Criação do RDS
```
[ ] Engine: PostgreSQL 16
[ ] Template: Free Tier
[ ] DB Instance ID definido
[ ] Master username e password definidos e anotados
[ ] DB Instance Class: db.t3.micro
[ ] Storage: 20GB gp2, auto-scaling DESATIVADO
[ ] VPC: mesma da EC2
[ ] Public access: No
[ ] Security Group do RDS criado:
    [ ] Inbound PostgreSQL (5432) → Security Group da EC2
[ ] Initial database name: nicia_track
[ ] Backup retention: 7 dias
[ ] RDS criado e disponível (status: available)
[ ] Endpoint anotado
```

### Conexão e migração
```
[ ] .env atualizado: PGHOST=<endpoint-rds>
[ ] .env atualizado: PGDATABASE=nicia_track
[ ] .env atualizado: PGUSER=<master-user>
[ ] .env atualizado: PGPASSWORD=<senha>
[ ] DB_SSLMODE=require no .env (production.py usa sslmode configurável)
[ ] Container reiniciado com novas variáveis
[ ] docker exec nicia-track python manage.py dbshell (conecta sem erro)
[ ] python manage.py migrate roda sem erro
[ ] python manage.py import_questions roda e importa 800 questões
[ ] python manage.py create_admin cria o admin
[ ] Login funciona com o banco no RDS
[ ] Backup automático verificado no console AWS
```

---

## Fase 3 — S3 Static e Media

### Criação dos buckets S3
```
[ ] Bucket static criado (nome globalmente único)
[ ] Bucket static: Block public access DESATIVADO (static é público)
[ ] Bucket static: Bucket policy com AllowPublicRead configurada
[ ] Bucket static: CORS configurado
[ ] Bucket media criado (ou usar mesmo bucket com prefixos)
[ ] IAM User criado com permissões mínimas nos buckets
[ ] Access Key ID e Secret gerados e anotados
```

### Configuração do Django
```
[ ] django-storages[s3] adicionado a requirements/production.txt
[ ] boto3 adicionado a requirements/production.txt
[ ] settings/production.py atualizado com STORAGES para S3
[ ] .env atualizado: AWS_ACCESS_KEY_ID=<chave>
[ ] .env atualizado: AWS_SECRET_ACCESS_KEY=<segredo>
[ ] .env atualizado: AWS_STORAGE_BUCKET_NAME=<nome>
[ ] docker build com as novas dependências
[ ] python manage.py collectstatic envia arquivos para S3
[ ] CSS/JS no browser vêm de URLs s3.amazonaws.com
[ ] Upload de avatar salva no S3
[ ] Avatar aparece na página de perfil
```

---

## Fase 4 — Nginx, HTTPS e Domínio

### DNS e Elastic IP
```
[x] Domínio registrado (nicia.paulodev.net via Cloudflare)
[x] Registro DNS tipo A apontando para Elastic IP 3.148.15.93
[x] nslookup nicia.paulodev.net retorna o IP correto
```

### Nginx
```
[x] Nginx instalado na EC2
[x] Arquivo de configuração criado em /etc/nginx/sites-available/
[x] nginx -t passa (sem erros de sintaxe)
[x] nginx recarregado
[x] http://nicia.paulodev.net/ funciona
```

### HTTPS com Let's Encrypt
```
[x] Certbot instalado
[x] certbot --nginx -d nicia.paulodev.net executado com sucesso
[x] Certificado obtido
[x] https://nicia.paulodev.net/ funciona com cadeado verde
[x] http:// redireciona para https:// automaticamente
[x] Renovação automática configurada (certbot renew --dry-run validado)
[x] ALLOWED_HOSTS=nicia.paulodev.net atualizado no .env
[x] CSRF_TRUSTED_ORIGINS=https://nicia.paulodev.net atualizado no .env
[x] Container reiniciado com novas variáveis
[x] Formulários funcionam (sem 403)
[x] curl -I https://nicia.paulodev.net mostra Strict-Transport-Security
[x] Porta 8000 fechada no Security Group (nunca foi aberta — confirmado)
```

---

## Fase 5 — Segurança, Custos e Monitoramento

### Segurança
```
[x] DEBUG=False verificado em produção
[x] SECRET_KEY forte e única para produção
[x] .env não está no git (verificado)
[x] SSH restrito ao IP próprio no Security Group (177.36.193.61/32)
[ ] Acesso SSH por senha desabilitado (apenas key pair)
[ ] fail2ban instalado (ou equivalente)
[x] Porta 8000 fechada no Security Group
[x] MFA habilitado na conta root e IAM User principal
[ ] IAM: aplicação sem permissões desnecessárias (criar IAM User específico para S3 na Fase 3)
```

### Custos
```
[x] AWS Budget configurado (alerta em USD 15/mês)
[ ] AWS Cost Explorer habilitado
[ ] Procedimento de stop/teardown documentado
[ ] Estimativa de custo mensal calculada
```

### Logs e monitoramento
```
[x] Logs do Gunicorn acessíveis (docker logs)
[ ] Logs do Nginx acessíveis (/var/log/nginx/)
[ ] Rotação de logs configurada
[ ] CloudWatch métricas básicas da EC2 ativas
[ ] Alarme de CPU alta criado
[ ] SENTRY_DSN configurado no .env
[ ] Sentry recebendo erros de teste
```

---

## Fase 6 — Documentação final e portfólio

```
[ ] 10_IMPLEMENTATION_LOG.md atualizado com todas as etapas
[ ] README_AWS.md completo com arquitetura final
[ ] Screenshots do AWS Console (EC2, Security Groups, Cloudflare DNS, HTTPS)
[ ] Perguntas do 09_INTERVIEW_STUDY_GUIDE.md respondidas sem consulta
[ ] Teste de destroy e rebuild: deletar recursos e recriar do zero
[ ] Outro desenvolvedor consegue replicar seguindo este repositório
```
