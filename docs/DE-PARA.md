# De/Para de skills

Três visões: (1) skills do repositório de Matt Pocock para este repositório; (2) skills da v1.2 deste repositório para a v2.0; (3) as dores relatadas e onde cada uma foi resolvida.

Legenda de **Situação**: **Novo** (não existia aqui), **Adaptado** (mesmo papel, reescrito para requisitos), **Renomeado**, **Mantido** (função preservada, conteúdo ampliado), **Sem equivalente** (fora do escopo: este repositório não gera código).

## 1. mattpocock/skills para requirements-skills

| Skill de Matt Pocock | Papel original | Skill aqui | Situação | O que mudou |
| --- | --- | --- | --- | --- |
| `ask-matt` | Roteador de fluxos | `ask-req` | Novo | Além do mapa, **lê o estado dos artefatos** (visão, backlog, Stale, CHG) e recomenda o próximo passo |
| `wayfinder` | Mapa de tickets de decisão para esforços grandes e nebulosos | `wayfinder` | Novo | Destino é visão ou spec; tipos de ticket: research, sketch, grilling, ask, task; resolve decisões e registra DEC; entrega para `create-product-vision` ou `to-spec` |
| `grill-me` | Entrevista implacável, sem estado | `grill-me` | Novo | Mesmo nome. Chama `grilling`; em **modo mudança** termina com análise de impacto (só no chat) |
| `grilling` | Primitiva de entrevista (rodadas, fronteira) | `grilling` | Novo | Tags Confirmed/Proposed/Pending, nunca responde pelo PO, **rodada de impacto** ao alterar item existente |
| `grill-with-docs` | Entrevista que grava glossário e ADRs | `grill-with-docs` | Novo | Chama `grilling` + `domain-modeling`; grava `GLOSSARY.md`, `DECISIONS.md` e `changes/CHG-NNN.md` |
| `domain-modeling` | Linguagem ubíqua e ADRs | `domain-modeling` | Renomeado (era `model-domain`) | Glossário com `_Avoid_` e status; decisões viram linhas DEC |
| `to-spec` | Conversa vira spec | `to-spec` | Novo | Gera `SPEC-NNN` (problema, resultado, histórias candidatas, regras, fora de escopo) |
| `to-tickets` | Spec vira tickets verticais com bloqueios | `split-backlog` | Adaptado | Fatias verticais, arestas **Blocked by**, quiz com o usuário, publica no tracker só com autorização |
| `implement` | Implementa um ticket por contexto limpo | `refine-request` | Adaptado | Refina **uma história** por contexto limpo, conduzindo as skills de escrita e verificação |
| `implement-spec` | Implementa a spec inteira em paralelo | n/a | Sem equivalente | Refinar histórias em paralelo ficou como evolução futura |
| `triage` | Máquina de estados de issues | `triage` | Adaptado | Categorias `new`/`change`; estados `needs-triage`, `needs-info`, `ready-for-refinement`, `ready-for-po`, `out-of-scope`; mudança dispara `impact-analysis` |
| `setup-matt-pocock-skills` | Configura tracker, labels, docs | `setup-requirements-repo` | Mantido | Também grava vocabulário de processo e regras operacionais (uma vez, em vez de 15 vezes) |
| `handoff` | Documento para outra sessão | `handoff` | Adaptado | Inclui passo do fluxo, IDs ativos, DECs abertas e skills sugeridas |
| `wait-what` | "Não entendi, re-explique" | `wait-what` | Adaptado | Linguagem simples no idioma do usuário, com vocabulário do `GLOSSARY.md` |
| `to-questionnaire` | Questionário para quem tem a resposta | `to-questionnaire` | Adaptado | Cita DEC/CAP/US desbloqueados; respostas viram DEC só se o responsável confirmar |
| `research` | Pesquisa em fontes primárias | `research` | Adaptado | Fontes: legislação, contratos, documentação de sistemas existentes |
| `retro` | Melhora o ambiente do agente | `retro` | Adaptado | Foca vocabulário, perguntas repetidas, retrabalho e checks determinísticos |
| `writing-for-agents` | Guia de escrita de skills | `docs/AUTHORING-SKILLS.md` | Adaptado | Vira documento do repositório, não skill |
| `code-review` | Revisão em dois eixos | `review-readiness` | Adaptado (parcial) | Eixos **Standards** (gates) e **Alignment** (visão e decisões); nunca assina pelo PO |
| `tdd` | Red-green-refactor | `design-test-scenarios` | Adaptado (parcial) | Casos de teste derivados de AC, independentes de implementação |
| `prototype` | Protótipo descartável | ticket `sketch` do `wayfinder` | Adaptado (parcial) | Artefato barato para reagir: exemplos, fluxo Mermaid, mock em texto |
| `pr`, `diagnosing-bugs`, `improve-codebase-architecture`, `codebase-design`, `wizard`, `teach` | Código, PR, arquitetura, aprendizado | n/a | Sem equivalente | Fora do foco de elucidação e documentação de requisitos |

## 2. requirements-skills v1.2 para v2.0

| v1.2 | v2.0 | Situação | Observação |
| --- | --- | --- | --- |
| (nenhuma) | `ask-req` | Novo | Roteador |
| (nenhuma) | `wayfinder` | Novo | Esforços grandes e nebulosos |
| (nenhuma) | `grill-me`, `grilling`, `grill-with-docs` | Novo | Antes dependia da skill de Matt; agora o repositório é autossuficiente |
| (nenhuma) | `impact-analysis` | Novo | Análise de impacto de mudanças; gera `CHG-NNN` e marca itens `Stale` |
| (nenhuma) | `to-spec` | Novo | Ponte entre entrevista e histórias |
| (nenhuma) | `triage`, `handoff`, `wait-what`, `to-questionnaire`, `research`, `retro` | Novo | Ver tabela 1 |
| `setup-requirements-repo` | `setup-requirements-repo` | Mantido | Absorve `initialize-requirements`; seeds de configuração dentro da skill |
| `initialize-requirements` | `setup-requirements-repo` | Mesclado | Arquivos de produto são criados sob demanda pela primeira skill que precisa deles |
| `create-product-vision` | `create-product-vision` | Mantido | Usa `grilling` para lacunas; revisão usa `impact-analysis` |
| `review-product-vision` | `review-product-vision` | Mantido | Passa a sugerir próximo passo |
| `refine-request` | `refine-request` | Mantido | Agora por história, em contexto limpo; modo mudança |
| `interview-product-owner` | `grilling` | Mesclado | Rodadas por fronteira com resposta recomendada |
| `model-domain` | `domain-modeling` | Renomeado | |
| `split-backlog` | `split-backlog` | Mantido | Fatias verticais, bloqueios, quiz; passa a ser acionada pelo usuário |
| `write-user-story` | `write-user-story` | Mantido | Modo revisão chama `impact-analysis`; template dentro da skill |
| `specify-requirements` | `specify-requirements` | Mantido | Procedimento detalhado |
| `define-acceptance-criteria` | `define-acceptance-criteria` | Mantido | Locale do Gherkin |
| `design-test-scenarios` | `design-test-scenarios` | Mantido | |
| `diagram-requirements` | `diagram-requirements` | Mantido | |
| `audit-traceability` | `audit-traceability` | Mantido | Novo `scripts/check-ids.py` (checagem determinística) e detecção de `Stale` |
| `review-readiness` | `review-readiness` | Mantido | Gates G1 a G9, incluindo frescor (G7) |

Removidos: adaptadores duplicados `.claude/skills/*` (substituídos por `scripts/install.sh`), o bloco "Shared operating rules" repetido em 15 skills (agora uma vez em `docs/agents/requirements-workflow.md`) e a pasta `templates/` (cada template mora na skill dona).

## 3. Dores relatadas e solução

| Dor | Solução |
| --- | --- |
| 1. Falta algo como `/ask-matt` | `ask-req`: roteador que lê o estado dos artefatos |
| 2. Falta algo como `/wayfinder` | `wayfinder`: mapa de tickets de decisão, com névoa e destino |
| 3. As skills não se conhecem | Toda skill termina em `## Next steps` com `➡️ Next step`; `ask-req` lista todas; o validador impede referência para skill inexistente e chamada de skill manual por outra skill |
| 4. Falta fluxo bem definido | Fluxo principal, on-ramps e fluxo de mudança em `docs/FLOW.md` e no README; máquina de estados da história; regras de fronteira de fase |
| 5. Alterar HU não gera análise de impacto | `impact-analysis` + **modo mudança** do `grilling` (rodada final de impacto, também em `/grill-me`); `write-user-story`, `specify-requirements`, `define-acceptance-criteria` e `design-test-scenarios` chamam a análise antes de editar; `CHG-NNN` e status `Stale` bloqueiam a prontidão |

## Aviso sobre colisão de nomes

Os nomes `grill-me`, `grilling`, `grill-with-docs`, `wayfinder`, `triage`, `to-spec`, `handoff`, `wait-what`, `to-questionnaire`, `research`, `retro` e `domain-modeling` coincidem de propósito com os de Matt Pocock. Se os dois repositórios estiverem instalados no mesmo agente, mantenha **uma** cópia de cada nome (aqui as versões são supersets para requisitos). Para convivência, use a invocação com namespace do seu agente, ou instale só um conjunto por projeto.
