from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# Home Page
@app.route('/')
def home():
    return render_template('index.html')


# Products Page
@app.route('/products')
def products():

    conn = get_db_connection()

    products = conn.execute(
        'SELECT * FROM products'
    ).fetchall()

    conn.close()

    return render_template(
        'products.html',
        products=products
    )


# Add Product
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():

    conn = get_db_connection()

    if request.method == 'POST':

        product_name = request.form['product_name']
        price = request.form['price']
        image = request.form['image']

        conn.execute(
            '''
            INSERT INTO products
            (product_name, price, image)
            VALUES (?, ?, ?)
            ''',
            (product_name, price, image)
        )

        conn.commit()
        conn.close()

        return redirect('/products')

    conn.close()

    return render_template('add_product.html')


# Edit Product
@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):

    conn = get_db_connection()

    product = conn.execute(
        'SELECT * FROM products WHERE product_id = ?',
        (id,)
    ).fetchone()

    if request.method == 'POST':

        product_name = request.form['product_name']
        price = request.form['price']
        image = request.form['image']

        conn.execute(
            '''
            UPDATE products
            SET product_name = ?,
                price = ?,
                image = ?
            WHERE product_id = ?
            ''',
            (product_name, price, image, id)
        )

        conn.commit()
        conn.close()

        return redirect('/products')

    conn.close()

    return render_template(
        'edit_product.html',
        product=product
    )


# Delete Product
@app.route('/delete_product/<int:id>')
def delete_product(id):

    conn = get_db_connection()

    conn.execute(
        'DELETE FROM products WHERE product_id = ?',
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/products')


# Customers Page
@app.route('/customers')
def customers():

    conn = get_db_connection()

    customers = conn.execute(
        'SELECT * FROM customers'
    ).fetchall()

    conn.close()

    return render_template(
        'customers.html',
        customers=customers
    )


# Add Customer
@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():

    conn = get_db_connection()

    if request.method == 'POST':

        customer_name = request.form['customer_name']
        phone = request.form['phone']

        conn.execute(
            '''
            INSERT INTO customers
            (customer_name, phone)
            VALUES (?, ?)
            ''',
            (customer_name, phone)
        )

        conn.commit()
        conn.close()

        return redirect('/customers')

    conn.close()

    return render_template('add_customer.html')


# Edit Customer
@app.route('/edit_customer/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):

    conn = get_db_connection()

    customer = conn.execute(
        'SELECT * FROM customers WHERE customer_id = ?',
        (id,)
    ).fetchone()

    if request.method == 'POST':

        customer_name = request.form['customer_name']
        phone = request.form['phone']

        conn.execute(
            '''
            UPDATE customers
            SET customer_name = ?,
                phone = ?
            WHERE customer_id = ?
            ''',
            (customer_name, phone, id)
        )

        conn.commit()
        conn.close()

        return redirect('/customers')

    conn.close()

    return render_template(
        'edit_customer.html',
        customer=customer
    )


# Delete Customer
@app.route('/delete_customer/<int:id>')
def delete_customer(id):

    conn = get_db_connection()

    conn.execute(
        'DELETE FROM customers WHERE customer_id = ?',
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/customers')


if __name__ == '__main__':
    app.run(debug=True)