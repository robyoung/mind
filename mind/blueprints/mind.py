from flask import (
    Blueprint, render_template, redirect, url_for, request,
    abort, flash, send_from_directory, session, jsonify, current_app
)
from flask_login import login_required, current_user

from mind.models import Question, Answer, User
from mind.app import db, google, LoginUser

mind = Blueprint('mind', __name__)


@mind.route('')
def index():
    question_slug = 'how-are-you-today'
    question_url = url_for('.show_question',
                           question=question_slug)
    return redirect(question_url), 302


@mind.route('/info')
def info():
    return jsonify(
        headers=dict(request.headers),
        session=dict(session)
    ), 200


@mind.route('/login')
def login():
    if current_app.config['ENVIRONMENT'] == 'dev':
        user = User.get_or_create('example@example.org')
        LoginUser.login(user, {
            'email': 'example@example.org',
            'given_name': 'Example',
        })
        return redirect(url_for('.index')), 302

    callback = url_for('.authorized', _external=True, _scheme='https')
    return google.authorize(callback=callback)


@mind.route('/logout')
def logout():
    session.pop('google_token', None)
    LoginUser.logout()
    flash('Logged out')
    return redirect(url_for('.index'))


@mind.route('/oauth2-callback')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return ('Access denied: ' +
                'reason={error_reason[0]} ' +
                'error={error_description[0]}').format(**request.args), 401

    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    user = User.get_or_create(me.data['email'])
    LoginUser.login(user, me.data)

    return redirect(url_for('.index')), 302


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


@mind.route('/static/<path:path>')
def static(path):
    return send_from_directory('static', path)


@mind.route('/settings')
@login_required
def show_settings():
    return render_template('show_settings.html')


@mind.route('/settings', methods=['POST'])
@login_required
def update_settings():
    current_user.user.twitter_handle = request.form['twitter_handle']
    db.session.add(current_user.user)
    db.session.commit()

    flash('Settings updated')

    return redirect(url_for('.show_settings')), 302


# Question related routes
@mind.route('/question', methods=['GET'])
def list_questions():
    questions = Question.query.all()

    return render_template('list_questions.html',
                           questions=questions)


@mind.route('/question', methods=['POST'])
def add_question():
    db.session.add(Question(title=request.form['question_title']))
    db.session.commit()

    return redirect(url_for('.list_questions'))


@mind.route('/question/<question>', methods=['GET'])
def show_question(question):
    return render_template('show_question.html',
                           question=question)


@mind.route('/question/<question>/answer', methods=['POST'])
@login_required
def add_answer(question):
    answer = Answer(
        question_id=question.id,
        answer=request.form['answer'],
        user=current_user.user
    )
    db.session.add(answer)
    db.session.commit()

    flash('Answer added')
    return redirect(url_for('.show_question', question=question))


def rangerer(start, end, step):
    while start <= end:
        yield start
        start += step


@mind.route('/question/<question>/stats', methods=['GET'])
@login_required
def show_question_stats(question):
    user = current_user.user

    return render_template('show_question_stats.html',
                           question=question,
                           stats=question.stats_for_user(user))


MODEL_URL_MAP = {
    'question': Question
}


@mind.url_defaults
def add_slug_to_url(endpoint, values):
    for field in MODEL_URL_MAP.keys():
        if field in values and hasattr(values[field], 'slug'):
            values[field] = values[field].slug


@mind.url_value_preprocessor
def resolve_slug(endpoint, values):
    for field, model in MODEL_URL_MAP.items():
        if field in values:
            record = model.query \
                    .filter_by(slug=values[field]) \
                    .one_or_none()
            if not record:
                abort(404)
            values[field] = record
