# Configuração Inicial da Conta AWS — Resumo Pareto (20% que gera 80% do entendimento)

## Objetivo

Preparar uma conta AWS para estudos e uso real seguindo as principais boas práticas de segurança e governança desde o primeiro dia.

Ao final da configuração, a conta ficou pronta para hospedar aplicações, criar infraestrutura e iniciar os estudos práticos de AWS sem depender da conta Root.

---

# 1. Configuração da Conta Root

## O que foi feito

* Criação/ativação da conta AWS
* Cadastro do cartão de crédito
* Verificação da conta
* Ativação de MFA na conta Root

## Por que isso é importante

A conta Root possui acesso total e irrestrito a todos os recursos da AWS.

Se alguém obtiver acesso à conta Root, poderá:

* Excluir toda a infraestrutura
* Criar recursos gerando custos
* Alterar configurações críticas
* Fechar a conta

Por isso a AWS recomenda:

```text
Root = Emergências
IAM User = Uso diário
```

## Conceito aprendido

### Root User

É o dono da conta AWS.

Utilizar apenas para:

* Configuração inicial
* Recuperação de acesso
* Operações críticas específicas

---

# 2. Criação do Budget (Controle de Custos)

## O que foi feito

Criado orçamento mensal:

```text
US$ 15/mês
```

Alertas automáticos:

```text
85%
100%
Previsão de atingir 100%
```

Notificações enviadas para:

```text
paulorgs.dev@gmail.com
```

## Por que isso é importante

Na AWS o principal erro dos iniciantes não é técnico.

É financeiro.

Exemplo:

```text
Criar EC2
Criar RDS
Esquecer ligado
Receber cobrança inesperada
```

O Budget funciona como um sistema de alerta antecipado.

## Conceito aprendido

### AWS Budgets

Ferramenta responsável por:

* Monitorar gastos
* Enviar alertas
* Evitar surpresas financeiras

---

# 3. Criação do Usuário IAM

## O que foi feito

Criado usuário:

```text
paulo-aws-admin
```

Com:

* Login no Console AWS
* Senha própria
* Troca obrigatória da senha inicial

## Por que isso é importante

A AWS trabalha com o princípio:

```text
Menor privilégio possível
```

Usuários IAM existem para evitar uso da conta Root.

## Conceito aprendido

### IAM User

Identidade criada para pessoas ou aplicações acessarem a AWS.

Exemplos:

```text
paulo-aws-admin
app-django
github-actions
jenkins
```

---

# 4. Criação do Grupo Administrators

## O que foi feito

Criado grupo:

```text
Administrators
```

Associado à política:

```text
AdministratorAccess
```

## Por que isso é importante

Em vez de dar permissões diretamente aos usuários:

```text
Usuário → Grupo → Permissões
```

A administração fica mais simples.

## Conceito aprendido

### IAM Group

Coleção de usuários que compartilham permissões.

Exemplo:

```text
Administrators
Developers
DevOps
Finance
```

---

# 5. Configuração de AdministratorAccess

## O que foi feito

Associada a política gerenciada pela AWS:

```text
AdministratorAccess
```

## O que ela permite

Acesso praticamente total aos serviços AWS.

Exemplos:

* EC2
* RDS
* S3
* VPC
* IAM
* CloudWatch
* Lambda

## Conceito aprendido

### IAM Policy

Documento que define permissões.

Estrutura lógica:

```text
Quem?
Pode fazer o quê?
Em quais recursos?
```

---

# 6. Problema Encontrado (Importante)

## O erro

O usuário foi criado.

O grupo foi criado.

A política foi criada.

Mas o usuário NÃO estava dentro do grupo.

Resultado:

```text
Access Denied
Permissões insuficientes
MFA inacessível
```

## Diagnóstico

Na lista de usuários apareceu:

```text
Grupo = 0
```

Isso indicava:

```text
Usuário não pertence a nenhum grupo
```

## Correção

Adicionado:

```text
paulo-aws-admin
```

ao grupo:

```text
Administrators
```

Problema resolvido imediatamente.

## Conceito aprendido

Herança de permissões.

```text
Usuário
   ↓
Grupo
   ↓
Policy
```

Se o usuário não estiver no grupo:

```text
Não recebe permissões.
```

---

# 7. Configuração de MFA no Usuário IAM

## O que foi feito

Configurado MFA no:

```text
paulo-aws-admin
```

Utilizando:

```text
Authenticator App
```

## Por que isso é importante

Mesmo que alguém descubra a senha:

```text
Sem o celular
↓
Sem acesso
```

## Conceito aprendido

### MFA (Multi-Factor Authentication)

Autenticação baseada em:

```text
Algo que você sabe
+
Algo que você possui
```

Exemplo:

```text
Senha
+
Código do aplicativo autenticador
```

---

# 8. Validação Final

## Teste realizado

Login com:

```text
paulo-aws-admin
```

Acesso ao:

```text
EC2
```

Resultado:

```text
Acesso liberado
Sem Access Denied
```

## O que isso comprovou

* IAM funcionando
* MFA funcionando
* Grupo funcionando
* Política funcionando
* Permissões funcionando

---

# Arquitetura Final da Conta

```text
Conta Root
│
├── MFA habilitado
│
└── Uso apenas emergencial

Grupo IAM
│
└── Administrators
     │
     └── AdministratorAccess

Usuário IAM
│
└── paulo-aws-admin
     │
     ├── Senha própria
     ├── MFA habilitado
     └── Uso diário da AWS
```

---

# O que Memorizar para Entrevistas e Certificações

Se lembrar apenas destes pontos, já absorveu a maior parte do aprendizado desta etapa:

### 1. Nunca usar Root no dia a dia

```text
Root = Emergência
IAM User = Trabalho diário
```

### 2. Sempre habilitar MFA

Em:

* Root
* Usuários IAM importantes

### 3. Usuários recebem permissões por grupos

```text
User → Group → Policy
```

### 4. Criar Budgets antes de criar infraestrutura

Evita custos inesperados.

### 5. AdministratorAccess é uma policy gerenciada pela AWS

Fornece acesso administrativo completo.

### 6. Access Denied normalmente é problema de IAM

Verificar:

* Usuário
* Grupo
* Policy
* Herança de permissões

---

# Próxima Etapa dos Estudos AWS

Ordem recomendada:

```text
✓ IAM
✓ Budgets
→ S3
→ VPC
→ EC2
→ Security Groups
→ RDS PostgreSQL
→ CloudWatch
→ Deploy Django
```

Essa sequência cobre a maior parte do conhecimento que você precisará para construir e implantar sua aplicação de estudos na AWS.

