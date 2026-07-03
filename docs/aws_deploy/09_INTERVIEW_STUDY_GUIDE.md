# 09 — Guia de Estudo para Entrevista Técnica

> Perguntas e respostas baseadas neste deploy real.
> Estude até conseguir responder cada uma em 60 segundos ou menos.
> Versão em inglês ao final.

---

## Perguntas em Português

---

### O que você deployou e como funciona?

"Deployei uma aplicação Django de preparação para concursos na AWS.
A aplicação roda num container Docker dentro de uma EC2.
Na frente fica o Nginx como proxy reverso, que cuida do HTTPS e passa
as requisições para o Gunicorn (servidor WSGI). O banco é um PostgreSQL
gerenciado no RDS. Arquivos de usuário ficam no S3.
Todo o ambiente é configurado via variáveis de ambiente — nenhum secret
está no código."

---

### Por que você usou EC2 e não Heroku ou Render?

"Para aprender. Heroku e Render abstraem a infraestrutura — você faz push
e o deploy acontece por magia. Na EC2, você instala Docker, configura o
Security Group, gerencia o processo gunicorn e entende o que acontece em
cada camada. É mais trabalhoso, mas entender o que está por baixo é o que
diferencia um desenvolvedor que só usa ferramentas de um que entende sistemas."

---

### Por que Docker?

"Docker garante paridade entre ambientes. O mesmo Dockerfile roda na minha
máquina, na EC2 e em qualquer lugar. Sem Docker, 'funciona na minha máquina'
é um problema real — diferenças de versão de Python, de biblioteca, de
sistema operacional causam bugs difíceis de reproduzir. Com Docker, o ambiente
é parte do código."

---

### Por que RDS e não PostgreSQL na própria EC2?

"Porque banco de dados e aplicação têm ciclos de vida diferentes.
A EC2 pode ser recriada, atualizada, substituída — sem afetar o banco.
O RDS gerencia backups automáticos, patches, failover. Se eu rodasse
PostgreSQL na EC2 e ela tivesse um problema de disco, perderia os dados.
Separar banco de aplicação é uma das práticas mais importantes de produção."

---

### Por que S3 para arquivos de mídia?

"Porque o disco do container é efêmero. Todo redeploy recria o container
do zero — tudo que foi salvo no disco é perdido. Avatares enviados pelos
usuários precisam sobreviver a redeploys. O S3 existe fora do container e
da EC2, é altamente durável e barato. Com S3, posso recriar a EC2 inteira
sem perder nenhum arquivo do usuário."

---

### O que é Nginx e por que ele está antes do Django?

"Nginx é um servidor web usado como proxy reverso. Ele fica entre o usuário
e o Django. O Nginx cuida de HTTPS (terminação SSL), redireciona HTTP para
HTTPS, adiciona headers de segurança e passa as requisições para o Gunicorn
na porta 8000. O Gunicorn não foi feito para estar na internet diretamente —
não tem TLS, rate limiting ou proteção contra conexões lentas. O Nginx cobre
essas responsabilidades."

---

### O que é Gunicorn e por que não usar `manage.py runserver` em produção?

"Gunicorn é o servidor WSGI de produção para Python. Ele cria múltiplos workers
(processos) que processam requisições em paralelo. O `runserver` do Django é
single-threaded e foi projetado para desenvolvimento — não tem workers paralelos,
não é otimizado para performance e não deve ser exposto à internet. Em produção,
Gunicorn + Nginx é o padrão para Django."

---

### Como Django funciona em produção? Qual é o papel do WSGI?

"WSGI (Web Server Gateway Interface) é o padrão de interface entre servidores web
Python e frameworks. O Gunicorn fala WSGI: recebe requisições HTTP e chama
`config.wsgi:application` — que é o ponto de entrada do Django. O Django processa
via middleware → views → templates e retorna uma resposta HTTP para o Gunicorn,
que devolve para o Nginx."

---

### Como você protegeu os secrets (senhas, chaves)?

"Nenhum secret está no código. Todos ficam em variáveis de ambiente, lidas
via `python-decouple` do arquivo `.env` (que está no .gitignore).
O `.env` é criado manualmente na EC2, com permissões 600 (apenas o dono lê).
A SECRET_KEY de produção é diferente da de desenvolvimento. Para escala maior,
usaria AWS SSM Parameter Store ou Secrets Manager para injetar as variáveis
sem precisar de um arquivo `.env` na máquina."

---

### Como você monitorou custos?

"Configurei um billing alert no AWS Budget para notificar por email quando
os custos mensais ultrapassassem USD 15. Habilitei o AWS Cost Explorer para
ver por serviço quanto está sendo cobrado. Para o laboratório, o custo fica
dentro do free tier (USD 0 nos primeiros 12 meses para t2.micro e db.t3.micro).
Documentei também como parar/deletar os recursos sem perder dados — snapshot
do RDS + stop da EC2 — para quando não estiver usando."

---

### O que faria diferente em uma aplicação maior ou mais crítica?

"Várias coisas. Primeiro, um Auto Scaling Group com múltiplas EC2 atrás de
um Application Load Balancer (ALB) — para escala horizontal e tolerância a falhas.
Segundo, RDS Multi-AZ para failover automático do banco. Terceiro, ElastiCache Redis
para cache de sessões e queries pesadas. Quarto, CloudFront na frente do S3 para
CDN global. Quinto, CI/CD com GitHub Actions — o push para main faz deploy automático.
Sexto, logging centralizado no CloudWatch com alertas. E migraria as migrations
para fora do CMD do Docker (via ECS task ou script separado) para suportar múltiplas
réplicas sem condição de corrida."

---

### O que é CSRF e como Django protege contra ele?

"CSRF (Cross-Site Request Forgery) é quando um site malicioso faz o browser do
usuário enviar uma requisição para sua aplicação, aproveitando a sessão ativa do
usuário. Django protege adicionando um token secreto em cada formulário. Quando
o formulário é enviado, Django verifica se o token é válido. Em HTTPS, Django
também verifica a origem via `CSRF_TRUSTED_ORIGINS` — rejeita POSTs de origens
não listadas."

---

### Por que ALLOWED_HOSTS existe no Django?

"Para proteger contra ataques de Host header injection. Um atacante pode manipular
o header Host de uma requisição HTTP para forçar redirecionamentos para domínios
maliciosos ou exfiltrar dados. Django verifica se o Host da requisição está na lista
`ALLOWED_HOSTS`. Se não estiver, retorna 400 — rejeitando a requisição antes de
qualquer processamento."

---

### O que é um Security Group e como você configurou o do RDS?

"Security Group é um firewall virtual da AWS. Define quais conexões de entrada e
saída são permitidas para um recurso (EC2, RDS). Para o RDS, configurei inbound
apenas na porta 5432 (PostgreSQL) com a origem sendo o Security Group da EC2 —
não o IP diretamente. Isso garante que apenas a aplicação pode acessar o banco.
Nenhuma conexão direta da internet ao banco é possível."

---

## Perguntas em inglês (English version)

---

### What did you deploy and how does it work?

"I deployed a Django application on AWS. It runs in a Docker container on an EC2
instance. Nginx sits in front as a reverse proxy — it handles HTTPS, terminates SSL,
and proxies requests to Gunicorn on port 8000. The database is a managed PostgreSQL
on RDS. User-uploaded files (avatars) are stored in S3. All secrets are managed
through environment variables — nothing sensitive is in the code."

---

### Why EC2 instead of a PaaS like Heroku or Render?

"To learn. PaaS platforms abstract away the infrastructure — it's easy but you don't
understand what's happening underneath. With EC2, I install Docker, configure the
firewall, manage processes, and understand each layer. That knowledge transfers
to any cloud environment."

---

### Why Docker?

"Environment parity. The same Dockerfile runs on my laptop and on EC2.
Without Docker, small differences in Python version, library versions, or OS
configuration cause hard-to-reproduce bugs. Docker makes the environment part
of the codebase — reproducible and portable."

---

### Why RDS instead of PostgreSQL on the EC2?

"Separation of concerns and reliability. If the EC2 fails or needs to be replaced,
the database on RDS is unaffected. RDS handles automated backups, security patches,
and failover. Running PostgreSQL on the same EC2 as the app means a single point
of failure for both the application and the data."

---

### Why S3 for media files?

"Container storage is ephemeral. Every redeploy recreates the container — anything
written to the container's filesystem is lost. User-uploaded files need to persist
across deployments. S3 lives outside the container and the EC2, is highly durable
(11 nines), and cheap. With S3, I can rebuild the entire EC2 without losing
any user data."

---

### What is Nginx doing in this stack?

"Nginx is acting as a reverse proxy and SSL terminator. It sits between the user
and Django: receives HTTPS connections, handles the TLS handshake, decrypts the
request, and proxies it as HTTP to Gunicorn on localhost:8000. It also redirects
HTTP to HTTPS and adds security headers. Gunicorn is excellent at running Python
but was never designed to be directly internet-facing."

---

### What is Gunicorn?

"Gunicorn is a Python WSGI HTTP server. It runs multiple worker processes that
handle requests in parallel. Django's `manage.py runserver` is single-threaded
and not production-ready. Gunicorn + Nginx is the standard production setup for
Django applications."

---

### How did you protect secrets?

"No secrets are in the codebase. All configuration (database credentials, secret key,
S3 keys) is loaded from environment variables using `python-decouple`. The `.env`
file is in `.gitignore` and was created manually on the EC2 with 600 permissions
(owner read-only). The production `SECRET_KEY` is different from development.
For a larger system, I would use AWS SSM Parameter Store or Secrets Manager."

---

### How did you handle cost control?

"I set up an AWS Budget alert to notify me via email when monthly costs exceed
USD 15. I also documented a 'teardown' procedure — how to stop resources without
losing data: snapshot the RDS, stop the EC2, release the Elastic IP. This lab
stays within the AWS free tier for the first 12 months."

---

### What would you do differently at scale?

"Several things: an Auto Scaling Group with multiple EC2 instances behind an
Application Load Balancer for horizontal scaling; RDS Multi-AZ for automatic
failover; ElastiCache Redis for session caching; CloudFront CDN in front of S3;
CI/CD with GitHub Actions for automated deployments; centralized logging in
CloudWatch; and I would separate database migrations from the container startup
command to avoid race conditions with multiple replicas."

---

## Termos técnicos — glossário rápido

| Termo | Significado |
|---|---|
| WSGI | Web Server Gateway Interface — padrão que permite servidores web e apps Python se comunicarem |
| SSL/TLS | Protocolo de criptografia que garante HTTPS |
| Proxy reverso | Servidor que recebe requisições e as encaminha para outro servidor |
| IAM | Identity and Access Management — sistema de permissões da AWS |
| Security Group | Firewall virtual da AWS que controla tráfego de rede |
| VPC | Virtual Private Cloud — rede privada isolada dentro da AWS |
| Idempotente | Operação que pode ser executada múltiplas vezes com o mesmo resultado |
| Free tier | Camada gratuita da AWS (12 meses para a maioria dos serviços) |
| EBS | Elastic Block Store — disco SSD persistente da EC2 |
| ECR | Elastic Container Registry — repositório de imagens Docker da AWS |
| ALB | Application Load Balancer — distribui tráfego entre múltiplas instâncias |
| Auto Scaling | Ajusta automaticamente o número de instâncias EC2 com base na demanda |
| CDN | Content Delivery Network — rede de servidores que serve conteúdo próximo ao usuário |
| Presigned URL | URL temporária com expiração para acessar objeto privado no S3 |
