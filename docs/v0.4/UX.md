# Voa Radar v0.4 — UX

## 1. Novas telas

- **Login / Cadastro** — formulário simples, e-mail + senha, link "esqueci minha senha".
- **Meus Radares** — lista de cards, um por Radar.
- **Criar/Editar Radar** — formulário (nome, origem, destino, condição).
- **Central de notificações** — lista cronológica, não lida em destaque.

## 2. Card de Radar

```
🔵 Meu Radar Recife
Belém → Recife
Até R$ 500

🟢 ATIVO
```

Estado pausado:

```
🟣 Meu Radar Recife
Belém → Recife
Até R$ 500

⚪ PAUSADO
```

Toque no card → editar. Ação secundária (menu/swipe) → pausar/ativar, excluir.

## 3. Empty state (sem Radares ainda)

Mensagem amigável convidando a criar o primeiro Radar a partir de uma busca já feita (reaproveitar contexto de origem/destino se o usuário veio da tela de resultados da v0.2/v0.3), não uma tela em branco genérica.

## 4. Notificação (central in-app)

```
🔥 Nova oportunidade encontrada!

Belém → Recife
R$ 429
31% abaixo da média histórica.

Ver oportunidade
```

Não lida: destaque visual (ponto/cor). Lida: sem destaque. Clique marca como lida e leva pro detalhe da oferta (mesma tela de Price Intelligence da v0.3).

## 5. Badge de contagem

Ícone de sino no header com contador de não lidas, visível em qualquer tela autenticada — consistente com o padrão de header já usado no resto do produto.

## 6. Estados

- **Loading**: skeleton, mesmo padrão visual já usado no Price Intelligence (v0.3 DEC — animate-pulse).
- **Empty**: "Você ainda não tem Radares ativos" / "Nenhuma notificação ainda" — nunca tela em branco sem explicação.
- **Erro**: mensagem amigável, nunca erro técnico cru (CLAUDE.md §15).
- **Radar pausado**: visualmente distinto (opacidade reduzida ou cor neutra), deixa claro que não está vigiando sem parecer quebrado.

## 7. Mobile-first

Todas as telas novas seguem o mesmo padrão responsivo já validado na v0.2/v0.3 (390px mobile, 1280px desktop).

## 8. Linguagem

Nunca "Alerta". Sempre "Radar". Ex.: "Criar Radar", "Meus Radares", "Radar ativo", nunca "criar alerta" — decisão de identidade de produto (`DECISIONS.md` DEC-100).
