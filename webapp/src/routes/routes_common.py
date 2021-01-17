from flask import render_template, request, redirect, url_for, session

from src import app, db
from src.database.models import User
from src.helper.consts import CURRENT_TASK
from src.helper.tools_common import is_signed_in, unlock_artifacts_by, who_is_signed_in, sign_in, sign_out, get_all_users
from src.helper.tools_labeling import get_labeling_status, get_n_labeled_artifact_per_user, get_overall_labeling_progress


@app.route("/")
def index():
    if is_signed_in():
        unlock_artifacts_by(who_is_signed_in())
        return render_template("common_pages/home.html", user_info=get_labeling_status(who_is_signed_in()),
                               currentTask=CURRENT_TASK['route'])
    else:
        return render_template("common_pages/index.html")


@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['user'].title()
        if username == "":
            return redirect(url_for('index'))
        user = User.query.filter_by(username=username).first()
        if user is not None:
            sign_in(username)
            return redirect(url_for('index'))
        else:
            session['new_user_username'] = username  # Pass username to register page
            return redirect(url_for('signup'))
    else:
        return "Not POST!"


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        if 'new_user_username' not in session:
            # Try to log-in from home
            return redirect(url_for('index'))
        else:
            tmp = session['new_user_username']  # Passed username from home page
            session.pop('new_user_username', None)
            return render_template('common_pages/signup.html', username=tmp)
    else:
        username = request.form['name']
        gender = request.form['gender']
        education = request.form['education']
        occupation = request.form['occupation']
        affiliation = request.form['affiliation']
        xp = request.form['years_xp']
        user_item = User(username=username, gender=gender, education=education, occupation=occupation, affiliation=affiliation, years_xp=xp)
        db.session.add(user_item)
        db.session.commit()
        sign_in(username)
        return redirect(url_for('index'))


@app.route("/signout", methods=['GET', 'POST'])
def signout():
    if request.method == 'GET':
        sign_out()
        return redirect(url_for('index'))
    else:
        return "Not GET!"


@app.route("/stat", methods=['GET'])
def stat():
    n_labeled_per_user = get_n_labeled_artifact_per_user()

    users_labeling_stat = []  # list to keep it sorted
    for username in get_all_users():
        users_labeling_stat.append({'username': username,
                                    'total_n_artifact': n_labeled_per_user.get(username, 0),
                                    'total_n_sentence': 0,
                                    'total_n_reviewed': 0
                                    })

    users_labeling_stat = sorted(users_labeling_stat, key=lambda element: element['total_n_artifact'], reverse=True)

    sources = get_overall_labeling_progress()
    sources_labeling_stat = {sources['source_id']: sources}

    return render_template('common_pages/stat.html',
                           users_labeling_stat=users_labeling_stat,
                           sources_labeling_stat=sources_labeling_stat,
                           user_info=get_labeling_status(who_is_signed_in()))


@app.route("/setstatus", methods=['GET', 'POST'])
def setstatus():
    if is_signed_in():
        global IS_SYSTEM_UP
        newStatus = request.args.get('status')
        if newStatus == '1':
            IS_SYSTEM_UP = True
        else:
            IS_SYSTEM_UP = False
        return "New Web App status: " + str(IS_SYSTEM_UP)
    else:
        return "Please Sign-in first."
