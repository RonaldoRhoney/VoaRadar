"""profiles.role + trigger que cria o profile e promove rhoneyinc@gmail.com

Skill RhoneyInc `admin-padrao`: rhoneyinc@gmail.com é sempre admin em
todo produto com conceito de admin, promovido automaticamente, nunca
por passo manual. O trigger em `auth.users` também resolve um problema
que o login social (Google, em preparação) ia criar: hoje quem cria a
linha em `profiles` é o endpoint /auth/signup do backend, mas um
cadastro via OAuth nunca passa por ali — o trigger cobre os dois
caminhos de uma vez, mesma referência já usada no hub RhoneyInc
(`RhoneyInc/schema.sql`, função `handle_new_user()`).

Revision ID: 0011
Revises: 0010
Create Date: 2026-08-14
"""

from alembic import op

revision = "0011"
down_revision = "0010"
branch_labels = None
depends_on = None

ADMIN_EMAIL = "rhoneyinc@gmail.com"


def upgrade() -> None:
    op.execute("ALTER TABLE profiles ADD COLUMN role text NOT NULL DEFAULT 'user'")
    op.execute("ALTER TABLE profiles ADD CONSTRAINT ck_profile_role CHECK (role IN ('user', 'admin'))")

    op.execute(
        f"""
        CREATE OR REPLACE FUNCTION public.handle_new_user()
        RETURNS trigger
        LANGUAGE plpgsql
        SECURITY DEFINER
        SET search_path = public
        AS $$
        BEGIN
          INSERT INTO public.profiles (id, role)
          VALUES (NEW.id, CASE WHEN NEW.email = '{ADMIN_EMAIL}' THEN 'admin' ELSE 'user' END)
          ON CONFLICT (id) DO NOTHING;
          RETURN NEW;
        END;
        $$
        """
    )
    op.execute(
        """
        CREATE TRIGGER on_auth_user_created
          AFTER INSERT ON auth.users
          FOR EACH ROW EXECUTE FUNCTION public.handle_new_user()
        """
    )

    # Promoção retroativa, caso a conta já exista de um cadastro anterior.
    op.execute(
        f"""
        UPDATE profiles SET role = 'admin'
        WHERE id = (SELECT id FROM auth.users WHERE email = '{ADMIN_EMAIL}')
        """
    )


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users")
    op.execute("DROP FUNCTION IF EXISTS public.handle_new_user()")
    op.execute("ALTER TABLE profiles DROP CONSTRAINT ck_profile_role")
    op.execute("ALTER TABLE profiles DROP COLUMN role")
