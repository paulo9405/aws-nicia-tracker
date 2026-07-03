# 06 — Fase 3: Static e Media Files no S3

> Migração dos arquivos estáticos e de mídia para Amazon S3.
> Resolve o problema de perda de arquivos em redeploys e prepara para escala horizontal.

---

## O que é S3

S3 (Simple Storage Service) é o armazenamento de objetos da AWS.
Não é um sistema de arquivos — é um banco de dados de chave/valor onde os
valores são arquivos (blobs binários) e as chaves são os "caminhos" (paths).

**Características:**
- Durabilidade: 99.999999999% (11 noves) — dados nunca se perdem
- Disponibilidade: 99.99% — sempre acessível
- Custo: USD 0.023/GB armazenado + USD 0.0004 por 1.000 requests
- Escalabilidade: armazena desde kilobytes até petabytes sem configuração

**Terminologia:**
- **Bucket:** o "container" do S3 (equivalente a um diretório raiz)
- **Object:** um arquivo individual dentro do bucket
- **Key:** o "caminho" do objeto (ex.: `static/css/main.css`)
- **ACL:** Access Control List — controla quem pode ler/escrever

---

## Diferença entre static files e media files

### Static files
**O que são:** arquivos fixos que fazem parte do código fonte.
- CSS do Bootstrap customizado
- JavaScript da aplicação
- Ícones, logos, imagens decorativas
- Arquivos do Django Admin

**Características:**
- Gerados pelo `collectstatic` a partir do código
- Não mudam durante o uso da aplicação
- Podem ser públicos (qualquer um pode baixar)
- Devem ter hash no nome para cache busting (WhiteNoise faz isso automaticamente)

**No projeto:**
- Origem: `static/` + Django admin + apps instalados
- Destino após collectstatic: `staticfiles/`
- Configuração: `STORAGES["staticfiles"]`

### Media files
**O que são:** arquivos enviados pelos usuários durante o uso da aplicação.
- Avatares (fotos de perfil)
- Qualquer upload feito através de um `ImageField` ou `FileField`

**Características:**
- Criados em runtime (não existem no código fonte)
- Pertencem a usuários específicos — podem ser privados
- Precisam ser persistentes entre redeploys

**No projeto:**
- Model: `Profile.avatar = models.ImageField(upload_to="avatars/")`
- Destino: `media/avatars/`
- Configuração: `STORAGES["default"]`

---

## Por que não depender do disco da EC2

### O problema atual

O `FileSystemStorage` (padrão) salva arquivos no disco do container Docker.
Quando o container é recriado (redeploy, atualização de imagem, reinício):

```
docker stop nicia-track
docker rm nicia-track          ← container e seu sistema de arquivos são deletados
docker run ... nicia-track     ← novo container: media/ está vazia!
```

Todos os avatares enviados pelos usuários são **perdidos**.

### A solução: S3

S3 existe **fora** do container e **fora** da EC2.
O container pode ser recriado, a EC2 pode ser substituída — os arquivos no S3
continuam existindo.

Além disso, com S3:
- Múltiplas instâncias EC2 acessam o mesmo conjunto de arquivos
- Backups automáticos por versionamento do bucket
- CDN (CloudFront) pode ser colocado na frente para performance global

---

## Como Django integra com S3

### Pacotes necessários
```
django-storages[s3]==1.14.x
boto3==1.34.x
```

`django-storages` é um pacote que implementa backends de storage alternativos
para Django. O backend `S3Boto3Storage` usa `boto3` (AWS SDK para Python)
para comunicar com o S3.

### Configuração em production.py

**Antes (situação atual):**
```python
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage"
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}
```

**Depois (com S3):**
```python
from decouple import config

AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
AWS_MEDIA_BUCKET_NAME = config("AWS_MEDIA_BUCKET_NAME", default=AWS_STORAGE_BUCKET_NAME)
AWS_S3_REGION_NAME = config("AWS_S3_REGION_NAME", default="us-east-1")
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

STORAGES = {
    "default": {                              # media files (uploads)
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "bucket_name": AWS_MEDIA_BUCKET_NAME,
            "location": "media",
            "file_overwrite": False,
        },
    },
    "staticfiles": {                          # static files
        "BACKEND": "storages.backends.s3boto3.S3ManifestStaticStorage",
        "OPTIONS": {
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "location": "static",
        },
    },
}

STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"
MEDIA_URL  = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"
```

---

## Variáveis de ambiente necessárias

```bash
# .env na EC2 (adicionar às variáveis existentes)

# Credenciais IAM (ou usar IAM Role na EC2 — mais seguro)
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...

# Buckets
AWS_STORAGE_BUCKET_NAME=nicia-track-static
AWS_MEDIA_BUCKET_NAME=nicia-track-media
AWS_S3_REGION_NAME=us-east-1
```

---

## Cuidados de permissão

### Princípio do menor privilégio

Crie um IAM User (ou Role) com apenas as permissões necessárias:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::nicia-track-static",
        "arn:aws:s3:::nicia-track-static/*",
        "arn:aws:s3:::nicia-track-media",
        "arn:aws:s3:::nicia-track-media/*"
      ]
    }
  ]
}
```

**Nunca use uma credencial `AdministratorAccess` para a aplicação.**

### IAM Role vs IAM User

| Abordagem | Segurança | Complexidade |
|---|---|---|
| IAM User + Access Keys no .env | Boa | Baixa |
| IAM Role associada à EC2 | Melhor | Média |

**IAM Role (recomendado em produção):**
A EC2 assume automaticamente a Role quando configurada.
O Django usa `boto3`, que detecta as credenciais do metadata service da EC2.
Sem chaves no `.env` — as credenciais nunca ficam em disco.

---

## Riscos de bucket público

### O que não fazer
```
Bucket policy: "AllowPublicRead" em TODOS os objetos
```

Se os media files (avatares) forem públicos, qualquer pessoa com a URL
pode acessar a foto de qualquer usuário — mesmo sem estar logado.

### O que fazer

**Static files:** podem ser públicos (CSS, JS são recursos que qualquer um pode baixar).

**Media files:** depende do conteúdo.
- Avatares: geralmente aceitável serem públicos (usuário escolheu exibir)
- Documentos pessoais: devem ser privados (acesso via presigned URLs)

Para avatares neste projeto, público é aceitável.
Para garantir privacidade, use `S3Boto3Storage` com `default_acl="private"`
e URLs pré-assinadas com expiração.

---

## Criando os buckets (passo a passo conceitual)

```
1. AWS Console → S3 → Create Bucket

   Bucket para static files:
   - Nome: nicia-track-static-<seu-nome>  (deve ser globalmente único)
   - Região: us-east-1
   - Block all public access: DESATIVAR (static files são públicos)
   - Bucket policy: {"Effect":"Allow","Principal":"*","Action":"s3:GetObject",...}

   Bucket para media files:
   - Nome: nicia-track-media-<seu-nome>
   - Região: us-east-1
   - Block all public access: MANTER (ou desativar se aceitar avatares públicos)

2. Configurar CORS no bucket de static files:
   [
     {
       "AllowedHeaders": ["*"],
       "AllowedMethods": ["GET"],
       "AllowedOrigins": ["https://seu-dominio.com"],
       "MaxAgeSeconds": 3000
     }
   ]
```

---

## Rodando collectstatic para o S3

Após configurar as variáveis e os buckets:

```bash
# Dentro do container (com as variáveis de ambiente corretas):
docker exec -it nicia-track python manage.py collectstatic --noinput

# Os arquivos serão enviados para:
# s3://nicia-track-static/static/css/...
# s3://nicia-track-static/static/js/...
# s3://nicia-track-static/static/admin/...
```

---

## Verificação final da Fase 3

```bash
# 1. Ver se os arquivos chegaram ao S3
# AWS Console → S3 → nicia-track-static → static/

# 2. Acessar a aplicação e inspecionar o HTML
# Botão direito → Inspecionar → aba Network
# Os arquivos CSS/JS devem vir de https://nicia-track-static.s3.amazonaws.com/...

# 3. Testar upload de avatar
# /conta/perfil/ → fazer upload de imagem → salvar
# Deve aparecer na URL s3.amazonaws.com/...

# 4. Verificar que MEDIA_URL está correto no template
# A tag <img src="{{ user.profile.avatar.url }}"> deve gerar URL do S3
```
