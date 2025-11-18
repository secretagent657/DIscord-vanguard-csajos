# Discord Role Checker Bot

## Projekt Leírása
Ez egy Discord bot, amely automatikusan kirúgja azokat a tagokat, akik nem kapnak megadott szerepet a beállított időn belül a szerverhez való csatlakozás után.

## Funkciók
- **Automatikus kick új tagoknál**: Ha egy új tag nem kap "Csajos" vagy "Impostor" szerepet 24 órán belül, a bot kirúgja őket
- **Automatikus rendszeres ellenőrzés**: A bot 5 óránként automatikusan ellenőrzi az ÖSSZES tagot és kirúgja, akiknek nincs szerepe
- **Beállítható várakozási idő**: `!time <percek>` vagy `!settime` paranccsal módosítható (admin jog szükséges)
- **Manuális ellenőrzés**: `!checkall` paranccsal bármikor ellenőrizheted az összes tagot
- **Log channel**: Minden esemény logolásra kerül a megadott csatornába

## Konfiguráció

### Szerepek
A `ROLE_NAMES` listában állíthatod be, mely szerepek számítanak "mentőöv"-nek:
```python
ROLE_NAMES = ["💅Csajos💅", "⚠️IMPOSTOR⚠️", "👀"]
```
Ha valamelyik szerep rajta van egy tagon, nem lesz kirúgva.

### Várakozási idő
Alapértelmezett: 24 óra (86400 másodperc)
```python
WAIT_TIME = 86400
```

### Log csatorna
Állítsd be a csatorna ID-ját:
```python
LOG_CHANNEL_ID = 1434206542131101810
```

## Használat

### Parancsok

#### Slash parancsok (/)
- `/pingg` - Válaszol "Pong!" (mindenki használhatja)
  - Egyszerű teszt parancs, hogy ellenőrizd, fut-e a bot

#### Prefix parancsok (!)
- `!time <percek>` - Várakozási idő módosítása percben (csak admin, bárhol használható)
  - Példa: `!time 10` - 10 perces várakozási idő beállítása
  
- `!settime <mennyiség> <egység>` - Várakozási idő módosítása időegységgel (csak admin, csak kijelölt csatornában)
  - Csak a 1434206542131101810 ID-jú csatornában használható
  - Támogatott egységek: perc, óra, nap, másodperc (magyar és angol variációk is)
  - Példák:
    - `!settime 2 óra` - 2 órás várakozási idő
    - `!settime 30 perc` - 30 perces várakozási idő
    - `!settime 1 nap` - 1 napos várakozási idő

- `!checkall` - Végignézi az összes jelenlegi tagot és kirúgja, akiknek nincs megadott szerepe (csak admin)
  - Nem csak az újonnan érkezőket ellenőrzi, hanem az összes tagot a szerveren
  - Botokat automatikusan kihagyja
  - Részletes összesítést ad a kirúgott/megtartott tagokról
  - ⚠️ FIGYELEM: Ez azonnal kirúgja azokat, akiknek nincs "💅Csajos💅", "⚠️IMPOSTOR⚠️" vagy "👀" szerepe!

## Discord Bot Beállítások
A botnak a következő intenteket kell engedélyezni a Discord Developer Portalon:
- `SERVER MEMBERS INTENT` - tagok követéséhez
- `GUILDS` - szerver információkhoz
- Opcionális: `MESSAGE CONTENT INTENT` a parancsok jobb működéséhez

## Futtatás
A bot automatikusan elindul a "Discord Bot" workflow segítségével.

## Aktuális Állapot
- ✅ Bot sikeresen bejelentkezve
- ⏰ Jelenlegi várakozási idő új tagoknak: 1440 perc (24 óra)
- 🔄 Automatikus ellenőrzés: 5 óránként (minden tag)
- 📋 Log csatorna: 1434206542131101810

## Megjegyzések
- A bot csak akkor tud kirúgni, ha van megfelelő jogosultsága (Kick Members)
- Ha nincs joga, figyelmeztetést küld a log csatornába
- A várakozási idő csak futás közben módosítható, újraindítás után visszaáll az alapértelmezettre
