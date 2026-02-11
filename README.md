# Vylepšený Task Manager

Tento projekt je **vylepšený správce úkolů** napsaný v Pythonu, který ukládá úkoly do MySQL databáze a podporuje operace CRUD (Create, Read, Update, Delete).  

Projekt zahrnuje také **automatizované testy** pomocí `pytest`, které ověřují správnou funkčnost přidávání, aktualizace a odstraňování úkolů.

---

## Funkce aplikace

- **Připojení k MySQL databázi**  
- **Vytvoření tabulky `ukoly`** pokud neexistuje  
- **CRUD operace**:
  - Přidat úkol (název, popis, výchozí stav: "Nezahájeno")  
  - Zobrazit úkoly (filtr: "Nezahájeno", "Probíhá")  
  - Aktualizovat stav úkolu ("Probíhá" / "Hotovo")  
  - Odstranit úkol  
- **Validace vstupů** a ošetření neexistujících ID  
---

## Požadavky

- Python 3.13+
- MySQL server
- `mysql-connector-python`  

```bash
  pip install mysql-connector-python
```
- pytest (pro spuštění testů)
```bash
pip install pytest
```

## Nastavení databáze

Vytvořte hlavní databázi:
```sql
CREATE DATABASE task_manager;
USE task_manager;

CREATE TABLE ukoly (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nazev VARCHAR(255) NOT NULL,
    popis TEXT NOT NULL,
    stav ENUM('Nezahájeno', 'Probíhá', 'Hotovo') DEFAULT 'Nezahájeno',
    datum_vytvoreni TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Vytvořte testovací databázi:
```sql
CREATE DATABASE task_manager_test;
USE task_manager_test;

CREATE TABLE ukoly (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nazev VARCHAR(255) NOT NULL,
    popis TEXT NOT NULL,
    stav ENUM('Nezahájeno', 'Probíhá', 'Hotovo') DEFAULT 'Nezahájeno',
    datum_vytvoreni TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
## Spuštění aplikace

Aktivujte virtuální prostředí:

Windows
```bash
venv\Scripts\activate
```

Spusťte aplikaci:
```bash
python main.py
```

Používejte menu:
```bash
1. Přidat úkol
2. Zobrazit úkoly
3. Aktualizovat úkol
4. Odstranit úkol
5. Ukončit program
```
## Spuštění testů

Ujistěte se, že testovací databáze existuje

Spusťte testy:
```bash
python -m pytest test_task_manager.py -v
```

Všechny testy ověřují správnou funkčnost CRUD operací

Testy pracují s testovací databází a po dokončení se data smažou

## Poznámky

Aplikace je navržena tak, aby logika byla oddělena od UI – umožňuje snadné testování

Testy zahrnují pozitivní i negativní scénáře pro přidání, aktualizaci a odstranění úkolů

Hotové úkoly se nezobrazují v hlavním seznamu úkolů
