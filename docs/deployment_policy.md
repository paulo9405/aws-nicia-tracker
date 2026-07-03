# Política de Deploy — Nícia Track (AWS Lab)

---

## Ambientes

### Desenvolvimento (Local)

Utilizado para:
- Desenvolvimento de funcionalidades
- Correção de bugs
- Testes unitários
- Testes rápidos

Tecnologias:
```
Notebook Local · Docker · PostgreSQL Local
```

---

### Homologação (Render + Neon)

Utilizado para:
- Validar deploy
- Testar migrations
- Testar funcionalidades em ambiente real
- Validar integrações
- Detectar problemas antes da produção

Tecnologias:
```
Render · Neon PostgreSQL
```

**Importante:**
- Não utilizar dados reais de usuários
- Utilizar contas de teste
- Este ambiente funciona como sandbox/homologação

---

### Produção (AWS)

Utilizado para:
- Usuários reais
- Dados reais
- Operação oficial do sistema

Tecnologias:
```
AWS EC2 · Docker · PostgreSQL · Nginx · Gunicorn · Cloudflare
```

URL: `https://nicia.paulodev.net`

---

## Fluxo Obrigatório de Deploy

Toda alteração deve seguir esta ordem:

```
Desenvolvimento Local
        ↓
Deploy Render (homologação)
        ↓
Testes e Validação
        ↓
Deploy AWS (produção)
```

**Não é permitido ir de Local direto para AWS** sem validação prévia no Render.

---

## Checklist de Deploy

### Etapa 1 — Desenvolvimento

- [ ] Funcionalidade implementada
- [ ] Testes executados (`pytest`)
- [ ] Migrations revisadas
- [ ] Código commitado e pushed

### Etapa 2 — Homologação (Render)

- [ ] Deploy realizado no Render
- [ ] Aplicação inicia corretamente
- [ ] Banco funciona
- [ ] Login funciona
- [ ] Nova funcionalidade funciona
- [ ] Nenhum erro nos logs

Aprovação obrigatória antes de avançar para produção.

### Etapa 3 — Produção (AWS)

Antes do deploy:
- [ ] Backup do banco AWS criado

```bash
docker compose -f docker-compose.prod.yml exec db \
  pg_dump -U nicia -d nicia_track -Fc \
  -f /tmp/backup_pre_deploy_$(date +%Y%m%d).dump

docker cp aws-nicia-db-1:/tmp/backup_pre_deploy_$(date +%Y%m%d).dump .
```

Deploy:
```bash
git pull
docker compose -f docker-compose.prod.yml up -d --build
```

Validação pós-deploy:
- [ ] Login funciona
- [ ] Funcionalidade alterada funciona
- [ ] Logs sem erros (`docker logs aws-nicia-web-1 --tail 50`)
- [ ] Banco com dados corretos

---

## Procedimento de Rollback

Se o deploy falhar:

1. Restaurar backup do banco (ver `11_DATABASE_MIGRATION_NEON_TO_EC2.md` para referência de técnica)
2. Voltar para a versão anterior do código: `git checkout <commit-anterior>`
3. Rebuild dos containers: `docker compose -f docker-compose.prod.yml up -d --build`
4. Validar funcionamento
