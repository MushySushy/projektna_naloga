# Analiza igralcev igre Minesweeper

## Opis
Klasična igra [Minesweeper](https://en.wikipedia.org/wiki/Minesweeper_(video_game)) je stara že preko 30 let, a jo kljub temu še vedno mnogo ljudi aktivno igra. Primarni kraj za to dejavnost je spletna stran [minesweeper.online](https://minesweeper.online), kjer lahko igralci tekmujejo v raznih kategorijah, kot so hitrost, učinkovitost, vztrajnost in mojsterstvo.

Ogledali si bomo podatke igralcev te igre in povezave med njimi. Na žalost je teh igralcev nekoliko preveč, da bi lahko vse obdelali (približno 6 milijonov), torej si bomo ogledali le najvišjih sto tisoč. To na srečo ne povzroči nobene pristranskosti s podatki, saj so igralci od sto tisoč naprej večinoma ljudje, ki so odigrali zgolj eno ali dve igri (to so tisti, ki imajo ime *Anonymous*).

## Uporaba
Za uporabo potrebujete python knjižnico `selenium`, ki jo lahko pridobite z ukazom `pip install selenium`.

Program je zelo specializiran, torej lahko kot uporabnik določite le 2 parametra: št. igralcev, ki jih želite nabrati, in ime izhodne datoteke. To sta parametra, ki ju sprejme funkcija `naberi_igralce(n, filename)`.

Tiste, ki se nameravate sami poigrati s tem programom, moram še opozoriti, da je proces precej počasen. Program nabere le 2 osebi na sekundo (nabor sto tisoč ljudi traja približno 14 ur).