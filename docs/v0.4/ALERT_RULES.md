# Voa Radar v0.4 — Regras de disparo e deduplicação

## 1. Condições de disparo (v0.4.0)

| Tipo | Regra | Exemplo |
|---|---|---|
| `PRICE_BELOW` | `preço_atual < condition_price` | "Avisar quando ficar abaixo de R$ 500" |
| `OPPORTUNITY_CLASSIFICATION` | `classification == condition_classification` (v0.4.0 só oferece `EXCELLENT`) | "Avisar quando for Excelente oportunidade" |

Um Radar tem exatamente uma condição ativa por vez — ver `DECISIONS.md` DEC-102 para o motivo de "por preço" e "por orçamento" terem sido unificados num único `PRICE_BELOW`.

## 2. Deduplicação / cooldown

**Decisão confirmada pelo usuário**: um Radar não gera nova notificação para o mesmo tipo de oportunidade dentro de **24 horas**, a menos que o novo preço seja pelo menos **5% menor** que o preço do último evento notificado daquele Radar.

```python
def should_notify(radar: RadarRow, new_price: float, now: datetime) -> bool:
    if radar.last_event_at is None:
        return True
    cooldown_expired = (now - radar.last_event_at) > timedelta(hours=24)
    meaningful_drop = radar.last_event_price is not None and new_price < radar.last_event_price * 0.95
    return cooldown_expired or meaningful_drop
```

- `radar_event` **sempre** é gravado quando o motor detecta um match (log de auditoria completo, `DATA_MODEL.md` §4), independente do cooldown.
- `notification` só é criada quando `should_notify` é verdadeiro.
- `radars.last_event_price`/`last_event_at` são atualizados a cada `radar_event` gravado (não só quando notifica) — assim o cooldown sempre compara contra o evento mais recente, não só contra a última notificação.

## 3. Por que 24h / 5%

Valor escolhido para equilibrar dois riscos: notificar demais (parecer spam, usuário desativa o Radar) e notificar de menos (perder uma queda real por estar "esperando" o cooldown acabar). Ambos os números são parâmetros de produto — revisáveis com dado real de uso, não uma verdade fixa. Se, depois de uso real, o cooldown se mostrar muito agressivo ou muito frouxo, é ajuste de configuração, não mudança de arquitetura.

## 4. Casos de borda

- **Radar recém-criado** (`last_event_at IS NULL`): primeira ocorrência sempre notifica.
- **Radar pausado**: nunca avaliado pelo engine — Radares `PAUSED` são excluídos da própria query de busca de candidatos (`ARCHITECTURE.md` §6), não filtrados depois.
- **Radar excluído no meio de uma avaliação em andamento**: fora de escopo de race condition para o MVP (avaliação é síncrona dentro do mesmo request de coleta, volume baixo) — sinalizar como risco aceito, não resolver preventivamente.
