# 08 — Fase 5: Segurança, Custos, Logs e Monitoramento

> Fechar as brechas de segurança, controlar custos e ganhar visibilidade do sistema.
> Esta fase é o que diferencia um "funciona" de um "está pronto para produção".

---

## IAM — Identity and Access Management

### O que é IAM
IAM é o sistema de identidade e permissões da AWS.
Define **quem** pode fazer **o quê** com **quais recursos**.

**Conceitos principais:**

| Conceito | O que é |
|---|---|
| **User** | Identidade humana ou de aplicação (tem credenciais permanentes) |
| **Group** | Conjunto de users com a mesma política |
| **Role** | Identidade temporária que um serviço assume (sem credenciais permanentes) |
| **Policy** | Documento JSON que define permissões (Allow/Deny em Actions/Resources) |

### IAM neste projeto

**Para a aplicação Django acessar S3:**
Opção A: IAM User + Access Keys no `.env` (simples, menos seguro)
Opção B: IAM Role associada à EC2 (sem credenciais em disco — recomendado)

**Para acesso humano ao console AWS:**
Nunca use a conta root (o email/senha de cadastro na AWS) para operações do dia a dia.
Crie um IAM User com MFA (autenticação de dois fatores) para acesso ao console.

### Princípio do menor privilégio
Cada entidade (user, role, aplicação) deve ter **apenas as permissões de que precisa**.

Exemplo ruim:
```json
{ "Effect": "Allow", "Action": "*", "Resource": "*" }   ← nunca faça isso
```

Exemplo correto para a aplicação (S3 apenas):
```json
{
  "Effect": "Allow",
  "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject", "s3:ListBucket"],
  "Resource": [
    "arn:aws:s3:::nicia-track-static",
    "arn:aws:s3:::nicia-track-static/*",
    "arn:aws:s3:::nicia-track-media/*"
  ]
}
```

---

## Security Groups — portas e acesso

### Regras para a EC2

```
Inbound (entrada):
  SSH (22)    → Apenas do seu IP (ex.: 203.0.113.42/32)
               NUNCA 0.0.0.0/0 para SSH
  HTTP (80)   → 0.0.0.0/0 (Nginx redireciona para HTTPS)
  HTTPS (443) → 0.0.0.0/0

Outbound (saída):
  Tudo permitido (padrão AWS — OK para esta aplicação)
```

### Regras para o RDS

```
Inbound:
  PostgreSQL (5432) → Security Group da EC2 (não IP direto)

Outbound:
  Nada (ou respostas automáticas)
```

### Por que restringir SSH (porta 22)

Bots na internet varrem IPs em busca de servidores SSH abertos 24 horas por dia.
Com a porta 22 aberta para `0.0.0.0/0`, você verá centenas de tentativas de login
por hora nos logs. Duas proteções:

1. **Security Group:** limitar a porta 22 ao seu IP (ou VPN)
2. **fail2ban:** bloqueia automaticamente IPs com muitas tentativas falhas

---

## DEBUG=False e SECRET_KEY

### DEBUG=False

`DEBUG=True` em produção expõe:
- Traceback completo do Python (com variáveis locais, paths do servidor)
- Lista de todas as URLs da aplicação
- Configurações do Django (pode incluir credenciais se mal configurado)
- SQL queries executadas (em alguns setups)

O `settings/production.py` já tem `DEBUG = False` fixo.
Mas atenção: se `DJANGO_SETTINGS_MODULE` apontar para `development` na EC2
por engano, `DEBUG` fica `True` (padrão em development.py).

**Verificação rápida:**
```bash
docker exec nicia-track python manage.py shell -c \
  "from django.conf import settings; print(settings.DEBUG)"
# Deve imprimir: False
```

### SECRET_KEY

`SECRET_KEY` é usado para assinar cookies de sessão, tokens CSRF e outros dados
sensíveis. Se vazar:
- Sessões de qualquer usuário podem ser forjadas
- Tokens CSRF podem ser forjados (ataques CSRF ficam possíveis)

**Regras:**
- Deve ter pelo menos 50 caracteres aleatórios
- Nunca commitar no Git
- Diferente entre dev e produção
- Rotacionar (trocar) se houver suspeita de exposição

**Gerar uma nova:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## .env — boas práticas

### O que nunca fazer

```bash
# NÃO fazer:
git add .env
git commit -m "add env file"   ← vaza todos os secrets

# NÃO fazer:
docker build --build-arg SECRET_KEY=chave-real .   ← fica na imagem

# NÃO fazer:
SECRET_KEY=chave123   ← chave fraca
```

### O que fazer

```bash
# .gitignore já inclui .env — verificar:
grep "\.env" .gitignore   # deve mostrar .env

# Criar o .env na EC2 manualmente (não via git)
ssh ubuntu@<IP-EC2>
nano /home/ubuntu/aws-nicia/.env

# Permissões restritivas no arquivo:
chmod 600 /home/ubuntu/aws-nicia/.env
# Apenas o dono (ubuntu) pode ler; outros não podem

# Verificar que .env não está no repositório:
git status   # .env não deve aparecer
git log --all -S "SECRET_KEY" --oneline   # não deve retornar nada
```

---

## Backups

### RDS
- Backups automáticos: habilitados por padrão (7 dias de retenção)
- Snapshots manuais: fazer antes de qualquer operação arriscada
- Point-in-time recovery: restaurar para qualquer segundo nos últimos N dias

### Código
- Git é o backup do código
- Certifique-se de que todos os commits estão no GitHub (remote)

### Media files (S3)
- S3 tem versionamento (opcional) — ativa para preservar versões de arquivos
- Replicação entre regiões (opcional, custo adicional)

### Banco de dados (lembrete)
```bash
# Criar snapshot antes de rodar migrations perigosas:
# AWS Console → RDS → Databases → nicia-track-db → Take Snapshot
```

---

## Logs

### Logs do Gunicorn (stdout do container)
```bash
# Logs em tempo real:
docker logs nicia-track --follow

# Últimas 100 linhas:
docker logs nicia-track --tail 100

# Logs do Django aparecem aqui também (WARNING+ em produção)
```

### Logs do Nginx
```bash
# Logs de acesso (quem acessou o quê):
sudo tail -f /var/log/nginx/access.log

# Logs de erro (problemas de conexão, 502, etc.):
sudo tail -f /var/log/nginx/error.log
```

### Configurar rotação de logs
Sem rotação, os logs crescem indefinidamente e enchem o disco da EC2:
```bash
# Instalar logrotate (já incluso no Ubuntu):
# Criar: /etc/logrotate.d/docker-nicia-track
/home/ubuntu/aws-nicia/logs/*.log {
    daily
    rotate 14
    compress
    missingok
    notifempty
}
```

### AWS CloudWatch Logs (opcional)
Para centralizar logs da EC2 e do Nginx no CloudWatch:
```bash
# Instalar o CloudWatch Agent:
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
sudo dpkg -i amazon-cloudwatch-agent.deb
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -a fetch-config -m ec2 -s -c file:/opt/aws/amazon-cloudwatch-agent/etc/config.json
```

---

## Billing alerts — como não ser surpreendido

### Por que é crítico
Na AWS, custos podem crescer rapidamente se você:
- Esquecer uma instância EC2 ligada
- Habilitar Multi-AZ no RDS sem querer
- Criar muitos snapshots
- Transferir dados internacionalmente

### Configurar alerta de billing

```
1. AWS Console → Billing → Budgets → Create Budget
2. Escolha: Cost Budget
3. Período: Monthly
4. Valor: USD 15 (ou o que fizer sentido)
5. Alertas:
   - 80% do orçamento → email
   - 100% do orçamento → email
6. Email de notificação: seu email
```

Também habilitar alertas de uso (usage alerts) para serviços específicos.

### Estimativa de custo do laboratório

| Serviço | Tipo | Custo mensal estimado |
|---|---|---|
| EC2 t2.micro | Free tier (12 meses) | USD 0 |
| RDS db.t3.micro | Free tier (12 meses) | USD 0 |
| S3 | < 1GB + requests | < USD 0.10 |
| Elastic IP | Associado e em uso | USD 0 |
| Dados transferidos | < 15GB/mês | USD 0 (free) |
| **Total** | | **< USD 1/mês** |

> Após 12 meses (free tier expira):
> EC2 t2.micro: ~USD 8.50/mês + RDS: ~USD 14/mês + storage: ~USD 5/mês
> **Total: ~USD 28/mês**

### Como parar/deletar recursos sem perder dados

```
Parar a EC2 (dados no EBS são preservados):
EC2 Console → Instances → Stop Instance
(A EC2 parada não cobra por hora de compute, mas cobra pelo EBS ~USD 0.08/GB/mês)

Pausar o RDS (não existe "stop" gratuito no RDS — pode criar snapshot e deletar):
1. Criar snapshot manual
2. Delete da instância RDS
3. Quando precisar: restore do snapshot (cria nova instância em ~5 min)

Deletar o laboratório inteiro (destrói tudo):
1. Snapshot do RDS
2. Delete RDS
3. Delete EC2
4. Delete Security Groups
5. Release Elastic IP
6. Delete S3 buckets (esvazie antes)
```

---

## Monitoramento básico

### CloudWatch métricas EC2 (gratuitas)
```
AWS Console → EC2 → Instances → sua instância → aba Monitoring

Métricas disponíveis:
- CPU Utilization
- Network In/Out
- Disk Read/Write Ops (não disponível para t2.micro com gp2 por padrão)
```

### Criar alarme de CPU alta
```
CloudWatch → Alarms → Create Alarm
→ EC2 → Per-Instance Metrics → CPUUtilization
→ Threshold: > 80% por 5 minutos
→ Action: notificar email
```

### Sentry (já presente no requirements/production.txt)
```bash
# .env na EC2:
SENTRY_DSN=https://xxx@xxx.ingest.sentry.io/xxx

# Sentry precisa ser inicializado no settings/production.py:
# (Verificar se já está configurado — sentry-sdk está no production.txt
#  mas pode precisar de inicialização explícita)
```

### Health check manual
```bash
# Criar um script de verificação periódica:
#!/bin/bash
STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/conta/login/)
if [ "$STATUS" != "200" ]; then
  echo "ALERTA: aplicação retornou $STATUS"
  # Enviar email ou notificação
fi
```

---

## Checklist de segurança final

```
[ ] DEBUG=False verificado em produção
[ ] SECRET_KEY forte (50+ chars) e única para produção
[ ] .env não está no git (git log --all -S "SECRET_KEY" não retorna nada)
[ ] SSH na porta 22 restrito ao seu IP no Security Group
[ ] fail2ban instalado (ou acesso SSH via VPN)
[ ] Chave SSH key pair ativa (não acesso por senha)
[ ] RDS não acessível da internet (Security Group correto)
[ ] IAM User/Role com permissões mínimas
[ ] Sem credenciais AdministratorAccess em uso pela aplicação
[ ] MFA habilitado na conta root AWS
[ ] Billing alert configurado
[ ] Sentry configurado para erros de produção
[ ] Logs com rotação configurada
[ ] CloudWatch alarme de CPU configurado
```
