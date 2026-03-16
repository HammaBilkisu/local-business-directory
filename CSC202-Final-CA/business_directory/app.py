from flask import Flask, render_template, request, redirect, url_for, flash, abort
from models import (
    Business, RecentlyAddedStack,
    init_db, get_all_businesses, insert_business,
    get_business_by_id, delete_business, count_businesses
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-me-in-production'

recently_added = RecentlyAddedStack()

CATEGORIES = [
    'Restaurant', 'Retail', 'Health & Beauty', 'Home Services',
    'Automotive', 'Education', 'Entertainment', 'Finance',
    'Legal', 'Technology', 'Other'
]


@app.before_request
def setup():
    init_db()


@app.route('/')
def index():
    search   = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()
    businesses = get_all_businesses(search=search, category=category)
    return render_template(
        'index.html',
        businesses=businesses,
        categories=CATEGORIES,
        search=search,
        selected_category=category,
        recent=recently_added.peek()
    )


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name        = request.form.get('name', '').strip()
        category    = request.form.get('category', '').strip()
        address     = request.form.get('address', '').strip()
        city        = request.form.get('city', '').strip()
        phone       = request.form.get('phone', '').strip()
        email       = request.form.get('email', '').strip()
        website     = request.form.get('website', '').strip()
        description = request.form.get('description', '').strip()

        if not name or not category or not city:
            flash('Name, category, and city are required.', 'danger')
            return render_template('add.html', categories=CATEGORIES, form=request.form)

        biz = Business(name, category, address, city, phone, email, website, description)
        insert_business(biz)          # biz.id is set after this call
        recently_added.push(biz)

        flash(f'"{biz.name}" has been added! Summary: {biz.get_summary()}', 'success')
        return redirect(url_for('index'))

    return render_template('add.html', categories=CATEGORIES, form={})


@app.route('/delete/<int:business_id>', methods=['POST'])
def delete(business_id):
    biz = get_business_by_id(business_id)
    if biz is None:
        abort(404)
    delete_business(business_id)
    flash(f'"{biz.name}" has been removed from the directory.', 'info')
    return redirect(url_for('index'))


@app.route('/about')
def about():
    total = count_businesses()
    return render_template('about.html', total=total)


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)
