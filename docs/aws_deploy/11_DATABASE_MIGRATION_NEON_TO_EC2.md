# 11 — Migração de Banco de Dados: Neon PostgreSQL → AWS EC2 PostgreSQL

> Migração completa dos dados de produção do Neon para o PostgreSQL em Docker na EC2.
> Inclui problema de incompatibilidade de versões e solução com container temporário.

---

## Objetivo

Migrar todos os dados do ambiente de produção hospedado no Neon PostgreSQL para o
PostgreSQL executando em Docker dentro de uma instância EC2 na AWS.

A migração precisava preservar:

- Usuários e senhas (hashes Django)
- Questões
- Plano de estudos
- Progresso dos alunos
- Exercícios respondidos
- Histórico completo da aplicação

---

## Arquitetura

### Origem

```
Render
  └─ Aplicação Django

Neon PostgreSQL 18
  └─ Banco de Produção
```

### Destino

```
AWS EC2

Docker
├─ Django
└─ PostgreSQL 16
```

---

## Problema Encontrado

Tentativa inicial de backup com `pg_dump` falhou:

```bash
pg_dump
# server version: 18.4
# pg_dump (PostgreSQL) 16.14
# pg_dump: error: aborting because of server version mismatch
```

O PostgreSQL não permite que um `pg_dump` de versão mais antiga exporte um banco
de versão mais nova.

**Solução:** usar um container Docker PostgreSQL 18 temporário para dump e restore.

---

## Passo 1 — Backup do banco AWS (segurança antes de alterar qualquer coisa)

```bash
docker compose -f docker-compose.prod.yml exec db \
  pg_dump -U nicia -d nicia_track -Fc \
  -f /tmp/aws_backup_before_restore.dump

docker cp aws-nicia-db-1:/tmp/aws_backup_before_restore.dump .
```

---

## Passo 2 — Testar conexão com o Neon

```bash
psql "$NEON_URL" -c '\dt'
# Resultado: 25 tabelas encontradas
```

`NEON_URL` no formato:
```
postgresql://USER:PASSWORD@HOST/neondb?sslmode=require
```

---

## Passo 3 — Gerar dump usando PostgreSQL 18

```bash
docker run --rm \
  -v $(pwd):/backup \
  postgres:18 \
  pg_dump \
  "$NEON_URL" \
  -Fc \
  -f /backup/backup_neon.dump
```

Arquivo gerado: `backup_neon.dump` (570 KB).

---

## Passo 4 — Validar dados antes da migração

| Tabela | Neon | AWS (antes) |
|---|---:|---:|
| accounts_user | 3 | 3 |
| questions_question | 800 | 800 |
| study_plan_studychapter | 98 | 98 |
| study_plan_lessonprogress | 16 | 0 |
| exams_useranswer | 85 | 0 |

Conclusão: estrutura correta na AWS, mas os dados de progresso dos usuários
(lessonprogress e useranswer) não haviam sido migrados.

---

## Passo 5 — Parar a aplicação (evitar escrita durante restore)

```bash
docker compose -f docker-compose.prod.yml stop web
```

---

## Passo 6 — Copiar dump para dentro do container

```bash
docker cp backup_neon.dump aws-nicia-db-1:/tmp/backup_neon.dump
```

---

## Passo 7 — Limpar banco AWS

```bash
docker compose -f docker-compose.prod.yml exec db psql -U nicia -d nicia_track
```

```sql
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
```

Garante que não haverá conflitos de tabelas durante o restore.

---

## Passo 8 — Problema no restore: incompatibilidade de versão do dump

```bash
pg_restore
# error: unsupported version (1.16) in file header
```

O dump foi criado pelo PostgreSQL 18 — o `pg_restore` do PostgreSQL 16 não
consegue interpretá-lo.

---

## Passo 9 — Restaurar usando PostgreSQL 18

Descobrir a rede Docker do container:
```bash
NETWORK=$(docker inspect aws-nicia-db-1 \
  --format '{{range $k,$v := .NetworkSettings.Networks}}{{$k}}{{end}}')
```

Executar restore com container temporário na mesma rede:
```bash
docker run --rm \
  --network "$NETWORK" \
  -v "$(pwd)":/backup \
  -e PGPASSWORD="$AWS_DB_PASSWORD" \
  postgres:18 \
  pg_restore \
  -h aws-nicia-db-1 \
  -U nicia \
  -d nicia_track \
  --no-owner \
  /backup/backup_neon.dump
```

Avisos esperados (não impedem a restauração — são objetos específicos do Neon):
```
transaction_timeout
neon_superuser
cloud_admin
ALTER DEFAULT PRIVILEGES
```

---

## Passo 10 — Validar migração

```bash
# Dentro do container PostgreSQL:
\dt
# 25 tabelas restauradas
```

```sql
SELECT COUNT(*) FROM study_plan_lessonprogress;  -- 16
SELECT COUNT(*) FROM exams_useranswer;           -- 85
SELECT id, email FROM accounts_user;             -- 3 usuários, incluindo niciadijkinga@hotmail.com
```

---

## Passo 11 — Subir aplicação

```bash
docker compose -f docker-compose.prod.yml start web
```

---

## Resultado Final

Migração concluída com sucesso. Todos os dados preservados:
usuários, credenciais, questões, capítulos, plano de estudos,
exercícios respondidos e progresso do aluno.

```
Internet → Cloudflare → AWS EC2 → Nginx → Gunicorn → Django → PostgreSQL (Docker)
```

---

## Lições Aprendidas

1. Sempre criar backup antes do restore.
2. Verificar compatibilidade de versões: o `pg_dump`/`pg_restore` deve ser da
   mesma versão (ou superior) ao servidor de origem.
3. Validar contagem de registros antes e depois — estrutura correta não garante
   que os dados foram migrados.
4. Containers temporários são a solução elegante para incompatibilidade de versões.
5. Avisos do Neon (`neon_superuser`, `cloud_admin`) são normais — não indicam falha.
6. Confirmar usuários e dados de negócio após a restauração, não só contagens técnicas.
