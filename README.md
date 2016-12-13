# CEDR

MFČR nabízí kompletní databázi dotací, CEDR, je ale poněkud složitá na technické a metodologické zpracování. Zde je rychlý přehled jak z N3 dumpů vytvořit CSV soubory, které jde dál jednoduše zpracovat.

První je třeba stáhnout všechny archivy s daty, krátký popis je ve složce [stahuj](stahuj). Pro pohodlnost jsem všechno přepakážoval do `tar.gz`, ale pokud máte dost místa, doporučuju rozbalit a pracovat s texty samotnými, krapet to zrychlí parsování (jde ale o asi 30 GB dat).

Data samotná jsou uložená jako klasické trojvlastnosti (předmět, predikát, objekt), které budeme parsovat a kategorizovat podle předmětu (u dotací je předmět dotace, u rozhodnutí to je rozhodnutí atd.). Problémem při tomto parsování je, že jedna z vlastností (sloupců v našem CSV) může být až na konci celého dumpu, takže musíme celkem hodně informací držet v paměti, než se nám sejdou všechny vlastnosti.

Každopádně je třeba mít v hlavě Obrázek 3 ze strany 12 v [technické dokumentaci CEDR](http://cedropendata.mfcr.cz/c3lod/C3_OpenData%20-%20datov%C3%A1%20sada%20IS%20CEDR%20III%20v2%2002.pdf), to je naprosto klíčové pro pochopení vztahů mezi datasety. My budeme exportovat dva typy CSV souborů. Data samotná a pak vztahové soubory - kde je napojení jednotlivých tabulek mezi sebou. Jakmile vyexportujete jednotlivé tabulky z `n3` do `csv`, bude třeba je spojovat (na základě jejich unikátních identifikátorů), to už nechám na vás, ale třeba pomocí knihovny `pandas` to je triviální.

Pár informací bokem:

- Vlastnosti v daných tabulkách nejsou vždy kompletní - tj. některé vlastnosti nejsou přítomny pro všechny řádky. Např. je 1577627 dotací, ale jen 294098 má název projektu. Podrobné statistiky toho, co je a co není, najdete [tady](stahuj/_freq.txt). Já vytahuji jen několik málo vlastností (většinou ty, které jsou ve všech záznamech), je ale možné tento seznam sloupců rozšířit, stačí změnit onen [ovládací soubor](extrahuj.csv)
- Během parsování se ukazuje, kolik řádků `n3` souboru se už zpracovalo. U těch větších datasetů to jde do desítek milionů, podrobnější čísla [tutaj](stahuj/_stats.txt).
- Celé to běží na Pythonu 3 bez jakýchkoliv externích knihoven. Na stažení a konvertování původních dat budete potřebovat něco jako `wget` a `arepack`. Na Unixech to existuje běžně, na Windows stačí Cygwin (nebo ten nový bash ve Windows 10).
- Nepoužívám RDF knihovny, protože jsou tuze pomalé (byť korektnější) a já potřeboval něco podobně rychlé jako IO.
- Ano, jde to exportovat pomocí [SPARQL](http://www.cambridgesemantics.com/semantic-university/sparql-by-example) samotného, ale na to je potřeba běžící SPARQL server. Ten od MFČR nám tohle nedá a provozovat něco vlastního je pomalejší než pustit jeden krátký skript nad dumpem.
- Časem nejspíš bude MFČR poskytovat tyto CSV dumpy samo, do té doby se tyhle kódy mohou hodit.
- Co se týče licencí, tak dejme tomu že volná, bez záruk a atribuční. Takže si to používejte dle libosti, ale za nic nemůžu a jestli z toho něco vznikne, tak nalinkujte tohle repo.

Stížnosti na [@kondrej](https://twitter.com/kondrej) nebo [email](mailto:ondrej.kokes@gmail.com).
