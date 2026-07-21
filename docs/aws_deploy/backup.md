# Objetivo

Quero implementar um sistema completo de backup automático para o PostgreSQL da aplicação **Nícia Track**, que está rodando na AWS.

O objetivo é ter uma solução simples, segura, automatizada e de baixo custo.

**Importante:**

Não quero que você implemente imediatamente.

Primeiro estude toda a documentação do projeto, compreenda completamente a arquitetura e somente depois apresente um plano detalhado da implementação.

Somente após minha aprovação comece a implementação.

---

# FASE 0 — Documentação da implementação (OBRIGATÓRIA)

Antes de iniciar qualquer alteração, crie um documento em:

```text
docs/backup_implementation.md
```

Esse documento será um material de estudo para mim.

Durante toda a implementação, ele deverá ser atualizado continuamente.

**Não quero apenas uma documentação final.**

Quero que, conforme cada etapa for sendo concluída, você registre o que foi feito.

O objetivo é que, ao final da implementação, esse documento conte toda a história da construção da funcionalidade.

Cada seção deve conter, de forma objetiva e didática:

* o que foi implementado;
* por que essa decisão foi tomada;
* quais alternativas existiam;
* por que essa abordagem foi escolhida;
* quais arquivos foram modificados;
* quais comandos importantes foram utilizados;
* quais problemas apareceram;
* como eles foram resolvidos;
* quais conceitos de AWS, Docker, Linux ou PostgreSQL aparecem nessa etapa;
* quais aprendizados são importantes para entrevistas técnicas.

Sempre que terminar uma fase da implementação, atualize esse documento antes de seguir para a próxima.

No final, esse arquivo deverá servir como um material completo de estudo e revisão.

---

# FASE 1 — Estudo da infraestrutura

Antes de qualquer alteração:

Leia toda a documentação referente ao deploy, infraestrutura, Docker, PostgreSQL e AWS.

Entenda completamente:

* arquitetura do projeto;
* estrutura de diretórios;
* docker-compose de produção;
* configuração do PostgreSQL;
* como os volumes Docker estão configurados;
* onde ficam as variáveis de ambiente;
* como o banco é acessado;
* como o deploy funciona;
* scripts existentes;
* padrões utilizados no projeto.

Depois disso, faça um resumo técnico da arquitetura para confirmar que compreendeu corretamente o ambiente.

Caso exista qualquer dúvida, interrompa o processo e pergunte antes de continuar.

Após concluir esta fase, atualize `docs/backup_implementation.md`.

---

# FASE 2 — Planejamento

Antes de escrever qualquer código:

Analise a melhor estratégia para este projeto.

Considere:

* PostgreSQL rodando em container Docker;
* aplicação hospedada em EC2;
* ainda não utilizamos RDS;
* ainda não utilizamos Amazon S3;
* queremos manter custo praticamente zero;
* queremos uma solução simples e fácil de manter;
* queremos minimizar risco de perda dos dados reais da Nícia.

Explique:

* vantagens da solução escolhida;
* possíveis riscos;
* alternativas;
* melhorias futuras.

Somente depois disso apresente o plano completo da implementação.

Após concluir esta fase, atualize `docs/backup_implementation.md`.

---

# FASE 3 — Estrutura dos diretórios

Organizar o projeto.

Sugestão:

```text
aws-nicia/

docs/

scripts/
    backup_database.sh

backups/

.gitignore
```

O diretório `backups/` deverá ficar no `.gitignore`.

Caso exista uma estrutura mais adequada, explique antes de alterar.

Após concluir esta fase, atualize `docs/backup_implementation.md`.

---

# FASE 4 — Implementação do script

Criar:

```text
scripts/backup_database.sh
```

Esse script deverá:

* utilizar pg_dump oficial do PostgreSQL;
* utilizar exclusivamente as variáveis de ambiente já existentes;
* não duplicar configurações;
* gerar backup completo do banco;
* compactar automaticamente utilizando gzip;
* utilizar data e hora no nome do arquivo;
* salvar automaticamente na pasta `backups`;
* validar se o backup realmente foi criado;
* validar que o arquivo possui tamanho maior que zero;
* interromper o processo caso exista qualquer erro;
* retornar mensagens claras de sucesso e erro;
* possuir comentários explicando cada etapa;
* retornar códigos de erro apropriados.

Após concluir esta fase, atualize `docs/backup_implementation.md`.

---

# FASE 5 — Rotação automática

Após criar um backup válido:

O próprio script deverá fazer automaticamente:

1. listar todos os backups existentes;
2. ordenar do mais recente para o mais antigo;
3. manter apenas os 15 backups mais recentes;
4. remover automaticamente todos os backups excedentes.

Não quero precisar apagar backups manualmente.

A remoção só poderá acontecer após a confirmação de que o novo backup foi criado corretamente.

Caso exista uma estratégia mais segura para essa rotação, explique antes de implementar.

Após concluir esta fase, atualize `docs/backup_implementation.md`.

---

# FASE 6 — Integração com Google Drive

Após o backup ser criado com sucesso:

Quero enviar automaticamente uma cópia para minha conta do Google Drive.

Utilizar preferencialmente o **rclone**, caso seja a melhor solução.

Implementar:

* instalação;
* configuração;
* autenticação;
* criação do remote;
* envio automático;
* validação do upload.

Fluxo esperado:

1. criar backup;
2. validar backup;
3. enviar para Google Drive;
4. confirmar upload;
5. somente depois executar a limpeza dos backups locais.

Caso o upload falhe:

* não apagar os backups locais;
* registrar erro no log;
* manter os arquivos para nova tentativa.

Após concluir esta fase, atualize `docs/backup_implementation.md`.

---

# FASE 7 — Logs

Criar um sistema simples de logs.

Registrar:

* início do backup;
* horário;
* duração;
* sucesso;
* falhas;
* upload para Google Drive;
* limpeza dos backups antigos.

Quero conseguir verificar facilmente se o backup ocorreu corretamente.

Após concluir esta fase, atualize `docs/backup_implementation.md`.

---

# FASE 8 — Automação

Depois de tudo funcionando manualmente:

Configurar execução automática utilizando cron.

Quero que o backup aconteça automaticamente todos os dias.

Explique:

* horário escolhido;
* justificativa técnica;
* como listar os crons;
* como editar;
* como remover;
* como testar sem esperar o horário programado.

Após essa etapa, não quero precisar executar nenhum comando manualmente.

Após concluir esta fase, atualize `docs/backup_implementation.md`.

---

# FASE 9 — Testes

Antes de considerar a implementação concluída:

Realizar testes completos.

Validar:

* backup criado corretamente;
* arquivo íntegro;
* restauração possível;
* upload funcionando;
* política de retenção funcionando;
* exclusão apenas dos backups excedentes;
* funcionamento do cron;
* comportamento em caso de erro.

Mostrar o resultado de todos os testes.
 Após concluir esta fase, atualize `docs/backup_implementation.md`.

---

# FASE 10 — Documentação final

Revisar completamente o arquivo:

```text
docs/backup_implementation.md
```

Garantir que ele contenha:

* objetivo da implementação;
* arquitetura utilizada;
* fluxo completo do backup;
* explicação de cada decisão técnica;
* conceitos importantes;
* comandos utilizados;
* problemas encontrados;
* soluções adotadas;
* boas práticas;
* possíveis perguntas de entrevista relacionadas a backup;
* respostas sugeridas para essas perguntas;
* como restaurar um backup;
* troubleshooting;
* resumo final dos aprendizados.

Este documento deve servir como um material de estudo para futuras entrevistas e revisões.

---

# FASE 11 — Melhorias futuras

Criar uma seção chamada **"Melhorias Futuras"**, sugerindo implementações como:

* envio também para Amazon S3;
* criptografia dos backups;
* verificação automática de integridade;
* notificações por e-mail;
* notificações via Discord ou Telegram;
* monitoramento;
* múltiplas cópias de segurança;
* migração futura para RDS utilizando backups gerenciados pela AWS.

Explicar brevemente por que cada melhoria seria interessante.

---

# Regras importantes

* Não implemente imediatamente.
* Primeiro leia toda a documentação.
* Depois apresente o plano completo.
* Aguarde minha aprovação.
* Somente depois implemente passo a passo.
* Ao finalizar **cada fase**, atualize obrigatoriamente `docs/backup_implementation.md`.
* Explique cada decisão técnica tomada.
* Sempre priorize simplicidade, segurança, baixo custo e facilidade de manutenção.
* A solução deve ser compatível com a infraestrutura atual do projeto e preparada para futuras evoluções sem necessidade de grandes alterações.

O objetivo final não é apenas ter um sistema de backup funcionando, mas também gerar uma documentação técnica de alta qualidade que explique todo o processo de implementação, permitindo que eu estude posteriormente tanto a solução quanto os conceitos envolvidos.

