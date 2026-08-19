# amflow-web

Veřejná stránka hlídače skladovosti **Amflow TL Carbon** → https://kolo.honeger.com

Obsah generuje `~/amflow-watch/checker.py` (launchd `com.petr.amflow-watch`, jednou za hodinu),
který po každém běhu přepíše `index.html` a pushne commit `auto-update`.

**Repo je veřejné.** Nikdy sem nepatří `state.db`, logy, `watchlist.json` ani jakékoli tokeny.

Vypnutí publikování: smazat `~/amflow-web` (checker si toho všimne a krok přeskočí).
