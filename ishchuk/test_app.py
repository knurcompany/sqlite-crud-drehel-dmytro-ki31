import tempfile
import unittest
import re
from pathlib import Path
try:
 from app import create_app
 import database_connector as db
except ImportError:
 create_app=None

class CrudTests(unittest.TestCase):
 def setUp(self):
  self.assertIsNotNone(create_app,'The task CRUD application must be implemented')
  self.tmp=tempfile.TemporaryDirectory()
  self.addCleanup(self.tmp.cleanup)
  self.app=create_app({'TESTING':True,'DATABASE':str(Path(self.tmp.name)/'test.db')})
  self.client=self.app.test_client()

 def token(self,path='/add'):
  page=self.client.get(path).get_data(as_text=True)
  return re.search(r'name="csrf_token" value="([^"]+)"',page).group(1)

 def test_complete_crud_with_literal_sql_text(self):
  with self.app.app_context():
   title="План O'Brien'); DROP TABLE tasks;--"
   data=dict(title=title,description='Навчальний запис',status='new',due_date='2026-11-10')
   item_id=db.insert_item(data)
   self.assertGreater(item_id,0)
   self.assertEqual(db.get_item_by_id(item_id)['title'],title)
   self.assertEqual(len(db.get_all_items()),1)
   data.update(title='Підготовка звіту',status='done')
   self.assertTrue(db.update_item(item_id,data))
   self.assertEqual(db.get_item_by_id(item_id)['status'],'done')
   self.assertTrue(db.delete_item(item_id))
   self.assertIsNone(db.get_item_by_id(item_id))
   self.assertEqual(db.get_all_items(),[])

 def test_browser_routes_create_edit_delete(self):
  self.assertEqual(self.client.get('/').status_code,200)
  data=dict(title='<script>alert(1)</script>',description='Лабораторна',status='new',due_date='2026-11-10',csrf_token=self.token())
  response=self.client.post('/add',data=data,follow_redirects=True)
  self.assertEqual(response.status_code,200)
  self.assertIn('&lt;script&gt;',response.get_data(as_text=True))
  with self.app.app_context():item_id=db.get_all_items()[0]['id']
  data.update(title='Завершено',status='done',csrf_token=self.token(f'/edit/{item_id}'))
  self.assertEqual(self.client.post(f'/edit/{item_id}',data=data).status_code,302)
  token=self.token('/')
  self.assertEqual(self.client.post(f'/delete/{item_id}',data={'csrf_token':token}).status_code,302)
  self.assertEqual(self.client.get(f'/edit/{item_id}').status_code,404)

 def test_invalid_data_and_csrf_are_rejected(self):
  self.assertEqual(self.client.post('/add',data={'title':'Task'}).status_code,400)
  data=dict(title='  ',description='',status='new',due_date='',csrf_token=self.token())
  self.assertEqual(self.client.post('/add',data=data).status_code,400)
  data.update(title='Task',status='invalid')
  self.assertEqual(self.client.post('/add',data=data).status_code,400)
  data.update(status='new',due_date='2026-02-30')
  self.assertEqual(self.client.post('/add',data=data).status_code,400)
  self.assertEqual(self.client.get('/delete/1').status_code,405)
  with self.app.app_context():self.assertEqual(db.get_all_items(),[])

if __name__=='__main__':unittest.main(verbosity=2)
