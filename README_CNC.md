---
title: Balíčkový manažer Spack
author: David Lukeš <lukes@korpus.cz>
date: 2017-09-25
...

# Úvod

Spack je balíčkový manažer, který umožňuje jednoduchou a pohodlnou instalaci
balíčků kompilovaných ze zdrojového kódu, včetně dohledávání závislostí. Díky
němu lze např. na starší verzi Ubuntu dostat nejnovější Python, aniž by se s
kompilací člověk musel patlat ručně, nebo mít na jednom systému přehledně víc
verzí téhož programu vedle sebe a přepínat si mezi nimi.

Plná dokumentace je k dispozi na adrese <http://spack.rtfd.io>, k základní
orientaci a používání by ale bohatě mělo stačit přečíst si *Quickstart* a
případně *FAQ* níže :)

# Quickstart

## Seznam lokálně nainstalovaných balíčků

`./bin/spack find` vypíše v současné době nainstalované balíčky.

## Seznam dostupných balíčků

`./bin/spack list` vypíše dostupné balíčky, `./bin/spack info <jméno_balíčku>`
vypíše informace o konkrétním balíčku. Pokud na seznamu nějaký požadovaný
software chybí, lze pro něj balíček vytvořit (`./bin/spack create`).

## Instalace nových balíčků

`./bin/spack install <jméno_balíčku>`, ale musí to pustit někdo, kdo smí
zapisovat do hierarchie pod tímto adresářem -- takže buď já, nebo kdokoli se
sudem na kterémkoli ze serverů, kde je tento adresář namountován. Ale byl bych
radši, kdybyste spíš dali vědět, kdyby vám tu něco chybělo :)

## Používání balíčků

Pokud chcete jen příležitostně použít konkrétní verzi nějakého programu, můžete
si k ní najít cestu třeba pomocí příkazu `find`:

```sh
$ find /cnk/common/tools/spack/opt -path \*/bin/python3
/cnk/common/tools/spack/opt/spack/linux-ubuntu12.04-x86_64/gcc-7.2.0/python-3.6.2-hzxqad2u2m74kzljgbrtx4s2j4ern3lw/bin/python3
```

Pokud chcete standardně ve svém prostředí používat nějakou sadu balíčků,
doporučuju následující postup:

```sh
$ ./bin/spack view --verbose add $HOME/.spackview python perl git
```

Tím se v adresáři `~/.spackview` vytvoří stejná adresářová struktura, jaká je
např. pod `/usr`...

```sh
$ tree -L 1 ~/.spackview
/cnk/users/home/lukes/.spackview
├── bin
├── etc
├── include
├── lib
├── libexec
├── man
└── share

7 directories, 0 files
```

... a nalinkují se do ní balíčky `python`, `perl` a `git` (binárky budou pod
`bin/`, manpages pod `man/` či `share/man/` atd.). Stačí tedy pak přidat tyto
adresáře do cesty přes příslušné proměnné prostředí `*PATH`...

Defaultně se vytvářejí symlinky, což mj. umožňuje, aby zdrojové soubory a view
byly na jiných filesystémech. Pokud ale chceme do view nalinkovat i balíčky,
které nějaké další balíčky rozšiřují (např. knihovnu `manatee` pro Python), a
zároveň se chceme vyhnout tomu, abychom kvůli jejich zprovoznění museli
manipulovat s příslušnými proměnnými prostředí (tj. např. pro Python upravit
`PYTHONPATH`), musíme už použít hardlinky. Stačí nahradit příkaz `add` příkazem
`hardlink`. Ovšem pozor, jak zmíněno výše, hardlinky nemůžou jít přes hranice
fyzického filesystému.

```sh
# v ~/.bashrc nebo podobném konfiguračním souboru
export PATH=$HOME/.spackview/bin:$PATH
export MANPATH=$HOME/.spackview/share/man:$MANPATH
export INFOPATH=$HOME/.spackview/share/info:$INFOPATH

# na tohle pozor, většinou to není potřeba (Spack cestu k dynamickým knihovnám
# navtrdo zapeče přes RPATH) a některým systémově nainstalovaným programům se
# naopak nemusí líbit  novější dynamické knihovny, které jim takto vnutíte
export LD_LIBRARY_PATH=$HOME/.spackview/lib:$LD_LIBRARY_PATH
```

... takže Python, Perl a Git nainstalované přes Spack se stanou vašimi
defaultními.

Toto není jediný způsob; všechny možnosti, které Spack nabízí, jsou dopodrobna
rozebrány zde:

<https://spack.readthedocs.io/en/latest/workflows.html#running-binaries-from-packages>

# FAQ (= otázky, které by někdo někdy možná mohl vznést)

## Jak moc se lze spolehnout na to, že verze balíčku, kterou používám, nebude v budoucnu přepsána nějakou novější?

Díky tomu, že Spack instaluje balíčky do adresářů namespaceovaných podle verze
OS, překladače, samotného balíčku a jeho závislostí (přes hash závislostního
stromu), můžou vedle sebe různé verze stejného balíčku jednoduše koexistovat.
Není tedy důvod při instalaci nové verze balíčku nějakou starší odinstalovávat.
Někdo může mít do svého `spack view` nalinkovaný Python 3.6, někdo 3.7 (až
vyjde).

## Skript s shebangem odkazujícím na program instalovaný přes Spack se nechce spustit

Délka shebangu je většinou omezená na 128 znaků, takže s reálnou cestou k
binárkám instalovaným přes Spack většinou neobstojíte. Mějme soubor
`script.py`:

```python
#!/cnk/common/tools/spack/opt/spack/linux-ubuntu12.04-x86_64/gcc-7.2.0/python-3.6.2-hzxqad2u2m74kzljgbrtx4s2j4ern3lw/bin/python3

print("Hello, world!")
```

Když se ho pokusíme spustit:

```sh
$ ./script.py
zsh: ./script.py: bad interpreter: /cnk/common/tools/spack/opt/spack/linux-ubuntu12.04-x86_64/gcc: no such file or directory
```

Vyřešit to lze buď tak, že do shebangu zadáme kratší cestu vytvořenou přes
symlink...

```
#!/cnk/users/home/lukes/.spackview/bin/python3

print("Hello, world!")
```

... nebo toto omezení obejdeme pomocí skriptu `./bin/sbang`:

```python
#!/cnk/common/tools/spack/bin/sbang
#!/cnk/common/tools/spack/opt/spack/linux-ubuntu12.04-x86_64/gcc-7.2.0/python-3.6.2-hzxqad2u2m74kzljgbrtx4s2j4ern3lw/bin/python3

print("Hello, world!")
```

## Jak nainstalovat manatee?

1. Naklonujte si tento repozitář.
2. Zkontrolujte verzi GCC, kterou máte k dispozici. Není-li řady 5 nebo 6,
   doporučuju nejdřív nainstalovat GCC 6.x: `bin/spack install gcc@6`
3. Nainstalujte manatee: `bin/spack install manatee-open`
4. Aktivujte knihovny pro Python a Perl:
   `bin/spack python activate_manatee_bindings.py activate`

Pokud budete chtít knihovny pro Python a Perl zase deaktivovat:
`bin/spack python activate_manatee_bindings.py deactivate`.

Pokud chcete knihovny pro Python a Perl používat nějakým jiným způsobem (bez
aktivace), různé tipy jsou k dispozici v dokumentaci balíčku `manatee-open`:
`bin/spack info manatee-open`.

## Jak řeší `spack view` konflikty a nekompatibility mezi balíčky?

Neřeší, prostě jen tupě nalinkuje zadané balíčky do adresářové struktury pod
uvedenou cestou (konkrétní verze balíčků lze zadat ručně, např. místo jména
balíčku `python` zadáte specifičtější identifikátor `python@3.6.2`). V praxi mi
to zatím nevadilo, nicméně chytřejší řešení je snad na cestě:
<https://github.com/LLNL/spack/pull/4585>

## Jak přidat novou verzi balíčku?

Většinou stačí zjistit hash pomocí `./bin/spack md5 <release_url>` a pak verzi
přidat pomocí `./bin/spack edit <jméno_balíčku>`.

## Jaké speciální funkce jsou dostupné při psaní balíčků?

Viz dokumentace modulu
[spack](http://spack.readthedocs.io/en/latest/spack.html#module-contents) (na
začátku `package.py` vždycky je `from spack import *`).

Kromě toho se hodí prozkoumat metody dostupné na příslušné třídě `*Package` a
[`PackageBase`](http://spack.readthedocs.io/en/latest/spack.html#spack.package.PackageBase),
z níž všechny třídy `*Package` dědí.

## Jak debugovat instalaci balíčku?

`bin/spack env <jméno_balíčku> bash` nastaví všechny potřebné proměnné prostředí
a otevře `bash`.
