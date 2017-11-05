FROM alpine

RUN apk add --update --no-cache curl

CMD ["curl", "-X", "POST", "http://mind:8000/api/send-reminders"]
