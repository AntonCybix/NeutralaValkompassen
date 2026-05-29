# Valkompass 2026 – neutral & anonym

En källbaserad, anonym valkompass för Sveriges åtta riksdagspartier inför valet 2026.
Hela appen är **en enda statisk fil** ([`index.html`](index.html)) utan byggsteg eller beroenden.

- **Anonymt:** inga partinamn, färger eller logotyper syns medan du svarar.
- **Källbaserat:** alla positioner är kodade ur partiernas eget publicerade 2026-material.
- **Rättvist:** saknad position straffar inte, frågorna lottas och visas i slumpad ordning.

## Köra lokalt

```bash
./host.sh          # startar på http://localhost:8000
./host.sh 3000     # valfri port
```
…eller öppna `index.html` direkt i en webbläsare.

## Bygga om datan

Frågebanken och partipositionerna ligger i [`build_data.py`](build_data.py); själva sidan
genereras av [`generate.py`](generate.py).

```bash
python3 build_data.py   # läser valkompass_riksdagspartier_2026.json -> distilled.json
python3 generate.py     # bäddar in datan -> index.html
```

## Testdeploy till GitHub Pages

Repot har ett färdigt GitHub Actions-workflow ([`.github/workflows/pages.yml`](.github/workflows/pages.yml))
som publicerar repo-roten till Pages vid varje push till `main`.

1. Skapa ett tomt repo på GitHub (t.ex. `Valkompass`).
2. Koppla på och pusha:
   ```bash
   git remote add origin https://github.com/<användarnamn>/Valkompass.git
   git push -u origin main
   ```
3. På GitHub: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
4. Sidan publiceras på `https://<användarnamn>.github.io/Valkompass/`.

Varje ny push till `main` deployar om automatiskt.
