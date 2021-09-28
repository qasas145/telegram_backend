"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import sqlite3
import socketio
import eventlet
from datetime import datetime
from Tools.functions import DeleteChat, SeeMessage, DeleteAccount

db=sqlite3.connect('data.db', check_same_thread=False)

cur=db.cursor()

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_wsgi_application()

sio = socketio.Server(async_mode='eventlet',cors_allowed_origins='*', logger=True, engineio_logger=True)

application = socketio.WSGIApp(sio, application)

timenow=datetime.utcnow()

@sio.on('sendmessagewithoutfilesorimages')
def sendmessagewithoutfilesorimages(data, data_main):
    cur.execute("INSERT INTO messages(content, year, month, day, hour,  minute, second, email_sender, email_reciever, email_to_see) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [data_main['content'], timenow.year, timenow.month, timenow.day, timenow.hour +2, timenow.minute, timenow.second, data_main['email_sender'], data_main['email_reciever'], data_main["email_reciever"]])
    db.commit()
    sio.emit('messagesended', {
        "state" :True,
        "email_reciever" :data_main['email_reciever'],
        "email_sender" :data_main["email_sender"],
        "pio" :"the message has been sent successfully"
    })
@sio.on('sendmessagewithimages')
def sendmessagewithoutfilesorimages(data, data_main):
    last_id=cur.execute("SELECT id FROM messages WHERE email_sender=? AND email_reciever=?", [data_main['email_sender'], data_main['email_reciever']]).fetchall()
    cur.execute("INSERT INTO images_for_message VALUES(?, ?)", [last_id[-1][0], data_main['src']])
    db.commit()
    sio.emit('messagesendedwithimages', {
        "state" :True,
        "email_sender" :data_main["email_sender"],
        "email_reciever" :data_main['email_reciever'],
        "pio" :"the message has been sent successfully"
    })
@sio.on("deletechat")
def deletechat(data, data_main) :
    process=DeleteChat(data_main["room_owner"], data_main["room_reciever"])
    process.deletechat()
    sio.emit("chatdeleted", {
        "room_reciever" :data_main["room_reciever"],
        "room_owner" :data_main["room_owner"],
        "state" :True,
        "pio" :"the chat has been deleted successfully",
    })
    return process.deletechat()
@sio.on("seemessage")
def seemessage(data, data_main) :
    process=SeeMessage(data_main["email_sender"], data_main["email_reciever"])
    process.seemessage()
    sio.emit("messageseen", {
        "email_sender" :data_main["email_sender"],
        "email_reciever" :data_main["email_reciever"],
        "state" :True,
        "pio" :"the message has been seen successfully"
    })
@sio.on("deleteaccount")
def deleteaccount(data, data_main):
    process=DeleteAccount(data_main["email"])
    process.deleteaccount()
    sio.emit("accountdeleted", {
        "email_deleted":data_main["email"],
        "state" :True,
        "pio" :"the account has been deleted successfully"
    })
eventlet.wsgi.server(eventlet.listen(('', 8000)), application)