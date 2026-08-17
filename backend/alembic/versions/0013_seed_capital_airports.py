"""seed capital airports (todas origens/destinos na criação de Radar)

Até aqui `airports` só tinha os 5 aeroportos que apareciam no mock de
Explore (BEL/REC/FOR/BSB/SSA) — o formulário de criação de Radar ficava
artificialmente limitado a eles, mesmo sem nenhuma razão técnica pra isso
(o seletor já lista tudo que existe na tabela, `app/api/airports.py`).

Popula as 27 capitais brasileiras (código IATA — dado estável e público,
não algo com risco de "schema não documentado" como o caso da ANAC) —
não o Brasil inteiro (300+ aeródromos, a maioria sem voo comercial
regular), pra não inflar o seletor com aeroporto que ninguém usa de
verdade. `ON CONFLICT (code) DO NOTHING` — idempotente, não duplica os 5
que já existem.

Revision ID: 0013
Revises: 0012
Create Date: 2026-08-17
"""

import uuid

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0013"
down_revision = "0012"
branch_labels = None
depends_on = None

# code, name (nome popular, mesmo padrão dos 5 já existentes), city
_CAPITAL_AIRPORTS = [
    ("RBR", "Plácido de Castro", "Rio Branco"),
    ("MCZ", "Zumbi dos Palmares", "Maceió"),
    ("MCP", "Macapá", "Macapá"),
    ("MAO", "Eduardo Gomes", "Manaus"),
    ("VIX", "Eurico de Aguiar Salles", "Vitória"),
    ("GYN", "Santa Genoveva", "Goiânia"),
    ("SLZ", "Marechal Cunha Machado", "São Luís"),
    ("CGB", "Marechal Rondon", "Cuiabá"),
    ("CGR", "Campo Grande", "Campo Grande"),
    ("CNF", "Tancredo Neves", "Belo Horizonte"),
    ("JPA", "Presidente Castro Pinto", "João Pessoa"),
    ("CWB", "Afonso Pena", "Curitiba"),
    ("THE", "Senador Petrônio Portella", "Teresina"),
    ("GIG", "Galeão", "Rio de Janeiro"),
    ("NAT", "Governador Aluízio Alves", "Natal"),
    ("POA", "Salgado Filho", "Porto Alegre"),
    ("PVH", "Porto Velho", "Porto Velho"),
    ("BVB", "Atlas Brasil Cantanhede", "Boa Vista"),
    ("FLN", "Hercílio Luz", "Florianópolis"),
    ("GRU", "Guarulhos", "São Paulo"),
    ("AJU", "Santa Maria", "Aracaju"),
    ("PMW", "Brigadeiro Lysias Rodrigues", "Palmas"),
]

airports_table = sa.table(
    "airports",
    sa.column("id", postgresql.UUID(as_uuid=True)),
    sa.column("code", sa.String),
    sa.column("name", sa.String),
    sa.column("city", sa.String),
    sa.column("country", sa.String),
    sa.column("created_at", sa.DateTime(timezone=True)),
)


def upgrade() -> None:
    conn = op.get_bind()
    for code, name, city in _CAPITAL_AIRPORTS:
        conn.execute(
            postgresql.insert(airports_table)
            .values(id=str(uuid.uuid4()), code=code, name=name, city=city, country="Brasil", created_at=sa.func.now())
            .on_conflict_do_nothing(index_elements=["code"])
        )


def downgrade() -> None:
    conn = op.get_bind()
    codes = [code for code, _, _ in _CAPITAL_AIRPORTS]
    conn.execute(airports_table.delete().where(airports_table.c.code.in_(codes)))
