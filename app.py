import requests
from flask import Flask, render_template, request, url_for
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, DateField


app = Flask(__name__)
app.config["SECRET_KEY"]="AZBYCXDW"
app.config["MONGO_URI"] = 'mongodb+srv://Carl:1234@cluster1.owuoy.mongodb.net/expenses?ssl=true&ssl_cert_reqs=CERT_NONE'
mongo = PyMongo(app)

def currency_converter(cost,currency):
    url="http://api.currencylayer.com/live?access_key=335a37605fffc10adb1ee45f6a95d631"
    response = requests.get(url).json()
    # & currencies = JPY, EUR, ARS
    # & from = currency()
    # & to = GBP
    # return converted_cost


insert = mongo.db.expenses

class expenseForm(FlaskForm):
    description = StringField('Description')
    category = SelectField('Category', choices=[('', ''), ('electric_car', 'Electric Car'), ('rocket_fuel', 'Rocket Fuel'), ('mars', 'going to Mars')])
    cost = DecimalField('Cost')
    currency = SelectField('Currency', choices=[('',''), ('EUR', 'European Dollar'), ('ARS', 'Argentinian Peso'), ('JPY', 'Japanese Yen')])
    date = DateField('Date', format='%m-%d-%Y')



def get_total_expenses():
   expenses_cat = mongo.db.expenses.find()
   total_cost_cat = 0
   for i in expenses_cat:
       total_cost_cat += float(i["cost"])


@app.route('/')
def index():
    my_expenses = mongo.db.expenses.find()
    total_cost=0
    for i in my_expenses:
        total_cost += float(i["cost"])

    return render_template("index.html", expenses=total_cost)


@app.route('/addExpenses', methods=["GET", "POST"])
def addExpenses():
    expense_form = expenseForm(request.form)
    if request.method == "POST":
        description = request.form['description']
        category = request.form['category']
        cost = request.form['cost']
        date = request.form['date']
        insert.insert_one({'description':description, "category":category, "cost":cost,"date":date})
        return render_template("expenseAdded.html")
    return render_template("addExpenses.html",form=expense_form)






app.run()