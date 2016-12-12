stahování a pár statistik raw dat

Na webu Ministerstva financí je možné stáhnout všechna raw data z [CEDR](http://cedr.mfcr.cz/cedr3internetv419/OpenData/DocumentationPage.aspx). Jsou poskytované jako 7zip soubory a aktualizované jednou za čtvrt roku.

Nabízeny jsou dva typy souborů - samotná data a číselníky. Číselníky jsou víceméně slovníky pro různé údaje - jde o linkovaná data, takže např. poskytovatel dotace není vypsát explicitně, ale je uveden jeho identifikátor, který pomocí číselníku přeložíme (denormalizujeme).

Jako první je tedy třeba stáhnout všechna data z odkazů, které jsou uvedeny ve [_stahuj.txt](_stahuj.txt) (např. skrz `wget`). Jelikož jde o 7zip, který nejde nativně v Pythonu zpracovat, použil jsem `arepack` na přeložení všech archivů do `tar.gz`, nemotorný bash skript je v [_repack.sh](_repack.sh).

V tomto stádiu jsou data připravena k dalšímu zpracování.
