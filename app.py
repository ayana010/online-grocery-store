from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Used for session (cart data is stored here)

# Connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('db/store.db')
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn

# Show product list
@app.route('/')
def index():
    search_query = request.args.get('q', '')
    selected_category = request.args.get('category', '')

    conn = get_db_connection()

    query = "SELECT * FROM products WHERE 1=1"
    params = []

    if search_query:
        query += " AND product_name LIKE ?"
        params.append(f"%{search_query}%")

    if selected_category:
        query += " AND category = ?"
        params.append(selected_category)

    products = conn.execute(query, params).fetchall()
    categories = conn.execute("SELECT DISTINCT category FROM products").fetchall()
    conn.close()

    return render_template('index.html', products=products, categories=categories, search_query=search_query, selected_category=selected_category)



# Add a product to the shopping cart
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        cart[product_id_str] += 1  # If already in cart, increase quantity
    else:
        cart[product_id_str] = 1   # Else, add it with quantity 1

    session['cart'] = cart
    return redirect(url_for('index'))

# Show the shopping cart
@app.route('/cart')
def view_cart():
    cart = session.get('cart', {})
    conn = get_db_connection()
    items = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = conn.execute(
            'SELECT * FROM products WHERE product_id = ?', (product_id,)
        ).fetchone()

        if product:
            subtotal = product['unit_price'] * quantity
            items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
            total_price += subtotal

    conn.close()
    return render_template('cart.html', items=items, total_price=total_price)


# Checkout form route (GET: show form, POST: handle form)
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        state = request.form.get('state')

        # 入力バリデーション
        if not all([name, email, phone, address, state]):
            return render_template('checkout.html', error="Please fill in all fields.")

        cart = session.get('cart', {})
        conn = get_db_connection()
        failed_items = []

        # 在庫チェック
        for product_id, quantity in cart.items():
            product = conn.execute('SELECT * FROM products WHERE product_id = ?', (product_id,)).fetchone()
            if product and quantity > product['in_stock']:
                failed_items.append(product['product_name'])

        if failed_items:
            conn.close()
            return redirect(url_for('view_cart'))

        # 在庫更新
        for product_id, quantity in cart.items():
            conn.execute(
                'UPDATE products SET in_stock = in_stock - ? WHERE product_id = ?',
                (quantity, product_id)
            )

        conn.commit()
        conn.close()

        # カートクリア
        session.pop('cart', None)

        # 確認ページへ
        return render_template('confirmation.html', name=name, email=email)

    return render_template('checkout.html')


# Route to remove a product from the cart using its product ID
@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        del cart[product_id_str]  # Remove item from cart
        session['cart'] = cart

    return redirect(url_for('view_cart'))

# Route to increase quantity of an item in the cart
@app.route('/increase_quantity/<int:product_id>')
def increase_quantity(product_id):
    cart = session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        cart[product_id_str] += 1
        session['cart'] = cart

    return redirect(url_for('view_cart'))

# Route to decrease quantity of an item in the cart
@app.route('/decrease_quantity/<int:product_id>')
def decrease_quantity(product_id):
    cart = session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        if cart[product_id_str] > 1:
            cart[product_id_str] -= 1
        else:
            del cart[product_id_str]  # Remove item if quantity is 1
        session['cart'] = cart

    return redirect(url_for('view_cart'))

@app.context_processor
def inject_helpers():
    def get_product(product_id):
        conn = get_db_connection()
        product = conn.execute('SELECT * FROM products WHERE product_id = ?', (product_id,)).fetchone()
        conn.close()
        return product
    return dict(get_product=get_product)

@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('view_cart'))


# Start the app
if __name__ == '__main__':
    app.run(debug=True)
