# CLAUDE.md — Instruções para Claude Code

Instruções que o Claude Code deve seguir em todas as sessões neste projeto.

---

## O que é este projeto

Laboratório de deploy AWS baseado no projeto Nícia Track (plataforma Django de
preparação para concursos). O objetivo é aprendizado de DevOps/AWS e construção
de portfólio técnico.

**Stack:** Django 4.2 · Python 3.12 · PostgreSQL · Bootstrap 5 · HTMX · Docker ·
Gunicorn · Nginx · Cloudflare · AWS EC2

**Documentação de referência:** `docs/aws_deploy/` (11 arquivos + checklist + política)

---

## Regra principal: fluxo obrigatório de deploy

```
Local → Render (homologação) → AWS (produção)
```

**Nunca sugerir ou executar deploy direto de Local para AWS.**
Qualquer alteração que vá para produção deve passar primeiro pelo Render.

---

## Ambientes

| Ambiente | Plataforma | Banco | Uso |
|---|---|---|---|
| Desenvolvimento | Local / Docker | PostgreSQL local | Código e testes |
| Homologação | Render | Neon PostgreSQL | Validação antes de produção |
| Produção | AWS EC2 | PostgreSQL (Docker) | Usuários e dados reais |

**URL de produção:** `https://nicia.paulodev.net`

---

## Antes de qualquer deploy em produção (AWS)

1. Confirmar que a alteração foi validada no Render.
2. Criar backup do banco antes de qualquer operação destrutiva:

```bash
docker compose -f docker-compose.prod.yml exec db \
  pg_dump -U nicia -d nicia_track -Fc \
  -f /tmp/backup_pre_deploy_$(date +%Y%m%d).dump

docker cp aws-nicia-db-1:/tmp/backup_pre_deploy_$(date +%Y%m%d).dump .
```

3. Nunca rodar `DROP`, `TRUNCATE` ou migrations sem backup confirmado.

---

## Infraestrutura de produção (AWS)

- **EC2:** Amazon Linux 2023, t3.micro, us-east-2
- **Elastic IP:** `3.148.15.93`
- **DNS:** Cloudflare → `nicia.paulodev.net`
- **Containers:** `docker-compose.prod.yml` (web + db)
- **Proxy:** Nginx (80→443 redirect, SSL terminado)
- **SSL:** Let's Encrypt via Certbot (renovação automática)
- **Security Group:** 22 (SSH→IP próprio), 80, 443 — porta 8000 fechada

---

## Documentação viva

Ao concluir qualquer etapa significativa, atualizar:

- `docs/aws_deploy/10_IMPLEMENTATION_LOG.md` — log de decisões e problemas
- `docs/aws_deploy/AWS_DEPLOY_CHECKLIST.md` — marcar itens concluídos

---

## Referência completa

Ver `docs/deployment_policy.md` para checklist detalhado e procedimento de rollback.
