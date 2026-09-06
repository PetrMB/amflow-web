#!/usr/bin/env python3
"""Render reviewed public offers only; private evidence must remain outside this repo."""
import json, html, re
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parent
LABEL={'candidate':'Web uvádí skladem','confirmed':'Potvrzený prodejný kus','demo':'Pouze demo / showroom','preorder':'Předobjednávka / termín','unknown':'Neověřeno'}
def validate(data):
 assert set(data)=={'generated','checked','model','size','schedule','shops'}
 assert data['size']=='L/XL'
 for key in ('generated','checked'):datetime.fromisoformat(data[key])
 for s in data['shops']:
  assert set(s)=={'name','url','price','status','note','source','date'}
  assert s['status'] in LABEL
  assert not s['url'] or s['url'].startswith('https://')
  assert not re.search(r'mail\.google|gmail\.com|@|proforma|záloh|pořadí|objednávkov.{0,10}čís|\b1a0[0-9a-f]{12,}',json.dumps(s,ensure_ascii=False),re.I)
  datetime.fromisoformat(s['date'])
  if s['status']=='confirmed':
   assert s['source']=='Výslovně potvrzený volný prodejný kus L/XL'
 return data

def render(data):
 validate(data); e=html.escape
 rank={'confirmed':0,'candidate':1,'demo':3,'preorder':4,'unknown':5}
 rows=[]
 for s in sorted(data['shops'],key=lambda x:rank[x['status']]):
  name=f'<a href="{e(s["url"])}" target="_blank" rel="noopener noreferrer">{e(s["name"])}</a>' if s['url'] else e(s['name'])
  rows.append(f'<tr data-status="{s["status"]}"><td><strong>{name}</strong><small>{e(s["source"])} · {e(s["date"])}</small></td><td class="price">{e(s["price"])}</td><td><span class="badge {s["status"]}">{LABEL[s["status"]]}</span><p>{e(s["note"])}</p></td></tr>')
 template=(ROOT/'template.html').read_text()
 values={'AVAILABILITY':('Nalezeno výslovné potvrzení prodejného kusu L/XL. Stav a datum důkazu jsou uvedené v tabulce.' if any(s['status']=='confirmed' for s in data['shops']) else 'Žádný nalezený podklad zatím jednoznačně nepotvrzuje volný kus L/XL k okamžitému prodeji.'),'ROWS':''.join(rows),'TOTAL':str(len(rows)),'HITS':str(sum(s['status']=='confirmed' for s in data['shops'])),'CANDIDATES':str(sum(s['status']=='candidate' for s in data['shops'])),'CHECKED':e(data['checked']),'WHEN':datetime.fromisoformat(data['checked']).astimezone().strftime('%d. %m. %Y · %H:%M'),'SCHEDULE':e(data['schedule'])}
 for key,value in values.items():template=template.replace('{{'+key+'}}',value)
 assert '{{' not in template
 return template
if __name__=='__main__':
 (ROOT/'index.html').write_text(render(json.loads((ROOT/'offers.json').read_text())))
 print('Rendered and validated public index.html')
