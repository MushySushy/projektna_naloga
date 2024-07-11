# Analiza igralcev igre Minesweeper

## Opis
Klasična igra [Minesweeper](https://en.wikipedia.org/wiki/Minesweeper_(video_game)) stara že preko 30 let, a jo kljub temu še vedno mnogo ljudi aktivno igra. Glaven kraj za to dejavnost je spletna stran [minesweeper.online](https://minesweeper.online), kjer lahko igralci tekmujejo v raznih kategorijah, kot so hitrost, učinkovitost, ustrajnost in t.i. mastery.

Ogledali si bomo **neki**. Na žalost je teh igralcev nekoliko pre več, da bi lahko vse obdelali (približno 6 milijona), torej si bomo ogledali le najvišjih 100 tisoč. To na srečo ne povzroči nobenih **biasov** s podatki, saj so igralci od 100 tisoč naprej večinoma ljudje, ki so odigrali zgolj 1 ali 2 igri (to so vsi "Anonymous").

## Uporaba
Za uporabo potrebujete python knjižnico `selenium`, ki jo lahko pridobite z ukazim `pip install selenium`.

Program je zelo specializiran, torej lahko kot uporabnik določite le 2 parametra: št. igralcev za nabrati, in ime izhodne datoteke. To sta parametar, ki ju sprejme funkcija `naberi_igralce(n, filename)`.

Tiste, ki se nameravate sami poigrati s tem programom, moram še opozoriti, da je proces precej počasen. Program nabere le 2 osebi na sekundo (nabor 100 tisoč ljudi traja približno 14 ur).