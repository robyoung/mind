from datetime import datetime, timedelta

from application import app
from mind.app import twitter_client
from mind.models import User


@app.cli.command('send-reminders')
def send_reminders():
    """
    Send reminder messages to users.
    """
    print('send-reminders {}'.format(twitter_client.base_url))
    users_needing_reminder = User.query.filter(
        User.latest_answer_created_at < datetime.utcnow() - timedelta(days=1),
        User.twitter_handle != None  # noqa: E711
    )
    for user in users_needing_reminder.all():
        twitter_client.PostDirectMessage(
            'Time to answer a question https://robyoung.digital/mind',
            screen_name=user.twitter_handle)
