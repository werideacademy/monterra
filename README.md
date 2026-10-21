# Monterra Group — sito web

Sito statico (HTML + CSS + JS), nessuna build necessaria. Pronto per GitHub + Vercel.

## Provare in locale

```bash
python3 -m http.server 8080
```
Poi apri http://localhost:8080

## Sostituire le foto

Metti le foto reali in `assets/img/photos/` con questi nomi (formato `.jpg`).
Finché una foto non esiste, il sito mostra automaticamente il segnaposto da `assets/img/placeholders/`.

| File                      | Sezione                              | Formato consigliato |
|---------------------------|--------------------------------------|---------------------|
| `hero.jpg`                | Hero (schermo intero)                | orizzontale, 2400px |
| `territorio.jpg`          | Il territorio è il nostro punto…     | orizzontale, 2400px |
| `service-trail.jpg`       | 01 Trail & Outdoor Infrastructure    | 4:3, 1600px         |
| `service-destination.jpg` | 02 Destination Development           | 4:3, 1600px         |
| `service-events.jpg`      | 03 Events & Experiences              | 4:3, 1600px         |
| `service-consulting.jpg`  | 04 Consulting & Project Development  | 4:3, 1600px         |
| `process.jpg`             | Banda dopo "From terrain to destination" | orizzontale, 2400px |
| `trail-hero.jpg`          | Built to be ridden (schermo intero)  | orizzontale, 2400px |
| `trail-1.jpg`, `trail-2.jpg` | Galleria trail                    | verticale, 1400px   |
| `destination-hero.jpg`    | From trail to destination            | orizzontale, 2400px |
| `destination-1.jpg`       | Un sistema, non una singola infrastruttura | verticale/4:3  |
| `contact.jpg`             | Contatti (sfondo)                    | orizzontale, 2400px |

Consiglio: comprimere le foto (es. squoosh.app) sotto ~400 KB ciascuna.

## Deploy
1. `git init` e push su GitHub.
2. Su Vercel: "Add New Project" → importa il repo → Framework preset: **Other** → Deploy.

## Ottimizzare nuove foto
Gli originali stanno in `_originals/` (esclusa da git). Per creare la versione web (ridimensionata, compressa, senza dati EXIF/GPS):

```bash
swift scripts/optimize.swift "_originals/foto.jpg" assets/img/photos/hero.jpg 2400 0.68
```

Poi genera le versioni WebP responsive (800w, 1600w, originale) usate dal `srcset` in `index.html`:

```bash
python3 scripts/webp.py
```
