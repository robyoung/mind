from datetime import datetime, timedelta

from flask import Blueprint, jsonify, url_for
from sqlalchemy import or_

from mind.models import User
from mind.app import twitter_client

api = Blueprint('api', __name__)


@api.route('')
def index():
    return jsonify(
        send_reminders=url_for('.send_reminders', _external=True))


@api.route('/send-reminders', methods=['POST'])
def send_reminders():
    yesterday = datetime.utcnow() - timedelta(days=1)
    users_needing_reminder = User.query.filter(
        or_(
            User.latest_answer_created_at < yesterday,
            User.latest_answer_created_at == None
        ),
        User.twitter_handle != None  # noqa: E711
    )
    count = 0
    for user in users_needing_reminder.all():
        twitter_client.PostDirectMessage(
            'Time to answer a question https://robyoung.digital/mind',
            screen_name=user.twitter_handle)
        count += 1
    return jsonify(message=f'Sent {count} reminders')
