+++
title = "Jak na animace v UO (UO Animation Guide)"
slug = "tutorial-jak-na-animace"
date = 2005-01-10T00:00:00
draft = false
categories = ["Tutorials"]
tags = ["M@B", "Manawydan Archive"]

[params]
  source = "ultima-cz"
+++

Tento článek vás naučí vkládat animace do UO. Použité programy: **InsideUO**, **UO Animation Calculator**, **Michelangelo**, **UOAnim**.

## 1. Základy

### Směry animace

Animace se v UO ukládají v pěti směrech: down (dolu), down-left (vlevo dolu), left (vlevo), up-left (vlevo nahoru), up (nahoru). Stíny se generují automaticky, průhledná barva animace je bílá a černá.

### Animation Block Offset

Offset směrů: +0 down, +1 down-left, +2 left, +3 up-left, +4 up.

### High Detail Creatures

| Offset | Druh animace | Počet snímků |
|--------|-------------|-------------|
| 0 | Walk | 10 |
| 5 | Stand | 1 |
| 10 | Die 1 | 4 |
| 15 | Die 2 | 4 |
| 20 | Attack 1 | 4-6 |
| 25 | Attack 2 | 4-6 |
| 30 | Attack 3 | 4-6 |
| 35 | Misc. 1 | 4 |
| 40 | Misc. 2 | 4 |
| 45 | Misc. 3 | 4 |
| 50 | Stumble | 4 |
| 55 | Misc. (Stomp) | 6 |
| 60 | Misc. (Cast) | 6 |
| 65 | Get Hit 1 | 4 |
| 70 | Misc. | 6 |
| 75 | Get Hit 2 | 4 |
| 80 | Get Hit 3 | 4 |
| 85 | Fidget 1 | 6 |
| 90 | Fidget 2 | 6 |
| 95 | Fly | 10 |
| 100 | Landing | ? |
| 105 | Die in Flight | 6 |

### Low Detail Creatures

| Offset | Druh animace | Počet snímků |
|--------|-------------|-------------|
| 0 | Walk | 5 |
| 5 | Run | 5 |
| 10 | Stand | 1 |
| 15 | Graze or Eat | 5 |
| 25 | Attack 1 | 5 |
| 30 | Attack 2 | 5 |
| 35 | Attack 3 | 5 |
| 40 | Die 1 | 6 |
| 45 | Fidget 1 | 6 |
| 50 | Fidget 2 | 6 |
| 55 | Lie Down | 5 |
| 60 | Die 2 | 6 |

### Human and Equipment

| Offset | Druh animace |
|--------|-------------|
| 0 | Walk Unarmed |
| 5 | Walk Armed |
| 10 | Run Unarmed |
| 15 | Run Armed |
| 20 | Stand |
| 25-30 | Fidget 1-2 |
| 35-40 | Stand Ready (1H/2H) |
| 45 | Attack 1H Weapon |
| 50-55 | Attack Unarmed 1-2 |
| 60-70 | Attack 2H (downstrike/wide/jab) |
| 75 | Walk Attack Mode |
| 80-85 | Cast (Directed/Area) |
| 90-95 | Attack Bow/Crossbow |
| 100 | Get Hit |
| 105-110 | Die (back/forward) |
| 115-145 | Horseback animations |
| 150 | Turn Around |
| 160 | Bow |
| 165 | Salute |

## 2. Tvorba animace

### Zjištění prvního animačního bloku

1. Spusťte **InsideUO**, klikněte na Animation
2. Vyberte kategorii a najděte požadovanou animaci
3. Poznamenejte si číslo modelu
4. Zapněte **UO Animation Calculator** a zadejte číslo modelu
5. Stiskněte Enter — zjistíte First Animation Frame

### Vytvoření patche pomocí UOAnim

1. Spusťte **UOAnim**
2. Klikněte na **Add Animation**
3. Zadejte číslo animačního bloku (First frame + offset + směr)
4. Klikněte **Add Image** a vyberte obrázek
5. Nastavte origin (x, y) — střet os se bere jako povrch
6. Opakujte pro všechny snímky podle tabulky
7. Vytvořte patch kliknutím na **Create Patch**

Poznámka: Tato verze UOAnim nemá import, takže co jednou vytvoříte nemůžete upravovat.

### Export do UO

1. Spusťte **Michelangelo**
2. Importujte UOP soubor(y)
3. Klikněte na **Export** a uložte jako verdata
4. Zkopírujte vytvořený soubor do adresáře s UO

---

*Archived from [ultima.cz](https://ultima.cz/) — Czech Ultima Online community site.*
