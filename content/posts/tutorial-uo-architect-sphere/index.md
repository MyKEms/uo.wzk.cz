+++
title = "Stavíte na Sphere? Zkuste UO Architect!"
slug = "tutorial-uo-architect-sphere"
date = 2006-07-26T00:00:00
draft = false
categories = ["Tutorials"]
tags = ["Aramis", "Manawydan Archive"]

[params]
  source = "ultima-cz"
+++

Návod jak v UO Architektu vytvořit stavbu a převést ji na Sphere server.

## Postup

1. Otevřeme UO Architekta a klikneme na **File > New Design**. Zvolíme rozměr plochy (např. 20x20) a klikneme **CREATE**.

   *Tip: Pokud máte větší plochu a nevidíte ji celou, posouváte ji stisknutím SHIFT + levé tlačítko myši.*

2. Objeví se plocha na kterou budeme stavět.

3. Pokud již máme hotovo, zvolíme **File > Save As**:
   - Name: barak
   - Category: barak
   - SubSection: První Pokusy
   - Klikněte **SAVE**

4. V příslušné sekci nalezneme náš dům a označíme si jej.

5. Klikneme na **File > Export > Multi Text (.txt)**. Uložíme soubor (pokud má být v textu mezera, uděláme pomlčku `_`).

6. Otevřeme uložený soubor a vyhledáme řádek `1 template id` a přepíšeme `1` na `0`.

7. Soubor uložíme a vhodíme do složky se Sphere. Spustíme Sphere (pokud již běží, resyncneme).

8. Nalognem se do hry a napíšeme příkaz: `.unextract barak.txt`

Objeví se kurzor a klikneme na místo, kde má být barák postaven. Hotovo!

*Poznámka: Na baráku se nemusí zobrazovat všechny itemy, protože client je nemusí stíhat načítat, ale jak jej přidáte do statiku, budou tam.*

---

*Archived from [ultima.cz](https://ultima.cz/) — Czech Ultima Online community site.*
