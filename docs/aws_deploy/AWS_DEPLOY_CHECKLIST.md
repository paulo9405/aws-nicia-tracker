# Checklist de Deploy AWS — Nícia Track

> Marque cada item conforme for concluído.
> Siga a ordem: cada fase depende da anterior.

---

## Fase 0 — Preparação local e repositório

```
[ ] Projeto clonado em diretório separado (aws-nicia ≠ projeto original)
[ ] git log --all -S "PASSWORD" não retorna nada
[ ] git log --all -S "SECRET_KEY" não retorna nada
[ ] .env está no .gitignore (verificado com: git check-ignore .env)
[ ] db.sqlite3 está no .gitignore
[ ] media/ está no .gitignore
[ ] .env.example está completo com todas as variáveis necessárias para AWS
[ ] README_AWS.md criado na raiz explicando o propósito do repositório
[ ] docs/aws_deploy/ criada com todos os documentos de planejamento
[ ] Conta AWS criada
[ ] MFA habilitado na conta root AWS
[ ] IAM User criado para uso diário (não usar root)
[ ] Billing alert configurado (ex.: USD 15/mês)
```

---

## Fase 1 — EC2 e Docker

### Criação da EC2
```
[ ] Região AWS selecionada (ex.: us-east-1 ou sa-east-1)
[ ] AMI Ubuntu 22.04 LTS selecionada
[ ] Tipo de instância: t2.micro (free tier)
[ ] Key pair criado e baixado (.pem) para SSH
[ ] Security Group criado com regras:
    [ ] SSH (22) → seu IP apenas
    [ ] HTTP (80) → 0.0.0.0/0
    [ ] HTTPS (443) → 0.0.0.0/0
[ ] EBS: 20GB gp3
[ ] EC2 criada e rodando
[ ] Elastic IP criado e associado à EC2
[ ] Acesso SSH testado: ssh -i chave.pem ubuntu@<IP>
```

### Instalação de dependências na EC2
```
[ ] Docker Engine instalado
[ ] Docker Compose plugin instalado
[ ] Git instalado
[ ] docker run hello-world funciona sem sudo
```

### Deploy da aplicação
```
[ ] Repositório clonado na EC2 (/home/ubuntu/aws-nicia)
[ ] .env criado na EC2 com permissão 600
[ ] .env contém SECRET_KEY forte (50+ chars)
[ ] .env contém DEBUG=False
[ ] .env contém DJANGO_SETTINGS_MODULE=config.settings.production
[ ] .env contém ALLOWED_HOSTS=<IP da EC2>
[ ] .env contém CSRF_TRUSTED_ORIGINS=http://<IP da EC2>:8000
[ ] docker build -t nicia-track:latest . (sem erros)
[ ] Container iniciado (docker ps mostra running)
[ ] docker logs nicia-track não mostra erros fatais
[ ] Gunicorn booting confirmado nos logs
[ ] curl http://localhost:8000/conta/login/ retorna 200
[ ] Acesso via browser: http://<IP>:8000/ funciona
[ ] Login com admin funciona
[ ] Questões aparecem no sistema
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
[ ] Domínio registrado (ou subdomínio disponível)
[ ] Registro DNS tipo A apontando para Elastic IP da EC2
[ ] nslookup <domínio> retorna o IP correto
```

### Nginx
```
[ ] Nginx instalado na EC2
[ ] Arquivo de configuração criado em /etc/nginx/sites-available/
[ ] Link simbólico em sites-enabled
[ ] nginx -t passa (sem erros de sintaxe)
[ ] nginx recarregado
[ ] http://<dominio>/ funciona (ainda sem HTTPS)
```

### HTTPS com Let's Encrypt
```
[ ] Certbot instalado
[ ] certbot --nginx -d <dominio> executado com sucesso
[ ] Certificado obtido
[ ] https://<dominio>/ funciona com cadeado verde
[ ] http:// redireciona para https:// automaticamente
[ ] Renovação automática configurada (crontab ou systemd timer)
[ ] ALLOWED_HOSTS=<dominio> atualizado no .env
[ ] CSRF_TRUSTED_ORIGINS=https://<dominio> atualizado no .env
[ ] Container reiniciado com novas variáveis
[ ] Formulários funcionam (sem 403)
[ ] curl -I https://<dominio> mostra Strict-Transport-Security
```

---

## Fase 5 — Segurança, Custos e Monitoramento

### Segurança
```
[ ] DEBUG=False verificado em produção
[ ] SECRET_KEY forte e única para produção
[ ] .env não está no git (verificado)
[ ] SSH restrito ao seu IP no Security Group
[ ] Acesso SSH por senha desabilitado (apenas key pair)
[ ] fail2ban instalado (ou equivalente)
[ ] RDS não acessível da internet (verificado)
[ ] IAM: aplicação sem permissões desnecessárias
[ ] MFA habilitado na conta root e IAM User principal
[ ] Porta 8000 fechada no Security Group (apenas 80 e 443)
```

### Custos
```
[ ] AWS Budget configurado (alerta em USD 15)
[ ] AWS Cost Explorer habilitado
[ ] Procedimento de stop/teardown documentado
[ ] Estimativa de custo mensal calculada
```

### Logs e monitoramento
```
[ ] Logs do Gunicorn acessíveis (docker logs)
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
[ ] Screenshots do AWS Console (EC2, RDS, S3, CloudWatch)
[ ] Perguntas do 09_INTERVIEW_STUDY_GUIDE.md respondidas sem consulta
[ ] Teste de destroy e rebuild: deletar recursos e recriar do zero
[ ] Outro desenvolvedor consegue replicar seguindo este repositório
```
