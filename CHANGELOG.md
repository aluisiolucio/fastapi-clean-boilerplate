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

- Documentação de uso, validação e atualização do template revisada, incluindo
  o uso de caminho absoluto em cópias locais para não quebrar `copier update`.
- Dependências e tarefas Poe alinhadas entre as variantes sync e async.
