"""empty message

Revision ID: 6d0b295636b7
Revises: 
Create Date: 2024-06-08 22:38:01.774775

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6d0b295636b7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('nauczyciele')
    op.drop_table('oplaty')
    op.drop_table('kategorie')
    op.drop_table('kursy')
    op.drop_table('wykladowcy')
    op.drop_table('wyplaty')
    op.drop_table('kursykategorie')
    op.drop_table('klienci')
    op.drop_table('uczestnicy')
    op.drop_table('udzialy')
    op.drop_table('moon_phases')
    op.drop_table('nowyjork')
    op.drop_table('zamowienia')
    op.drop_table('przedmioty')
    op.drop_table('towary')
    op.drop_table('Fazy księżyca')
    with op.batch_alter_table('dane_spektroskopowe', schema=None) as batch_op:
        batch_op.add_column(sa.Column('compound_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('ppm', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('hz', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('intensity', sa.Float(), nullable=True))
        batch_op.drop_constraint('fk_zwiazek_id', type_='foreignkey')
        batch_op.create_foreign_key(None, 'zwiazki_chemiczne', ['compound_id'], ['id'])
        batch_op.drop_column('HNMR_ppm')
        batch_op.drop_column('hnmr_hz')
        batch_op.drop_column('warunki_eksp')
        batch_op.drop_column('rozpuszczalnik')
        batch_op.drop_column('widmo')
        batch_op.drop_column('typ_spektroskopii')
        batch_op.drop_column('hnmr_int')
        batch_op.drop_column('zwiazek_id')
        batch_op.drop_column('czestotliwosc_ir')
        batch_op.drop_column('delta_c')
        batch_op.drop_column('intensywnosc_ms')
        batch_op.drop_column('intensywnosc_ir')
        batch_op.drop_column('masa_ms')

    with op.batch_alter_table('zwiazki_chemiczne', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('formula', sa.String(), nullable=True))
        batch_op.drop_column('atomy_p')
        batch_op.drop_column('aromatyczny')
        batch_op.drop_column('atomy_h')
        batch_op.drop_column('struktura_strukturalna')
        batch_op.drop_column('temp_top')
        batch_op.drop_column('temp_wrze')
        batch_op.drop_column('atomy_s')
        batch_op.drop_column('rozpuszczalnik')
        batch_op.drop_column('atomy_j')
        batch_op.drop_column('struktura_3d')
        batch_op.drop_column('gestosc')
        batch_op.drop_column('masa_molowa')
        batch_op.drop_column('atomy_c')
        batch_op.drop_column('sklad_procentowy')
        batch_op.drop_column('atomy_n')
        batch_op.drop_column('referencja')
        batch_op.drop_column('atomy_br')
        batch_op.drop_column('nasycony')
        batch_op.drop_column('struktura_sumaryczna')
        batch_op.drop_column('atomy_cl')
        batch_op.drop_column('atomy_o')
        batch_op.drop_column('nazwa')
        batch_op.drop_column('izomeria')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('zwiazki_chemiczne', schema=None) as batch_op:
        batch_op.add_column(sa.Column('izomeria', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('nazwa', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('atomy_o', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('atomy_cl', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('struktura_sumaryczna', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('nasycony', sa.BOOLEAN(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('atomy_br', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('referencja', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('atomy_n', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('sklad_procentowy', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('atomy_c', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('masa_molowa', sa.NUMERIC(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('gestosc', sa.NUMERIC(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('struktura_3d', postgresql.BYTEA(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('atomy_j', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('rozpuszczalnik', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('atomy_s', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('temp_wrze', sa.NUMERIC(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('temp_top', sa.NUMERIC(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('struktura_strukturalna', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('atomy_h', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('aromatyczny', sa.BOOLEAN(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('atomy_p', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.drop_column('formula')
        batch_op.drop_column('name')

    with op.batch_alter_table('dane_spektroskopowe', schema=None) as batch_op:
        batch_op.add_column(sa.Column('masa_ms', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('intensywnosc_ir', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('intensywnosc_ms', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('delta_c', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('czestotliwosc_ir', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('zwiazek_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('hnmr_int', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('typ_spektroskopii', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('widmo', postgresql.BYTEA(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('rozpuszczalnik', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('warunki_eksp', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('hnmr_hz', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('HNMR_ppm', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('fk_zwiazek_id', 'zwiazki_chemiczne', ['zwiazek_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
        batch_op.drop_column('intensity')
        batch_op.drop_column('hz')
        batch_op.drop_column('ppm')
        batch_op.drop_column('compound_id')

    op.create_table('Fazy księżyca',
    sa.Column('Data', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('Czas', postgresql.ARRAY(postgresql.TIME()), autoincrement=False, nullable=True),
    sa.Column('Faza [%]', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('Etap cyklu [dni]', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('Promień [arcsec]', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('Odległość [km]', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('Kąt położenia [°]', sa.NUMERIC(), autoincrement=False, nullable=True)
    )
    op.create_table('towary',
    sa.Column('kod', sa.INTEGER(), server_default=sa.text("nextval('towary_kod_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('nazwa', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('cena', postgresql.MONEY(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('kod', name='towary_pkey'),
    sa.UniqueConstraint('nazwa', name='towary_nazwa_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('przedmioty',
    sa.Column('id_przed', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('nazwa', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('prowadzacy', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('rodzaj', sa.VARCHAR(length=11), server_default=sa.text("'obowiazkowy'::character varying"), autoincrement=False, nullable=True),
    sa.Column('rok_studiow', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.CheckConstraint("rodzaj::text = ANY (ARRAY['obowiazkowy'::character varying, 'obieralny'::character varying]::text[])", name='przedmioty_rodzaj_check'),
    sa.ForeignKeyConstraint(['prowadzacy'], ['nauczyciele.id'], name='przedmioty_prowadzacy_fkey'),
    sa.PrimaryKeyConstraint('id_przed', name='przedmioty_pkey')
    )
    op.create_table('zamowienia',
    sa.Column('id_zam', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('data_zam', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('data_realizacji', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('sztuk', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('klient', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('towar', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['klient'], ['klienci.numer'], name='zamowienia_klient_fkey'),
    sa.ForeignKeyConstraint(['towar'], ['towary.kod'], name='zamowienia_towar_fkey'),
    sa.PrimaryKeyConstraint('id_zam', name='pk_zam_id')
    )
    op.create_table('nowyjork',
    sa.Column('rok', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('temp_f', sa.REAL(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('rok', name='nowyjork_pkey')
    )
    op.create_table('moon_phases',
    sa.Column('time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('radius', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('cycle_stage', sa.NUMERIC(), autoincrement=False, nullable=False),
    sa.Column('distance', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('angle', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('phase', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.CheckConstraint('0::numeric <= phase AND phase <= 100::numeric', name='ck_moon_phase'),
    sa.PrimaryKeyConstraint('time', name='pk_moon_time')
    )
    op.create_table('udzialy',
    sa.Column('uczestnik', sa.CHAR(length=11), autoincrement=False, nullable=False),
    sa.Column('kurs', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('data_udzial', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('status', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('punkty', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.CheckConstraint("status::text = ANY (ARRAY['w toku'::character varying, 'ukonczony'::character varying, 'nieukonczony'::character varying]::text[])", name='ck_udzial_status'),
    sa.ForeignKeyConstraint(['kurs'], ['kursy.id'], name='fk_udzial_kurs'),
    sa.ForeignKeyConstraint(['uczestnik'], ['uczestnicy.pesel'], name='fk_udzial_uczestnik'),
    sa.PrimaryKeyConstraint('uczestnik', 'kurs', name='pk_udzial'),
    postgresql_ignore_search_path=False
    )
    op.create_table('uczestnicy',
    sa.Column('pesel', sa.CHAR(length=11), autoincrement=False, nullable=False),
    sa.Column('imie', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('nazwisko', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('adres', sa.VARCHAR(length=50), server_default=sa.text("'Poznań'::character varying"), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('pesel', name='pk_uczestnicy_pesel'),
    postgresql_ignore_search_path=False
    )
    op.create_table('klienci',
    sa.Column('numer', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('nazwisko', sa.VARCHAR(length=30), autoincrement=False, nullable=False),
    sa.Column('typ', sa.VARCHAR(length=3), autoincrement=False, nullable=True),
    sa.Column('adres', sa.VARCHAR(length=100), server_default=sa.text("'Poznan'::character varying"), autoincrement=False, nullable=True),
    sa.CheckConstraint("nazwisko::text ~~ '[A-Z]%%'::text", name='ck_nazw'),
    sa.CheckConstraint("typ::text = ANY (ARRAY['zwykly'::character varying, 'staly'::character varying, 'premium'::character varying]::text[])", name='klienci_typ_check'),
    sa.PrimaryKeyConstraint('numer', name='pk_klienci_nr')
    )
    op.create_table('kursykategorie',
    sa.Column('kurs', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('kategoria', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['kategoria'], ['kategorie.id'], name='kursykategorie_kategoria_fkey'),
    sa.ForeignKeyConstraint(['kurs'], ['kursy.id'], name='kursykategorie_kurs_fkey'),
    sa.PrimaryKeyConstraint('kurs', 'kategoria', name='pk_kurs_kategoria')
    )
    op.create_table('wyplaty',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('pracownik', sa.VARCHAR(length=10), autoincrement=False, nullable=True),
    sa.Column('data', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('miesiac', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('kwartal', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('rok', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('pensja', sa.REAL(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='wyplaty_pkey')
    )
    op.create_table('wykladowcy',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('nazwisko', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='ok_wykl_id'),
    sa.UniqueConstraint('email', name='wykladowcy_email_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('kursy',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('nazwa', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('liczba_dni', sa.SMALLINT(), autoincrement=False, nullable=True),
    sa.Column('cena', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('wykladowca', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('kontynuacja', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.CheckConstraint('liczba_dni >= 1 AND liczba_dni <= 5', name='ck_kursy_dni'),
    sa.ForeignKeyConstraint(['kontynuacja'], ['kursy.id'], name='fk_kurs_kurs'),
    sa.ForeignKeyConstraint(['wykladowca'], ['wykladowcy.id'], name='fk_kurs_wykl'),
    sa.PrimaryKeyConstraint('id', name='pk_kursy_kod'),
    sa.UniqueConstraint('nazwa', name='uq_kursy_nazwa'),
    postgresql_ignore_search_path=False
    )
    op.create_table('kategorie',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('nazwa', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='kategorie_pkey')
    )
    op.create_table('oplaty',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('numer_raty', sa.SMALLINT(), autoincrement=False, nullable=True),
    sa.Column('uczestnik', sa.CHAR(length=11), autoincrement=False, nullable=True),
    sa.Column('kurs', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('kwota', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['uczestnik', 'kurs'], ['udzialy.uczestnik', 'udzialy.kurs'], name='fk_udzial_uczestnik_kurs'),
    sa.PrimaryKeyConstraint('id', name='oplaty_pkey')
    )
    op.create_table('nauczyciele',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('nazwisko', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('stanowisko', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('dyzur', sa.VARCHAR(length=3), autoincrement=False, nullable=True),
    sa.Column('zarobek', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.CheckConstraint("dyzur::text = ANY (ARRAY['pon'::character varying, 'wt'::character varying, 'sr'::character varying, 'czw'::character varying, 'pt'::character varying]::text[])", name='ck_naucz_dyz'),
    sa.CheckConstraint("nazwisko::text ~~ '[A-Z]%%'::text", name='ck_naucz_nazw'),
    sa.CheckConstraint('zarobek >= 1000::numeric', name='ck_naucz_zarob'),
    sa.PrimaryKeyConstraint('id', name='pk_naucz_id')
    )
    # ### end Alembic commands ###