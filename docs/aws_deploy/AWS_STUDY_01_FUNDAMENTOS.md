# AWS STUDY 01 — Fundamentos AWS (a partir do meu deploy real)

> Material de estudo pessoal baseado na implementação real do projeto **Nícia Track**
> (aplicação Django) na AWS. Não é documentação de deploy — é material de aprendizado
> para revisão, NotebookLM, flashcards, quizzes, mapas mentais e entrevistas.
>
> **Regra de ouro deste material:** distinguir sempre o que foi **implementado de verdade**
> do que está apenas **planejado**.
>
> | Implementado de verdade | Apenas planejado (ainda não feito) |
> |---|---|
> | Conta AWS, MFA, IAM, Budget | RDS (banco gerenciado) |
> | EC2 (Amazon Linux 2023, t3.micro, us-east-2) | S3 (static/media) |
> | Elastic IP, Security Groups, SSH | CloudWatch |
> | Docker + Docker Compose + PostgreSQL em container | CI/CD (GitHub Actions) |
> | Nginx + HTTPS (Let's Encrypt) + Cloudflare DNS | fail2ban, IAM Role na EC2 |

---

## Como usar este arquivo

Cada conceito segue a mesma estrutura, para facilitar geração de flashcards e podcasts:

- **O que é**
- **Para que serve**
- **Quando usar**
- **Como foi usado no MEU projeto**
- **Erros comuns**
- **Como explicar em entrevista**

No final: a seção **Pareto AWS** — os 20% que dão 80% do entendimento.

---

# 1. Conta AWS

**O que é:** a conta que agrupa toda a sua infraestrutura, cobrança e identidades na AWS.
É criada com um email + cartão de crédito.

**Para que serve:** é o "container" de tudo — recursos (EC2, S3, RDS), usuários (IAM),
faturamento. Tudo que você cria vive dentro de uma conta.

**Quando usar:** sempre. É o ponto de partida obrigatório.

**Como foi usado no meu projeto:** criei e ativei a conta com cartão de crédito,
verifiquei o email, e imediatamente configurei segurança (MFA) e controle de custo (Budget)
**antes** de criar qualquer recurso.

**Erros comuns:**
- Sair criando recursos antes de configurar Budget → fatura surpresa.
- Usar o email/senha da conta (Root) no dia a dia.

**Como explicar em entrevista:** "A primeira coisa que fiz numa conta nova não foi criar
servidor — foi habilitar MFA na conta root e criar um Budget de alerta de custo. Segurança
e custo antes de infraestrutura."

---

# 2. Root User (usuário raiz)

**O que é:** o dono absoluto da conta AWS. É o login de email/senha usado no cadastro.
Tem poder total e irrestrito — inclusive fechar a conta e alterar faturamento.

**Para que serve:** apenas operações críticas: configuração inicial, recuperação de acesso,
mudança de plano de suporte, fechamento de conta.

**Quando usar:** quase nunca. A regra é:
```
Root      = emergências
IAM User  = trabalho diário
```

**Como foi usado no meu projeto:** usei o Root só para o setup inicial e **habilitei MFA nele**.
Depois criei um IAM User (`paulo-aws-admin`) e passei a usar exclusivamente esse usuário.

**Erros comuns:**
- Usar Root no dia a dia (se vazar, perde-se tudo).
- Não habilitar MFA no Root.
- Gerar Access Keys para o Root (nunca faça isso).

**Como explicar em entrevista:** "Root é como a chave-mestra do prédio: você guarda no cofre
e usa só em emergência. Para o dia a dia, cada pessoa tem sua própria chave (IAM User)."

---

# 3. IAM (Identity and Access Management)

**O que é:** o sistema de identidade e permissões da AWS. Responde três perguntas:
**Quem?** pode fazer **o quê?** em **quais recursos?**

**Para que serve:** controlar acesso. Criar usuários, grupos, papéis e políticas que
determinam exatamente o que cada identidade pode ou não fazer.

**Quando usar:** sempre que precisar dar acesso a uma pessoa ou a uma aplicação.

**Como foi usado no meu projeto:** criei o grupo `Administrators` com a política
`AdministratorAccess`, o usuário `paulo-aws-admin`, e coloquei o usuário no grupo.
As permissões fluem por **herança**: `User → Group → Policy`.

**Erros comuns:**
- Dar permissões direto ao usuário (difícil de gerenciar) em vez de via grupo.
- Criar o usuário e esquecer de colocá-lo no grupo → **Access Denied** (aconteceu comigo).
- Dar permissões amplas demais para aplicações (violar menor privilégio).

**Como explicar em entrevista:** "IAM é o porteiro da AWS. Todo `Access Denied` começa
por aí: verifico usuário, grupo, política e a herança entre eles."

---

# 4. IAM User (usuário IAM)

**O que é:** uma identidade para uma pessoa **ou** uma aplicação acessar a AWS.
Tem credenciais permanentes (senha para console, e/ou Access Keys para API).

**Para que serve:** substituir o uso do Root. Cada humano/serviço tem sua própria identidade.

**Quando usar:** para acesso humano ao console (com senha + MFA) e para aplicações que
precisam de credenciais fixas (embora IAM Role seja preferível para apps na EC2).

**Como foi usado no meu projeto:** criei `paulo-aws-admin` com login no console, senha própria
e **troca obrigatória de senha no primeiro acesso**. Esse é o usuário que uso todo dia.
Um IAM User específico para a aplicação (só S3) está planejado para a fase do S3.

**Erros comuns:**
- Compartilhar um único IAM User entre várias pessoas.
- Deixar Access Keys antigas ativas.
- Colocar Access Keys no código/git.

**Como explicar em entrevista:** "Cada identidade é um IAM User separado — auditoria e
revogação ficam simples. Se um vaza, revogo só ele."

---

# 5. IAM Group (grupo IAM)

**O que é:** um conjunto de usuários que compartilham as mesmas permissões.

**Para que serve:** administrar permissões em escala. Em vez de anexar políticas a cada
usuário, você anexa ao grupo e adiciona usuários ao grupo.

**Quando usar:** sempre que houver mais de um usuário com o mesmo papel (Admins, Devs, DevOps).

**Como foi usado no meu projeto:** criei o grupo `Administrators` e associei a política
`AdministratorAccess`. O `paulo-aws-admin` herda as permissões por estar no grupo.

**Erros comuns:**
- Criar o grupo e a política mas **esquecer de adicionar o usuário ao grupo** → Access Denied
  (foi exatamente meu erro; o campo "Grupo" aparecia como `0`).

**Como explicar em entrevista:** "Permissões vão para grupos, não para pessoas.
`User → Group → Policy`. Onboarding de alguém novo é só colocar no grupo certo."

---

# 6. IAM Policy (política IAM)

**O que é:** um documento JSON que define permissões. Estrutura lógica:
**Effect** (Allow/Deny) + **Action** (o que) + **Resource** (onde).

**Para que serve:** descrever exatamente quais ações são permitidas em quais recursos.

**Quando usar:** sempre que precisar conceder ou negar acesso. Pode usar políticas
**gerenciadas pela AWS** (prontas) ou **customizadas** (você escreve o JSON).

**Como foi usado no meu projeto:** usei a política gerenciada `AdministratorAccess`
(acesso total) para o grupo de administração humana. Para a aplicação, a política planejada
é restrita ao S3:
```json
{
  "Effect": "Allow",
  "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject", "s3:ListBucket"],
  "Resource": ["arn:aws:s3:::nicia-track-media", "arn:aws:s3:::nicia-track-media/*"]
}
```

**Erros comuns:**
- `"Action": "*", "Resource": "*"` para aplicações → violação grave de menor privilégio.
- Confundir permissão da pessoa (admin) com permissão da aplicação (mínima).

**Como explicar em entrevista:** "Política é o contrato: quem, pode o quê, onde. Para humano
admin, uso a gerenciada `AdministratorAccess`. Para a app, escrevo uma política mínima só do S3."

---

# 7. MFA (Multi-Factor Authentication)

**O que é:** autenticação com dois fatores — algo que você **sabe** (senha) + algo que você
**possui** (código do app autenticador no celular).

**Para que serve:** mesmo que a senha vaze, sem o celular não há acesso.

**Quando usar:** obrigatório no Root e em qualquer IAM User importante.

**Como foi usado no meu projeto:** habilitei MFA via authenticator app **no Root** e
**no `paulo-aws-admin`**.

**Erros comuns:**
- MFA só no Root, esquecendo os IAM Users administrativos.
- Perder o dispositivo sem backup dos códigos de recuperação.

**Como explicar em entrevista:** "Senha sozinha é um fator só. MFA adiciona 'algo que você tem'.
No mínimo Root e admins precisam ter."

---

# 8. AWS Budgets

**O que é:** ferramenta de monitoramento de custo que envia alertas quando o gasto se aproxima
de um limite definido.

**Para que serve:** evitar surpresas na fatura — o erro nº 1 de iniciantes na AWS é **financeiro**,
não técnico (esquecer um recurso ligado).

**Quando usar:** **antes** de criar qualquer infraestrutura.

**Como foi usado no meu projeto:** criei um Budget de **US$ 15/mês** com alertas em **85%**,
**100%** e **previsão de 100%**, notificando meu email.

**Erros comuns:**
- Criar EC2/RDS, esquecer ligado e receber cobrança inesperada.
- Não configurar alerta de **previsão** (só reage quando já estourou).

**Como explicar em entrevista:** "Antes de qualquer recurso, criei um Budget de US$15 com alertas.
Na AWS, o susto maior costuma ser a fatura, não o código."

---

# 9. EC2 (Elastic Compute Cloud)

**O que é:** máquina virtual (servidor) na nuvem AWS. Você escolhe SO, CPU/RAM e paga por hora.
Tem acesso root via SSH.

**Para que serve:** rodar sua aplicação. É o componente central — tudo executa nela
(Docker, Nginx, Gunicorn, Django, e no meu caso até o PostgreSQL em container).

**Quando usar:** quando você quer controle total do ambiente (diferente de um PaaS como Render,
que esconde o servidor).

**Como foi usado no meu projeto:**
- **AMI:** Amazon Linux 2023 (não Ubuntu — decisão consciente).
- **Tipo:** t3.micro (free tier, geração mais nova que t2.micro).
- **Região:** us-east-2 (Ohio).
- Dentro dela instalei Docker, Docker Compose, Git, Nginx e Certbot.

**Erros comuns:**
- Assumir Ubuntu: no Amazon Linux o gerenciador é `dnf` (não `apt`) e o usuário SSH é
  `ec2-user` (não `ubuntu`).
- Deixar a instância ligada sem uso (custa por hora fora do free tier).

**Como explicar em entrevista:** "EC2 é um servidor virtual com controle total. Escolhi
Amazon Linux 2023 t3.micro no free tier e rodo tudo em Docker dentro dela."

---

# 10. AMI (Amazon Machine Image)

**O que é:** um "molde" (imagem) de sistema operacional + software pré-instalado usado para
criar uma instância EC2.

**Para que serve:** definir o ponto de partida da máquina (qual SO, quais pacotes já vêm).

**Quando usar:** ao lançar uma EC2 você **sempre** escolhe uma AMI.

**Como foi usado no meu projeto:** escolhi a AMI do **Amazon Linux 2023**. O plano original
previa Ubuntu 22.04 — mudei conscientemente. Impacto real: comandos com `dnf` em vez de `apt`,
usuário `ec2-user`, e diferenças na instalação de Nginx/Certbot/Docker Compose.

**Erros comuns:**
- Copiar tutoriais de Ubuntu e rodar `apt install` num Amazon Linux (falha).

**Como explicar em entrevista:** "AMI é o template do SO da instância. Usei Amazon Linux 2023;
isso muda o gerenciador de pacotes para `dnf` e o usuário SSH para `ec2-user`."

---

# 11. Instance Types (tipos de instância)

**O que é:** as "famílias e tamanhos" de EC2 (ex.: t2.micro, t3.micro, m5.large), cada uma com
combinação de vCPU, RAM e rede diferente.

**Para que serve:** dimensionar a máquina para a carga — mais CPU/RAM = mais capacidade e custo.

**Quando usar:** escolher o menor tipo que atende sua carga. Para labs/estudos, os `micro`
do free tier.

**Como foi usado no meu projeto:** **t3.micro** (1 vCPU burstable, 1GB RAM). Escolhi t3 em vez
de t2 porque é geração mais nova (melhor performance) e continua no free tier.

**Erros comuns:**
- Superdimensionar "por garantia" → custo desnecessário.
- Esquecer que os `micro` têm pouca RAM (1GB) — builds pesados podem faltar memória.

**Como explicar em entrevista:** "Comecei pequeno com t3.micro no free tier. Se a carga crescer,
mudo o tipo da instância sem recriar o servidor."

---

# 12. EBS (Elastic Block Store)

**O que é:** disco SSD persistente que se conecta à EC2 (como um HD/SSD de rede).
Sobrevive à parada da instância.

**Para que serve:** armazenar o SO e os dados da EC2 de forma persistente.

**Quando usar:** toda EC2 tem pelo menos um volume EBS (o disco raiz).

**Como foi usado no meu projeto:** a EC2 usa o volume EBS raiz padrão. **Importante:** meu
PostgreSQL roda em container Docker na EC2 — os dados do banco vivem em volume Docker no EBS.
Se o EBS/instância se perder sem backup, perco o banco (por isso backups manuais com `pg_dump`).

**Erros comuns:**
- Achar que "parar a EC2" apaga os dados — não apaga; o EBS persiste (mas cobra ~USD 0.08/GB/mês).
- Confundir armazenamento **efêmero do container** com o EBS persistente.

**Como explicar em entrevista:** "EBS é o disco persistente da EC2. Parar a instância preserva
o EBS; terminar a instância pode apagá-lo. Por isso banco crítico idealmente vai para RDS."

---

# 13. Elastic IP (IP elástico)

**O que é:** um endereço IPv4 público **fixo** que você aloca e associa a uma EC2.

**Para que serve:** garantir que o IP não mude quando você para/reinicia a instância —
essencial para DNS não quebrar.

**Quando usar:** quando um domínio aponta para a EC2 (registro A) e você precisa de estabilidade.

**Como foi usado no meu projeto:** aloquei o Elastic IP **`3.148.15.93`** e associei à EC2.
O DNS no Cloudflare (`nicia.paulodev.net`) aponta para esse IP fixo.

**Erros comuns:**
- Usar o IP público padrão (temporário) no DNS → some ao reiniciar → site fora do ar.
- Alocar Elastic IP e **não associar** a nada → a AWS cobra por IP ocioso.

**Como explicar em entrevista:** "IP público padrão muda no reboot. Aloquei um Elastic IP fixo
(3.148.15.93) para o DNS continuar apontando certo depois de reinícios."

---

# 14. Security Groups (grupos de segurança)

**O que é:** firewall virtual **stateful** que controla tráfego de entrada (inbound) e saída
(outbound) de um recurso (EC2, RDS).

**Para que serve:** permitir só as portas/origens necessárias. É a primeira linha de defesa de rede.

**Quando usar:** toda EC2/RDS tem um. Configure sempre com o mínimo necessário.

**Como foi usado no meu projeto (estado final):**
```
22/TCP  (SSH)   → 177.36.193.61/32   (apenas meu IP)
80/TCP  (HTTP)  → 0.0.0.0/0          (qualquer um)
443/TCP (HTTPS) → 0.0.0.0/0          (qualquer um)
Porta 8000      → NÃO exposta        (Gunicorn só acessível localmente pelo Nginx)
```

**Erros comuns:**
- Abrir SSH (22) para `0.0.0.0/0` → bots tentam brute force 24h/dia.
- Expor a porta da aplicação (8000) direto → Gunicorn cru na internet.
- (No futuro RDS) abrir 5432 para a internet em vez de para o SG da EC2.

**Como explicar em entrevista:** "Security Group é firewall stateful. SSH só do meu IP, 80 e 443
abertos, e a porta 8000 do Gunicorn nunca exposta — só o Nginx fala com ele localmente."

---

# 15. SSH (Secure Shell)

**O que é:** protocolo para acesso remoto seguro e criptografado ao terminal da EC2.

**Para que serve:** administrar o servidor (instalar pacotes, ver logs, rodar comandos).

**Quando usar:** toda administração da EC2 é via SSH.

**Como foi usado no meu projeto:** conectei com
`ssh -i nicia-track-key.pem ec2-user@3.148.15.93`. Note **`ec2-user`** (Amazon Linux),
não `ubuntu`. A chave `.pem` precisa de permissão restrita (`chmod 400`).

**Erros comuns:**
- Errar o usuário (`ubuntu` vs `ec2-user`) → "Permission denied".
- Chave com permissão aberta (`chmod 644`) → SSH recusa ("unprotected private key").
- Perder o `.pem` (não dá para baixar de novo).

**Como explicar em entrevista:** "Acesso a EC2 é por SSH com chave privada. No Amazon Linux o
usuário é `ec2-user`, e a chave `.pem` precisa de `chmod 400`."

---

# 16. Key Pair (par de chaves)

**O que é:** um par de chaves criptográficas (pública + privada). A AWS guarda a **pública** na
EC2; você guarda a **privada** (arquivo `.pem`).

**Para que serve:** autenticar o SSH sem senha — mais seguro que senha.

**Quando usar:** ao criar a EC2 você gera/escolhe um key pair para poder acessá-la.

**Como foi usado no meu projeto:** gerei `nicia-track-key.pem`, baixei e apliquei `chmod 400`.
É a única forma de entrar na instância.

**Erros comuns:**
- Commitar o `.pem` no git.
- Perder o `.pem` → precisa de workaround (não há redownload).

**Como explicar em entrevista:** "Autenticação por par de chaves: a pública fica na EC2, a
privada comigo. Mais seguro que senha e é o padrão de acesso SSH na AWS."

---

# 17. VPC (Virtual Private Cloud) — visão geral

**O que é:** a rede privada isolada onde seus recursos AWS vivem. Define faixas de IP, sub-redes,
tabelas de rota e gateways.

**Para que serve:** isolar e organizar a rede. Recursos numa VPC podem conversar de forma privada
(sem sair para a internet).

**Quando usar:** sempre existe uma. Toda conta tem uma **VPC default** — foi a que usei.

**Como foi usado no meu projeto:** usei a VPC **default**. A EC2 vive nela. No futuro, o RDS
ficaria na **mesma VPC**, com Security Group aceitando 5432 **apenas** do SG da EC2 — assim o
banco nunca é exposto à internet.

**Erros comuns:**
- Colocar RDS numa VPC/sub-rede sem rota para a EC2 → app não conecta.
- Marcar RDS como "publicly accessible" sem necessidade.

**Como explicar em entrevista:** "VPC é a rede privada da AWS. Usei a default no lab. O ponto-chave
é que EC2 e (futuro) RDS ficam na mesma VPC e conversam de forma privada, sem expor o banco."

---

# 18. RDS (Relational Database Service) — conceitual (PLANEJADO, não implementado)

> ⚠️ **No meu projeto o banco NÃO está no RDS.** Ele roda como **PostgreSQL em container Docker
> na própria EC2.** RDS é uma evolução planejada.

**O que é:** banco de dados relacional **gerenciado** pela AWS (PostgreSQL, MySQL, etc.).
A AWS cuida de instalação, patches, backups automáticos e failover.

**Para que serve:** ter banco confiável sem administrar o motor do banco manualmente.

**Quando usar:** quando você quer backups automáticos, resiliência e separar o ciclo de vida do
banco do ciclo de vida da aplicação.

**Como se conecta ao meu projeto:** hoje o Django aponta as variáveis `PG*` para o container
`db`. Migrar para RDS seria: criar a instância, apontar `PGHOST` para o endpoint do RDS e usar
`DB_SSLMODE=require`. **Nenhuma linha de código Python muda** — só variáveis de ambiente.

**Por que ainda não migrei:** quis validar todo o stack (Docker, Nginx, HTTPS, migração de dados)
antes de adicionar a complexidade e o custo do RDS.

**Erros comuns (quando migrar):**
- Security Group do RDS mal configurado → EC2 não conecta.
- Esquecer que **RDS cobra por hora mesmo parado** (não há "stop" gratuito como na EC2).

**Como explicar em entrevista:** "Hoje meu Postgres roda em container na EC2. Sei o trade-off:
RDS traria backups automáticos e failover, mas custo por hora contínuo. Para o lab, comecei
simples e deixei RDS como próximo passo — e migrar é só trocar variáveis de ambiente."

---

# 19. S3 (Simple Storage Service) — conceitual (PLANEJADO, não implementado)

> ⚠️ **No meu projeto ainda NÃO uso S3.** Static files são servidos por **WhiteNoise** (dentro do
> Gunicorn) e media files (avatares) ficam no disco do container.

**O que é:** armazenamento de **objetos** (arquivos) — um banco chave/valor onde a chave é o
"caminho" e o valor é o arquivo. Não é sistema de arquivos.

**Para que serve:** guardar arquivos de forma durável (11 noves) e barata, **fora** do servidor.

**Quando usar:** para media files (uploads de usuário) que não podem sumir em redeploy, e para
static files quando há múltiplas instâncias.

**Como se conecta ao meu projeto:** o problema real é que media no disco do container é **efêmero**
— redeploy recria o container e os avatares somem. A solução planejada: `django-storages` + `boto3`
apontando o storage `default` para um bucket S3. Static seguiria com WhiteNoise ou iria para S3.

**Erros comuns (quando implementar):**
- Deixar bucket de media público sem querer → expõe arquivos de usuários.
- Credenciais amplas demais (deveria ser IAM só com ações de S3 nos buckets certos).

**Como explicar em entrevista:** "Ainda uso WhiteNoise para static e disco para media, o que é
efêmero. O passo planejado é S3 para media, porque o disco do container se perde no redeploy.
S3 vive fora da EC2 e é durável."

---

# 20. CloudWatch — conceitual (PLANEJADO, não implementado)

> ⚠️ **Não implementado.** Hoje observo a aplicação por `docker logs` e logs do Nginx no servidor.

**O que é:** serviço de monitoramento e observabilidade da AWS — métricas, logs centralizados e
alarmes.

**Para que serve:** enxergar CPU/rede/disco, centralizar logs e disparar alarmes (ex.: CPU > 80%).

**Quando usar:** quando você precisa de visibilidade e alertas automáticos em produção.

**Como se conecta ao meu projeto:** métricas básicas da EC2 (CPU, rede) já existem no console
gratuitamente. O plano é: criar **alarme de CPU alta**, instalar o CloudWatch Agent para
centralizar logs do Nginx/Gunicorn, e complementar com Sentry para erros de aplicação.

**Erros comuns:**
- Operar produção "no escuro", sem métricas nem alarme.
- Logs sem rotação enchendo o disco da EC2.

**Como explicar em entrevista:** "Hoje uso `docker logs` e logs do Nginx. O próximo passo de
observabilidade é CloudWatch: alarme de CPU e logs centralizados, mais Sentry para exceptions."

---

# Conceitos de aplicação que apareceram (não-AWS, mas essenciais)

Estes não são serviços AWS, mas foram centrais no deploy e caem em entrevista:

| Conceito | Papel de 1 linha |
|---|---|
| **Docker** | Empacota app + dependências num container reproduzível (paridade dev/prod) |
| **Docker Compose** | Sobe múltiplos containers (web + db) com um comando |
| **Nginx** | Proxy reverso + terminação SSL na frente do Gunicorn |
| **Gunicorn** | Servidor WSGI de produção (workers paralelos) que roda o Django |
| **Django** | Framework web (views → services → ORM → PostgreSQL) |
| **PostgreSQL** | Banco relacional (no meu caso, em container Docker) |
| **Cloudflare** | DNS + CDN + proteção DDoS (usei no lugar do Route 53) |
| **Let's Encrypt / Certbot** | Certificado SSL gratuito com renovação automática |
| **WhiteNoise** | Serve static files direto do processo Django/Gunicorn |

---

# Pareto AWS

> **20% dos conceitos que me dão 80% do entendimento.**
> Se eu dominar só estes, entendo a espinha dorsal do que fiz.

### 1. Root vs IAM User
`Root = emergência`, `IAM User = dia a dia`. MFA em ambos. Todo `Access Denied` começa no IAM.

### 2. Herança de permissões
`User → Group → Policy`. Permissões vão para **grupos**, não para pessoas. Esquecer de colocar
o usuário no grupo = Access Denied.

### 3. Budget antes de infra
O maior risco na AWS é a **fatura**, não o código. Budget com alertas **antes** de criar recursos.

### 4. EC2 é só a máquina
EC2 = servidor virtual com controle total. **Tudo** roda dentro dela via Docker. A AMI define o
SO (Amazon Linux 2023 → `dnf` + `ec2-user`).

### 5. Elastic IP para não quebrar o DNS
IP público padrão muda no reboot. Elastic IP fixo (3.148.15.93) mantém o DNS estável.

### 6. Security Group = firewall stateful, com menor exposição
SSH só do meu IP; 80/443 abertos; **8000 nunca exposta**. Só o Nginx fala com o Gunicorn.

### 7. Menor privilégio
Admin humano pode usar `AdministratorAccess`; **aplicação nunca**. App recebe só o que precisa
(ex.: S3 específico).

### 8. Managed vs self-managed (RDS vs Postgres em container)
Entender o trade-off é mais importante que a ferramenta: gerenciado (RDS) traz backups/failover
com custo por hora; self-managed (container) é mais barato e simples, mas você cuida de tudo.

### 9. Efêmero vs persistente
Disco do **container é efêmero** (some no redeploy). EBS/S3/RDS **persistem**. Por isso media
deveria ir para S3 e banco crítico para RDS.

### 10. Separar responsabilidades no stack
`Nginx (borda/TLS)` ≠ `Gunicorn (rodar Python)` ≠ `Django (lógica)` ≠ `PostgreSQL (dados)`.
Cada camada faz uma coisa bem feita.

---

## Mapa mental (texto) — para gerar diagrama

```
CONTA AWS
├── Segurança
│   ├── Root (emergência) + MFA
│   ├── IAM User paulo-aws-admin (dia a dia) + MFA
│   ├── IAM Group Administrators
│   └── IAM Policy AdministratorAccess
├── Custo
│   └── Budget US$15 (alertas 85% / 100% / previsão)
├── Computação
│   └── EC2 (AMI Amazon Linux 2023, t3.micro, us-east-2)
│       ├── EBS (disco persistente)
│       ├── Elastic IP 3.148.15.93
│       ├── Key Pair nicia-track-key.pem (SSH ec2-user)
│       └── Security Group (22→meu IP, 80, 443; 8000 fechada)
├── Rede
│   └── VPC default
├── Dentro da EC2 (aplicação)
│   ├── Docker + Docker Compose
│   ├── PostgreSQL (container)  ← RDS é o plano futuro
│   ├── Gunicorn → Django
│   ├── Nginx (proxy + SSL)
│   └── Cloudflare DNS + Let's Encrypt HTTPS
└── PLANEJADO (não implementado)
    ├── RDS · S3 · CloudWatch · CI/CD
    └── fail2ban · IAM Role na EC2
```
