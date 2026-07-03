# 04 — Fase 1: Deploy na EC2 com Docker

> Guia conceitual e passo a passo para colocar a aplicação rodando numa EC2.
> Não execute ainda — leia e entenda antes de agir.

---

## O que é EC2

EC2 (Elastic Compute Cloud) é o serviço de máquinas virtuais da AWS.
Você aluga um servidor virtual, paga por hora de uso e tem acesso root via SSH.

**Vantagens:**
- Controle total: você instala, configura e gerencia tudo
- Free tier: `t2.micro` (1 vCPU, 1GB RAM) é gratuito por 12 meses
- Escalável: muda o tipo da instância sem recriar o servidor

**Analogia:** EC2 é como alugar um computador na nuvem. Você acessa pelo terminal,
instala o que precisar e roda sua aplicação — igual a um VPS (DigitalOcean, Linode).

---

## Por que usar EC2 neste laboratório

1. **Aprendizado**: diferente do Render (que abstrai tudo), a EC2 expõe o que acontece
   por baixo — instalação de Docker, configuração de firewall, gerenciamento de processos.
2. **Portfólio**: saber fazer deploy em EC2 é uma habilidade valorizada no mercado.
3. **Base para o resto**: RDS, S3 e Nginx (próximas fases) se integram naturalmente
   com uma EC2 dentro da mesma VPC.

---

## O que precisa ser instalado na EC2

```
Sistema operacional: Ubuntu 22.04 LTS (AMI pública gratuita)

Pacotes necessários:
- Docker Engine
- Docker Compose (plugin v2)
- Git (para clonar o repositório)
- ufw ou configuração de Security Groups (firewall)
```

**Nada mais.** Toda a aplicação — Python, Django, PostgreSQL local (se necessário),
dependências — roda dentro dos containers Docker. A EC2 é apenas a máquina que
hospeda esses containers.

---

## Como o projeto chegaria à EC2

### Opção A: git clone (recomendada para este laboratório)
```bash
# Na EC2, após instalar Git:
git clone https://github.com/seu-usuario/aws-nicia.git
cd aws-nicia
```

**Vantagem:** atualizar é simples (`git pull` + rebuild Docker).
**Cuidado:** repositório deve ser público ou você precisa configurar SSH key.

### Opção B: SCP / SFTP (transferência direta de arquivos)
```bash
# Na sua máquina local:
scp -i chave.pem -r ./aws-nicia ubuntu@<IP-EC2>:/home/ubuntu/
```

**Vantagem:** não precisa de repositório público.
**Desvantagem:** trabalhoso para atualizações.

### Opção C: Docker image via ECR
Construir a imagem localmente, fazer push para ECR (Amazon Container Registry)
e fazer pull na EC2. Mais profissional, mas mais complexo — fica para uma fase avançada.

---

## Como Docker seria usado

### Build da imagem
```bash
cd /home/ubuntu/aws-nicia

# Build a imagem de produção
docker build -t nicia-track:latest .

# O build executa collectstatic internamente (via Dockerfile)
# Isso gera os arquivos em staticfiles/ dentro da imagem
```

### Criar o arquivo .env na EC2
```bash
# Copiar o template
cp .env.example .env

# Editar com os valores reais (NÃO commitar este arquivo)
nano .env
```

Conteúdo mínimo para Fase 1 (com SQLite ainda):
```bash
DJANGO_SETTINGS_MODULE=config.settings.production
SECRET_KEY=<gere-com-python-manage.py-shell>
DEBUG=False
ALLOWED_HOSTS=<ip-publico-da-ec2>
CSRF_TRUSTED_ORIGINS=http://<ip-publico-da-ec2>

# Banco ainda não configurado para Fase 1
# Mas production.py espera PostgreSQL...
# Solução: usar development.py temporariamente OU
# rodar um container PostgreSQL local para a Fase 1
```

> **Nota sobre banco na Fase 1:**
> `config.settings.production` assume PostgreSQL. Para a Fase 1 (validação inicial),
> você tem duas opções:
> 1. Usar `DJANGO_SETTINGS_MODULE=config.settings.development` e deixar SQLite
>    (simples, mas não testa os settings de produção)
> 2. Rodar um container PostgreSQL local via Docker Compose (testa mais perto do real)
>
> A opção 2 é recomendada: `docker compose up -d db` sobe o PostgreSQL do compose.

### Rodar o container
```bash
# Opção A: docker run (mais explícito)
docker run -d \
  --name nicia-track \
  --env-file .env \
  -p 8000:8000 \
  nicia-track:latest

# Opção B: docker compose (mais conveniente)
# (adaptar docker-compose.yml para não usar runserver em dev)
docker compose up -d
```

---

## Como rodar migrations

O Dockerfile já roda `migrate` no CMD antes de subir o gunicorn.
Mas se precisar rodar manualmente (ex.: após mudança no banco):

```bash
# Entrar no container em execução
docker exec -it nicia-track bash

# Dentro do container:
python manage.py migrate --noinput
python manage.py import_study_plan
python manage.py populate_chapter_content
python manage.py import_questions docs/15_BANCO_MESTRE_DE_QUESTOES.md
python manage.py create_admin
```

Ou rodar em um container temporário (sem iniciar o gunicorn):
```bash
docker run --rm \
  --env-file .env \
  nicia-track:latest \
  python manage.py migrate --noinput
```

---

## Como criar o superusuário

O management command `create_admin` já faz isso automaticamente.
Ele lê `ADMIN_EMAIL` e `ADMIN_PASSWORD` do `.env`:

```bash
# Adicionar ao .env:
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=SenhaForte123!

# O create_admin roda automaticamente no CMD do Dockerfile.
# Para rodar manualmente:
docker exec -it nicia-track python manage.py create_admin
```

---

## Como testar se a aplicação subiu

### 1. Verificar se o container está rodando
```bash
docker ps
# Deve mostrar nicia-track rodando há X segundos/minutos
```

### 2. Verificar logs do container
```bash
docker logs nicia-track --follow
# Procurar por: "[INFO] Booting worker with pid: ..."
# Erros comuns aparecem aqui
```

### 3. Testar localmente na EC2
```bash
# Dentro da EC2 (não do seu computador):
curl http://localhost:8000/conta/login/
# Deve retornar HTML com 200 OK
```

### 4. Testar do seu computador
```bash
curl http://<IP-PUBLICO-EC2>:8000/conta/login/
# A porta 8000 deve estar aberta no Security Group
```

### 5. Acessar no browser
```
http://<IP-PUBLICO-EC2>:8000/
# Deve aparecer a tela de login do Nícia Track
```

---

## Possíveis erros e como diagnosticar

### Erro: `DisallowedHost at /`
**Sintoma:** Django retorna 400 com "Invalid HTTP_HOST header"
**Causa:** `ALLOWED_HOSTS` não contém o IP/domínio que você está acessando
**Fix:** editar `.env` → `ALLOWED_HOSTS=<ip-da-ec2>` → reiniciar o container

```bash
docker stop nicia-track
docker rm nicia-track
docker run -d --name nicia-track --env-file .env -p 8000:8000 nicia-track:latest
```

### Erro: porta 8000 não responde
**Possível causa 1:** Security Group não tem a porta 8000 liberada
**Fix:** AWS Console → EC2 → Security Groups → Inbound Rules → Add Rule:
  Type: Custom TCP, Port: 8000, Source: 0.0.0.0/0

**Possível causa 2:** container não está rodando
```bash
docker ps -a    # mostra todos, incluindo parados
docker logs nicia-track  # ver por que parou
```

### Erro: `OperationalError: could not connect to server`
**Causa:** Django não consegue conectar ao banco de dados
**Fix:**
- Verificar que as variáveis `PG*` no `.env` estão corretas
- Verificar que o PostgreSQL está rodando (container ou RDS)
- Verificar Security Group (para RDS)

### Erro: `CSRF verification failed`
**Causa:** `CSRF_TRUSTED_ORIGINS` não inclui a origem do browser
**Fix:** editar `.env` → `CSRF_TRUSTED_ORIGINS=http://<ip-da-ec2>:8000`

### Erro: `No module named 'config'`
**Causa:** `DJANGO_SETTINGS_MODULE` errado ou `PYTHONPATH` incorreto
**Fix:** verificar que `DJANGO_SETTINGS_MODULE=config.settings.production` está no `.env`

### Erro: static files não aparecem (CSS quebrado)
**Causa A:** `collectstatic` não rodou
**Fix:** `docker exec nicia-track python manage.py collectstatic --noinput`

**Causa B:** `DJANGO_SETTINGS_MODULE` é o de desenvolvimento (usa storage simples)
**Fix:** confirmar que é `config.settings.production`

---

## Checklist da Fase 1

```
[ ] Instância EC2 criada (Ubuntu 22.04, t2.micro)
[ ] Key pair configurado (acesso SSH)
[ ] Security Group com portas 22, 80, 443 (e temporariamente 8000)
[ ] Docker instalado na EC2
[ ] Repositório clonado na EC2
[ ] .env criado com valores corretos
[ ] docker build executado com sucesso
[ ] Container rodando (docker ps)
[ ] curl http://localhost:8000/ retorna 200
[ ] Acesso via IP público funciona
[ ] Login com admin funciona
[ ] Questões aparecem no sistema
```

---

## Próximo passo

Após a Fase 1 funcionar, migrar o banco para RDS (Fase 2) para ter persistência real.
O banco local (container Docker ou SQLite) é apenas para validação inicial.
