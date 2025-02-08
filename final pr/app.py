import os
from functools import wraps  # Додано імпорт wraps
from cs50 import SQL
from flask import Flask, jsonify, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure database
db = SQL("sqlite:///gameshop.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def apology(message, code=400):
    """Renders error message"""
    return render_template("apology.html", message=message, code=code)

@app.route("/")
def index():
    search_query = request.args.get("search", "").strip()
    selected_tag = request.args.get("tag")

    # Базовий запит
    query = """
        SELECT DISTINCT g.*
        FROM games g
    """
    params = []

    where_clauses = []

    if selected_tag:
        query += " JOIN game_tags gt ON g.id_game = gt.id_game JOIN tags t ON gt.id_tag = t.id_tag"
        where_clauses.append("t.tag_name = ?")
        params.append(selected_tag)

    if search_query:
        where_clauses.append("g.title LIKE ?")
        params.append(f"%{search_query}%")

    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)

    # Передаємо параметри правильно, навіть якщо вони порожні
    game_info = db.execute(query, *params)  # Розпаковуємо список `params`

    # Отримуємо всі доступні теги
    tags = db.execute("SELECT tag_name FROM tags ORDER BY tag_name")

    return render_template("index.html", game_info=game_info, tags=tags, selected_tag=selected_tag)



@app.route("/contacts")
@login_required
def contacts():
    return render_template("contacts.html")

@app.route("/cart")
@login_required
def cart():
    user_id = session.get("user_id")

    cart_items = db.execute("""
        SELECT games.id_game, games.title, games.price, games.image_url, cart_items.quantity
        FROM cart_items
        JOIN games ON cart_items.id_game = games.id_game
        WHERE cart_items.id_user = ?
    """, (user_id,))

    total_price = sum(item["price"] for item in cart_items)

    return render_template("cart.html", cart_items=cart_items, total_price=total_price)

@app.route("/remove_from_cart/<int:game_id>", methods=["POST"])
@login_required
def remove_from_cart(game_id):
    try:
        db.execute("DELETE FROM cart_items WHERE id_user = ? AND id_game = ?", session["user_id"], game_id)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/checkout", methods=["POST"])
@login_required
def checkout():
    try:
        user_id = session["user_id"]

        # Додаємо всі ігри з кошика в бібліотеку користувача
        db.execute("""
            INSERT OR IGNORE INTO user_games (id_user, id_game)
            SELECT id_user, id_game FROM cart_items WHERE id_user = ?
        """, user_id)

        # Очищаємо кошик
        db.execute("DELETE FROM cart_items WHERE id_user = ?", user_id)

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return apology("must provide username and password", 403)

        rows = db.execute("SELECT * FROM users WHERE nickname = ?", username)

        if len(rows) != 1 or not check_password_hash(rows[0]["password_hash"], password):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id_user"]
        return redirect("/")

    return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")

@app.route("/library")
@login_required
def library():
    user_id = session.get("user_id")  # Безпечний доступ
    search_query = request.args.get("q", "").strip()

    print(f"User ID: {user_id}")  # Перевірка, чи є user_id
    print(f"Search Query: {search_query}")  # Перевірка запиту

    if not user_id:
        return redirect(url_for("login"))  # Якщо user_id немає – перенаправити на логін

    query = """
        SELECT games.id_game, games.title, games.price, games.image_url
        FROM user_games
        JOIN games ON user_games.id_game = games.id_game
        WHERE user_games.id_user = ?
    """

    params = [user_id]

    if search_query:
        query += " AND games.title LIKE ?"
        params.append(f"%{search_query}%")

    print(f"SQL Query: {query}")  # Друк SQL-запиту

    try:
        user_games = db.execute(query, params)
    except Exception as e:
        print(f"Database Error: {e}")  # Вивід помилки
        user_games = []

    return render_template("library.html", user_games=user_games)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_repeat = request.form.get("password_repeat")

        if not username or not password or not password_repeat:
            return render_template("register.html", error="All fields are required.")

        if password != password_repeat:
            return render_template("register.html", error="Passwords do not match.")

        existing_user = db.execute("SELECT * FROM users WHERE nickname = ?", username)

        if existing_user:
            return render_template("register.html", error="Username already exists.")

        password_hash = generate_password_hash(password)
        db.execute("INSERT INTO users (nickname, password_hash) VALUES (?, ?)",
                   username, password_hash)

        return redirect("/")

    return render_template("register.html")

@app.route("/game/<int:game_id>")
def game(game_id):
    try:
        # Get game information
        game = db.execute("SELECT * FROM games WHERE id_game = ?", game_id)
        if not game:
            return apology("Game not found", 404)
        game = game[0]

        # Get reviews
        reviews = db.execute("""
            SELECT r.*, u.nickname
            FROM reviews r
            JOIN users u ON r.id_user = u.id_user
            WHERE r.id_game = ?
            ORDER BY r.review_date DESC
        """, game_id)

        # Calculate average rating
        avg_rating = db.execute("""
            SELECT AVG(rating) as avg_rating
            FROM reviews
            WHERE id_game = ?
        """, game_id)[0]['avg_rating']

        # Initialize user-specific variables
        in_cart = False
        user_owns_game = False
        user_reviewed = False

        # Check user-specific information only if user is logged in
        if session.get("user_id"):
            # Check if game is in cart
            in_cart = db.execute("""
                SELECT quantity FROM cart_items
                WHERE id_user = ? AND id_game = ?
            """, session["user_id"], game_id)

            # Check if user owns the game
            user_owns_game = db.execute("""
                SELECT 1 FROM user_games
                WHERE id_user = ? AND id_game = ?
            """, session["user_id"], game_id)

            # Check if user has reviewed the game
            user_reviewed = db.execute("""
                SELECT 1 FROM reviews
                WHERE id_user = ? AND id_game = ?
            """, session["user_id"], game_id)

        return render_template("game.html",
                             game=game,
                             reviews=reviews,
                             avg_rating=avg_rating,
                             user_owns_game=bool(user_owns_game),
                             user_reviewed=bool(user_reviewed),
                             in_cart=bool(in_cart),
                             is_logged_in=bool(session.get("user_id")))
    except Exception as e:
        return apology(f"Database error occurred: {e}", 500)


@app.route("/add_to_cart/<int:game_id>", methods=["POST"])
@login_required
def add_to_cart(game_id):
    try:
        existing_item = db.execute("""
            SELECT quantity FROM cart_items
            WHERE id_user = ? AND id_game = ?
        """, session["user_id"], game_id)

        if existing_item:
            db.execute("""
                UPDATE cart_items
                SET quantity = quantity + 1
                WHERE id_user = ? AND id_game = ?
            """, session["user_id"], game_id)
        else:
            db.execute("""
                INSERT INTO cart_items (id_user, id_game, quantity)
                VALUES (?, ?, 1)
            """, session["user_id"], game_id)

        flash("Game added to cart successfully!")
    except Exception as e:
        flash(f"Error occurred while adding game to cart: {e}")
    return redirect(f"/game/{game_id}")


@app.route("/review/<int:game_id>", methods=["POST"])
@login_required
def add_review(game_id):
    rating = request.form.get("rating")
    review_text = request.form.get("review_text")

    if not rating or not review_text:
        flash("Please provide both rating and review text")
        return redirect(f"/game/{game_id}")

    try:
        db.execute("""
            INSERT INTO reviews (id_user, id_game, review_text, rating)
            VALUES (?, ?, ?, ?)
        """, (session["user_id"], game_id, review_text, rating))
        flash("Review added successfully!")
    except Exception as e:
        flash(f"Error occurred while adding review: {e}")
    return redirect(f"/game/{game_id}")

