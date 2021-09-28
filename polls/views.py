from django.shortcuts import render
from django.http import  HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from Tools.functions import Configure, Signup, Login, Logout, ChangeProfileImage, RemoveProfileImage, ChangeName, ChangePio, ChangePhone, ChangeEmail, SendMessageWithoutFilesOrImages, SendMessageWithImages, SendMessageWithFiles, getRooms, getChat, DeleteChat
from pyqas import pyqas
from Tools import serliazier
from datetime import datetime
import json
import sqlite3
db=sqlite3.connect('data.db', check_same_thread=False)
cur=db.cursor()
@csrf_exempt
def configure(request) :
    Configure.configure()
    return HttpResponse('hello from the configure div')
@csrf_exempt
def login(request) :
    data=json.loads(request.body)
    process=Login(data['email'], data['password'])
    return process.login()
@csrf_exempt
def logout(request) :
    data=json.loads(request.body)
    process=Logout(data['email'])
    return process.logout()
@csrf_exempt
def signup(request) :
    data=json.loads(request.body)
    process=Signup(data['name'], data['email'], data['phone'], data['password'], data['pio'], data['profileimage'])
    return process.signup()
@csrf_exempt
def getdataforuser(request) :
    data=json.loads(request.body)
    process=getDataForUser(data['email'])
    return process
@csrf_exempt
def search(request) :
    data=json.loads(request.body)
    process=Search(data['email'], data['name'])
    return process
@csrf_exempt
def changeprofileimage(request) :
    data=json.loads(request.body)
    process=ChangeProfileImage(data['profile_image_src'], data['email'])
    return process.changeprofileimage()
@csrf_exempt
def removeprofileimage(request) :
    data=json.loads(request.body)
    process=RemoveProfileImage(data['email'], data['id'])
    return process.removeprofileimage()
@csrf_exempt
def changename(request) :
    data=json.loads(request.body)
    process=ChangeName(data['email'], data['newname'])
    return process.changeName()
@csrf_exempt
def changepio(request) :
    data=json.loads(request.body)
    process=ChangePio(data['email'], data['newname'])
    return process.changepio()
@csrf_exempt
def changePhone(request):
    data=json.loads(request.body)
    process=ChangePhone(data["email"], data["newphone"],)
    return process.changePhone()
@csrf_exempt
def changeEmail(request):
    data=json.loads(request.body)
    process=ChangeEmail(data["email"], data["newemail"])
    return process.changeEmail()
@csrf_exempt
def sendmessagewithoutfilesorimages(request) :
    data=json.loads(request.body)
    timenow=datetime.utcnow()
    process=SendMessageWithoutFilesOrImages(data['content'], data['image'], data['file'], timenow.year, timenow.month, timenow.day, timenow.hour + 2 , timenow.minute, timenow.second, data['email_sender'], data['email_reciever'])
    return process.sendMessageWithoutFilesOrImages()
@csrf_exempt
def sendmessagewithfiles(request) :
    data=json.loads(request.body)
    timenow=datetime.utcnow()
    process1=SendMessageWithoutFilesOrImages(data['content'], timenow.year, timenow.month, timenow.day, timenow.hour + 2 , timenow.minute, timenow.second, data['email_sender'], data['email_reciever'])
    process12=SendMessageWithFiles(data['message_id'], data['file'])
    return process2.sendMessageWithFiles()
@csrf_exempt
def sendmessagewithimages(request) :
    data=json.loads(request.body)
    timenow=datetime.utcnow()
    process1=SendMessageWithoutFilesOrImages(data['content'], timenow.year, timenow.month, timenow.day, timenow.hour + 2 , timenow.minute, timenow.second, data['email_sender'], data['email_reciever'])
    process12=SendMessageWithImages(data['message_id'], data['image'])
    return process2.sendMessageWithImages()
@csrf_exempt
def getrooms(request) :
    data=json.loads(request.body)
    process=getRooms(data['email'])
    return process
@csrf_exempt
def getchat(request) :
    data=json.loads(request.body)
    process=getChat(data['room_owner'], data['room_reciever'])
    return process
# defs two
def getDataForUser(email) :
    lst=[]
    res_main_data=cur.execute(f"SELECT * FROM user WHERE email='{email}'").fetchone()
    res_profile_image=cur.execute(f"SELECT * FROM profile_images WHERE email='{email}'").fetchall()
    try :
        if len(res_profile_image) >=1 :
            for i in range(0, len(res_profile_image)) :
                lst.append(res_profile_image[i])
            return serliazier.SerliazeprofileData(res_main_data, res_profile_image)
        else :
            return serliazier.SerliazeprofileData(res_main_data, [("https://images.pexels.com/photos/1799904/pexels-photo-1799904.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940", email, 2)])
    except :
        return serliazier.SerliazeprofileData(res_main_data, [("https://images.pexels.com/photos/1799904/pexels-photo-1799904.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940", email, 2)])
def Search(email, name) :
    res_data=[]
    lst_data=[]
    final_res_data=[]
    res=cur.execute("SELECT name, pio, email FROM user").fetchall()
    for item in res :
        data_query={
            "name" :item[0],
            "pio" :item[1],
            "email" :item[2]
        }
        lst_data.append(data_query)
    for item in lst_data :
        if name in item['name'] and email!=item['email'] :
            res_data.append(item)
    for item in res_data: 
        res_profile_images=cur.execute("SELECT src FROM profile_images WHERE email=?", [item['email']]).fetchall()
        newitem={
            "name" :item['name'],
            "pio" :item['pio'],
            "email" :item['email'],
            "profile_image" :res_profile_images[-1]
        }
        final_res_data.append(newitem)
    return JsonResponse(final_res_data, safe=False)    
# Create your views here.