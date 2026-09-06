# Amflow TL Carbon L/XL

Veřejný přehled https://kolo.honeger.com, GitHub Pages z main.

`offers.json` obsahuje pouze veřejné nabídky a bezpečně zobecněnou dostupnost.
`python3 render.py` zkontroluje schéma a sestaví `index.html` z `template.html`.
`python3 test_render.py` ověří oddělení soukromých údajů, escapování a pravidla dostupnosti.

Obsah kontroluje naplánovaný Codex agent dvakrát denně (07:00 a 19:00 Europe/Prague) na dostupném Macu. Web funguje nezávisle na Macu; čerstvost dat nikoli. Při nedostupném Macu nebo konektoru se kontrola může zpozdit. Datum každého zdroje je samostatné, čas souhrnné kontroly neznamená nové ověření všech řádků.

Do tohoto veřejného repozitáře nikdy nepatří osobní komunikace, objednávky, platby, pořadí, přílohy, Gmail odkazy, databáze, logy či tokeny. Hlavní soukromá tabulka a provozní evidence jsou u správce lokálně mimo repo. Automatické kontroly nikoho nekontaktují.

Historický externí checker.py zde nebyl verzovaný. Od 6. září 2026 je renderer a veřejný datový model přímo součástí projektu; získávání a vyhodnocování nových zdrojů zajišťuje agent s webem a Gmail konektorem.
