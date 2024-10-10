from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, quote

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Display portfolio"""
    userId = int(session["user_id"])
    username = db.execute("SELECT username FROM users WHERE id = ?", userId)[0]["username"]
    userStocks = db.execute("SELECT * FROM stocks WHERE user_id = ?", userId)
    stocks = []
    total = 0

    for row in userStocks:
        stockData = quote(row["symbol"])
        ownedShares = row["shares"]
        price = stockData["price"]
        sharesValue = price * ownedShares
        total += sharesValue
        stocks.append(
            {
                "symbol": stockData["symbol"],
                "name": stockData["name"],
                "shares": ownedShares,
                "price": round(price, 2),
                "total": round(sharesValue, 2),
                "logo": stockData["logo"]
            }
        )

    return render_template("index.html", stocks=stocks, total=round(total, 2), username=username)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            flash("Must provide a username.", "warning")
            return redirect('/register')

        # Ensure password was submitted
        elif not password or not confirmation:
            flash("Must provide a password.", "warning")
            return redirect('/register')

        # Query database for username
        user = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username doesn't exist
        if user:
            flash("Username already exists.", "danger")
            return redirect('/register')

        # Ensure passwords match
        if password != confirmation:
            flash("Passwords do not match.", "danger")
            return redirect('/register')

        # Hashes the password
        hash = generate_password_hash(password)

        # INSERT the new user into db
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)

        flash("Registered successfully, you can now log in.", "success")
        return redirect('/login')


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            flash("Must provide a username.", "warning")
            return redirect('/login')

        # Ensure password was submitted
        elif not password:
            flash("Must provide a password.", "warning")
            return redirect('/login')

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], password
        ):
            flash("Invalid username and/or password.", "danger")
            return redirect("/")

        # Clear session
        session.clear()

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/profile", methods=["POST"])
@login_required
def porfile():
    userId = session["user_id"]
    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    # Ensure data was submitted
    if not username and (not password or not confirmation):
        flash("Invalid data.", "warning")
        return redirect("/")

    # Query database for user
    user = db.execute("SELECT * FROM users WHERE id = ?", userId)
    if not user:
        flash("User not found", "danger")
        return redirect("/")

    # Change username
    if username:
        # Query database for username
        users = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username doesn't exist
        if (users):
            flash("Username already exists.", "warning")
            return redirect("/")

        # UPDATE username
        db.execute("UPDATE users SET username = ? WHERE id = ?", username, userId)

        flash("Username updated.", "success")
    elif password:
        # Ensure passwords match
        if password != confirmation:
            flash("Passwords do not match.", "danger")
            return redirect('/')

        # Hashes the password
        hash = generate_password_hash(password)

        # UPDATE password
        db.execute("UPDATE users SET hash = ? WHERE id = ?", hash, userId)

        flash("Password updated.", "success")

    return redirect("/")


@app.route("/add", methods=["POST"])
@login_required
def add():
    """Add shares of stock"""
    userId = session["user_id"]
    symbol = request.form.get("symbol")
    shares = request.form.get("shares")

    # Ensure values are valid
    if not symbol or not shares or not shares.isdigit():
        flash("Invalid symbol or shares.", "warning")
        return redirect("/")

    # Ensure the value is not negative or zero
    shares = int(shares)
    if shares < 1:
        flash("Invalid symbol or shares.", "warning")
        return redirect("/")

    # Ensure the symbol is valid
    symbol = symbol.upper()
    result = quote(symbol)
    if not result:
        flash("Symbol not found.", "warning")
        return redirect("/")

    # Get curent shares
    stocks = db.execute("SELECT * FROM stocks WHERE user_id = ? AND symbol = ?", userId, symbol)
    if stocks:
        flash("This symbol is already in your portfolio. Use the table to edit the shares.", "info")
        return redirect("/")

    # INSERT new row
    db.execute("INSERT INTO stocks (symbol, shares, user_id) VALUES(?, ?, ?)", symbol, shares, userId)

    return redirect("/")

@app.route("/delete", methods=["post"])
@login_required
def delete():
    """Delete portfolio"""
    userId = session["user_id"]

    # Get curent shares
    stocks = db.execute("SELECT * FROM stocks WHERE user_id = ?", userId)
    if stocks:
        # DELETE
        db.execute("DELETE FROM stocks WHERE user_id = ?", userId)

    return redirect("/")


@app.route("/edit", methods=["POST"])
@login_required
def edit():
    """Edit shares"""
    userId = int(session["user_id"])
    data = request.form
    stocks = {}

    # Validate data
    for item in data:
        print(item, data[item])
        symbol = item.upper()
        shares = data[item]

        # Ensure data is valid
        if not symbol or not shares or not shares.isdigit():
            flash("Invalid data.", "danger")
            return redirect("/")

        # Ensure the value is not negative
        shares = int(shares)
        if shares < 0:
            flash("Invalid data.", "danger")
            return redirect("/")

        # Ensure the symbol is valid
        result = quote(symbol)
        if not result:
            flash("Symbol not found.", "warning")
            return redirect("/")

        # If pass all validation add to stocks
        stocks[symbol] = shares

    # Query the data base to update portfolio
    for stock in stocks:
        symbol = stock
        shares = stocks[stock]

        # Get stocks
        curentStocks = db.execute("SELECT * FROM stocks WHERE user_id = ? AND symbol = ?", userId, symbol)
        if len(curentStocks) == 0:
            # INSERT row
            db.execute("INSERT INTO stocks (symbol, shares, user_id) VALUES(?, ?, ?)", symbol, shares, userId)
        elif shares == 0:
            # DELETE row
            db.execute("DELETE FROM stocks WHERE user_id = ? AND symbol = ?", userId, symbol)
        else:
            # UPDATE row
            db.execute(
                "UPDATE stocks SET shares = ? WHERE user_id = ? AND symbol = ?",
                shares,
                userId,
                symbol,
            )

    return redirect("/")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
