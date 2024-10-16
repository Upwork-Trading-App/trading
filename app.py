from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import re
from models import db, Users, Portfolio, PortfolioStock, Stock, Order, Transaction, CashTransaction

app = Flask(__name__)
    
app.config['SECRET_KEY'] = 'eGRklsAtNW6FQ48egn9bExF3WFLH2P'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/trading'
  
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
   
bcrypt = Bcrypt(app)
db.init_app(app)
migrate = Migrate(app, db)  

with app.app_context():
    db.create_all()

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST':
        fullname = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        user_exists = Users.query.filter_by(email=email).first() is not None
        
        if user_exists:
            message = 'Email already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address!'
        elif not fullname or not username or not password or not email:
            message = 'Please fill out the form!'
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = Users(full_name=fullname, email=email, username=username, password_hash=hashed_password, role='customer')
            db.session.add(new_user)
            db.session.commit()
            message = 'You have successfully registered!'
            return redirect(url_for('login'))  # Redirect to login after registration success

    return render_template('auth/register.html', message=message)


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email == '' or password == '':
            message = 'Please enter email and password!'
        else:
            user = Users.query.filter_by(email=email).first()
            
            if user is None:
                message = 'Please enter correct email / password!'
            else:
                if not bcrypt.check_password_hash(user.password_hash, password):
                    message = 'Please enter correct email and password!'
                else:    
                    session['loggedin'] = True
                    session['userid'] = user.id
                    session['name'] = user.full_name
                    session['email'] = user.email
                    message = 'Logged in successfully!'
                    return redirect(url_for('dashboard'))

    return render_template('auth/login.html', message=message)

@app.route("/", methods =['GET', 'POST'])
def dashboard():
    if 'loggedin' in session:        
        return render_template("dashboard.html")
    return redirect(url_for('login'))   
 
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))


### USERS
@app.route('/users', methods=['GET'])
def list_users():
    if 'loggedin' in session:
        users = Users.query.all()
        return render_template('users/list.html', users=users)
    return redirect(url_for('login'))

@app.route('/users/view/<int:user_id>')
def view_user(user_id):
    user = Users.query.get_or_404(user_id)
    return render_template('users/view.html', user=user)

@app.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = Users.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.full_name = request.form['full_name']
        user.username = request.form['username']
        user.email = request.form['email']
        user.role = request.form['role']
        
        new_password = request.form['password']
        if new_password:  
            hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            user.password_hash = hashed_password  
        
        db.session.commit()
        
        return redirect(url_for('list_users'))
    
    return render_template('users/edit.html', user=user)

@app.route('/users/delete/<int:user_id>')
def delete_user(user_id):
    user = Users.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('list_users'))


### PORTFOLIOS
@app.route('/portfolio/create', methods=['GET', 'POST'])
def create_portfolio():
    users = Users.query.all()  # Get all users to show in the dropdown
    if request.method == 'POST':
        user_id = request.form['user_id']
        cash_balance = float(request.form['cash_balance'])
        total_value = float(request.form['total_value'])

        portfolio = Portfolio(user_id=user_id, cash_balance=cash_balance, total_value=total_value)
        db.session.add(portfolio)
        db.session.commit()

        return redirect(url_for('list_portfolios'))

    return render_template('portfolio/create.html', action='Create', users=users)


@app.route('/portfolios')
def list_portfolios():
    portfolios = Portfolio.query.all()
    return render_template('portfolio/list.html', portfolios=portfolios)

@app.route('/portfolio/edit/<int:id>', methods=['GET', 'POST'])
def edit_portfolio(id):
    portfolio = Portfolio.query.get_or_404(id)
    
    if request.method == 'POST':
        portfolio.cash_balance = float(request.form['cash_balance'])
        portfolio.total_value = float(request.form['total_value'])
        db.session.commit()

        return redirect(url_for('list_portfolios'))

    return render_template('portfolio/edit.html', portfolio=portfolio)

@app.route('/portfolio/delete/<int:id>')
def delete_portfolio(id):
    portfolio = Portfolio.query.get_or_404(id)
    db.session.delete(portfolio)
    db.session.commit()
    
    return redirect(url_for('list_portfolios'))


### PORTFOLIO STOCK
@app.route('/portfolio_stock/create', methods=['GET', 'POST'])
def create_portfolio_stock():
    if request.method == 'POST':
        portfolio_id = request.form['portfolio_id']
        stock_id = request.form['stock_id']
        quantity = int(request.form['quantity'])
        average_price = float(request.form['average_price'])

        portfolio_stock = PortfolioStock(portfolio_id=portfolio_id, stock_id=stock_id, quantity=quantity, average_price=average_price)
        db.session.add(portfolio_stock)
        db.session.commit()

        return redirect(url_for('list_portfolio_stocks'))

    return render_template('portfolio_stock/create.html')

@app.route('/portfolio_stocks')
def list_portfolio_stocks():
    portfolio_stocks = PortfolioStock.query.all()
    return render_template('portfolio_stock/list.html', portfolio_stocks=portfolio_stocks)

@app.route('/portfolio_stock/edit/<int:id>', methods=['GET', 'POST'])
def edit_portfolio_stock(id):
    portfolio_stock = PortfolioStock.query.get_or_404(id)
    
    if request.method == 'POST':
        portfolio_stock.quantity = int(request.form['quantity'])
        portfolio_stock.average_price = float(request.form['average_price'])
        db.session.commit()

        return redirect(url_for('list_portfolio_stocks'))

    return render_template('portfolio_stock/edit.html', portfolio_stock=portfolio_stock)

@app.route('/portfolio_stock/delete/<int:id>')
def delete_portfolio_stock(id):
    portfolio_stock = PortfolioStock.query.get_or_404(id)
    db.session.delete(portfolio_stock)
    db.session.commit()
    
    return redirect(url_for('list_portfolio_stocks'))


### STOCK
@app.route('/stock/create', methods=['GET', 'POST'])
def create_stock():
    if request.method == 'POST':
        ticker = request.form['ticker']
        company_name = request.form['company_name']
        volume = int(request.form['volume'])
        initial_price = float(request.form['initial_price'])
        current_price = float(request.form['current_price'])
        market_cap = float(request.form['market_cap'])

        stock = Stock(ticker=ticker, company_name=company_name, volume=volume, initial_price=initial_price, current_price=current_price, market_cap=market_cap)
        db.session.add(stock)
        db.session.commit()

        return redirect(url_for('list_stocks'))

    return render_template('stock/create.html')

@app.route('/stocks')
def list_stocks():
    stocks = Stock.query.all()
    return render_template('stock/list.html', stocks=stocks)


@app.route('/stock/edit/<int:id>', methods=['GET', 'POST'])
def edit_stock(id):
    stock = Stock.query.get_or_404(id)
    
    if request.method == 'POST':
        stock.ticker = request.form['ticker']
        stock.company_name = request.form['company_name']
        stock.volume = int(request.form['volume'])
        stock.current_price = float(request.form['current_price'])
        stock.market_cap = float(request.form['market_cap'])
        db.session.commit()

        return redirect(url_for('list_stocks'))

    return render_template('stock/edit.html', stock=stock)

@app.route('/stock/delete/<int:id>')
def delete_stock(id):
    stock = Stock.query.get_or_404(id)
    db.session.delete(stock)
    db.session.commit()
    
    return redirect(url_for('list_stocks'))


### ORDER
@app.route('/order/create', methods=['GET', 'POST'])
def create_order():
    if request.method == 'POST':
        user_id = request.form['user_id']
        stock_id = request.form['stock_id']
        order_type = request.form['order_type']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        status = 'pending'  # Orders are created as pending initially

        order = Order(user_id=user_id, stock_id=stock_id, order_type=order_type, quantity=quantity, price=price, status=status)
        db.session.add(order)
        db.session.commit()

        return redirect(url_for('list_orders'))

    return render_template('order/create.html')

@app.route('/orders')
def list_orders():
    orders = Order.query.all()
    return render_template('order/list.html', orders=orders)

@app.route('/order/edit/<int:id>', methods=['GET', 'POST'])
def edit_order(id):
    order = Order.query.get_or_404(id)
    
    if request.method == 'POST':
        order.quantity = int(request.form['quantity'])
        order.price = float(request.form['price'])
        order.status = request.form['status']
        db.session.commit()

        return redirect(url_for('list_orders'))

    return render_template('order/edit.html', order=order)

@app.route('/order/delete/<int:id>')
def delete_order(id):
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    
    return redirect(url_for('list_orders'))


### TRANSACTION
@app.route('/transaction/create', methods=['GET', 'POST'])
def create_transaction():
    if request.method == 'POST':
        user_id = request.form['user_id']
        order_id = request.form['order_id']
        transaction_type = request.form['transaction_type']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        total = price * quantity

        transaction = Transaction(user_id=user_id, order_id=order_id, transaction_type=transaction_type, quantity=quantity, price=price, total=total)
        db.session.add(transaction)
        db.session.commit()

        return redirect(url_for('list_transactions'))

    return render_template('transaction/create.html')

@app.route('/transactions')
def list_transactions():
    transactions = Transaction.query.all()
    return render_template('transaction/list.html', transactions=transactions)

@app.route('/transaction/edit/<int:id>', methods=['GET', 'POST'])
def edit_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    
    if request.method == 'POST':
        transaction.quantity = int(request.form['quantity'])
        transaction.price = float(request.form['price'])
        transaction.total = transaction.quantity * transaction.price
        db.session.commit()

        return redirect(url_for('list_transactions'))

    return render_template('transaction/edit.html', transaction=transaction)

@app.route('/transaction/delete/<int:id>')
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()
    
    return redirect(url_for('list_transactions'))


### CASH TRANSACTION
@app.route('/cash_transaction/create', methods=['GET', 'POST'])
def create_cash_transaction():
    if request.method == 'POST':
        user_id = request.form['user_id']
        transaction_type = request.form['transaction_type']
        amount = float(request.form['amount'])

        cash_transaction = CashTransaction(user_id=user_id, transaction_type=transaction_type, amount=amount)
        db.session.add(cash_transaction)
        db.session.commit()

        return redirect(url_for('list_cash_transactions'))

    return render_template('cash_transaction/create.html')

@app.route('/cash_transactions')
def list_cash_transactions():
    cash_transactions = CashTransaction.query.all()
    return render_template('cash_transaction/list.html', cash_transactions=cash_transactions)

@app.route('/cash_transaction/edit/<int:id>', methods=['GET', 'POST'])
def edit_cash_transaction(id):
    cash_transaction = CashTransaction.query.get_or_404(id)
    
    if request.method == 'POST':
        cash_transaction.amount = float(request.form['amount'])
        db.session.commit()

        return redirect(url_for('list_cash_transactions'))

    return render_template('cash_transaction/edit.html', cash_transaction=cash_transaction)

@app.route('/cash_transaction/delete/<int:id>')
def delete_cash_transaction(id):
    cash_transaction = CashTransaction.query.get_or_404(id)
    db.session.delete(cash_transaction)
    db.session.commit()
    
    return redirect(url_for('list_cash_transactions'))




if __name__=='__main__':
    app.run(debug=True)