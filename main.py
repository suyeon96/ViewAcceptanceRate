import requests
from bs4 import BeautifulSoup

def make_soup(url: str, enco: str) -> BeautifulSoup:
    res = requests.get(url)
    return BeautifulSoup(res.content.decode(enco, 'replace'), 'html.parser')

def crolling_jinhak(soup: BeautifulSoup, school: str, selector: str) -> list:
    table = soup.select_one(
        selector
    )
    trs = table.select('tr')
    data = []

    for idx, tr in enumerate(trs):
        if idx > 0 and idx < len(trs)-1:
            deptCell, capaCell, applyCell, rateCell = tr.find_all('td')[-4:]
            d = {
                'school' : school,
                'dept' : deptCell.text.strip() if len(deptCell.text.strip()) < 10 else deptCell.text.strip()[-9:],
                'capa' : capaCell.text.strip(),
                'apply' : applyCell.text.strip(),
                'rate' : rateCell.text.strip()
            }
            data.append(d)
    return data

def crolling_uway(soup: BeautifulSoup, school: str, code: str) -> list:
    table = soup.select_one(
        code + ' > table'
    )
    trs = table.select('tr')
    data = []

    for idx, tr in enumerate(trs):
        if idx > 0 and idx < len(trs)-1:
            rowspan = int(tr.find_all('td')[0].attrs['rowspan'])
            if school == '국민대학교': rowspan += 1
            elif school == '중앙대학교': rowspan += 1
            d = {
                'school' : school,
                'dept' : tr.find_all('td')[rowspan-1].text.strip(),
                'capa' : tr.find_all('td')[-3].text.strip(),
                'apply' : tr.find_all('td')[-2].text.strip(),
                'rate' : tr.find_all('td')[-1].text.strip()
            }
            data.append(d)
    return data

def print_console(result: list):
    print("{:<7} | {:<7} | {:<10} | {:<13}".format('Capacity', 'Apply', 'Rate', 'Dept'))
    print("=================================================")
    for i in result:
        print(f">> {i[0].get('school')} << ")
        for j in i:
            print("{:<7} | {:<7} | {:<10} | {:<13}".format(j.get('capa'), j.get('apply'), j.get('rate') if float(
                j.get('rate').split(':')[0]) < 10 else '\033[93m' + j.get('rate') + '\033[0m', j.get('dept')))
        print("-------------------------------------------------")

if __name__ == '__main__':
    jinhakrepo = [['숭실대학교', 'http://addon.jinhakapply.com/RatioV1/RatioH/Ratio11010151.html', '#SelType407 > table'],
                  ['숙명여자대학교', 'http://addon.jinhakapply.com/RatioV1/RatioH/Ratio10980381.html', '#SelType480 > table'],
                  ['한양대학교', 'http://addon.jinhakapply.com/RatioV1/RatioH/Ratio11650381.html', '#SelType4L > table'],
                  ['동국대학교', 'http://addon.jinhakapply.com/RatioV1/RatioH/Ratio10550201.html', '#SelType41AK > table.tableRatio3'],
                  ['홍익대학교', 'http://addon.jinhakapply.com/RatioV1/RatioH/Ratio11720211.html', '#SelType45101 > table']
    ]
    uwayrepo = [['중앙대학교', 'http://ratio.uwayapply.com/Sl5KOjhMSmYlJjomSmZmVGY', '#Div_0014'],
                ['건국대학교', 'http://ratio.uwayapply.com/Sl5KOTo5V2E5SmYlJjomSmZmVGY=', '#Div_0018'],
                ['경희대학교', 'http://ratio.uwayapply.com/Sl5KOnw5SmYlJjomSmZmVGY=', '#Div_01324'],
                ['광운대학교', 'http://ratio.uwayapply.com/Sl5KTjlKZiUmOiZKZmZUZg==', '#Div_0097'],
                ['국민대학교', 'http://ratio.uwayapply.com/Sl5KVyVNOWFhOUpmJSY6JkpmZlRm', '#Div_0031'],
                ['서울과기대', 'http://ratio.uwayapply.com/Sl5KMDpXJkpmJSY6JkpmZlRm', '#Div_0007']
    ]
    result = []

    for v in jinhakrepo:
        school = v[0]
        url = v[1]
        selector = v[2]
        soup = make_soup(url, 'utf-8')
        result.append(crolling_jinhak(soup, school, selector))

    for v in uwayrepo:
        school = v[0]
        url = v[1]
        selector = v[2]
        soup = make_soup(url, 'euc-kr')
        result.append(crolling_uway(soup, school, selector))

    print_console(result)