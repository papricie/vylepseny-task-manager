import pytest
from main import pripojeni_db, pridat_ukol, aktualizovat_ukol, odstranit_ukol, zobrazit_ukoly

# Fixture pro připojení k testovací DB
@pytest.fixture
def connection():
    # připojení k testovací DB
    conn = pripojeni_db()
    conn.database = "task_manager_test"  # přepíšeme DB
    yield conn
    # Smazat všechna testovací data po každém testu
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ukoly;")
    conn.commit()
    conn.close()

# ----------------------------
# Testy pro pridat_ukol
# ----------------------------

def test_pridat_ukol_ok(connection):
    pridat_ukol(connection, "Testovací úkol", "Popis testu")
    cursor = connection.cursor()
    cursor.execute("SELECT nazev, popis FROM ukoly WHERE nazev='Testovací úkol'")
    result = cursor.fetchone()
    assert result == ("Testovací úkol", "Popis testu")

def test_pridat_ukol_nok(connection):
    # Negativní test: prázdný název
    with pytest.raises(ValueError):
        pridat_ukol(connection, "", "Popis testu")

# ----------------------------
# Testy pro aktualizovat_ukol
# ----------------------------

def test_aktualizovat_ukol_ok(connection):
    # Přidáme úkol
    pridat_ukol(connection, "Úkol k update", "Popis")
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM ukoly WHERE nazev='Úkol k update'")
    ukol_id = cursor.fetchone()[0]

    # Aktualizace stavu
    aktualizovat_ukol(connection, ukol_id, "Probíhá")
    cursor.execute("SELECT stav FROM ukoly WHERE id=%s", (ukol_id,))
    stav = cursor.fetchone()[0]
    assert stav == "Probíhá"

def test_aktualizovat_ukol_nok(connection):
    # Negativní test: neexistující ID
    with pytest.raises(ValueError):
        aktualizovat_ukol(connection, 9999, "Hotovo")

# ----------------------------
# Testy pro odstranit_ukol
# ----------------------------

def test_odstranit_ukol_ok(connection):
    # Přidáme úkol
    pridat_ukol(connection, "Úkol k smazání", "Popis")
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM ukoly WHERE nazev='Úkol k smazání'")
    ukol_id = cursor.fetchone()[0]

    # Smazání úkolu
    odstranit_ukol(connection, ukol_id)
    cursor.execute("SELECT * FROM ukoly WHERE id=%s", (ukol_id,))
    result = cursor.fetchone()
    assert result is None

def test_odstranit_ukol_nok(connection):
    # Negativní test: neexistující ID
    with pytest.raises(ValueError):
        odstranit_ukol(connection, 9999)
