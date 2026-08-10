# Pravdepodobný vývoj výkonu batérie

Webová aplikácia, ktorá z GPX stopy vypočíta priebeh kapacity batérie e-biku po trase,
bod, kde batéria dosiahne 0 %, a odhad dojazdu v každom mieste.

Beží celá v prehliadači. Žiadny server, žiadna databáza, žiadne odosielanie údajov —
GPX súbor ani odčítania batérie neopustia zariadenie.

## Obsah balíka

| Súbor | Účel |
|---|---|
| `index.html` | celá aplikácia (výpočet, rozhranie, graf) |
| `manifest.webmanifest` | údaje na inštaláciu na plochu telefónu |
| `sw.js` | servisný pracovník, vďaka nemu funguje bez signálu |
| `icon-192.png`, `icon-512.png`, `icon-maskable-512.png` | ikony pre Android |
| `apple-touch-icon.png` | ikona pre iPhone |
| `favicon-32.png` | ikona v karte prehliadača |

Všetky súbory patria do jedného priečinka. Nič sa nesťahuje z internetu, takže
aplikácia nemá žiadne vonkajšie závislosti.

## Nasadenie

### Netlify Drop — najrýchlejšie, bez účtu

1. Otvorte <https://app.netlify.com/drop>
2. Pretiahnite tam celý priečinok s týmito súbormi
3. Dostanete adresu typu `https://nazov.netlify.app`

Na neskoršie úpravy si založte účet zadarmo, inak sa adresa po čase uvoľní.

### Cloudflare Pages — trvalejšie riešenie

1. Účet na <https://dash.cloudflare.com>
2. Workers & Pages → Create → Pages → Upload assets
3. Nahrajte priečinok, potvrďte

Zvládne aj vlastnú doménu a nasadenie z Gitu.

### GitHub Pages

1. Nový repozitár, nahrajte doň súbory
2. Settings → Pages → Source: `main`, priečinok `/ (root)`
3. Adresa bude `https://meno.github.io/nazov-repozitara/`

### Vlastný server

Stačí ľubovoľný statický web. Podmienkou je **HTTPS** (alebo `localhost`) —
bez neho prehliadač nespustí servisného pracovníka a odpadne offline režim.

Nginx:

```nginx
location /bateria/ {
    alias /var/www/bateria/;
    index index.html;
}
```

### Miestne skúšanie

```bash
cd priečinok-s-aplikáciou
python3 -m http.server 8000
```

Potom `http://localhost:8000/`. Otvorenie priamo cez `file://` funguje len čiastočne:
pretiahnutie súboru myšou a trvalé ukladanie profilov prehliadač v tom režime zakáže.

## Inštalácia na telefón

**iPhone:** otvorte adresu v Safari → tlačidlo Zdieľať → Pridať na plochu.

**Android:** Chrome sám ponúkne inštaláciu, prípadne menu → Pridať na plochu.

Po inštalácii sa aplikácia otvára na celú obrazovku a funguje aj bez signálu —
hodí sa to, keďže na trase býva pokrytie slabé.

## Aktualizácia

Po zmene ktoréhokoľvek súboru zvýšte v `sw.js` číslo verzie:

```js
var VERSION = "bateria-v2";
```

Bez toho si prehliadač ponechá starú kópiu a zmenu neuvidíte.

## Ako sa to používa

1. Nahrajte GPX — funguje záznam z jazdy aj trasa z plánovača
2. Doplňte hmotnosti, kapacitu batérie a odpory podľa plášťov a posedu
3. Zadajte odčítania zo zobrazovača: kilometer a zostatok v %
4. Vypočítať

Odčítania sú kľúčové. Bez nich aplikácia iba odhaduje podiel jazdca na práci; s jedným
odčítaním klesne chyba zhruba na tretinu, s dvomi a viac sa navyše ukáže, či ste po celej
trase držali rovnaký režim asistencie.

Odčítania robte po úseku dlhom aspoň 10 km so zmiešaným terénom. Krátky úsek je
nepoužiteľný, lebo zobrazovač ukazuje percentá po skokoch, a úsek vedúci prevažne
z kopca tiež — na zjazde koná prácu gravitácia, nie motor.

## Profily jazdcov

Ukladajú sa do prehliadača, teda zostávajú na zariadení a nikam sa neodosielajú.
Medzi zariadeniami sa neprenášajú samy — na to slúžia tlačidlá **Vyviezť** a **Priniesť**,
ktoré profily prevedú na krátky text a späť.

## Presnosť

Model počíta mechanickú prácu zo sklonu, valivého odporu, odporu vzduchu a zrýchlenia,
a kalibruje ju na skutočné odčítania batérie.

- s jedným odčítaním: rádovo ±15 %
- s dvomi a viac pri nemennom režime asistencie: ±5 až 10 %

Neuvažuje rekuperáciu a nepozná vietor, ktorý sa z GPX zistiť nedá. Starnúca batéria má
nižšiu skutočnú kapacitu, než je uvedená na štítku — ak sedí všetko ostatné a výsledok
je sústavne optimistický, skúste kapacitu znížiť.
