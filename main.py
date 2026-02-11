import mysql.connector
from mysql.connector import Error

def pripojeni_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="cvbnm",
            database="task_manager"
        )
        if connection.is_connected():
            print("Připojeno k databázi")
            return connection
    except Error as e:
        print("Chyba při připojení k databázi:", e)
        return None


def vytvoreni_tabulky(connection):
    try:
        cursor = connection.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS ukoly (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nazev VARCHAR(255) NOT NULL,
            popis TEXT NOT NULL,
            stav ENUM('Nezahájeno', 'Probíhá', 'Hotovo') DEFAULT 'Nezahájeno',
            datum_vytvoreni TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(query)
        connection.commit()
        print("Tabulka ukoly je připravena.")
    except Error as e:
        print("Chyba při vytváření tabulky:", e)


def pridat_ukol(connection, nazev, popis):
    if not nazev or not popis:
        raise ValueError("Název i popis jsou povinné.")

    cursor = connection.cursor()
    query = """
    INSERT INTO ukoly (nazev, popis)
    VALUES (%s, %s)
    """
    cursor.execute(query, (nazev, popis))
    connection.commit()


def pridat_ukol_ui(connection):
    nazev = input("Zadej název úkolu: ").strip()
    popis = input("Zadej popis úkolu: ").strip()

    try:
        pridat_ukol(connection, nazev, popis)
        print("Úkol byl úspěšně přidán.")
    except ValueError as e:
        print(e)

def zobrazit_ukoly(connection):
    cursor = connection.cursor()
    query = """
    SELECT id, nazev, popis, stav
    FROM ukoly
    WHERE stav IN ('Nezahájeno', 'Probíhá')
    """
    cursor.execute(query)
    return cursor.fetchall()

def zobrazit_ukoly_ui(connection):
    ukoly = zobrazit_ukoly(connection)

    if not ukoly:
        print("Žádné úkoly k zobrazení.")
        return

    print("\nSeznam úkolů:")
    for id_, nazev, popis, stav in ukoly:
        print(f"{id_}. {nazev} | {popis} | {stav}")



def aktualizovat_ukol(connection, ukol_id, novy_stav):
    if novy_stav not in ("Probíhá", "Hotovo"):
        raise ValueError("Neplatný stav.")

    cursor = connection.cursor()

    # ověření existence
    cursor.execute("SELECT id FROM ukoly WHERE id = %s", (ukol_id,))
    if cursor.fetchone() is None:
        raise ValueError("Úkol s tímto ID neexistuje.")

    # update
    cursor.execute(
        "UPDATE ukoly SET stav = %s WHERE id = %s",
        (novy_stav, ukol_id)
    )
    connection.commit()


def aktualizovat_ukol_ui(connection):
    ukoly = zobrazit_ukoly(connection)

    if not ukoly:
        print("Žádné úkoly k aktualizaci.")
        return

    print("\nÚkoly:")
    for id_, nazev, _, stav in ukoly:
        print(f"{id_}. {nazev} | {stav}")

    try:
        ukol_id = int(input("Zadej ID úkolu: "))
        novy_stav = input("Nový stav (Probíhá/Hotovo): ").strip()

        aktualizovat_ukol(connection, ukol_id, novy_stav)
        print("Stav úkolu byl aktualizován.")
    except ValueError as e:
        print(e)



def odstranit_ukol(connection, ukol_id):
    cursor = connection.cursor()

    # ověření existence
    cursor.execute("SELECT id FROM ukoly WHERE id = %s", (ukol_id,))
    if cursor.fetchone() is None:
        raise ValueError("Úkol s tímto ID neexistuje.")

    cursor.execute("DELETE FROM ukoly WHERE id = %s", (ukol_id,))
    connection.commit()

def odstranit_ukol_ui(connection):
    ukoly = zobrazit_ukoly(connection)

    if not ukoly:
        print("Žádné úkoly k odstranění.")
        return

    print("\nÚkoly:")
    for id_, nazev, _, stav in ukoly:
        print(f"{id_}. {nazev} | {stav}")

    try:
        ukol_id = int(input("Zadej ID úkolu ke smazání: "))
        odstranit_ukol(connection, ukol_id)
        print("Úkol byl odstraněn.")
    except ValueError as e:
        print(e)


def hlavni_menu():
    conn = pripojeni_db()
    if not conn:
        return

    vytvoreni_tabulky(conn)

    while True:
        print("\n--- Task Manager ---")
        print("1. Přidat úkol")
        print("2. Zobrazit úkoly")
        print("3. Aktualizovat úkol")
        print("4. Odstranit úkol")
        print("5. Ukončit")

        volba = input("Vyber možnost: ")

        if volba == "1":
            pridat_ukol_ui(conn)
        elif volba == "2":
            zobrazit_ukoly_ui(conn)
        elif volba == "3":
            aktualizovat_ukol_ui(conn)
        elif volba == "4":
            odstranit_ukol_ui(conn)
        elif volba == "5":
            print("Konec programu.")
            break
        else:
            print("Neplatná volba.")

if __name__ == "__main__":
    hlavni_menu()


