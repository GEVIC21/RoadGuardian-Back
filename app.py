from charity import app
from flask import Flask, render_template, redirect, request, url_for
import stripe


public_key = "pk_test_TYooMQauvdEDq54NiTphI7jx"
stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"

if __name__ == '__main__':
    app.run(debug=True)
