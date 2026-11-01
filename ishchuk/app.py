"""Local single-user task notebook. Run: python app.py."""
from pathlib import Path
from datetime import date
import secrets
from flask import Flask,abort,redirect,render_template,request,session,url_for
import database_connector as db

STATUSES={'new':'Нове','in_progress':'У роботі','done':'Виконано'}

def create_app(config=None):
 app=Flask(__name__)
 app.config.update(SECRET_KEY=secrets.token_hex(32),DATABASE=str(Path(__file__).with_name('data.db')))
 if config:app.config.update(config)
 with app.app_context():db.create_db_table()

 @app.context_processor
 def template_values():
  if 'csrf_token' not in session:session['csrf_token']=secrets.token_urlsafe(24)
  return {'csrf_token':session['csrf_token'],'statuses':STATUSES}

 @app.before_request
 def check_csrf():
  if request.method=='POST':
   token=session.get('csrf_token','')
   if not token or not secrets.compare_digest(token,request.form.get('csrf_token','')):abort(400)

 def read_form():
  data={key:request.form.get(key,'').strip() for key in ('title','description','status','due_date')}
  error=''
  if not 1<=len(data['title'])<=120:error='Назва має містити від 1 до 120 символів.'
  elif len(data['description'])>2000:error='Опис має містити до 2000 символів.'
  elif data['status'] not in STATUSES:error='Оберіть коректний стан.'
  elif data['due_date']:
   try:date.fromisoformat(data['due_date'])
   except ValueError:error='Вкажіть коректну дату.'
  return data,error

 @app.get('/')
 def index():return render_template('index.html',items=db.get_all_items())

 @app.route('/add',methods=['GET','POST'])
 def add():
  item={'title':'','description':'','status':'new','due_date':''};error=''
  if request.method=='POST':
   item,error=read_form()
   if not error:
    db.insert_item(item)
    return redirect(url_for('index'))
  return render_template('form.html',item=item,error=error,editing=False),(400 if error else 200)

 @app.route('/edit/<int:item_id>',methods=['GET','POST'])
 def edit(item_id):
  item=db.get_item_by_id(item_id)
  if item is None:abort(404)
  error=''
  if request.method=='POST':
   item,error=read_form()
   if not error:
    db.update_item(item_id,item)
    return redirect(url_for('index'))
  return render_template('form.html',item=item,error=error,editing=True),(400 if error else 200)

 @app.post('/delete/<int:item_id>')
 def delete(item_id):
  if not db.delete_item(item_id):abort(404)
  return redirect(url_for('index'))

 return app

if __name__=='__main__':create_app().run(host='127.0.0.1',port=5058,debug=False)
