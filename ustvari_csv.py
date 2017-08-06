import orodja
import re




def zajemi_monstre():
    osnovni_naslov = 'https://www.db.yugioh-card.com/yugiohdb/card_search.action'
    parametri = 'ope=1&sort=2&rp=100'
    for stran in range(1, 54):
        naslov = '{}?{}&page={}'.format(osnovni_naslov, parametri, stran)
        ime_datoteke = 'monstri/{:02}.html'.format(stran)
        orodja.shrani(naslov, ime_datoteke)



def pocisti_monstra(monster):
    podatki = monster.groupdict()
    podatki['Ime'] = podatki['Ime'].strip()
    podatki['Atribut'] = podatki['Atribut'].strip()
    podatki['Level_Rank'] = int(podatki['Level_Rank'])
    podatki['Tip'] = podatki['Tip'].strip()
    podatki['ATK'] = 0 if podatki['ATK'] == '?' else int(podatki['ATK'])
    podatki['DEF'] = 0 if podatki['DEF'] == '?' else int(podatki['DEF'])
    return podatki



def pripravi_monstre():
    regex_monstra = re.compile(
        r'<span class="card_status">.*?<strong>(?P<Ime>.+?)</strong>'
        r'.*? class="box_card_attribute">.*?<.*?>.*?<span>(?P<Atribut>.+?)</span>'
        r'.*? class="box_card_level_rank (level|rank)">.*?<.*?>.*?<span>(Level|Rank) (?P<Level_Rank>.+?)</span>'
        r'.*? class="card_info_species_and_other_item">.*?>(?P<Tip>.+?)<'
        r'.*? class="atk_power">ATK (?P<ATK>.+?)</span>'
        r'.*? class="def_power">DEF (?P<DEF>.+?)</span>'
        ,
        flags=re.DOTALL
    )

    monstri = []
    for html_datoteka in orodja.datoteke('monstri'):
        for monster in re.finditer(regex_monstra, orodja.vsebina_datoteke(html_datoteka)):
         #   print(monster.group('Ime'), monster.group('Atribut'), monster.group('Level_Rank'), monster.group('Tip'), monster.group('ATK'), monster.group('DEF'))
         #   print(monster.groupdict())
            monstri.append(pocisti_monstra(monster))

    orodja.zapisi_tabelo(monstri, ['Ime', 'Atribut', 'Level_Rank', 'Tip', 'ATK', 'DEF'], 'monstri.csv')
    


zajemi_monstre()    
pripravi_monstre()
