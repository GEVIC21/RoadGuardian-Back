from flask import render_template,request,Blueprint
from charity.models import BlogPost
from flask import Flask, render_template, redirect, request, url_for
import stripe


public_key = "pk_test_TYooMQauvdEDq54NiTphI7jx"
stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"

core = Blueprint('core',__name__)


@core.route('/')
def index():
    '''
    This is the home page view. Notice how it uses pagination to show a limited
    number of posts by limiting its query size and then calling paginate.
    '''
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=10)
    return render_template('index.html',blog_posts=blog_posts,public_key=public_key)

@core.route('/info')
def info():
    '''
    Example view of any other "core" page. Such as a info page, about page,
    contact page. Any page that doesn't really sync with one of the models.
    '''
    return render_template('info.html')


@core.route('/thankyou')
def thankyou():
   
    return render_template('thankyou.html')

@core.route('/payement', methods=['GET', 'POST'])
def payement():
    customer = stripe.Customer.create(
        email= request.form["stripeEmail"], 
        source= request.form['stripeToken']
        )
    
    charge = stripe.Charge.create(
        customer=customer.id,
        amount=1000,
        currency='usd',
        description='Donation'
    )
   
    return redirect(url_for('core.thankyou'))
