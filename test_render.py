import copy,json,unittest
from pathlib import Path
from render import render,validate,current
class PublicBoundary(unittest.TestCase):
 def setUp(self):self.data=json.loads(Path(__file__).with_name('offers.json').read_text())
 def test_private_fields_rejected(self):
  self.data['shops'][0]['gmail']='private'
  with self.assertRaises(AssertionError):validate(self.data)
 def test_mail_link_rejected(self):
  self.data['shops'][0]['url']='https://mail.google.com/mail/#all/example'
  with self.assertRaises(AssertionError):validate(self.data)
 def test_unproven_confirmation_rejected(self):
  self.data['shops'][0]['status']='confirmed'
  with self.assertRaises(AssertionError):validate(self.data)
 def test_escape_and_static_rows(self):
  self.data['shops'][0]['name']='<script>alert(1)</script>'
  page=render(self.data)
  self.assertNotIn('<script>alert(1)</script>',page)
  self.assertEqual(page.count('<tr data-age='),len(self.data['shops']))
 def test_cutoff_boundary_and_undated(self):
  sample=copy.deepcopy(self.data['shops'][0])
  for date,expected in [('2026-08-31',False),('2026-09-01',True),(None,False)]:
   sample['information_date']=date
   self.assertEqual(current(sample,self.data),expected)
 def test_partial_run_shows_actual_time_without_refreshing_evidence(self):
  self.data['last_run']='2026-09-07T07:11:00+00:00'
  self.data['checked']='2026-09-06T19:57:00+00:00'
  self.data['generated']='2026-09-08T10:00:00+00:00'
  self.data['run_status']='partial'
  self.data['failed_sources']=['bikearei','Goisern Bikeworld']
  page=render(self.data)
  self.assertIn('07. 09. 2026 · 09:11',page)
  self.assertIn('06. 09. 2026 · 21:57',page)
  self.assertIn('Částečná kontrola',page)
  self.assertIn('Nedostupné zdroje: bikearei, Goisern Bikeworld',page)
  self.assertNotIn('08. 09. 2026 · 12:00',page)
 def test_complete_run_cannot_hide_failed_sources(self):
  self.data['run_status']='complete'
  self.data['failed_sources']=['bikearei']
  with self.assertRaises(AssertionError):validate(self.data)
 def test_no_demo_counted_confirmed(self):
  for term in ['Braunschweig','Wellmann','Steyr','Regensburg']:
   self.assertEqual(next(s for s in self.data['shops'] if term in s['name'])['status'],'demo')
if __name__=='__main__':unittest.main()
