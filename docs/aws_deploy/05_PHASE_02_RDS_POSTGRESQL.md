# 05 — Fase 2: Banco PostgreSQL no RDS

> Migração do banco de dados para o Amazon RDS (Relational Database Service).
> Nenhum código Python precisa mudar — apenas as variáveis de ambiente.

---

## O que é RDS

RDS (Relational Database Service) é o banco de dados gerenciado da AWS.
Você escolhe o banco (PostgreSQL, MySQL, etc.), tamanho e versão — a AWS cuida
de instalação, patches, backups e failover.

**O que a AWS gerencia automaticamente:**
- Instalação e configuração do PostgreSQL
- Patches de segurança e de versão
- Backups automáticos (configuráveis, até 35 dias)
- Snapshots manuais
- Failover (Multi-AZ, se habilitado)
- Métricas (CPU, conexões, armazenamento, IOPS)

**O que você ainda gerencia:**
- Schemas e tabelas (via migrations)
- Dados (seu conteúdo)
- Usuários e senhas do banco
- Security Groups (quem pode conectar)

---

## Por que usar PostgreSQL gerenciado no RDS

### Comparação: SQLite vs PostgreSQL local vs RDS

| Característica | SQLite | PostgreSQL local (EC2) | RDS PostgreSQL |
|---|---|---|---|
| Concorrência | Limitada | Boa | Boa |
| Persistência | Arquivo local | Disco EC2 | Independente da EC2 |
| Backup automático | Não | Não | Sim |
| Escalabilidade | Mínima | Limitada | Alta |
| HA / Failover | Não | Não | Sim (Multi-AZ) |
| Custo | Zero | +EC2 storage | Free tier disponível |
| Operação | Zero | Alta | Baixa |

**Para desenvolvimento:** SQLite é perfeito (zero configuração, zero custo).
**Para produção:** RDS é a escolha correta (confiabilidade, backups, separação).

**Por que não rodar PostgreSQL na própria EC2:**
- Se a EC2 tiver um problema (disco cheio, instância corrompida), você perde o banco
- Backups manuais são esquecíveis
- Upgrades de versão são manuais e arriscados
- RDS isola o banco da aplicação — cada um escala independentemente

---

## Diferenças práticas: sslmode

O `settings/production.py` já tem:
```python
"OPTIONS": {"sslmode": "require"},
```

Isso significa que o Django **exige** conexão criptografada com o banco.
O RDS suporta SSL por padrão — você não precisa configurar nada extra.
Apenas certifique-se de que o endpoint do RDS é o correto.

---

## Variáveis de ambiente necessárias

Após criar o RDS, você terá um endpoint assim:
```
nicia-track-db.abc123xyz.us-east-1.rds.amazonaws.com
```

Atualize o `.env` na EC2:
```bash
PGDATABASE=nicia_track
PGUSER=nicia_track
PGPASSWORD=<senha-definida-na-criação-do-rds>
PGHOST=nicia-track-db.abc123xyz.us-east-1.rds.amazonaws.com
PGPORT=5432
```

Nenhuma linha de código Python precisa mudar.
O Django lerá as variáveis via `python-decouple` e usará o RDS automaticamente.

---

## Security Groups — configuração crítica

Este é o passo mais propenso a erro. O RDS não deve ser acessível da internet.

### Security Group do RDS (regras de entrada):
```
Tipo:     PostgreSQL
Protocolo: TCP
Porta:    5432
Origem:   Security Group da EC2  ← não use 0.0.0.0/0 aqui!
```

**Por que usar Security Group como origem (e não IP):**
O IP da EC2 pode mudar (se parar e reiniciar). Usar o Security Group como origem
garante que qualquer instância EC2 com aquele Security Group pode conectar,
independentemente do IP.

### Testando a conexão:
```bash
# Dentro da EC2:
docker exec -it nicia-track bash

# Dentro do container:
python manage.py dbshell
# Deve abrir o prompt: nicia_track=>
# Se der timeout, o Security Group está bloqueando
```

---

## Rodando migrations no RDS

Após configurar as variáveis e verificar a conexão:

```bash
# Opção 1: via container em execução
docker exec -it nicia-track python manage.py migrate --noinput

# Opção 2: container temporário (não inicia gunicorn)
docker run --rm --env-file .env nicia-track:latest \
  python manage.py migrate --noinput

# Importar dados (management commands idempotentes):
docker exec -it nicia-track python manage.py import_study_plan
docker exec -it nicia-track python manage.py populate_chapter_content
docker exec -it nicia-track python manage.py import_questions docs/15_BANCO_MESTRE_DE_QUESTOES.md
docker exec -it nicia-track python manage.py create_admin
```

**Atenção:** o CMD do Dockerfile já roda todos esses comandos automaticamente
ao iniciar o container. Rodar manualmente é necessário apenas se precisar
reexecutar sem reiniciar o container.

---

## Backup do RDS

### Backups automáticos (habilitados por padrão):
- Janela de backup: AWS escolhe um horário de baixo uso (configurável)
- Retenção: 7 dias (padrão, configurável até 35 dias)
- Point-in-time recovery: restaurar para qualquer segundo nos últimos N dias

### Snapshots manuais:
```
AWS Console → RDS → Databases → nicia-track-db → Actions → Take Snapshot
```
Snapshots manuais nunca expiram automaticamente (você paga pelo armazenamento).

### Restaurar:
Snapshots criam uma nova instância RDS. Você atualiza o endpoint no `.env` da EC2.
O banco antigo e o novo ficam em paralelo — migração sem downtime é possível.

---

## Cuidados de custo

### Free tier RDS:
- `db.t3.micro` ou `db.t2.micro`: 750 horas/mês grátis por 12 meses
- 20GB de armazenamento SSD grátis
- 20GB de armazenamento de backup grátis

### Atenção:
- **RDS cobra por hora mesmo parado.** Diferente da EC2, não existe "stopped" gratuito
  no RDS — você paga enquanto a instância existe, mesmo sem uso.
- **Para o laboratório:** ao terminar os estudos, **fazer snapshot e deletar a instância**.
  Depois, restore do snapshot cria a instância novamente quando precisar.
- **Multi-AZ:** dobra o custo — não habilite no laboratório.
- **Storage auto-scaling:** pode crescer sem você perceber — verifique o limite.

### Estimativa de custo (fora do free tier):
```
db.t3.micro:     ~USD 0.016/hora = USD 11.50/mês
20GB storage:    ~USD 2.30/mês
Backups (20GB):  grátis
Total estimado:  ~USD 14/mês
```

---

## Criando o RDS (passo a passo conceitual)

```
1. AWS Console → RDS → Create Database

2. Opções:
   - Engine: PostgreSQL
   - Version: 16 (mesma do docker-compose.yml)
   - Template: Free Tier
   - DB Instance ID: nicia-track-db
   - Master username: nicia_track
   - Master password: <gere uma senha forte>
   - DB Instance Class: db.t3.micro
   - Storage: 20GB gp2, sem auto-scaling (para controlar custo)
   - VPC: default (mesma da EC2)
   - Public access: No (muito importante!)
   - VPC Security Group: criar novo ou usar o da EC2
   - Database name: nicia_track
   - Backup: 7 dias
   - Monitoring: básico (grátis)
   - Maintenance window: qualquer horário fora do pico

3. Após criar (~5 minutos):
   - Anotar o Endpoint (ex: nicia-track-db.abc123.us-east-1.rds.amazonaws.com)
   - Configurar Security Group para aceitar apenas a EC2
```

---

## Verificação final da Fase 2

```bash
# 1. Conectar ao banco via dbshell
docker exec -it nicia-track python manage.py dbshell
\dt   # listar tabelas — deve mostrar todas as tabelas Django

# 2. Verificar contagem de questões
docker exec -it nicia-track python manage.py shell -c \
  "from apps.questions.models import Question; print(Question.objects.count())"
# Deve mostrar: 800

# 3. Testar login via browser
# http://<IP-EC2>:8000/conta/login/
# Login com ADMIN_EMAIL e ADMIN_PASSWORD

# 4. Verificar backup automático
# AWS Console → RDS → Automated Backups → deve mostrar o banco
```
