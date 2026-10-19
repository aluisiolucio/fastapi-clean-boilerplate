# Changelog

Todas as mudanças relevantes deste template são documentadas neste arquivo.

O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/)
e o versionamento segue [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [Não lançado]

### Adicionado

- Geração de `.copier-answers.yml` pelo template, permitindo `copier update`
  nos projetos criados.
- Validação de `SECRET_KEY` com no mínimo 32 caracteres.
- `CommitRequiredError` para erros de domínio que precisam persistir alterações
  antes de propagar, com teste de regressão do reuso de refresh token.
- Licença Apache-2.0 completa, selecionável via `license`, declarada no
  `pyproject.toml` e incluída na imagem Docker.
- CRUD inicial configurável em tempo de cópia: `include_crud`, `resource_name`,
  `resource_plural` e `resource_fields`, com validação de nomes, tipos, campos
  reservados e limites de tamanho.
- Tipos suportados no CRUD v1: `str`, `text`, `int`, `float`, `bool`, `datetime`
  e `uuid`; `required` e `max_length` (apenas strings) por campo.
- `include_crud=false` gera o projeto apenas com auth, health e infraestrutura
  compartilhada, sem entidade, use cases, rota, tabela ou testes de CRUD.
- `PATCH` parcial com `model_dump(exclude_unset=True)`: campo omitido não muda,
  opcional aceita `null` e obrigatório com `null` retorna 422.

### Corrigido

- Reuso de refresh token agora revoga toda a família e persiste a revogação
  mesmo quando a exceção é propagada.
- Logout de refresh token já revogado deixa de ser tratado como reuso.
- Nome de item em branco ou composto apenas por espaços retorna erro de
  validação (422) em vez de erro interno (500).
- Modo assíncrono instala `greenlet` via `sqlalchemy[asyncio]`.
- Substituição de `httpx` por `httpx2`, eliminando o aviso de depreciação do
  Starlette.
- Configuração do Alembic atualizada de `version_path_separator` para
  `path_separator`.
- Import de testcontainers atualizado para `testcontainers.community.postgres`.
- Tarefas `test-unit` e `test-integration` não aplicam mais o limite de
  cobertura; a cobertura mínima de 80% fica restrita a `poe test`.
- Ajustes de whitespace nos templates Jinja para lint e formatação das duas
  variantes.
- `SECRET_KEY` do `docker-compose.yml` ajustada ao mínimo de 32 caracteres.

### Alterado

- CRUD deixou de ser fixo em `Item`: os arquivos, classes, rotas e tabelas agora são
  gerados a partir de `resource_name`, `resource_plural` e `resource_fields`,
  preservando `Item`/`items` como default.
- Campos opcionais de string passam a gerar `str | None` no domínio e no schema de
  resposta (antes, string opcional era tratada sem `None`).
- Documentação de uso, validação e atualização do template revisada, incluindo
  o uso de caminho absoluto em cópias locais para não quebrar `copier update`.
- Dependências e tarefas Poe alinhadas entre as variantes sync e async.
