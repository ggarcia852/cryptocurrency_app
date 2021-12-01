from re import U
from app import app, db
from flask import render_template, redirect, url_for, flash
from app.forms import AddAssetForm, LoginForm, RegisterForm, SearchForm
from flask_login import login_user ,logout_user, current_user, login_required
from app.models import User, Wallet
import json
import requests
from datetime import datetime


local_currency = 'USD'
local_symbol = '$'

api_key = 'd0fe3ffb-ff96-4162-abe2-08b6a1b4b770'
headers = {'X-CMC_PRO_API_KEY': api_key, 'Accept': 'application/json', 'Accept-Encoding': 'deflate, gzip'}

base_url = 'https://pro-api.coinmarketcap.com'


@app.route('/')
def index():
    global_url = base_url + '/v1/global-metrics/quotes/latest?convert=' + local_currency

    request = requests.get(global_url, headers=headers)
    results = request.json()
    data = results['data']

    active = data['active_cryptocurrencies']

    last_update = data['last_updated']
    updated = datetime.strptime(last_update, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%H:%M %m/%d/%Y')

    eth_dom = data['eth_dominance']
    btc_dom = data['btc_dominance']

    total_vol_24hr = data['quote'][local_currency]['total_volume_24h']
    volume_change24 = data['quote'][local_currency]['total_volume_24h_yesterday_percentage_change']
    total_market_cap = data['quote'][local_currency]['total_market_cap']
    market_cap_change24 = data['quote'][local_currency]['total_market_cap_yesterday_percentage_change']

    total_market_cap = round(total_market_cap, 2)
    total_vol_24hr = round(total_vol_24hr, 2)
    market_cap_change24 = round(market_cap_change24, 2)
    volume_change24 = round(volume_change24, 2)

    eth_dom = round(eth_dom, 2)
    btc_dom = round(btc_dom, 2)

    total_market_cap_string = local_symbol + '{:,}'.format(total_market_cap)
    total_vol_24hr_string = local_symbol + '{:,}'.format(total_vol_24hr)
    
    form = SearchForm()
    if form.validate_on_submit():
        symbol = form.symbol.data.upper()

    return render_template('index.html', form=form, title='Home | Crypto~VRSE', last_update=updated, active=active, market_cap=total_market_cap_string, total_vol=total_vol_24hr_string, eth=eth_dom, btc=btc_dom, market_change=market_cap_change24, vol_change=volume_change24 )


@app.route('/register', methods=['GET', 'POST'])
def register():


    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data

        existing = User.query.filter_by(username=username).all()
        if existing:
            flash(f'The username {username} is already registered. Please try again.', 'danger')
            return redirect(url_for('register'))        

        new_user = User(name, username, email, password)
        db.session.add(new_user)
        db.session.commit()

        flash(f'Welcome, {name}! You have successfully created a new account. Please sign in to start building your wallet!', 'primary')
        return redirect(url_for('login'))


    search_form = SearchForm()
    if search_form.validate_on_submit():
        symbol = search_form.symbol.data.upper()
  

    return render_template('register.html', title = 'Create Account | Crypto~VRSE', form=form, search_form=search_form)


@app.route('/about')
def about():
    form = SearchForm()
    if form.validate_on_submit():
        symbol = form.symbol.data.upper()
    return render_template('about.html', title='About | Crypto~VRSE', form=form)


@app.route('/contact')
def contact():
    form = SearchForm()
    if form.validate_on_submit():
        symbol = form.symbol.data.upper()
    return render_template('contact.html', title='Contact | Crypto~VRSE', form=form)


@app.route('/my_account')
def my_account():
    return render_template('my_account.html', title='My Account | Crypto~VRSE')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash('Your username or password is incorrect', 'primary')
            return redirect(url_for('login'))

        login_user(user)
        flash(f'Hi, {user.name}- You have successfully logged in.', 'primary')
        return redirect(url_for('mywallet'))


    search_form = SearchForm()
    if search_form.validate_on_submit():
        symbol = search_form.symbol.data.upper()

    return render_template('login.html', title= 'Sign In | Crypto~VRSE', form=form, search_form=search_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/qutoes', methods=['GET','POST'])
def search():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        symbol = search_form.symbol.data.upper()
  
    url = base_url + '/v1/cryptocurrency/quotes/latest?convert=' + local_currency + '&symbol=' + symbol

    request = requests.get(url, headers=headers)
    results = request.json()
    data = results['data']

    
    coin = data[symbol]
    name = coin['name']
    symbol_2 = coin['symbol']

    last_update = coin['last_updated']
    updated = datetime.strptime(last_update, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%H:%M %m/%d/%Y')

    rank= coin['cmc_rank']
    price = coin['quote'][local_currency]['price']
    volume_24hr = coin['quote'][local_currency]['volume_24h']
    volume_change_24hr = coin['quote'][local_currency]['volume_change_24h']
    percent_change_1hr = coin['quote'][local_currency]['percent_change_1h']
    percent_change_24hr = coin['quote'][local_currency]['percent_change_24h']
    percent_change_7d = coin['quote'][local_currency]['percent_change_7d']
    market_cap = coin['quote'][local_currency]['market_cap']
    market_cap_dom = coin['quote'][local_currency]['market_cap_dominance']

    price = round(price, 6)
    percent_change_24hr = round(percent_change_24hr, 2)
    market_cap = round(market_cap, 2)

    price_string = ' {:,}'.format(price)
    percent_change_24hr_string = ' {:,}'.format(percent_change_24hr)
    market_cap_string = ' {:,}'.format(market_cap)



    ###### META  #######
    meta_url = base_url + '/v1/cryptocurrency/info?&symbol=' + symbol

    request_2 = requests.get(meta_url, headers=headers)
    results_2 = request_2.json()
    data = results_2['data']

    name = data[symbol]['name']
    desription = data[symbol]['description']
    logo = data[symbol]['logo']
    website = data[symbol]['urls']['website'][0]
    if data[symbol]['urls']['technical_doc']:
        white_paper = data[symbol]['urls']['technical_doc'][0]  
    else:
        white_paper = data[symbol]['urls']['website'][0]
    if data[symbol]['urls']['twitter']:
        twitter = data[symbol]['urls']['twitter'][0]
    else:
        twitter = 'https://twitter.com'
    if data[symbol]['urls']['reddit']:
        reddit = data[symbol]['urls']['reddit'][0]
    else: 
        reddit = 'https://www.reddit.com' 


    return render_template('quotes.html', form=search_form, symbol=coin, symbol_2=symbol_2, name=name, description=desription, logo=logo, website=website, twitter=twitter, reddit=reddit, white_paper=white_paper, 
            price=price_string, change24=percent_change_24hr_string, market_cap=market_cap_string,
            last_update=updated, volume_24hr=volume_24hr, volume_change_24hr=volume_change_24hr, percent_change_1hr=percent_change_1hr,
            percent_change_7d=percent_change_7d, market_cap_dom=market_cap_dom, rank=rank)


@app.route('/top100')
def top100():
    url = base_url + '/v1/cryptocurrency/listings/latest?convert=' + local_currency

    request = requests.get(url, headers=headers)
    results = request.json()
    data = results['data']

    last_update = data[0]['last_updated']
    updated = datetime.strptime(last_update, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%H:%M %m/%d/%Y')


    form = SearchForm()
    if form.validate_on_submit():
        symbol = form.symbol.data.upper()

    # date_added = data['date_added']
    # date_added_formatted = datetime.strptime(date_added, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%H:%M %m/%d/%Y')


    # for coin in data:
    #     name = coin['name']
    #     symbol = coin['symbol']
        # price = coin['quote'][local_currency]['price']
    #     percent_change_24hr = coin['quote'][local_currency]['percent_change_24h']
    #     market_cap = coin['quote'][local_currency]['market_cap']

        # price = round(price, 2)
    #     percent_change_24hr = round(percent_change_24hr, 2)
    #     market_cap = round(market_cap, 2)

        # price_string = local_currency + ' {:,}'.format(price)
    #     percent_change_24hr_string = local_currency + ' {:,}'.format(percent_change_24hr)
    #     market_cap_string = local_currency + ' {:,}'.format(market_cap)
    
    return render_template('listings.html', form=form, title='Top 100 Cryptocurrencies | Crypto~VRSE', data=data, updated=updated) #, data=data, name=name, symbol=symbol, price=price_string, market_cap=market_cap_string, change24=percent_change_24hr_string)



@app.route('/mywallet', methods=['GET','POST'])
@login_required
def mywallet():
    wallet = current_user.coins
    total_coins = len(wallet) 

    form = AddAssetForm()
    if form.validate_on_submit():
        symbol = form.symbol.data.upper()
        amount = form.amount.data

        new_asset = Wallet(symbol, amount, current_user.id)
        db.session.add(new_asset)
        db.session.commit()
        flash (f'You have sussessfully added a new asset!', 'primary')
        return redirect(url_for('mywallet'))
        # global_url = base_url + '/v1/cryptocurrency/quotes/latest?convert=' + local_currency + '&symbol=' + symbol

        # request = requests.get(global_url, headers=headers)
        # results = request.json()

        # data = results['data']
        # coin = data[symbol]
        # print(data)


        # return render_template('mywallet.html', title='My Wallet | Crypto~VRSE', wallet=wallet, total_coins=total_coins, form=form, coin=coin)

    return render_template('mywallet.html', title='My Wallet | Crypto~VRSE', wallet=wallet, total_coins=total_coins, form=form)



@app.route('/mywallet/<int:wallet_id>')
def asset_detail(wallet_id):
    asset = Wallet.query.get_or_404(wallet_id)

    symbol = asset.symbol.upper()


    ###### META DATA #########
    meta_url = base_url + '/v1/cryptocurrency/info?&symbol=' + symbol

    request = requests.get(meta_url, headers=headers)
    results = request.json()
    data = results['data']

   
    name = data[symbol]['name']
    desription = data[symbol]['description']
    logo = data[symbol]['logo']
    website = data[symbol]['urls']['website'][0]
    if data[symbol]['urls']['technical_doc']:
        white_paper = data[symbol]['urls']['technical_doc'][0]  
    else:
        white_paper = data[symbol]['urls']['website'][0]
    if data[symbol]['urls']['twitter']:
        twitter = data[symbol]['urls']['twitter'][0]
    else:
        twitter = 'https://twitter.com'
    if data[symbol]['urls']['reddit']:
        reddit = data[symbol]['urls']['reddit'][0]
    else: 
        reddit = 'https://www.reddit.com'
  


    ########### COIN DATA   ##########

    global_url = base_url + '/v1/cryptocurrency/quotes/latest?convert=' + local_currency + '&symbol=' + symbol

    request2 = requests.get(global_url, headers=headers)
    results2 = request2.json()

    data2 = results2['data']
    coin = data2[symbol]
   

    last_update = coin['last_updated']
    updated = datetime.strptime(last_update, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%H:%M %m/%d/%Y')

    rank= coin['cmc_rank']
    price = coin['quote'][local_currency]['price']
    volume_24hr = coin['quote'][local_currency]['volume_24h']
    volume_change_24hr = coin['quote'][local_currency]['volume_change_24h']
    percent_change_1hr = coin['quote'][local_currency]['percent_change_1h']
    percent_change_24hr = coin['quote'][local_currency]['percent_change_24h']
    percent_change_7d = coin['quote'][local_currency]['percent_change_7d']
    market_cap = coin['quote'][local_currency]['market_cap']
    market_cap_dom = coin['quote'][local_currency]['market_cap_dominance']

    price = round(price, 6)
    percent_change_24hr = round(percent_change_24hr, 2)
    market_cap = round(market_cap, 2)

    price_string = ' {:,}'.format(price)
    percent_change_24hr_string = ' {:,}'.format(percent_change_24hr)
    market_cap_string = ' {:,}'.format(market_cap)

    usd_value = asset.amount * price

   

    return render_template('asset_details.html', asset=asset, title=f'{asset.symbol} Details | Crypto~VRSE', symbol=symbol, name=name, description=desription, logo=logo, website=website, twitter=twitter, reddit=reddit, white_paper=white_paper, 
            price=price_string, change24=percent_change_24hr_string, market_cap=market_cap_string, usd_value=usd_value,
            last_update=updated, volume_24hr=volume_24hr, volume_change_24hr=volume_change_24hr, percent_change_1hr=percent_change_1hr,
            percent_change_7d=percent_change_7d, market_cap_dom=market_cap_dom, rank=rank)


@app.route('/mywallet/<int:wallet_id>/delete', methods=['POST'])
@login_required
def delete_asset(wallet_id):
    asset = Wallet.query.get_or_404(wallet_id)

    db.session.delete(asset)
    db.session.commit()

    flash("Your asset has been deleted.", 'primary')
    return redirect(url_for('mywallet'))


@app.route('/mycharts')
@login_required
def my_charts():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        symbol = search_form.symbol.data.upper()
    return render_template('mycharts.html', form=search_form)

@app.route('/trending')
@login_required
def trending():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        symbol = search_form.symbol.data.upper()
    return render_template('trending.html', form=search_form)