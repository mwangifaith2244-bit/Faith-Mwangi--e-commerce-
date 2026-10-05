from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "shop.db"

app = Flask(__name__)
app.secret_key = "change-this-secret-key"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            image TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            total REAL NOT NULL,
            payment_status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    count = conn.execute(
        "SELECT COUNT(*) FROM products"
    ).fetchone()[0]

    if count == 0:
        products = [
            (
                "Classic Sneakers",
                "Shoes",
                "Comfortable everyday sneakers.",
                2500,
                "css/classic-sneaker.jpg"
            ),
            (
                "Ladies Handbag",
                "Bags",
                "Stylish handbag for everyday use.",
                1800,
                "css/ladies-handbag.jpg"
            ),
            (
                "Cotton Hoodie",
                "Clothing",
                "Warm unisex cotton hoodie.",
                2200,
                "css/cotton-hoodie.jpg"
            ),
            (
                "Smart Watch",
                "Electronics",
                "Affordable smartwatch with useful daily features.",
                3500,
                "css/smart-watch.jpg"
            ),
            (
                "Wireless Earbuds",
                "Electronics",
                "Compact wireless earbuds.",
                2000,
                "css/wireless-earbuds.jpg"
            ),
            (
                "Denim Jacket",
                "Clothing",
                "Classic denim jacket.",
                3000,
                "css/denim-jacket.jpg"
            )
        ]

        conn.executemany(
            """
            INSERT INTO products
            (name, category, description, price, image)
            VALUES (?, ?, ?, ?, ?)
            """,
            products
        )

    image_updates = {
        "Classic Sneakers": "css/classic-sneaker.jpg",
        "Ladies Handbag": "css/ladies-handbag.jpg",
        "Cotton Hoodie": "css/cotton-hoodie.jpg",
        "Smart Watch": "css/smart-watch.jpg",
        "Wireless Earbuds": "css/wireless-earbuds.jpg",
        "Denim Jacket": "css/denim-jacket.jpg"
    }

    for name, image in image_updates.items():
        conn.execute(
            "UPDATE products SET image = ? WHERE name = ?",
            (image, name)
        )

    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = get_db()

    products = conn.execute(
        "SELECT * FROM products ORDER BY id DESC LIMIT 6"
    ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        products=products
    )


@app.route("/products")
def products():
    category = request.args.get("category", "")
    search = request.args.get("search", "")

    conn = get_db()

    if category:
        rows = conn.execute(
            """
            SELECT * FROM products
            WHERE category = ?
            ORDER BY id DESC
            """,
            (category,)
        ).fetchall()

    elif search:
        rows = conn.execute(
            """
            SELECT * FROM products
            WHERE name LIKE ?
            OR description LIKE ?
            ORDER BY id DESC
            """,
            (f"%{search}%", f"%{search}%")
        ).fetchall()

    else:
        rows = conn.execute(
            "SELECT * FROM products ORDER BY id DESC"
        ).fetchall()

    categories = conn.execute(
        "SELECT DISTINCT category FROM products"
    ).fetchall()

    conn.close()

    return render_template(
        "products.html",
        products=rows,
        categories=categories,
        selected_category=category,
        search=search
    )


@app.route("/product/<int:product_id>")
def product(product_id):
    conn = get_db()

    item = conn.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,)
    ).fetchone()

    conn.close()

    if item is None:
        flash("Product not found.")
        return redirect(url_for("products"))

    return render_template(
        "product.html",
        product=item
    )


def cart_items():
    cart = session.get("cart", {})

    if not cart:
        return [], 0

    ids = list(cart.keys())
    placeholders = ",".join(["?"] * len(ids))

    conn = get_db()

    rows = conn.execute(
        f"""
        SELECT * FROM products
        WHERE id IN ({placeholders})
        """,
        ids
    ).fetchall()

    conn.close()

    items = []
    total = 0

    for row in rows:
        qty = int(cart[str(row["id"])])
        subtotal = row["price"] * qty

        items.append({
            "product": row,
            "quantity": qty,
            "subtotal": subtotal
        })

        total += subtotal

    return items, total


@app.route("/cart")
def cart():
    items, total = cart_items()

    return render_template(
        "cart.html",
        items=items,
        total=total
    )


@app.route("/cart/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    quantity = max(
        1,
        int(request.form.get("quantity", 1))
    )

    cart = session.get("cart", {})

    key = str(product_id)

    cart[key] = int(
        cart.get(key, 0)
    ) + quantity

    session["cart"] = cart

    flash("Product added to your cart.")

    return redirect(
        request.referrer or url_for("products")
    )


@app.route("/cart/remove/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", {})

    cart.pop(
        str(product_id),
        None
    )

    session["cart"] = cart

    return redirect(
        url_for("cart")
    )


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    items, total = cart_items()

    if not items:
        flash("Your cart is empty.")

        return redirect(
            url_for("products")
        )

    if request.method == "POST":
        name = request.form["name"].strip()
        phone = request.form["phone"].strip()
        address = request.form["address"].strip()

        if not name or not phone or not address:
            flash("Please fill in all checkout details.")

            return render_template(
                "checkout.html",
                items=items,
                total=total
            )

        conn = get_db()

        cur = conn.execute(
            """
            INSERT INTO orders
            (
                customer_name,
                phone,
                address,
                total,
                payment_status
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                name,
                phone,
                address,
                total,
                "PAID - DEMO MPESA"
            )
        )

        order_id = cur.lastrowid

        conn.commit()
        conn.close()

        session["cart"] = {}

        return render_template(
            "success.html",
            order_id=order_id,
            total=total,
            phone=phone,
            name=name
        )

    return render_template(
        "checkout.html",
        items=items,
        total=total
    )


@app.route("/orders")
def orders():
    conn = get_db()

    rows = conn.execute(
        """
        SELECT * FROM orders
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    return render_template(
        "orders.html",
        orders=rows
    )


@app.route("/admin")
def admin():
    conn = get_db()

    rows = conn.execute(
        """
        SELECT * FROM products
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    return render_template(
        "admin.html",
        products=rows
    )


@app.route("/admin/add", methods=["POST"])
def admin_add():
    name = request.form["name"].strip()
    category = request.form["category"].strip()
    description = request.form["description"].strip()
    price = float(request.form["price"])

    image = request.form.get(
        "image",
        "placeholder.jpg"
    ).strip()

    if not image:
        image = "placeholder.jpg"

    conn = get_db()

    conn.execute(
        """
        INSERT INTO products
        (name, category, description, price, image)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            name,
            category,
            description,
            price,
            image
        )
    )

    conn.commit()
    conn.close()

    flash("Product added.")

    return redirect(
        url_for("admin")
    )


@app.route(
    "/admin/delete/<int:product_id>",
    methods=["POST"]
)
def admin_delete(product_id):
    conn = get_db()

    conn.execute(
        "DELETE FROM products WHERE id = ?",
        (product_id,)
    )

    conn.commit()
    conn.close()

    flash("Product deleted.")

    return redirect(
        url_for("admin")
    )


@app.context_processor
def inject_cart_count():
    cart = session.get("cart", {})

    return {
        "cart_count": sum(
            int(q) for q in cart.values()
        )
    }


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
