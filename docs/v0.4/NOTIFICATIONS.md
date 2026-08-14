# Voa Radar v0.4 — Notificações

## 1. Escopo v0.4.0

Só central de notificações **in-app**. E-mail, push, Telegram e WhatsApp ficam explicitamente fora — ver `PRD.md` §3.

## 2. Ciclo de vida

```
RadarEvaluationService detecta match + passa no cooldown (ALERT_RULES.md)
        ↓
notification criada (read_at = NULL)
        ↓
Usuário abre a central → GET /notifications
        ↓
Usuário clica na notificação → marca read_at = now() → navega pro detalhe da oferta
```

Não existe exclusão de notificação na v0.4.0 — só lida/não lida. Excluir é melhoria futura, registrar se pedido.

## 3. Conteúdo

```
type: OPPORTUNITY_FOUND
title: "Nova oportunidade encontrada!"
message: "Belém → Recife, R$ 429, 31% abaixo da média histórica."
```

`title`/`message` são montados pelo backend no momento da criação (não recalculados na leitura) — texto congela o contexto do momento do disparo, mesmo que o preço mude depois. Consistente com `radar_events` sendo um log imutável (`DATA_MODEL.md` §4).

## 4. API

- `GET /notifications` — lista as do usuário autenticado, mais recentes primeiro.
- `PATCH /notifications/{id}/read` — marca como lida. 404 se não pertence ao usuário (nunca 403 — ver `SECURITY.md` §4).
- Contagem de não lidas: campo derivado na resposta da lista, ou endpoint próprio `GET /notifications/unread-count` — decidir na fase de implementação conforme necessidade real do frontend (não antecipar).

## 5. Relação com Radar Events

Uma `notification` sempre referencia o `radar_event` que a originou (`DATA_MODEL.md` §5) — o vínculo existe para permitir, no futuro, que um mesmo evento gere notificações em múltiplos canais sem duplicar a lógica de "o que aconteceu". Na v0.4.0 a relação é 1:1 na prática (só existe o canal in-app).
