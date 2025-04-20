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
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('index.html', products=products)

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
        address = request.form.get('address')

        # Check if any required field is missing
        if not name or not email or not address:
            error = "Please fill in all required fields."
            return render_template('checkout.html', error=error)

        # ↓↓↓ Stock update starts here ↓↓↓
        cart = session.get('cart', {})
        conn = get_db_connection()

        for product_id, quantity in cart.items():
            conn.execute(
            'UPDATE products SET in_stock = in_stock - ? WHERE product_id = ?',
            (quantity, product_id)
            )

        conn.commit()
        conn.close()
        # ↑↑↑ Stock updated in database ↑↑↑

        # Clear the cart
        session.pop('cart', None)

        # Show confirmation page
        return render_template('confirmation.html', name=name)

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



# Start the app
if __name__ == '__main__':
    app.run(debug=True)
