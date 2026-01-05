from flask import Flask, render_template, request, redirect, url_for, session, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this in production

# Email report route (demo: sends to configured email)
@app.route('/send_report')
def send_report():
	# CONFIGURE THESE:
	sender_email = 'krishsharma292006@gmail.com'
	sender_password = 'your_app_password'  # Use app password for Gmail
	recipient_email = 'recipient@example.com'
	smtp_server = 'smtp.gmail.com'
	smtp_port = 587

	expenses = load_expenses()
	total = sum(float(e.get('amount', 0)) for e in expenses)
	html = f"""
	<h2>Monthly Expense Report</h2>
	<p>Total Expenses: <b>${total:.2f}</b></p>
	<table border='1' cellpadding='6' style='border-collapse:collapse;'>
		<tr><th>Name</th><th>Amount</th><th>Category</th><th>Date</th></tr>
		{''.join(f'<tr><td>{e.get('name','')}</td><td>{e.get('amount','')}</td><td>{e.get('category','')}</td><td>{e.get('date','')}</td></tr>' for e in expenses)}
	</table>
	"""
	msg = MIMEMultipart('alternative')
	msg['Subject'] = 'Your Monthly Expense Report'
	msg['From'] = sender_email
	msg['To'] = recipient_email
	msg.attach(MIMEText(html, 'html'))
	try:
		server = smtplib.SMTP(smtp_server, smtp_port)
		server.starttls()
		server.login(sender_email, sender_password)
		server.sendmail(sender_email, recipient_email, msg.as_string())
		server.quit()
		return 'Report sent successfully!'
	except Exception as e:
		return f'Error sending email: {e}'
# Admin dashboard route
@app.route('/admin')
def admin_dashboard():
	from collections import defaultdict
	category_data = defaultdict(float)
	for e in expenses:
		cat = e.get('category', 'Other')
		category_data[cat] += float(e.get('amount', 0))
	return render_template('admin.html', total=total, category_data=dict(category_data), expenses=expenses)
import csv
from flask import Response
# CSV export route
@app.route('/export_csv')
def export_csv():
	expenses = load_expenses()
	month = request.args.get('month')
	year = request.args.get('year')
	filtered_expenses = expenses
	if month and year:
		filtered_expenses = [e for e in expenses if e.get('date', '').startswith(f'{year}-{month.zfill(2)}')]
	def generate():
		data = [['Name', 'Amount', 'Category', 'Date']]
		for e in filtered_expenses:
			data.append([
				e.get('name', ''),
				e.get('amount', ''),
				e.get('category', ''),
				e.get('date', '')
			])
		output = []
		writer = csv.writer(output)
		for row in data:
			writer.writerow(row)
		return '\n'.join([','.join(map(str, row)) for row in data])
	return Response(generate(), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=expenses.csv"})

from flask import Flask, render_template, request, redirect, url_for, session, flash
from auth import load_users, save_users
from werkzeug.security import generate_password_hash, check_password_hash

import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this in production


DATA_FILE = 'expenses.json'

def load_expenses():
	if os.path.exists(DATA_FILE):
		with open(DATA_FILE, 'r') as f:
			try:
				return json.load(f)
			except json.JSONDecodeError:
				return []
	return []

def save_expenses(expenses):
	with open(DATA_FILE, 'w') as f:
		json.dump(expenses, f)


@app.route('/')
def index():
	expenses = load_expenses()
	# Prepare overview data for chart
	income = [0]*12
	outcome = [0]*12
	for e in expenses:
		try:
			m = int(e.get('date', '2026-01-01')[5:7]) - 1
			amt = float(e.get('amount', 0))
			income[m] += amt
		except Exception:
			pass
	overview_data = {'income': income, 'outcome': outcome}
	# Most spent category logic
	from collections import Counter
	if expenses:
		cat_counter = Counter(e.get('category', 'Other') for e in expenses)
		most_spent_category = cat_counter.most_common(1)[0][0]
	else:
		most_spent_category = 'N/A'
	from datetime import datetime
	return render_template('dashboard.html', expenses=expenses, overview_data=overview_data, datetime=datetime, most_spent_category=most_spent_category)


# Analytics page
@app.route('/analytics')
def analytics():
	return render_template('analytics.html')

# Wallet page
@app.route('/wallet')
def wallet():
	return render_template('wallet.html')

# Accounts page
import uuid
from werkzeug.utils import secure_filename
@app.route('/accounts', methods=['GET', 'POST'])
def accounts():
	profile_pic = None
	if request.method == 'POST':
		file = request.files.get('avatar')
		if file and file.filename:
			ext = file.filename.rsplit('.', 1)[-1].lower()
			filename = f"{uuid.uuid4().hex}.{ext}"
			filepath = os.path.join('static', 'profile_pics', secure_filename(filename))
			file.save(filepath)
			profile_pic = filename
	return render_template('accounts.html', profile_pic=profile_pic)

# Settings page
@app.route('/settings')
def settings():
	return render_template('settings.html')

# Help Centre page
@app.route('/help')
def help_centre():
	return render_template('help.html')

@app.route('/add', methods=['POST'])
def add_expense():
	expenses = load_expenses()
	print('Form data:', dict(request.form))  # Debug: print form data
	name = request.form.get('name')
	amount = request.form.get('amount')
	category = request.form.get('category')
	date = request.form.get('date') or datetime.now().strftime('%Y-%m-%d')
	if name and amount and category:
		expenses.append({'name': name, 'amount': float(amount), 'category': category, 'date': date})
		save_expenses(expenses)
		flash('Expense added successfully!', 'success')
	else:
		flash('Please fill all fields.', 'danger')
	return redirect(url_for('index'))

@app.route('/delete/<int:index>', methods=['POST'])
def delete_expense(index):
	expenses = load_expenses()
	if 0 <= index < len(expenses):
		expenses.pop(index)
		save_expenses(expenses)
	return redirect(url_for('index'))

@app.route('/session_test')
def session_test():
    import random
    if 'test' not in session:
        session['test'] = random.randint(1000, 9999)
        return f"Session test value set: {session['test']} (refresh to check persistence)"
    else:
        return f"Session test value is: {session['test']} (session is working)"

if __name__ == '__main__':
	app.run(debug=True)
