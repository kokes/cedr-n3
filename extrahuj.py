from glob import glob
import csv
import tarfile
import io
import os
import gzip
from collections import defaultdict, OrderedDict


# ## Číselníky
# Napřed načteme číselníky, které budeme používat jako slovníky pro údaje v samotném CEDRu.
# Tohle budem držet v paměti a pak za chodu nahrazovat.

print('Načítám číselníky')
gfn = glob('data/ciselnik*.tar.gz')
cdt = dict()

for gf in gfn:
    tf = tarfile.open(gf, 'r:gz')
    for fnm in tf.getmembers():
        if '/ciselnik' not in fnm.name: continue
        if not fnm.name.endswith('.n3'): continue
    #     print(fnm)

        ff = tf.extractfile(fnm.name)
        
        for j in ff:
            if b'/title>' not in j: continue
            d = j.split()
            key = d[0][1:-1].decode('ascii')
            val = (b' '.join(d[2:-1])).decode('unicode-escape')
            if val.startswith('"'):
                val = val[1:val.rindex('"')]

            cdt[key] = val

def extrahuj(ff, chces, tfn):
    """
    Hlavní funkce pro extkrakci vlastností z jedné CEDR tabulky.
    Načtení všech dat do RAM není nutné, průběžně se kontroluje, zda je
    možné vyexportovat část dat (pro ty řádky, kde máme všechny sloupce).
    
    Přijímá tři argumenty:
     - ff: file handler vstupu
     - chces: seznam sloupců, které chceme vytáhnout
     - tfn: název souboru, kam se to bude sypat
    """
    ns = '<http://cedropendata.mfcr.cz/c3lod/'
    
    schces = set(chces)
    lc = len(chces)
    ret = dict()
    counts = defaultdict(lambda: 0) # (int) by stacilo, ne?
    
    fb = io.StringIO(newline='')
    # jen header
    w = csv.writer(fb)
    w.writerow(chces)
    
    for j, ln in enumerate(ff):
        if j % (1000*100) == 0: print('%s: %d' % (tfn, j), end='\r')
        if j>0 and j % (1000*100) == 0:
            kc = list(counts.keys()) # protoze budem menit
            for k in kc:
                if counts[k] != lc: continue # jeste nemame vse
                w.writerow(ret[k].values())
                del ret[k]
                del counts[k]

        els = ln.decode('unicode-escape').split()
        if len(els) == 4:
            els = els[:3] # mazem tecku na konci
        else:
            els = els[:2] + [' '.join(els[2:-1])] # pro pripad ze ma treti pole mezery (-1 pro vynechani tecky)    

        idd = els[0][els[0].rindex('/')+1:-1]
        if '#' not in els[1]: continue # title
        slvs = els[1][els[1].index('#')+1:-1]
        if slvs not in schces: continue

        assert els[2][0] in ['<', '"']
        if els[2][0] == '<':
            assert els[2].startswith(ns), els[2]
            trd = cdt[els[2][1:-1]]
            #trd = els[2][len(ns):-1] # -1 pro trimovani '>'
            #trd = els[2][els[2].rindex('/')+1:-1] # id po slovese
        else:
            # hodnota mezi uvozovkama
            if '"' not in els[2][1:]:
                trd = els[2][1:].strip()
            else:
                trd = els[2][1:els[2][1:].rindex('"')+1]

        if idd not in ret:
            ret[idd] = OrderedDict.fromkeys(chces)

        ret[idd][slvs] = trd
        counts[idd] += 1

    # vypsat zbyvajici
    for j,k in ret.items():
        w.writerow(k.values())
        
    with open(tfn, 'w') as f:
        f.write(fb.getvalue())


def cti_vazby(ff, slvs, tfn):
    """
    Pro extrakci vybraných vztahů z n3 souboru.
    
    Vytáhne jen potřebný sloupec. Použijeme pro napojení našich CSV souborů.
    """
    hd = False

    slvs = bytes('#%s>' % slvs, encoding='ascii')

    tf = open(tfn, 'w', encoding='ascii', newline='')
    cw = csv.writer(tf)

    for j, rw in enumerate(ff):
        if slvs not in rw: continue
        dd = rw.decode('ascii').split()

        if not hd:    
            hda = dd[0].split('/')[-2]
            hdb = dd[2].split('/')[-2]
            hd = True
            cw.writerow([hda, hdb])

        a = dd[0][dd[0].rindex('/')+1:-1]
        b = dd[2][dd[2].rindex('/')+1:-1]
        cw.writerow([a, b])

    tf.close()    


# =========================================

"""
Jdem načítat jednotlivé soubory a parsovat je.
Pro jednoduchost jsem veškeré argumenty naházel
do extrahuj.csv. Je tam jméno tar.gz souboru,
jméno n3 souboru v něm, seznam sloupců a název
výsledného souboru.
"""

print('Načítám data')

if not os.path.isdir('csv'):
    os.mkdir('csv')

with open('extrahuj.csv') as cf:
    cr = csv.reader(cf)
    hd = next(cr)

    ex = [{hd[j]: vl for j,vl in enumerate(row)} for row in cr]

for j, ee in enumerate(ex):
    print('\nProcesuju %s (%d/%d)' % (ee['targz'], j+1, len(ex)))
    with tarfile.open(ee['targz'], 'r:gz') as tf:
        ff = tf.extractfile(ee['soubor'])
        extrahuj(ff, ee['chcem'].split(', '), ee['cil'])


# Vazby
# =====

print('Načítám vazby')

with tarfile.open('./data/PrijemcePomoci.n3.tar.gz', 'r:gz') as tf:
    ff = tf.extractfile('./cedr/PrijemcePomoci.n3')
    cti_vazby(ff, 'obdrzelDotaci', 'csv/_obdrzelDotaci.csv')

with tarfile.open('./data/Dotace.n3.tar.gz', 'r:gz') as tf:
    ff = tf.extractfile('./cedr/Dotace.n3')
    cti_vazby(ff, 'byloRozhodnuto', 'csv/_byloRozhodnuto.csv')
