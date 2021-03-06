"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken.
"""


from flask import Flask, request, render_template, make_response, session, flash, redirect, url_for, escape
import jinja2

import model


app = Flask(__name__)

# Need to use Flask sessioning features

app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def index():
    """Return homepage."""
    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melons = model.Melon.get_all()
    return render_template("all_melons.html",
                           melon_list=melons)


@app.route("/melon/<int:id>")
def show_melon(id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = model.Melon.get_by_id(id)
    print type(melon)
    print melon
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def shopping_cart():
    """Display content of shopping cart."""

    cart = {}
    current_cart = session.get('cart', [])
    all_melons_total = 0

    for melon_id in current_cart:

        melon = cart.setdefault(melon_id, {})

        if melon:
            melon['qty'] += 1

        else:
            melon_data = model.Melon.get_by_id(melon_id)

            melon['common_name'] = melon_data.common_name
            melon['unit_cost'] = melon_data.price
            melon['qty'] = 1

        print melon['qty']
        melon['melon_cost'] = melon['unit_cost'] * melon['qty']
        print melon['melon_cost']
        print all_melons_total

        all_melons_total += melon['unit_cost']
        print all_melons_total

    # Now, get a list of the all melons we've put into that dict
    cart = cart.values()

    return render_template("cart.html", cart=cart, order_total=all_melons_total)

@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Successfully added to cart'.
    """

    cart = session.setdefault('cart', [])

    cart.append(id)

    melon = model.Melon.get_by_id(id)
    print melon.common_name     

    flash("Successfully added to cart!")
    return redirect('/cart')


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    # TODO: Need to implement this!

    return "Oops! This needs to be implemented"


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True)
