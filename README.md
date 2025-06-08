# 📝 Real-time Notepad

Üdvözöllek a Real-time Notepad projektben! Ez az alkalmazás azért született, hogy a jegyzetelés ne csak egyszerű, hanem élmény is legyen – akár egyedül, akár barátokkal, kollégákkal vagy tanulótársakkal használod.

Képzeld el, hogy egy közös jegyzetfüzetben dolgozhattok, ahol mindenki látja a másik gondolatait, ötleteit, és minden változás azonnal megjelenik mindenkinek. Nem kell többé e-mailben küldözgetni a jegyzeteket vagy aggódni, hogy elveszik valami – minden automatikusan mentődik, és bármikor visszatérhetsz a korábbi jegyzeteidhez.

A Real-time Notepad célja, hogy a közös munka gördülékeny, gyors és örömteli legyen. Legyen szó tanulásról, brainstormingról vagy csak egy egyszerű bevásárlólistáról, ez az eszköz segít, hogy mindenki ugyanazt lássa, és mindenki hozzá tudjon tenni valamit.

## ✨ Miért fogod szeretni?

- **Valós idejű szinkronizáció** – Amit írsz, azonnal megjelenik mindenkinél.
- **Automatikus mentés** – Nem kell aggódnod, hogy elveszik a munkád.
- **Jegyzetek elmentése és visszatöltése** – Bármikor visszanézheted vagy újra felhasználhatod a régi ötleteidet.
- **Keresés** – Gyorsan megtalálod, amit keresel.
- **Reszponzív, modern felület** – Akár telefonon, akár gépen használod, mindig kényelmes.
- **Sötét mód** – Kíméli a szemed, ha este dolgozol.
- **Valós idejű statisztikák** – Látod, mennyit írtál, hányan vagytok, mikor mentettél utoljára.

Ez a projekt nem csak egy technológiai megoldás, hanem egy közösségi élmény. Próbáld ki, vond be a barátaidat, és tapasztald meg, milyen egyszerű és szórakoztató lehet a közös jegyzetelés!

![Python](https://img.shields.io/badge/Python-3.7+-blue?style=flat-square)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green?style=flat-square)
![SocketIO](https://img.shields.io/badge/SocketIO-5.3.6-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

## ✨ Jellemzők

### 🚀 Fő funkciók
- **Valós idejű szinkronizáció** - Minden változás azonnal megjelenik az összes csatlakozott eszközön
- **Automatikus mentés** - A tartalom automatikusan mentődik JSON formátumban
- **Mentett jegyzetek kezelése** - Jegyzetek mentése megadott névvel, betöltése és törlése
- **Aktív felhasználók számlálása** - Valós idejű statisztika a csatlakozott felhasználókról
- **Keresés** - Mentett jegyzetek között való keresés
- **Reszponzív design** - Működik asztali és mobil eszközökön egyaránt

### 🎨 Felhasználói élmény
- **Classless CSS** - Modern, tiszta megjelenés framework nélkül
- **Dark mode támogatás** - Automatikus sötét mód detektálás
- **Valós idejű statisztikák** - Karakterek, szavak, sorok száma
- **Toast üzenetek** - Felhasználóbarát visszajelzések
- **Modal ablakok** - Elegáns jegyzet mentési felület

### 🔧 Technikai jellemzők
- **WebSocket kommunikáció** - Flask-SocketIO alapú real-time kapcsolat
- **Session kezelés** - Intelligens felhasználó nyomonkövetés
- **JSON adattárolás** - Egyszerű, fájl alapú adatmegőrzés
- **Thread-safe műveletek** - Biztonságos párhuzamos hozzáférés
- **Automatikus session tisztítás** - Memóriaszivárgás megelőzése

## 🛠️ Telepítés

### Előfeltételek
- Python 3.7 vagy újabb
- pip package manager

### 1. Klónozás és navigálás
```bash
git clone https://github.com/vnorman1/real-time-notepad--.git
cd real-time-notepad
```

### 2. Virtuális környezet létrehozása
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Függőségek telepítése
```bash
pip install -r requirements.txt
```

### 4. Alkalmazás indítása
```bash
python app.py
```

Az alkalmazás elérhető lesz a `http://localhost:5000` címen.

## 📋 Használat

### Alapvető használat
1. **Nyisd meg a böngészőt** és navigálj a `http://localhost:5000` címre
2. **Kezdj el írni** - a változások automatikusan szinkronizálódnak
3. **Nyisd meg ugyanazt a címet több eszközön** - láthatod a valós idejű szinkronizációt

### Jegyzetek kezelése
- **Mentés**: Kattints a "💾 Mentés másként" gombra és adj meg egy címet
- **Betöltés**: Kattints egy mentett jegyzetre a listában
- **Törlés**: Használd a "🗑️" gombot a mentett jegyzeteknél
- **Keresés**: Írd be a keresett szöveget a keresőmezőbe

### Statisztikák
A jobb oldali panelen valós időben láthatod:
- Karakterek száma
- Szavak száma  
- Sorok száma
- Aktív felhasználók száma
- Utolsó mentés időpontja

## 🏗️ Projekt struktúra

```
real-time-notepad/
├── app.py                 # Fő Flask alkalmazás
├── requirements.txt       # Python függőségek
├── notes.json            # Aktuális jegyzet tárolása
├── saved_notes.json      # Mentett jegyzetek
├── templates/
│   └── index.html        # Frontend HTML/CSS/JS
└── README.md             # Projektdokumentáció
```

## 🔧 Konfiguráció

### Környezeti változók
Az alkalmazás a következő beállításokat használja:

```python
# app.py
HOST = '0.0.0.0'          # Szerver címe (minden interfészen)
PORT = 5000               # Port szám
DEBUG = True              # Debug mód (fejlesztéshez)
SECRET_KEY = 'notepad-secret-key-2025'  # Flask secret key
```

### Fájlok
- `notes.json` - Az aktuális jegyzet tartalma és session adatok
- `saved_notes.json` - A mentett jegyzetek listája

## 🌐 API Dokumentáció

### WebSocket Events

#### Kliens → Szerver
| Event | Paraméterek | Leírás |
|-------|-------------|--------|
| `content_change` | `{content: string}` | Szöveg változás küldése |
| `save_note_as` | `{title: string, content: string}` | Jegyzet mentése névvel |
| `load_saved_note` | `{id: number}` | Mentett jegyzet betöltése |
| `delete_saved_note` | `{id: number}` | Mentett jegyzet törlése |
| `search_saved_notes` | `{query: string}` | Keresés mentett jegyzetek között |
| `get_saved_notes` | - | Mentett jegyzetek lekérése |
| `get_stats` | - | Statisztikák lekérése |

#### Szerver → Kliens
| Event | Adatok | Leírás |
|-------|--------|--------|
| `content_update` | `{content: string, last_modified: string}` | Szöveg frissítés |
| `user_count` | `{count: number}` | Aktív felhasználók száma |
| `saved_notes_update` | `{notes: array}` | Mentett jegyzetek frissítése |
| `stats_update` | `{characters, words, lines, ...}` | Statisztikák frissítése |
| `save_success` | `{message: string}` | Sikeres művelet visszajelzés |
| `error` | `{message: string}` | Hibaüzenet |

## 🚦 Fejlesztés

### Fejlesztői környezet indítása
```bash
# Debug módban (automatikus újraindítás)
python app.py

# Vagy Flask fejlesztői szerverrel
set FLASK_APP=app.py
set FLASK_ENV=development
flask run
```

### Kód struktúra
- **Backend**: Flask + SocketIO (Python)
- **Frontend**: Vanilla JavaScript + CSS Variables
- **Adattárolás**: JSON fájlok
- **Kommunikáció**: WebSocket (Socket.IO)

### Stílus irányelvek
- Clean Code elvek alkalmazása
- Kommentált kód magyar nyelven
- Reszponzív design first
- Progresszív fejlesztés (PE)

## 🔒 Biztonság

### Implementált biztonsági intézkedések
- **CORS védelem** - Engedélyezett origin-ek kezelése
- **Session tisztítás** - Automatikus régi session-ök törlése  
- **Input validáció** - Felhasználói adatok ellenőrzése
- **File lock** - Thread-safe fájl műveletek
- **Memory management** - Session limit és időalapú cleanup

### Ajánlott biztonsági lépések produkciós környezetben
- HTTPS használata
- Erős SECRET_KEY beállítása
- Rate limiting implementálása
- Input szanitizálás bővítése
- Autentikáció hozzáadása

## 🐛 Hibakeresés

### Gyakori problémák

**A felhasználók száma rosszul jelenik meg**
```bash
# Megoldás: Restart az alkalmazás és session tisztítás
python app.py
```

**WebSocket kapcsolat hibák**
```bash
# Ellenőrizd a port foglaltságot
netstat -an | findstr 5000

# Módosítsd a portot az app.py-ban ha szükséges
```

**JSON fájl hibák**
```bash
# Töröld a korrupt fájlokat - újra létrejönnek
del notes.json saved_notes.json
```

### Logolás
Az alkalmazás konzolon keresztül logol. Debug információkért állítsd be:
```python
DEBUG = True  # app.py-ban
```

## 🤝 Közreműködés

1. **Fork** a projektet
2. **Branch** létrehozása: `git checkout -b feature/amazing-feature`
3. **Commit** változások: `git commit -m 'Add some amazing feature'`
4. **Push** a branch-re: `git push origin feature/amazing-feature`
5. **Pull Request** nyitása

## 📝 Changelog

### v1.0.0 (2025-06-03)
- ✨ Kezdeti verzió
- 🚀 Real-time szinkronizáció
- 💾 Jegyzetek mentése/betöltése/törlése
- 🔍 Keresés funkció
- 📊 Valós idejű statisztikák
- 🎨 Reszponzív UI

## 👥 Szerzők

- **Norman** - *Kezdeti munka* - [GitHub](https://github.com/vnorman1)

