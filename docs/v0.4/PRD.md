# Voa Radar v0.4 — PRD (Radar & Alertas)

## 1. Proposta

> "Avise-me quando aparecer uma oportunidade."

O usuário configura um Radar (origem, destino, condição) uma vez, e o Voa Radar passa a vigiar por ele — sem precisar voltar todo dia pra conferir preço manualmente.

## 2. Escopo da v0.4.0 (release inicial)

### 2.1 Identidade (auth mínima)
- Cadastro (e-mail + senha).
- Login / logout.
- Sessão persistida (refresh automático).
- Recuperação de senha ("esqueci minha senha").
- Perfil básico (sem edição de dados além do essencial).

Fora de escopo: OAuth social, 2FA, edição de perfil rica.

### 2.2 Radar
- Criar Radar: nome, origem, destino (obrigatório, sem "qualquer destino" — ver §3), condição de disparo.
- Editar Radar (mesmos campos da criação).
- Ativar / pausar Radar (🟢 ativo / ⚪ pausado).
- Excluir Radar.
- Listar "Meus Radares".

### 2.3 Condição de disparo
Um Radar tem exatamente uma condição, escolhida na criação:
- **Por preço**: avisar quando o preço da rota ficar abaixo de R$ X (cobre tanto "abaixo de um valor fixo" quanto "abaixo do meu orçamento" — são a mesma operação do ponto de vista do motor, ver `DATA_MODEL.md`).
- **Por oportunidade**: avisar quando o Price Intelligence classificar a rota como "Excelente oportunidade" (`classification=EXCELLENT`).

### 2.4 Monitoramento
- Orientado a evento: toda vez que uma nova observação de preço é registrada para uma rota, os Radares ativos daquela rota são avaliados automaticamente (ver `RADAR_ENGINE.md`).
- Não há worker/scheduler novo na v0.4.0 — nenhuma verificação "de tempos em tempos" independente de uma nova observação chegar.

### 2.5 Notificações
- Central de notificações in-app (lista, com lido/não lido).
- Uma notificação por evento de Radar disparado.
- Deduplicação/cooldown (ver `ALERT_RULES.md`) — não repetir a mesma oportunidade sem melhora relevante dentro de 24h.

Fora de escopo da v0.4.0: e-mail, push, Telegram, WhatsApp.

## 3. Fora de escopo (adiado deliberadamente)

| Item | Motivo | Quando |
|---|---|---|
| "Qualquer destino" no Radar | Uma rota por Radar mantém o motor de avaliação barato e previsível; "qualquer destino" multiplica o espaço de comparação e só faz sentido com estratégia de coleta real definida | v0.4.x |
| Origem → região | Passo intermediário entre destino específico e "qualquer destino" | v0.4.x |
| Condições combinadas (preço E classificação) | Hoje um Radar = uma condição; combinar exige `radar_conditions` como tabela própria | Quando houver pedido real |
| Notificação por e-mail/push/WhatsApp/Telegram | Reduzir complexidade inicial — validar o motor de disparo antes de somar canais externos | Depois da v0.4.0 |
| OAuth social, 2FA | Fora do mínimo necessário pra Radar ter dono | Não planejado |

## 4. Fluxo do usuário

```
Login
  ↓
Meus Radares (lista, vazia no início)
  ↓
Criar Radar
  ↓
Origem, destino, condição
  ↓
Ativar Radar
  ↓
(tempo passa, novas observações de preço entram no sistema)
  ↓
Radar dispara → Notificação criada
  ↓
Usuário vê 🔔 na central de notificações
  ↓
Clica → vai pro detalhe da oferta (reaproveita Price Intelligence da v0.3)
```

## 5. Critérios de sucesso (qualitativo, v0.4.0)

- Um usuário consegue criar, editar, pausar e excluir um Radar sem ambiguidade na interface.
- Um Radar ativo realmente dispara quando a condição é satisfeita, e não dispara quando não é (testável de ponta a ponta com dados semeados, como a v0.3 já faz).
- Um usuário nunca vê Radar ou notificação de outro usuário, em nenhuma circunstância (ver `SECURITY.md`).
- Nenhuma notificação duplicada para a mesma oportunidade dentro da janela de cooldown.
