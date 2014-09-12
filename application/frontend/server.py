import os
from datetime import datetime

from flask import (
    abort,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from flask.ext.login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from forms import (
    ChangeForm,
    ConfirmForm,
    LoginForm
)

from application.services import (
    post_to_cases,
    is_matched,
    is_owner
)

from application.auth.models import User

from application import (
    app,
    db
)

from utils import get_or_log_error

@app.template_filter()
def format_date_YMD(value):
    new_date = datetime.strptime(value, '%Y-%m-%d')
    return new_date.strftime('%d %B %Y')

@app.template_filter()
def format_date_DMY(value):
    new_date = datetime.strptime(value, '%d-%m-%Y')
    return new_date.strftime('%d %B %Y')


@app.template_filter()
def currency(value):
    """Format a comma separated  currency to 2 decimal places."""
    return "{:,.2f}".format(float(value))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/property/<title_number>')
@login_required
def property_by_title(title_number):
    title_url = "%s/%s/%s" % (
        app.config['AUTHENTICATED_SEARCH_API'],
        'auth/titles',
        title_number)
    app.logger.info("Requesting title url : %s" % title_url)
    response = get_or_log_error(title_url)
    title = response.json()
    app.logger.info("Found the following title: %s" % title)
    owner = is_owner(current_user, title_number)
    return render_template(
        'view_property.html',
        title=title,
        is_owner=owner,
        apiKey=os.environ['OS_API_KEY'])


# Sticking to convention, "/property/<title_number>" will show the
# resource, and "/property/<title_number>/edit" will show a form
# to edit said resource. Here we go a step further, and limit
# the form to a section on the resource, e.g. "proprietor".
@app.route('/property/<title_number>/edit/title.proprietor.<int:proprietor_index>', methods=['GET', 'POST'])
@login_required
def property_by_title_edit_proprietor(title_number, proprietor_index):
    if is_owner(current_user, title_number):
        form = ChangeForm(request.form, marriage_country='GB')
        if request.method == 'GET':
            title = _get_title(title_number)
            app.logger.info("Found the following title: %s" % title)
            form.title_number.data = title['title_number']
            proprietor = title['proprietors'][proprietor_index-1]
            form.proprietor_full_name.data = proprietor['full_name']

        if form.validate_on_submit():
            if 'confirm' in form and form.confirm.data:
                # the title will be persisted in its entirety when
                # it's sent to the casework system

                # HACK read title again instead of getting it from session
                title = _get_title(title_number)
                title['proprietors'][proprietor_index - 1] = {'full_name' : form.proprietor_new_full_name.data}
                form.title.data = title

                post_to_cases('change-name-marriage', form.data)
                form.title.data
                # TODO handle non-200 responses, and ack accordingly.
                return render_template('acknowledgement.html', form=form)
            else:
                from datatypes.validators.iso_country_code_validator import countries
                country = countries.get(alpha2=form.data['marriage_country']).name
                return render_template('confirm.html', form=ConfirmForm(obj=form.data), country=country)
        return render_template('edit_property.html', form=form)
    else:
        abort(401)

def _get_title(title_number):
    title_url = "%s/%s/%s" % (
    app.config['AUTHENTICATED_SEARCH_API'],
    'auth/titles',
    title_number)
    app.logger.debug("Requesting title url : %s" % title_url)
    response = get_or_log_error(title_url)
    return response.json()

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.email.data)
        if user and user.check_password(form.password.data) and is_matched(user):
            login_user(user, remember=form.remember.data)
            return redirect(form.next.data or url_for('.index'))
        else:
            flash("Invalid login")
    return render_template("auth/login_user.html", form=form)


@app.route("/logout")
@login_required
def logout():
    session.pop("lrid", None)
    logout_user()
    return redirect(url_for('.login'))
