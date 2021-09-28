import sqlite3
from django.http import JsonResponse
from . import serliazier
from . import pyqas
from datetime import datetime
db=sqlite3.connect("data.db", check_same_thread=False)
cur=db.cursor()
class Configure :
    def configure() :
        cur.execute("CREATE TABLE IF NOT EXISTS user(name VARCHAR(15) NOT NULL, email VARCHAR(20) NOT NULL PRIMARY KEY, phone INTEGER NOT NULL, password VARCHAR(25) NOT NULL)")
        cur.execute("CREATE TABLE IF NOT EXISTS profile_images(src BLOB, email VARCHAR(20), FOREIGN KEY(email) REFERENCES user(email))")
        cur.execute("CREATE TABLE IF NOT EXISTS messages(content TEXT NOT NULL, image BLOB, file VARBINARY, year INTEGER, month INTEGER, day INTEGER, hour INTEGER, minute INTEGER, second INTEGER, email_sender VARCHAR(20), email_reciver VARCHAR(20), FOREIGN KEY(email_sender) REFERENCES user(email), FOREIGN KEY(email_reciver) REFERENCES user(email))")
        cur.execute("CREATE TABLE IF NOT EXISTS activity(last_seen_year INTEGER, last_seen_month INTEGER, last_seen_day INTEGER, last_seen_hour INTEGER, last_seen_miute INTEGER, last_seen_second INTEGER, email VARCHAR(20) ,FOREIGN KEY(email) REFERENCES user(email))")
        cur.execute("CREATE TABLE IF NOT EXISTS images_for_message(message_id INTEGER, src BLOB, FOREIGN KEY(message_id) REFERENCES messages(id))")
        cur.execute("CREATE TABLE IF NOT EXISTS files_for_message(message_id INTEGER, file BLOB, FOREIGN KEY(message_id) REFERENCES messages(id))")
        db.commit()
        # cur.execute("DELETE FROM messages")
        # cur.execute("DELETE FROM images_for_message")
        # db.commit()
        # cur.execute("ALTER TABLE messages ADD COLUMN seen BOOLEAN DEFAULT false")
        # cur.execute("ALTER TABLE messages ADD CONSTRAINT FK_PersonOrder FOREIGN KEY (email_to_see) REFERENCES user(email);")
        # db.commit()
        # cur.execute("ALTER TABLE messages ADD email_to_see VARCHAR(20)")
        # db.commit()
        # cur.execute("DELETE FROM images_for_message")
        # db.commit()
        # cur.execute("ALTER TABLE activity ADD COLUMN active BOOLEAN DEFAULT FALSE")
        # db.commit()
        # alter the tables
        # old cur.execute("ALTER TABLE user ADD COLUMN pio VARCHAR(15)")
        # old cur.execute("ALTER TABLE messages RENAME email_reciver TO email_reciever")
        # old db.commit()
        # cur.execute("DELETE FROM user")
        # cur.execute("DELETE FROM messages")
        # cur.execute("DELETE FROM profile_images")
        # cur.execute("DELETE FROM profile_images")
        # cur.execute("ALTER TABLE profile_images ADD COLUMN id INTEGER")
        # cur.execute("ALTER TABLE profile_images ADD PRIMARY KEY (id)")
        # db.commit()
        # res=cur.execute("SELECT * FROM profile_images").fetchall()
        # for i in range(0, len(res)) :
        #     cur.execute("INSERT INTO profile_images(id) VALUES(?)", [i+1])
        #     db.commit()
class Login:
    def __init__(self, email, password):
        self.email=email
        self.password=password
    def login(self) :
        timenow=datetime.utcnow()
        res=cur.execute("SELECT * FROM user WHERE email=? AND password=?", [self.email, self.password]).fetchone()
        try :
            print('is that the main of that function')
            if len(res)>=1 :
                res_last_seen=cur.execute("SELECT * FROM activity WHERE email=?", [self.email]).fetchall()
                try :
                    if len(res_last_seen)>=1 :
                        if timenow.hour==22 :
                            cur.execute("UPDATE activity SET last_seen_year=?, last_seen_month=?, last_seen_day=?, last_seen_hour=?, last_seen_miute=?, last_seen_second=?, active=? WHERE email=?", [timenow.year, timenow.month, timenow.day +1, 00, timenow.minute, timenow.second, True,  self.email])
                            db.commit()
                        elif timenow.hour==23 :
                            cur.execute("UPDATE activity SET last_seen_year=?, last_seen_month=?, last_seen_day=?, last_seen_hour=?, last_seen_miute=?, last_seen_second=?, active=? WHERE email=?", [timenow.year, timenow.month, timenow.day +1, 1, timenow.minute, timenow.second, True,  self.email])
                            db.commit()
                        else :
                            cur.execute("UPDATE activity SET last_seen_year=?, last_seen_month=?, last_seen_day=?, last_seen_hour=?, last_seen_miute=?, last_seen_second=?, active=? WHERE email=?", [timenow.year, timenow.month, timenow.day, timenow.hour+2, timenow.minute, timenow.second, True,  self.email])
                            db.commit()
                    else :
                        if timenow.hour==22 :
                            cur.execute("INSERT INTO activity VALUES(?, ?, ?, ?, ?, ?, ?, ?)", [timenow.year, timenow.month, timenow.day +1, 00, timenow.minute, timenow.second, self.email, True])
                            db.commit()
                        elif timenow.hour==23 :
                            cur.execute("INSERT INTO activity VALUES(?, ?, ?, ?, ?, ?, ?, ?)", [timenow.year, timenow.month, timenow.day +1, 1, timenow.minute, timenow.second, self.email, True])
                            db.commit()
                        else :
                            cur.execute("INSERT INTO activity VALUES(?, ?, ?, ?, ?, ?, ?, ?)", [timenow.year, timenow.month, timenow.day, timenow.hour + 2, timenow.minute, timenow.second, self.email, True])
                            db.commit()
                except :
                    if timenow.hour==22 :
                            cur.execute("INSERT INTO activity VALUES(?, ?, ?, ?, ?, ?, ?, ?)", [timenow.year, timenow.month, timenow.day +1, 00, timenow.minute, timenow.second, self.email, True])
                            db.commit()
                    elif timenow.hour==23 :
                        cur.execute("INSERT INTO activity VALUES(?, ?, ?, ?, ?, ?, ?, ?)", [timenow.year, timenow.month, timenow.day +1, 1, timenow.minute, timenow.second, self.email, True])
                        db.commit()
                    else :
                        cur.execute("INSERT INTO activity VALUES(?, ?, ?, ?, ?, ?, ?, ?)", [timenow.year, timenow.month, timenow.day, timenow.hour + 2, timenow.minute, timenow.second, self.email, True])
                        db.commit()
                return JsonResponse({
                    "state" :True,
                    "pio" :"you have logged in successfully"
                })
        except :
            return JsonResponse({
                "state" :False,
                "pio" :"the password or the email isnot correct"
            })
class Logout :
    def __init__(self, email) :
        self.email=email
    def logout(self) :
        timenow=datetime.utcnow()
        if timenow.hour==22 :
            cur.execute("UPDATE activity SET last_seen_year=?, last_seen_month=?, last_seen_day=?, last_seen_hour=?, last_seen_miute=?, last_seen_second=?, active=? WHERE email=?", [timenow.year, timenow.month, timenow.day +1, 00, timenow.minute, timenow.second, False, self.email ])
            db.commit()
        elif timenow.hour==23 :
            cur.execute("UPDATE activity SET last_seen_year=?, last_seen_month=?, last_seen_day=?, last_seen_hour=?, last_seen_miute=?, last_seen_second=?, active=? WHERE email=?", [timenow.year, timenow.month, timenow.day +1, 1, timenow.minute, timenow.second, False, self.email ])
            db.commit()
        else :
            cur.execute("UPDATE activity SET last_seen_year=?, last_seen_month=?, last_seen_day=?, last_seen_hour=?, last_seen_miute=?, last_seen_second=?, active=? WHERE email=?", [timenow.year, timenow.month, timenow.day, timenow.hour+2 , timenow.minute, timenow.second, False, self.email ])
            db.commit()
        return JsonResponse({
            "state" :True,
            "pio" :"you have logged out successfully"
        })
class Signup :
    def __init__(self, name, email, phone, password, pio, profileimage) :
        self.name = name
        self.email=email
        self.phone=phone
        self.password=password
        self.pio=pio
        self.profileimage=profileimage
    def signup(self) :
        timenow=datetime.utcnow()
        res=cur.execute("SELECT email FROM user").fetchall()
        chck=[email for email in res if email==self.email]
        if len(chck)>=1 :
            return JsonResponse({"state" :False, "pio" :"the email is used before"})
        else :
            cur.execute("INSERT INTO profile_images(src, email) VALUES(?, ?)", [self.profileimage, self.email])
            cur.execute("INSERT INTO user(name, email, phone, password, pio) VALUES(?, ?, ?, ?, ?)", [self.name, self.email, self.phone, self.password, self.pio])
            cur.execute("INSERT INTO activity VALUES(?, ?, ?, ?, ?, ?, ?, ?)", [timenow.year, timenow.month, timenow.day, timenow.hour, timenow.minute, timenow.second, self.email, True])
            db.commit()
            return JsonResponse({
                "state" :True,
                "pio" :"you have signup successfully"
            })
class SendMessageWithoutFilesOrImages :
    def __init__(self, content, image, file, year, month, day, hour, minute, second, email_sender, email_reciever) :
        self.content=content
        self.image=image
        self.file=file
        self.year=year
        self.month=month
        self.day=day
        self.hour=hour
        self.minute=minute
        self.second=second
        self.email_sender=email_sender
        self.email_reciever=email_reciever
    def sendMessageWithoutFilesOrImages(self) :
        if self.hour==23 :
            cur.execute("INSERT INTO messages(content, year, month, day, hour,  minute, second, email_sender, email_reciever) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", [self.content, self.year, self.month, self.day +1, 1, self.minute, self.second, self.email_sender, self.email_reciever])
            db.commit()
            return JsonResponse({"state" :True, "pio" :"the message has been sent successfully"})
        elif self.hour==2 :
            cur.execute("INSERT INTO messages(content, year, month, day, hour,  minute, second, email_sender, email_reciever) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", [self.content, self.year, self.month, self.day +1, 00, self.minute, self.second, self.email_sender, self.email_reciever])
            db.commit()
            return JsonResponse({"state" :True, "pio" :"the message has been sent successfully"})
        else :
            cur.execute("INSERT INTO messages(content, year, month, day, hour,  minute, second, email_sender, email_reciever) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", [self.content, self.year, self.month, self.day, self.hour, self.minute, self.second, self.email_sender, self.email_reciever])
            db.commit()
            return JsonResponse({"state" :True, "pio" :"the message has been sent successfully"})
class SendMessageWithFiles :
    def __init__(self, message_id, file) :
        self.message_id=message_id
        self.file=file
    def sendMessageWithFiles(self) :
        cur.execute("INSERT INTO files_for_message(message_id, file)", [self.message_id, self.file])
        db.commit()
        return JsonResponse({"state" :True, "pio" :"the file has been sent successfully"})
class SendMessageWithImages :
    def __init__(self, message_id, image) :
        self.message_id=message_id
        self.image=image
    def sendMessageWithFiles(self) :
        cur.execute("INSERT INTO images_for_message(message_id, file)", [self.message_id, self.image])
        db.commit()
        return JsonResponse({"state" :True, "pio" :"the image has been sent successfully"})
class SeeMessage :
    def __init__(self, email_sender, email_reciever) :
        self.email_sender=email_sender
        self.email_reciever=email_reciever
    def seemessage(self) :
        cur.execute("UPDATE messages set seen=true WHERE email_sender=? AND email_to_see=? AND email_reciever=?", [self.email_sender, self.email_reciever, self.email_reciever])
        db.commit()
class DeleteChat :
    def __init__(self, room_owner, room_reciever) :
        self.room_owner=room_owner
        self.room_reciever=room_reciever
    def deletechat(self) :
        res_ids=cur.execute("SELECT id FROM messages WHERE email_sender=? AND email_reciever=? OR email_sender=? AND email_reciever=?", [self.room_owner, self.room_reciever, self.room_reciever, self.room_owner]).fetchall()
        for item in res_ids:
            cur.execute("DELETE FROM images_for_message WHERE message_id=?", [item[0]])
            cur.execute("DELETE FROM files_for_message WHERE message_id=?", [item[0]])
            db.commit()
        cur.execute("DELETE FROM messages WHERE email_sender=? AND email_reciever=? OR email_sender=? AND email_reciever=?", [self.room_owner, self.room_reciever, self.room_reciever, self.room_owner])
        db.commit()
class ChangeProfileImage :
    def __init__(self, profile_image_src, email) :
        self.profile_image_src=profile_image_src
        self.email=email
    def changeprofileimage(self) :
        cur.execute("INSERT INTO profile_images(src, email) VALUES(?, ?)", [self.profile_image_src, self.email])
        db.commit()
        return JsonResponse({
            "state" :True,
            "pio" :"the profile image has been updated"
        })
class RemoveProfileImage :
    def __init__(self, email, id) :
        self.email=email
        self.id=id
    def removeprofileimage(self) :
        cur.execute("DELETE FROM profile_images WHERE email=? AND id=?", [self.email, self.id])
        db.commit()
        return JsonResponse({
            "state" :True,
            "pio" :"the profile image has been removed"
        })
class ChangeName :
    def __init__(self, email, newname) :
        self.email=email
        self.newname=newname
    def changeName(self) :
        cur.execute("UPDATE user set name=? WHERE email=?", [self.newname, self.email])
        db.commit()
        return JsonResponse({
            "state" :True,
            "pio" :"the name has been updated successfully"
        })
class ChangePio :
    def __init__(self, email, newpio) :
        self.email=email
        self.newpio=newpio
    def changepio(self) :
        cur.execute("UPDATE user set pio=? WHERE email=?", [self.newpio, self.email])
        db.commit()
        return JsonResponse({
            "state" :True,
            "pio" :"the name has been updated successfully"
        })
class ChangePhone :
    def __init__(self, email, newphone) :
        self.email=email
        self.newphone=newphone
    def changePhone(self) :
        res=cur.execute("SELECT phone FROM user WHERE phone=?", [self.newphone]).fetchall()
        try :
            if len(res)>=1 :
                return JsonResponse({
                    "state" :False,
                    "pio" :"this phone number is used already"
                })
            else :
                cur.execute("UPDATE user SET phone=?", [self.newphone])
                db.commit()
                return JsonResponse({
                    "state" :True,
                    "pio":"the phone has been updated"
                })
        except :
            cur.execute("UPDATE user SET phone=?", [self.newphone])
            db.commit()
            return JsonResponse({
                "state" :True,
                "pio":"the phone has been updated"
            })
class ChangeEmail :
    def __init__(self, email, newemail) :
        self.email=email
        self.newemail=newemail
    def changeEmail(self) :
        res=cur.execute("SELECT email FROM user WHERE email=?", [self.newemail]).fetchall()
        try :
            if len(res)>=1 :
                return JsonResponse({
                    "state" :False,
                    "pio" :"this email is used already"
                })
            else :
                cur.execute("UPDATE user SET email=?", [self.newemail])
                db.commit()
                return JsonResponse({
                    "state" :True,
                    "pio" :"the email is used already"
                })
        except :
            cur.execute("UPDATE user SET email=?", [self.newemail])
            db.commit()
            return JsonResponse({
                "state" :True,
                "pio" :"the email has been updated"
            })
class DeleteAccount :
    def __init__(self, email) :
        self.email=email
    def deleteaccount(self) :
        res_ids=cur.execute("SELECT id FROM messages WHERE email_sender=? OR email_reciever=?", [self.email, self.email]).fetchall()
        cur.execute("DELETE FROM user WHERE email=?", [self.email])
        cur.execute("DELETE FROM profile_images WHERE email=?", [self.email])
        cur.execute("DELETE FROM activity WHERE email=?", [self.email])
        cur.execute("DELETE FROM activity WHERE email=?", [self.email])
        for item in res_ids:
            cur.execute("DELETE FROM images_for_message WHERE message_id=?", [item[0]])
            cur.execute("DELETE FROM files_for_message WHERE message_id=?", [item[0]])
            db.commit()
        cur.execute("DELETE FROM messages WHERE email_sender=? OR email_reciever=?", [self.email, self.email])
        db.commit()
# defs
def getRooms(email) :
    lst=[]
    fltred_lst=[]
    data_lst=[]
    msgs_list=[]
    res=cur.execute("SELECT email_sender, email_reciever FROM messages WHERE email_sender=? OR email_reciever=?", [email, email]).fetchall()
    for item in res :
        lst.append(item[0])
        lst.append(item[1])
    for item in pyqas.Reverse_Lst(lst) :
        if item not in fltred_lst and item!=email :
            fltred_lst.append(item)
    for item in fltred_lst :
        data_res=cur.execute("SELECT name FROM user WHERE email=?", [item]).fetchall()
        profile_images=cur.execute("SELECT src FROM profile_images WHERE email=?", [item]).fetchall()
        msgs_res=cur.execute("SELECT content, year, month, day, hour, minute, second, email_sender, email_reciever, id, seen, email_to_see FROM messages WHERE email_sender=? AND email_reciever=? OR email_sender=? AND email_reciever=?", [email, item, item, email]).fetchall()
        res_images=cur.execute("SELECT * FROM images_for_message WHERE message_id=?", [msgs_res[-1][9]]).fetchall()
        res_unseen_msgs=cur.execute("SELECT * FROM messages WHERE email_sender=? AND email_reciever=? AND seen=false", [item, email]).fetchall()
        res_unseen_msgs_length=[]
        try :
            if len(res_unseen_msgs)>=1 :
                res_unseen_msgs_length.append(len(res_unseen_msgs))
            else :
                res_unseen_msgs_length.append(0)
        except :
            res_unseen_msgs_length.append(0)
        if len(res_images)>=1 :
            data_res_json={
                "name" :data_res[0][0],
                "room_owner":email,
                "room_reciver":item,
                "profile_image" : profile_images[-1][0],
                "last_message_content" :"Media Files",
                "last_message_year" :msgs_res[-1][1],
                "last_message_month" :msgs_res[-1][2],
                "last_message_day" :msgs_res[-1][3],
                "last_message_hour" :msgs_res[-1][4],
                "last_message_minute" :msgs_res[-1][5],
                "last_message_second" :msgs_res[-1][6],
                "last_message_email_sender" :msgs_res[-1][7],
                "last_message_reciever" :msgs_res[-1][8],
                "last_message_seen" :msgs_res[-1][10],
                "last_message_email_to_see" :msgs_res[-1][11],
                "last_message_id" :msgs_res[-1][9],
                "unseen_messages_length" :res_unseen_msgs_length[0],
            }
            msgs_list.append(data_res_json)
        else :
            data_res_json={
                "name" :data_res[0][0],
                "room_owner":email,
                "room_reciver":item,
                "profile_image" : profile_images[-1][0],
                "last_message_content" :msgs_res[-1][0],
                "last_message_year" :msgs_res[-1][1],
                "last_message_month" :msgs_res[-1][2],
                "last_message_day" :msgs_res[-1][3],
                "last_message_hour" :msgs_res[-1][4],
                "last_message_minute" :msgs_res[-1][5],
                "last_message_second" :msgs_res[-1][6],
                "last_message_email_sender" :msgs_res[-1][7],
                "last_message_reciever" :msgs_res[-1][8],
                "last_message_seen" :msgs_res[-1][10],
                "last_message_email_to_see" :msgs_res[-1][11],
                "last_message_id" :msgs_res[-1][9],
                "unseen_messages_length" :res_unseen_msgs_length[0],
            }
            msgs_list.append(data_res_json)
    return JsonResponse(msgs_list, safe=False)
def getChat(room_owner, room_reciever) :
    lst_msgs=[]
    # first getting the data of the email of the room_reciever
    res_data=cur.execute("SELECT name FROM user WHERE email=?", [room_reciever]).fetchone()
    res_profile_images=cur.execute("SELECT src FROM profile_images WHERE email=?", [room_reciever]).fetchall()
    res_state=cur.execute("SELECT * FROM activity WHERE email=?", [room_reciever]).fetchone()
    data_json={
        "name" :res_data[0],
        "email" :room_reciever,
        "profile_image" :res_profile_images[-1][0],
        "last_seen_year" :res_state[0],
        "last_seen_month" :res_state[1],
        "last_seen_day" :res_state[2],
        "last_seen_hour" :res_state[3],
        "last_seen_minute" :res_state[4],
        "last_seen_second" :res_state[5],
        "active" :res_state[7],
    }
    # my data 
    res_my_data=cur.execute("SELECT name FROM user WHERE email=?", [room_owner]).fetchone()
    res_my_profile_images=cur.execute("SELECT src FROM profile_images WHERE email=?", [room_owner]).fetchall()
    my_data={
        "name" :res_my_data[0],
        "profile_image" :res_my_profile_images[-1][0],
    }
    # end of the my data
    res_msgs=cur.execute("SELECT * FROM messages WHERE email_sender=? AND email_reciever=? OR email_sender=? AND email_reciever=?", [room_owner, room_reciever, room_reciever, room_owner]).fetchall()
    for msg in res_msgs :
        lst_files=[]
        lst_images=[]
        lst_files.clear()
        lst_images.clear()
        res_files=cur.execute("SELECT file FROM files_for_message WHERE message_id=?", [msg[-3]]).fetchall()
        res_images=cur.execute("SELECT src FROM images_for_message WHERE message_id=?", [msg[-3]]).fetchall()
        # query files
        try :
            for file in res_files :
                files_query={
                    "file" :file[0]
                }
                lst_msgs.append(file_query)
        except :
            pass
        # query images
        try :
            for image in res_images :
                image_query={
                    "src" :image[0],
                    "id" :msg[-3],
                }
                lst_images.append(image_query)
        except :
            pass
        msg_query={
            "content" :msg[0],
            "year" :msg[1],
            "month" :msg[2],
            "day" :msg[3],
            "hour" :msg[4],
            "minute" :msg[5],
            "second" :msg[6],
            "email_sender" :msg[7],
            "email_reciever" :msg[8],
            "seen":msg[10],
            "email_to_see" :msg[11],
            "id" :msg[9],
            "files":lst_files,
            "images":lst_images,
        }
        lst_msgs.append(msg_query)
    lst_dates=[]
    all_msgs_query=[]
    for msg in pyqas.Reverse_Lst(lst_msgs) :
        data_date={
            "year" :msg["year"],
            "month" :msg["month"],
            "day" :msg["day"]
        }
        lst_dates.append(data_date)
    for item in pyqas.Remove_Duplicates(lst_dates):
        lst_msgs_query=[]
        for msg in pyqas.Reverse_Lst(lst_msgs) :
            if (msg["year"]==item["year"] and msg["month"]==item["month"] and msg["day"]==item["day"]) :
                lst_msgs_query.append(msg)
        data_msgs_query={
            "year" :item["year"],
            "month" :item["month"],
            "day" :item["day"],
            "msgs" :pyqas.Reverse_Lst(lst_msgs_query)
        }
        all_msgs_query.append(data_msgs_query)
    room_chat={
        "msgs" :all_msgs_query,
        "data_chat" :data_json,
        "my_data" :my_data,
    }
    return JsonResponse(room_chat, safe=False)
    # end of the first step