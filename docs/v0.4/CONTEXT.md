# Voa Radar v0.4 — Contexto

## 1. Onde estamos

v0.3.0 está consolidada: Price Intelligence (score, classificação, confiança) rodando contra o Supabase real, RLS habilitado nas 6 tabelas existentes (5 de negócio + `alembic_version`), 44/44 testes passando, auditoria formal das "5 falhas de vibe coding" concluída sem pendência crítica em aberto. Existem 2 commits de segurança (`b36e624`, `a7c698b`) que entraram depois da tag `v0.3.0` — `v0.3.1` ainda não foi cortada (pendência conhecida, não bloqueia a v0.4).

Ainda não existe: autenticação, conceito de usuário dono de dado, qualquer forma de monitoramento contínuo, ou notificação.

## 2. Evolução do produto

```
v0.1  Fundação
v0.2  Para onde posso viajar?      (exploração por orçamento)
v0.3  Esse preço é bom?            (inteligência de preço)
v0.4  Avise-me quando aparecer uma oportunidade.   (monitoramento pessoal)
```

## 3. O que a v0.4 é

A v0.4 introduz o conceito de **Radar**: o usuário salva um critério de vigilância (origem, destino, condição de disparo) e o sistema passa a avaliar automaticamente cada novo dado de preço contra os Radares ativos, gerando uma notificação quando a condição é atingida.

Não é "criar um alerta" — é um produto com identidade própria: **"Meu Radar Recife"**, não "Alerta #1".

## 4. Por que isso exige autenticação

Um Radar pertence a alguém. Sem usuário dono, "meus Radares" não existe, e a RLS que acabamos de auditorar na v0.3 (`docs/v0.3/AUDIT_SECURITY.md`) não tem o que proteger de forma diferenciada. A auth entra na v0.4 não como funcionalidade nova isolada, mas como pré-requisito estrutural do Radar — ver `docs/v0.4/DECISIONS.md` DEC-101.

## 5. O que a v0.4 explicitamente não é

- Não é o motor de coleta automática de preços reais (isso é v0.5+, quando um provider real for integrado).
- Não é canal de notificação externo (e-mail/push/WhatsApp/Telegram ficam fora — só central in-app).
- Não suporta "qualquer destino" no release inicial (v0.4.0) — só origem + destino específico.
- Não é uma plataforma de usuários completa — só o mínimo pra um Radar ter dono: cadastro, login, logout, sessão.

## 6. Documentos desta versão

`PRD.md`, `UX.md`, `ARCHITECTURE.md`, `DATA_MODEL.md`, `RADAR_ENGINE.md`, `ALERT_RULES.md`, `NOTIFICATIONS.md`, `SECURITY.md`, `ROADMAP.md`, `DECISIONS.md`. `IMPLEMENTATION.md` e `ACCEPTANCE.md` só são criados quando a fase de código começar (FASE 5 em diante) — este pacote cobre as FASE 0–4 (definição), ainda sem código.
