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
 def test_no_demo_counted_confirmed(self):
  for term in ['Braunschweig','Wellmann','Steyr','Regensburg']:
   self.assertEqual(next(s for s in self.data['shops'] if term in s['name'])['status'],'demo')
if __name__=='__main__':unittest.main()
