# AWS STUDY 03 — Preparação para Entrevista

> Transforma o deploy real do **Nícia Track** em munição para entrevista.
> Baseado no que eu **realmente** fiz. Onde algo é **planejado** (RDS, S3, CloudWatch, CI/CD),
> está marcado — para eu nunca dizer numa entrevista que fiz algo que não fiz.
>
> **Cola de contexto:** Django em Docker numa **EC2 (Amazon Linux 2023, t3.micro, us-east-2)**;
> **Nginx** (proxy + SSL) → **Gunicorn** → **Django** → **PostgreSQL em container**; DNS e HTTPS
> por **Cloudflare** + **Let's Encrypt**; Elastic IP `3.148.15.93`; dados migrados do **Neon**.

---

# Parte 1 — Perguntas e Respostas (50+)

### AWS — Conta, IAM, Segurança

**1. O que você deployou na AWS?**
Uma aplicação Django (Nícia Track, plataforma de estudos para concursos) rodando em Docker numa
EC2, com Nginx como proxy reverso e HTTPS, PostgreSQL em container, DNS e SSL via Cloudflare +
Let's Encrypt.

**2. Qual foi a primeira coisa que você fez na conta AWS?**
Segurança e custo antes de infraestrutura: MFA na conta Root, criação de um IAM User para uso
diário e um Budget de US$ 15/mês com alertas.

**3. Por que não usar a conta Root no dia a dia?**
Root tem poder total e irrestrito (inclusive fechar a conta). Se vazar, perde-se tudo. Uso Root só
em emergências; para o dia a dia criei o IAM User `paulo-aws-admin` com MFA.

**4. Explique `User → Group → Policy`.**
Permissões vão para grupos, não para pessoas. O usuário entra no grupo e **herda** a política.
Facilita administrar em escala.

**5. Conte um erro de IAM que você cometeu.**
Criei usuário, grupo e política, mas esqueci de colocar o usuário no grupo. Resultado: `Access
Denied` e MFA inacessível. O campo "Grupo = 0" foi o diagnóstico. Adicionei ao grupo e as
permissões vieram por herança.

**6. O que é uma IAM Policy?**
Um documento JSON com `Effect` (Allow/Deny), `Action` (o que) e `Resource` (onde). Usei a
gerenciada `AdministratorAccess` para o admin humano.

**7. O que é o princípio do menor privilégio?**
Cada identidade recebe só o que precisa. Admin humano pode ter `AdministratorAccess`, mas a
aplicação nunca — ela receberia só ações de S3 nos buckets certos (planejado).

**8. O que é MFA e onde você usou?**
Autenticação de dois fatores (senha + código do app). Habilitei no Root e no IAM User admin.

**9. Como você controlou custos?**
Budget de US$ 15/mês com alertas em 85%, 100% e previsão. O lab fica no free tier. Também sei o
procedimento de teardown (backup + parar/deletar recursos).

**10. O que é o AWS Budget e por que criá-lo antes da infra?**
Ferramenta de alerta de gasto. Na AWS o erro nº 1 é financeiro (esquecer recurso ligado); o
Budget é o alarme antecipado.

### AWS — EC2, Rede, Storage

**11. O que é EC2?**
Máquina virtual na AWS, com controle total via SSH. É onde tudo roda: Docker, Nginx, Gunicorn,
Django e o PostgreSQL em container.

**12. Qual AMI e tipo de instância você usou e por quê?**
Amazon Linux 2023, t3.micro, us-east-2. t3 é geração mais nova que t2 (melhor performance) e ainda
free tier. Amazon Linux muda o gerenciador para `dnf` e o usuário SSH para `ec2-user`.

**13. O que é uma AMI?**
O molde de SO/software da instância. A minha foi Amazon Linux 2023.

**14. O que é EBS?**
Disco SSD persistente da EC2. Sobrevive à parada da instância. Meu volume Docker do PostgreSQL
vive no EBS.

**15. O que é um Elastic IP e por que você usou?**
IP público fixo. Usei `3.148.15.93` para o DNS do Cloudflare não quebrar quando a EC2 reinicia
(o IP público padrão muda).

**16. O que é um Security Group?**
Firewall virtual stateful. No meu: SSH (22) só do meu IP, HTTP (80) e HTTPS (443) abertos, porta
8000 fechada.

**17. Por que a porta 8000 não está aberta?**
Porque o Gunicorn não deve ficar exposto direto à internet (sem TLS, rate limiting, proteção
slowloris). Só o Nginx, localmente, fala com ele.

**18. Como você acessa a EC2?**
Por SSH com par de chaves: `ssh -i nicia-track-key.pem ec2-user@3.148.15.93`. A chave `.pem` tem
`chmod 400`.

**19. O que é um Key Pair?**
Par de chaves criptográficas: a pública fica na EC2, a privada (`.pem`) comigo. Autentica o SSH
sem senha.

**20. O que é VPC?**
Rede privada isolada onde os recursos AWS vivem. Usei a VPC default. Num futuro RDS, ele ficaria
na mesma VPC, acessível só pela EC2.

**21. Você usou RDS?**
Não. Meu banco é PostgreSQL em container Docker na EC2. RDS é um passo planejado. Sei o trade-off:
RDS traz backups automáticos e failover, mas cobra por hora mesmo parado.

**22. Você usou S3?**
Ainda não. Static files são servidos por WhiteNoise e media (avatares) ficam no disco do
container. S3 é planejado para resolver o disco efêmero do container.

**23. Você usou CloudWatch?**
Não implementado. Hoje uso `docker logs` e logs do Nginx. CloudWatch (alarme de CPU, logs
centralizados) está planejado, junto com Sentry.

**24. Por que Cloudflare e não Route 53?**
Já tinha conta no Cloudflare, que dá DNS + CDN + proteção DDoS grátis. Route 53 seria a opção
100% AWS.

### Deploy, Nginx, Gunicorn, HTTPS

**25. Descreva o caminho de uma requisição.**
Usuário → Cloudflare/DNS resolve `nicia.paulodev.net` → Elastic IP → Nginx (443, termina SSL) →
Gunicorn (8000, local) → Django → PostgreSQL (container) → volta o HTML.

**26. O que o Nginx faz no seu stack?**
Proxy reverso e terminação SSL: recebe HTTPS, valida certificado, redireciona HTTP→HTTPS, adiciona
headers de segurança e repassa como HTTP para o Gunicorn.

**27. Por que não expor o Django/Gunicorn direto?**
Gunicorn é ótimo para rodar Python mas não tem TLS, rate limiting nem proteção contra conexões
lentas. Nginx cobre a borda.

**28. O que é Gunicorn?**
Servidor WSGI de produção com workers paralelos. Roda `config.wsgi:application`.

**29. Por que não usar `runserver` em produção?**
É single-thread, de desenvolvimento, não otimizado e inseguro para exposição na internet.

**30. O que é WSGI?**
A interface padrão entre servidores web Python e frameworks. Gunicorn fala WSGI e chama o Django.

**31. Como você configurou HTTPS?**
Let's Encrypt + Certbot no Nginx (porta 443, redirect automático, renovação automática validada
com `--dry-run`), e no Django reativei `SECURE_SSL_REDIRECT`, HSTS e secure cookies.

**32. O que é `SECURE_PROXY_SSL_HEADER` e por que importa?**
Diz ao Django para confiar no header `X-Forwarded-Proto: https` do Nginx. Sem isso, com
`SECURE_SSL_REDIRECT`, o Django entraria em loop de redirect (a requisição que chega dele é HTTP).

**33. Você teve problema ao ligar HTTPS cedo demais?**
Sim. Liguei `SECURE_SSL_REDIRECT=True` antes do HTTPS existir e tomei 301 em loop. Desativei
temporariamente HSTS/redirect/cookies e reativei só depois do Nginx+certificado prontos.

**34. O que faz o `ALLOWED_HOSTS`?**
Django rejeita (400) requisições cujo header `Host` não esteja na lista. Protege contra Host header
injection. Configurei com `nicia.paulodev.net`.

**35. O que é `CSRF_TRUSTED_ORIGINS`?**
Lista de origens confiáveis para POST em HTTPS. Sem incluir `https://nicia.paulodev.net`, os
formulários dariam 403.

**36. O que é CSRF e como o Django protege?**
Cross-Site Request Forgery: um site malicioso usa a sessão ativa do usuário. Django insere um token
secreto em cada formulário e valida na submissão; em HTTPS também confere a origem.

### Docker

**37. Por que Docker?**
Paridade dev/prod e reprodutibilidade. O mesmo Dockerfile roda na minha máquina e na EC2. Acaba
com "na minha máquina funciona".

**38. O que é Docker Compose e como você o usou?**
Orquestra múltiplos containers. Criei `docker-compose.prod.yml` com `web` (Gunicorn/Django) e `db`
(PostgreSQL), usando imagem pré-construída.

**39. Conte um problema real com Docker Compose.**
No Amazon Linux 2023 o `docker-compose-plugin` não está nos repos. Instalei o binário oficial do
GitHub manualmente em `/usr/local/lib/docker/cli-plugins/`.

**40. Por que `docker compose restart` não bastou numa mudança de `.env`?**
Porque `restart` não recarrega variáveis do `.env`. Precisei de `down && up -d`.

**41. O que significa o disco do container ser efêmero?**
Todo redeploy recria o container e apaga o que foi escrito no disco dele. Por isso avatares no
disco somem — e por isso media deveria ir para S3.

### Linux / Operação

**42. Diferença prática entre Amazon Linux e Ubuntu no seu deploy?**
Gerenciador `dnf` (não `apt`), usuário SSH `ec2-user` (não `ubuntu`), e instalação diferente de
Nginx/Certbot/Compose.

**43. Como você vê logs da aplicação?**
`docker logs nicia-track --follow` (Gunicorn/Django) e `/var/log/nginx/access.log` e `error.log`.

**44. Como você garante que Docker roda sem sudo?**
Adicionei `ec2-user` ao grupo `docker`.

**45. Como você protege o arquivo `.env`?**
Está no `.gitignore`, criado manualmente na EC2 com `chmod 600` (só o dono lê). `SECRET_KEY` de
produção é diferente da de dev.

### PostgreSQL / Migração

**46. Onde roda seu banco e qual o risco?**
PostgreSQL em container Docker na EC2. Risco: sem backup automático e atrelado à EC2; por isso faço
`pg_dump` manual e planejo migrar para RDS.

**47. Descreva a migração de dados que você fez.**
Migrei os dados do Neon PostgreSQL 18 (que servia o Render) para o PostgreSQL 16 em container:
backup preventivo → dump do Neon → comparar contagens → `DROP SCHEMA public CASCADE` → restore →
validar.

**48. Qual foi o problema de versão e como resolveu?**
`pg_dump`/`pg_restore` v16 não lidam com o servidor Postgres 18 (`server version mismatch` /
`unsupported version 1.16`). Usei um container temporário `postgres:18` para dump e restore. No
restore, conectei-o na mesma rede Docker do banco (`--network`) e usei `--no-owner`.

**49. Como você validou a migração?**
Contando registros antes e depois: `lessonprogress` (16) e `useranswer` (85) existiam no Neon mas
não na AWS. Confirmei 25 tabelas, as contagens e os 3 usuários reais após o restore.

**50. Qual a lição da migração?**
Estrutura correta não garante dados migrados. Sempre contar registros antes e depois, e sempre
fazer backup antes de operações destrutivas como `DROP SCHEMA`.

### Segurança / Arquitetura / Escala

**51. Como você protegeu os secrets?**
Nada de secret no código. Tudo em `.env` (fora do git, `chmod 600`) lido por `python-decouple`.
Para escala, usaria SSM Parameter Store ou Secrets Manager.

**52. Que headers de segurança você aplicou?**
No Nginx: HSTS (`Strict-Transport-Security`), `X-Content-Type-Options: nosniff`, `X-Frame-Options`.
No Django: HSTS, secure cookies, `SECURE_SSL_REDIRECT`.

**53. Quais riscos de segurança ainda estão abertos?**
SSH ainda aceita senha (planejo desabilitar), sem `fail2ban`, e a aplicação usa `.env` em vez de
IAM Role. São itens planejados de hardening.

**54. O que você faria diferente em escala/produção crítica?**
Auto Scaling + ALB (múltiplas EC2), RDS Multi-AZ, ElastiCache Redis, CloudFront na frente do S3,
CI/CD com GitHub Actions, logs no CloudWatch, e migrations fora do CMD do container (evitar corrida
com réplicas).

**55. Como parar o lab sem perder dados?**
Backup do banco (`pg_dump`), parar a EC2 (EBS persiste), e — no futuro RDS — snapshot antes de
deletar. Manter Elastic IP associado ou liberar para não pagar por IP ocioso.

---

# Parte 2 — Flashcards (80+)

> Formato: **Pergunta / Resposta.** Curtos, para revisão rápida e geração automática.

**F1.** P: Root vs IAM User? R: Root = emergência; IAM User = dia a dia.
**F2.** P: Herança de permissões IAM? R: User → Group → Policy.
**F3.** P: Meu erro clássico de IAM? R: Usuário fora do grupo → Access Denied.
**F4.** P: O que é IAM Policy? R: JSON com Effect + Action + Resource.
**F5.** P: Policy do admin humano? R: `AdministratorAccess` (gerenciada).
**F6.** P: Menor privilégio? R: Cada identidade só com o que precisa.
**F7.** P: MFA é? R: Senha (sabe) + código do app (possui).
**F8.** P: Onde habilitei MFA? R: Root e IAM User admin.
**F9.** P: Valor do meu Budget? R: US$ 15/mês.
**F10.** P: Alertas do Budget? R: 85%, 100% e previsão de 100%.
**F11.** P: Erro nº 1 de iniciante na AWS? R: Financeiro (esquecer recurso ligado).
**F12.** P: O que é EC2? R: Máquina virtual na AWS com acesso root via SSH.
**F13.** P: Minha AMI? R: Amazon Linux 2023.
**F14.** P: Meu tipo de instância? R: t3.micro (free tier).
**F15.** P: Minha região? R: us-east-2 (Ohio).
**F16.** P: t3 vs t2? R: t3 é geração mais nova, melhor performance, ainda free tier.
**F17.** P: Usuário SSH no Amazon Linux? R: `ec2-user` (não `ubuntu`).
**F18.** P: Gerenciador de pacotes no Amazon Linux? R: `dnf` (não `apt`).
**F19.** P: O que é AMI? R: Molde de SO/software da instância.
**F20.** P: O que é EBS? R: Disco SSD persistente da EC2.
**F21.** P: O que é Elastic IP? R: IP público fixo alocado à EC2.
**F22.** P: Meu Elastic IP? R: 3.148.15.93.
**F23.** P: Por que Elastic IP? R: IP padrão muda no reboot e quebra o DNS.
**F24.** P: O que é Security Group? R: Firewall virtual stateful.
**F25.** P: Minha regra SSH? R: Porta 22 só do meu IP (177.36.193.61/32).
**F26.** P: Portas abertas ao público? R: 80 e 443.
**F27.** P: Porta 8000 está? R: Fechada — Gunicorn nunca exposto direto.
**F28.** P: Comando SSH que usei? R: `ssh -i nicia-track-key.pem ec2-user@3.148.15.93`.
**F29.** P: Permissão da chave `.pem`? R: `chmod 400`.
**F30.** P: O que é Key Pair? R: Chave pública na EC2, privada comigo.
**F31.** P: O que é VPC? R: Rede privada isolada da AWS.
**F32.** P: Qual VPC usei? R: A default.
**F33.** P: Uso RDS? R: Não — Postgres em container. RDS é planejado.
**F34.** P: Trade-off do RDS? R: Backups/failover, mas cobra por hora mesmo parado.
**F35.** P: Uso S3? R: Não ainda. WhiteNoise para static, disco para media.
**F36.** P: Por que S3 para media? R: Disco do container é efêmero.
**F37.** P: Durabilidade do S3? R: 11 noves (99,999999999%).
**F38.** P: Uso CloudWatch? R: Não. Uso `docker logs` e logs do Nginx.
**F39.** P: DNS que usei? R: Cloudflare (não Route 53).
**F40.** P: Por que Cloudflare? R: DNS + CDN + DDoS grátis; já tinha conta.
**F41.** P: Meu domínio? R: https://nicia.paulodev.net.
**F42.** P: Papel do Nginx? R: Proxy reverso + terminação SSL.
**F43.** P: Por que não expor Gunicorn? R: Sem TLS, rate limiting nem proteção slowloris.
**F44.** P: O que é Gunicorn? R: Servidor WSGI de produção com workers.
**F45.** P: Por que não `runserver` em prod? R: Single-thread, de dev, inseguro.
**F46.** P: O que é WSGI? R: Interface entre servidor web Python e o framework.
**F47.** P: Ponto de entrada do Django no Gunicorn? R: `config.wsgi:application`.
**F48.** P: SSL gratuito que usei? R: Let's Encrypt via Certbot.
**F49.** P: Validade do certificado Let's Encrypt? R: 90 dias (renovação automática).
**F50.** P: Como validei a renovação? R: `certbot renew --dry-run`.
**F51.** P: O que faz `SECURE_PROXY_SSL_HEADER`? R: Django confia no `X-Forwarded-Proto: https`.
**F52.** P: Sem esse header, o que acontece? R: Loop infinito de redirect HTTPS.
**F53.** P: Erro de HTTPS prematuro? R: `SECURE_SSL_REDIRECT=True` deu 301 em loop.
**F54.** P: O que faz `ALLOWED_HOSTS`? R: Rejeita (400) Host não listado.
**F55.** P: Protege contra o quê? R: Host header injection.
**F56.** P: O que é `CSRF_TRUSTED_ORIGINS`? R: Origens confiáveis para POST em HTTPS.
**F57.** P: Sem ela, o que acontece? R: Formulários dão 403.
**F58.** P: O que é CSRF? R: Site malicioso usa a sessão ativa do usuário.
**F59.** P: Como Django protege de CSRF? R: Token secreto em cada formulário.
**F60.** P: Por que Docker? R: Paridade dev/prod e reprodutibilidade.
**F61.** P: O que é Docker Compose? R: Orquestra múltiplos containers com um comando.
**F62.** P: Meus serviços no compose? R: `web` (Gunicorn/Django) e `db` (PostgreSQL).
**F63.** P: Problema do Compose no AL2023? R: Plugin não está nos repos; instalei binário manual.
**F64.** P: `docker compose restart` recarrega `.env`? R: Não; use `down && up -d`.
**F65.** P: Disco do container é? R: Efêmero — some no redeploy.
**F66.** P: Rodo Docker sem sudo como? R: `ec2-user` no grupo `docker`.
**F67.** P: Versão do Docker que instalei? R: 25.0.14.
**F68.** P: Meu banco roda onde? R: Container Docker na EC2 (PostgreSQL 16).
**F69.** P: De onde migrei os dados? R: Neon PostgreSQL 18 (que servia o Render).
**F70.** P: Erro de versão no dump? R: `server version mismatch` (v16 vs 18).
**F71.** P: Erro no restore? R: `unsupported version 1.16`.
**F72.** P: Solução do problema de versão? R: Container temporário `postgres:18`.
**F73.** P: Como o container temp acessou o banco? R: Mesma rede Docker (`--network`).
**F74.** P: Flag no restore para objetos do Neon? R: `--no-owner`.
**F75.** P: Avisos normais do Neon? R: `neon_superuser`, `cloud_admin`, `transaction_timeout`.
**F76.** P: O que faltava na AWS antes da migração? R: lessonprogress (16) e useranswer (85).
**F77.** P: Lição da migração? R: Estrutura correta ≠ dados migrados; contar antes/depois.
**F78.** P: Antes de `DROP SCHEMA`, o que fiz? R: Backup com `pg_dump`.
**F79.** P: Como protejo secrets? R: `.env` fora do git, `chmod 600`, `python-decouple`.
**F80.** P: `DEBUG` em produção? R: `False` (sempre).
**F81.** P: Por que `DEBUG=False`? R: `True` expõe traceback, URLs e configs.
**F82.** P: Para que serve `SECRET_KEY`? R: Assina sessões e tokens CSRF.
**F83.** P: Headers de segurança no Nginx? R: HSTS, nosniff, X-Frame-Options.
**F84.** P: Como vejo logs do Gunicorn? R: `docker logs nicia-track --follow`.
**F85.** P: Por que testar com IP real, não localhost? R: `server_name` do Nginx não bate localhost.
**F86.** P: Escala: como distribuir tráfego? R: ALB + Auto Scaling com múltiplas EC2.
**F87.** P: Escala: failover de banco? R: RDS Multi-AZ.
**F88.** P: Escala: CDN na frente do S3? R: CloudFront.
**F89.** P: Escala: deploy automático? R: CI/CD com GitHub Actions.
**F90.** P: Idempotente significa? R: Rodar N vezes dá o mesmo resultado.

---

# Parte 3 — Quiz (30 questões, múltipla escolha)

> Marque a alternativa correta. Gabarito ao final.

**Q1.** Qual SO foi usado na EC2?
a) Ubuntu 22.04  b) Amazon Linux 2023  c) Debian 12  d) Windows Server

**Q2.** Qual o usuário SSH padrão nesse SO?
a) ubuntu  b) admin  c) ec2-user  d) root

**Q3.** Qual gerenciador de pacotes se usa nesse SO?
a) apt  b) yum-only  c) dnf  d) pacman

**Q4.** Onde roda o banco de dados neste projeto?
a) RDS  b) Container Docker na EC2  c) Neon  d) SQLite local

**Q5.** Qual serviço de DNS foi usado?
a) Route 53  b) Cloudflare  c) GoDaddy  d) Bind local

**Q6.** Qual o Elastic IP da EC2?
a) 3.148.15.93  b) 10.0.0.1  c) 177.36.193.61  d) 8.8.8.8

**Q7.** A porta 8000 (Gunicorn) está:
a) Aberta para 0.0.0.0/0  b) Fechada no Security Group  c) Aberta só na 443  d) Redirecionada

**Q8.** A regra de SSH (22) permite acesso de:
a) 0.0.0.0/0  b) Qualquer VPC  c) Apenas meu IP (/32)  d) Apenas a AWS

**Q9.** Qual o papel principal do Nginx aqui?
a) Banco de dados  b) Proxy reverso + terminação SSL  c) Servidor WSGI  d) Cache Redis

**Q10.** Por que não expor o Gunicorn direto?
a) É lento demais  b) Não tem TLS/rate limiting/proteção slowloris  c) Não roda Python  d) Custa mais

**Q11.** O que é WSGI?
a) Um banco  b) Interface servidor web Python ↔ framework  c) Um firewall  d) Um container

**Q12.** Certificado SSL veio de:
a) AWS ACM  b) Let's Encrypt (Certbot)  c) Cloudflare Origin  d) Comprado

**Q13.** Validade do certificado Let's Encrypt:
a) 30 dias  b) 90 dias  c) 1 ano  d) Infinita

**Q14.** `SECURE_PROXY_SSL_HEADER` serve para:
a) Habilitar gzip  b) Django confiar no `X-Forwarded-Proto`  c) Criar cookie  d) Abrir a 443

**Q15.** Ligar `SECURE_SSL_REDIRECT` antes do HTTPS causou:
a) 404  b) 500  c) 301 em loop  d) 403

**Q16.** `ALLOWED_HOSTS` protege contra:
a) SQL injection  b) Host header injection  c) XSS  d) CSRF

**Q17.** Sem `CSRF_TRUSTED_ORIGINS` correto, formulários dão:
a) 200  b) 301  c) 403  d) 502

**Q18.** Por que Docker?
a) Mais barato  b) Paridade dev/prod e reprodutibilidade  c) Substitui o Nginx  d) É banco

**Q19.** Problema do Docker Compose no Amazon Linux 2023:
a) Não existe Docker  b) Plugin não está nos repos (instalação manual)  c) Só roda com sudo  d) Sem rede

**Q20.** `docker compose restart` após mudar o `.env`:
a) Recarrega tudo  b) Não recarrega o `.env` (precisa `down && up`)  c) Apaga o banco  d) Falha sempre

**Q21.** Disco do container é:
a) Persistente  b) Efêmero (some no redeploy)  c) Igual ao EBS  d) Um bucket S3

**Q22.** De onde os dados foram migrados?
a) RDS  b) Neon PostgreSQL 18  c) MySQL  d) MongoDB

**Q23.** O erro de versão no dump/restore ocorreu porque:
a) Falta de disco  b) pg_dump/restore v16 não lê servidor v18  c) Senha errada  d) Rede caiu

**Q24.** A solução para a incompatibilidade de versão foi:
a) Reinstalar tudo  b) Container temporário `postgres:18`  c) Downgrade do Neon  d) Ignorar

**Q25.** No restore, o container temporário acessou o banco via:
a) Internet pública  b) Mesma rede Docker (`--network`)  c) SSH  d) VPN

**Q26.** O que faltava na AWS antes da migração?
a) Usuários  b) lessonprogress e useranswer  c) Questões  d) Nada

**Q27.** Lição principal da migração:
a) Estrutura correta garante dados  b) Estrutura correta ≠ dados migrados  c) Backup é opcional  d) Versão não importa

**Q28.** Valor e alertas do Budget:
a) US$5, 50%  b) US$15, 85%/100%/previsão  c) US$100, 90%  d) Sem alertas

**Q29.** MFA foi habilitado em:
a) Só no Root  b) Root e IAM User admin  c) Só no IAM User  d) Em nenhum

**Q30.** Qual destes NÃO foi implementado (é planejado)?
a) Nginx  b) HTTPS  c) RDS  d) Elastic IP

### Gabarito
1-b · 2-c · 3-c · 4-b · 5-b · 6-a · 7-b · 8-c · 9-b · 10-b · 11-b · 12-b · 13-b · 14-b · 15-c ·
16-b · 17-c · 18-b · 19-b · 20-b · 21-b · 22-b · 23-b · 24-b · 25-b · 26-b · 27-b · 28-b · 29-b · 30-c

---

# Parte 4 — Entrevista Simulada

> Diálogo completo com respostas-modelo, cobrindo AWS, Deploy, Docker, Linux, Django,
> PostgreSQL e Segurança.

**Entrevistador:** Me fala de um projeto que você colocou em produção na nuvem.
**Você:** Deployei uma aplicação Django de estudos para concursos na AWS. Roda em Docker numa EC2
Amazon Linux, com Nginx como proxy reverso e HTTPS, Gunicorn servindo o Django e PostgreSQL em
container. O DNS e o SSL são via Cloudflare e Let's Encrypt. Migrei os dados reais de um Postgres
gerenciado (Neon) para esse ambiente.

**Entrevistador:** Por que EC2 e não um PaaS como Render?
**Você:** O projeto já rodava no Render; a EC2 foi escolha de aprendizado. No PaaS a infra é
mágica; na EC2 eu instalo Docker, configuro o Security Group, gerencio o Nginx e entendo cada
camada. Esse conhecimento transfere para qualquer nuvem.

**Entrevistador:** Como você estruturou a segurança da conta?
**Você:** MFA no Root, que uso só em emergência; um IAM User `paulo-aws-admin` com MFA para o dia
a dia; permissões via grupo (`Administrators` → `AdministratorAccess`). Inclusive tomei um Access
Denied por ter esquecido de colocar o usuário no grupo — o campo "Grupo = 0" me denunciou.

**Entrevistador:** E controle de custo?
**Você:** Budget de US$ 15/mês com alertas em 85%, 100% e previsão. O lab fica no free tier, e
tenho o procedimento de teardown documentado.

**Entrevistador:** Explica o papel do Nginx e do Gunicorn.
**Você:** Nginx é a borda: termina o SSL, redireciona HTTP→HTTPS, adiciona headers de segurança e
repassa como HTTP para o Gunicorn no localhost:8000. Gunicorn é o servidor WSGI que roda o Django
com workers paralelos. Gunicorn não é feito para exposição direta — por isso a porta 8000 fica
fechada no Security Group.

**Entrevistador:** Teve algum problema com o HTTPS?
**Você:** Sim. Liguei `SECURE_SSL_REDIRECT` no Django antes de o HTTPS existir e caí num loop de
301. Desativei temporariamente e reativei junto com o Nginx e o certificado. O detalhe que fecha a
conta é o `SECURE_PROXY_SSL_HEADER`: sem ele, o Django não sabe que a requisição original era HTTPS
e entra em loop de redirect.

**Entrevistador:** Por que Docker?
**Você:** Paridade dev/prod. O mesmo Dockerfile roda na minha máquina e na EC2. Usei Docker Compose
com dois serviços, web e db. No Amazon Linux tive que instalar o Compose manualmente porque o
plugin não está nos repositórios.

**Entrevistador:** Diferença de operar Amazon Linux vs Ubuntu?
**Você:** Gerenciador `dnf` em vez de `apt`, usuário SSH `ec2-user` em vez de `ubuntu`, e
instalação diferente de Nginx, Certbot e Compose. Copiar tutorial de Ubuntu quebra.

**Entrevistador:** Onde roda o banco e por que não RDS?
**Você:** PostgreSQL em container na EC2. RDS é o próximo passo — sei que traz backups automáticos e
failover, mas cobra por hora mesmo parado. Quis validar o stack inteiro antes de adicionar custo.
Migrar é barato: só trocar `PGHOST` e `DB_SSLMODE`, sem mexer no código.

**Entrevistador:** Conta a migração de dados.
**Você:** Vim do Neon Postgres 18 para o Postgres 16 em container. Fiz backup preventivo, dump do
Neon, comparei contagens, dei `DROP SCHEMA public CASCADE`, restaurei e validei. O `pg_dump` e o
`pg_restore` v16 não lidavam com o servidor 18, então usei um container temporário `postgres:18`
para dump e restore, conectando-o na mesma rede Docker do banco. A grande lição: as tabelas já
existiam na AWS, mas o progresso dos alunos não — só contando registros antes e depois eu percebi.

**Entrevistador:** Como protege os secrets?
**Você:** Nada no código. Tudo em `.env` fora do git, `chmod 600`, lido por `python-decouple`.
`SECRET_KEY` de produção diferente de dev, `DEBUG=False`. Para escala, migraria para SSM Parameter
Store ou Secrets Manager.

**Entrevistador:** O que você faria diferente numa app crítica?
**Você:** Auto Scaling com ALB, RDS Multi-AZ, ElastiCache Redis, CloudFront na frente do S3, CI/CD
com GitHub Actions, logs no CloudWatch, e separaria as migrations do CMD do container para não ter
condição de corrida com múltiplas réplicas.

**Entrevistador:** Última: como você sabe que o sistema está no ar e saudável?
**Você:** Hoje é observabilidade básica: `docker logs` para Gunicorn/Django, logs do Nginx, e
`curl -I https://nicia.paulodev.net` mostrando o HSTS. CloudWatch (alarme de CPU, logs
centralizados) e Sentry são os próximos passos.

---

# Parte 5 — Respostas em Inglês (simples)

**Tell me about your AWS experience.**
"I deployed a Django web application on AWS from scratch. I set up the account securely with MFA
and an IAM user, launched an EC2 instance running Amazon Linux, and ran the app in Docker. I put
Nginx in front as a reverse proxy with HTTPS, used Gunicorn to serve Django, and ran PostgreSQL in
a container. I also migrated real production data from a managed Postgres (Neon) into this
environment."

**What did you deploy?**
"A Django study platform for public exams. It runs in Docker on an EC2 instance. Nginx handles
HTTPS and proxies to Gunicorn on port 8000, Django runs the logic, and PostgreSQL stores the data.
DNS and SSL are handled by Cloudflare and Let's Encrypt."

**Why Docker?**
"Environment parity. The same Dockerfile runs on my laptop and on EC2, so there are no
'works on my machine' problems. I used Docker Compose to run the web and database containers
together."

**Why EC2?**
"To learn the infrastructure. A PaaS hides the server; with EC2 I install Docker, configure the
firewall, and manage each layer myself. That knowledge transfers to any cloud."

**Why PostgreSQL?**
"It's a robust relational database that handles concurrency well and integrates natively with
Django. My app has relational data — users, questions, answers, study progress."

**Why Nginx?**
"Nginx is a reverse proxy and SSL terminator. It handles HTTPS, redirects HTTP to HTTPS, adds
security headers, and forwards requests to Gunicorn. Gunicorn is great at running Python but is not
meant to be directly exposed to the internet."

**How did you secure the application?**
"MFA on both root and my IAM user, least privilege for permissions, secrets kept out of the code in
a `.env` file with 600 permissions, `DEBUG=False`, a strong unique `SECRET_KEY`, HTTPS with HSTS,
SSH restricted to my own IP, and the application port never exposed — only Nginx talks to Gunicorn
locally."

**How did you manage costs?**
"I created an AWS Budget of 15 dollars a month with alerts at 85 percent, 100 percent, and a
forecast alert. The lab stays within the free tier, and I documented how to tear resources down
without losing data."

---

# Parte 6 — Resumo Pareto

## "Se eu tivesse apenas 30 minutos para revisar antes de uma entrevista"

**A arquitetura em uma frase:**
Usuário → Cloudflare/DNS → Elastic IP (3.148.15.93) → **Nginx** (443, SSL) → **Gunicorn** (8000,
local) → **Django** → **PostgreSQL em container**.

**Os 10 pontos que mais caem:**

1. **Segurança primeiro:** MFA (Root + IAM User), IAM `User → Group → Policy`, Budget US$15 antes
   de qualquer infra.
2. **EC2 = controle total:** Amazon Linux 2023 (`dnf`, `ec2-user`), t3.micro, us-east-2. Tudo roda
   dentro dela via Docker.
3. **Elastic IP fixo** para o DNS não quebrar. **Security Group** com SSH só do meu IP e **porta
   8000 fechada**.
4. **Nginx ≠ Gunicorn ≠ Django ≠ Postgres** — cada camada uma responsabilidade. Nunca exponha o
   Gunicorn direto.
5. **HTTPS em dois lugares:** Nginx (certificado Let's Encrypt, redirect) **e** Django
   (`SECURE_SSL_REDIRECT`, HSTS, `SECURE_PROXY_SSL_HEADER` para evitar loop de redirect).
6. **`ALLOWED_HOSTS`** (anti Host injection, 400) e **`CSRF_TRUSTED_ORIGINS`** (anti 403 em POST).
7. **Docker:** paridade dev/prod; Compose instalado manualmente no AL2023; `restart` não recarrega
   `.env` (use `down && up`); disco do container é **efêmero**.
8. **Banco em container (não RDS):** sei o trade-off; RDS traz backup/failover mas custa por hora.
   Migração para RDS = só variáveis.
9. **Migração Neon 18 → EC2 16:** incompatibilidade de versão resolvida com container temporário
   `postgres:18`; **contar registros antes/depois**; backup antes de `DROP SCHEMA`.
10. **Planejado, não feito:** RDS, S3, CloudWatch, CI/CD. Nunca afirmar que fiz — sei o porquê e o
    como de cada um.

**Uma frase de impacto para abrir a entrevista:**
"Fiz um deploy completo de Django na AWS: da segurança da conta ao HTTPS, incluindo uma migração de
banco com incompatibilidade de versão que resolvi com um container temporário. Entendo cada camada
porque configurei cada uma manualmente."
