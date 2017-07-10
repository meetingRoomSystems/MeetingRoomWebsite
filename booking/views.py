from django.shortcuts import render
from django.http import HttpResponse
from .forms import GetRegister, GetLogin
import json,requests,datetime
from django.shortcuts import redirect
from .models import UserInfo
# Create your views here.

def index(request):
    return render(request,'index.html',{
            'errorMessage' : '',
            'visibility':'hidden',
        })

def login(request):
    username = ''
    password = ''
    if request.method == 'POST':
        form = GetLogin(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
    loginURL = 'https://compulynxmeetingrooms.000webhostapp.com/login.php?username={}&user_password={}'.format(username,password)
    loginResults =  json.loads(requests.get(loginURL).text)
    successCode = loginResults['success']
    if(successCode == 1):
        fullname = loginResults['fullname']
        try:
            database = UserInfo.objects.get(username = username)
            if(database.loggedIn):
                return render(request,'index.html',{
                        'errorMessage' : 'Already logged in. Please log out first',
                        'visibility':'visible',
                    })
            database.loggedIn = True
            database.save()
            exists = True
        except UserInfo.DoesNotExist:
            exists = False

        if(exists):
            return redirect(homepage,username=username)
        else:
            createUser = UserInfo(username = username,fullname=fullname,loggedIn=True,role = loginResults['role'] )
            createUser.save()
            return redirect(homepage,username=username)
    else:
        return render(request,'index.html',{
                'errorMessage' : 'Invalid username/password',
                'visibility':'hidden',
            })

def register(request):
    username = ''
    password = ''
    fullname = ''
    if request.method == 'POST':
        form = GetRegister(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            fullname = form.cleaned_data['fullname']
    loginURL = 'https://compulynxmeetingrooms.000webhostapp.com/register.php?fullname={}&username={}&user_password={}'.format(fullname,username,password)
    loginResults =  json.loads(requests.get(loginURL).text)
    successCode = loginResults['success']
    if(successCode == 1):
        createUser = UserInfo(username = username,fullname=fullname,loggedIn=True,role='user')
        createUser.save()
        return redirect(homepage,username=username)
    else:
        return render(request,'index.html',{
                'errorMessage' : 'Username already exists',
                'visibility':'hidden',

            })

def logOutAll(request):
    username = ''
    password = ''
    if request.method == 'POST':
        form = GetLogin(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
    loginURL = 'https://compulynxmeetingrooms.000webhostapp.com/login.php?username={}&user_password={}'.format(username,password)
    loginResults =  json.loads(requests.get(loginURL).text)
    successCode = loginResults['success']
    if(successCode == 1):
        fullname = loginResults['fullname']
        try:
            database = UserInfo.objects.get(username = username)
            if(database.loggedIn):
                database.loggedIn = False
                database.save()
                return render(request,'index.html',{
                        'errorMessage' : '',
                        'visibility':'hidden',
                    })
        except UserInfo.DoesNotExist:
            return render(request,'index.html',{
                    'errorMessage' : 'Invalid username/password',
                    'visibility':'visible',
                })
    else:
        return render(request,'index.html',{
                'errorMessage' : 'Invalid username/password',
                'visibility':'visible',
            })

def homepage(request,username):
    try:
        user = UserInfo.objects.get(username = username)
        if(user.loggedIn):
            fullname = user.fullname
            username = user.username
            role = user.role
        else:
            return render(request,'index.html',{
                    'errorMessage' : 'Please Log in first',
                    'visibility':'hidden',
                })
    except Exception:
        return render(request,'index.html',{
              'errorMessage' : 'Please Log in first',
              'visibility':'hidden',
          })

    upcomingURL = 'https://compulynxmeetingrooms.000webhostapp.com/getbooking.php?username={}'.format(username)
    print(upcomingURL)
    upcomingResults =  json.loads(requests.get(upcomingURL).text)

    upcomingBookings = upcomingResults['bookings']

    allBookingURL = 'https://compulynxmeetingrooms.000webhostapp.com/getbooking.php?booking_date={}'.format(datetime.datetime.today().strftime('%Y-%m-%d'))
    allBookingResults =  json.loads(requests.get(allBookingURL).text)
    allBookings = allBookingResults['bookings']
    if request.session.has_key('message'):
        message = request.session['message']
        del request.session['message']
        return render(request,'homepage.html',{
            'fullname':fullname.title(),
            'username':username,
            'bookings':upcomingBookings,
            'allBookings':allBookings,
            'message': message,
            'role' : role,
       })

    else:
        return render(request,'homepage.html',{
            'fullname':fullname.title(),
            'username':username,
            'bookings':upcomingBookings,
            'allBookings':allBookings,
            'role' : role,
         })

def rooms(request,username):
    try:
        user = UserInfo.objects.get(username = username)
        if(user.loggedIn):
            fullname = user.fullname
            username = user.username
            role = user.role
        else:
            return render(request,'index.html',{
              'errorMessage' : 'Please Log in first',
              'visibility':'hidden',
          })
    except Exception:
        return render(request,'index.html',{
              'errorMessage' : 'Please Log in first',
              'visibility':'hidden',
          })

    return render(request,'rooms.html',{
        'fullname':fullname.title(),
        'username':username,
        'role' : role,
    })

def newBooking(request,username):
    try:
        user = UserInfo.objects.get(username = username)
        if(user.loggedIn):
            fullname = user.fullname
            username = user.username
            role = user.role
        else:
            return render(request,'index.html',{
                    'errorMessage' : 'Please Log in first',
                    'visibility':'hidden',
                })
    except Exception:
        return render(request,'index.html',{
              'errorMessage' : 'Please Log in first',
              'visibility':'hidden',
          })

    if request.method == 'POST':
        date = request.POST.get('date')
        type = request.POST.get('type')

        if type == '1':
            outside = True
        else:
            outside = False

        if outside:
            return render(request,'newBooking.html',{
                'fullname':fullname.title(),
                'username':username,
                'date':'1',
                'role' : role,
            })
        else:
            allBookingURL = 'https://compulynxmeetingrooms.000webhostapp.com/getbooking.php?booking_date={}&room=0'.format(date)
            allBookingResults =  json.loads(requests.get(allBookingURL).text)

            allTimings = ["08:00:00","08:30:00","09:00:00","09:30:00","10:00:00","10:30:00","11:00:00","11:30:00","12:00:00","12:30:00","13:00:00","13:30:00","14:00:00","14:30:00","15:00:00","15:30:00","16:00:00", "16:30:00", "17:00:00","17:30:00"]
            booked_times_1 = []
            booked_times_2 = []
            booked_times_3 = []
            booked_times_4 = []
            room1 = []
            room2 = []
            room3 = []
            room4 = []
            if(allBookingResults['success'] == 2):
                for booking_time in allBookingResults['room1']:
                    booked_times_1.append(booking_time)
                for booking_time in allBookingResults['room2']:
                    booked_times_2.append(booking_time)
                for booking_time in allBookingResults['room3']:
                    booked_times_3.append(booking_time)
                for booking_time in allBookingResults['room4']:
                    booked_times_4.append(booking_time)
                for time in allTimings:
                    if time not in booked_times_1:
                        room1.append(time)
                    if time not in booked_times_2:
                        room2.append(time)
                    if time not in booked_times_3:
                        room3.append(time)
                    if time not in booked_times_4:
                        room4.append(time)
            response_data = {'room1':room1,'room2':room2,'room3':room3,'room4':room4}

            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )

    return render(request,'newBooking.html',{
        'fullname':fullname.title(),
        'username':username,
        'role' : role,

    })

def makeBooking(request,username,room,date,time):
    try:
        user = UserInfo.objects.get(username = username)
        if(user.loggedIn):
            fullname = user.fullname
            username = user.username
            role = user.role
        else:
            return render(request,'index.html',{
              'errorMessage' : 'Please Log in first',
              'visibility':'hidden',
          })
    except Exception:
        return render(request,'index.html',{
              'errorMessage' : 'Please Log in first',
              'visibility':'hidden',
          })

    capacity = request.GET.get('capacity')
    date = date[0:4] + '-' + date[4:6] + '-' + date[6:]
    time = time[0:2]+ ":" + time[2:4] + ":" + time[4:]
    makeBookingURL = 'https://compulynxmeetingrooms.000webhostapp.com/setbooking.php?fullname={}&username={}&capacity={}&room={}&booking_date={}&booking_time={}'.format(fullname,username,capacity,room,date,time)
    makeBookingResults =  json.loads(requests.get(makeBookingURL).text)
    checkIfMade = makeBookingResults['success']
    if(checkIfMade == 1):
        request.session['message'] = "Booking has been made"
        return redirect(homepage,username=username)
    else:
        request.session['message'] = "Booking has not been made. Try again later"
        return redirect(homepage,username=username)

def allBookings(request,username):
    try:
        user = UserInfo.objects.get(username = username)
        if(user.loggedIn):
            fullname = user.fullname
            username = user.username
            role = user.role
        else:
            return render(request,'index.html',{
              'errorMessage' : 'Please Log in first',
              'visibility':'hidden',
          })
    except Exception:
        return render(request,'index.html',{
              'errorMessage' : 'Please Log in first',
              'visibility':'hidden',
          })

    if request.method == 'POST':
        date = request.POST.get('date')
        type = request.POST.get('type')

        if type == '1':
            outside = True
        else:
            outside = False

        if outside:
            return render(request,'allBookings.html',{
                'fullname':fullname.title(),
                'username':username,
                'date':'1',
                'role' : role,
            })
        else:
            allBookingURL = 'https://compulynxmeetingrooms.000webhostapp.com/getbooking.php?booking_date={}'.format(date)
            allBookingResults =  json.loads(requests.get(allBookingURL).text)
            allBookings = allBookingResults['bookings']
            response_data = {"bookings":allBookings}

            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
    else:
        return render(request,'allBookings.html',{
            'fullname':fullname.title(),
            'username':username,
            'date':'2',
            'role' : role,
        })

def adminSettings(request,username):
    try:
        user = UserInfo.objects.get(username = username)
        if(user.loggedIn):
            fullname = user.fullname
            username = user.username
            role = user.role
            if(role != 'admin'):
                return redirect(homepage,username = username)
        else:
            return render(request,'index.html',{
              'errorMessage' : 'Please Log in first',
              'visibility':'hidden',
             })
    except Exception:
        return render(request,'index.html',{
              'errorMessage' : 'Please Log in first',
              'visibility':'hidden',
          })

    allBookingURL = 'https://compulynxmeetingrooms.000webhostapp.com/getbooking.php?all=1'
    allBookingResults =  json.loads(requests.get(allBookingURL).text)
    allBookings = allBookingResults['bookings']
    results = []
    for book in allBookings:
        availableRoomsURL = 'https://compulynxmeetingrooms.000webhostapp.com/getbooking.php?booking_date={}&booking_time={}&room=0'.format(book['booking_date'],book['booking_time'])
        availableRoomsResults =  json.loads(requests.get(availableRoomsURL).text)
        availableRooms = []
        if(availableRoomsResults['room1'] == []):
            availableRooms.append('1')
        if(availableRoomsResults['room2'] == []):
            availableRooms.append('2')
        if(availableRoomsResults['room3'] == []):
            availableRooms.append('3')
        if(availableRoomsResults['room4'] == []):
            availableRooms.append('4')
        bookingDetails = {'username':book['username'],'fullname':book['fullname'],'booking_date':book['booking_date'],'booking_time':book['booking_time'],'room':book['room'],'capacity':int(book['capacity']),'availabeRooms':availableRooms}
        results.append(bookingDetails)
    updated = ''
    deleteOld = ''
    if request.session.has_key('updated'):
        updated = request.session['updated']
        del request.session['updated']
    if request.session.has_key('deleteOld'):
        deleteOld = request.session['deleteOld']
        del request.session['deleteOld']

    return render(request,'admin.html',{
        'fullname':fullname.title(),
        'username':username,
        'bookings':results,
        'updated': updated,
        'deleteOld':deleteOld,
        'role' : role,
   })

def changeRoom(request,admin,username,date,time,oldroom,newroom):
    try:
        user = UserInfo.objects.get(username = admin)
        if(user.loggedIn):
            fullname = user.fullname
            admin = user.username
            role = user.role
            if(role != 'admin'):
                return redirect(request,username = admin)
        else:
            return render(request,'index.html',{
              'errorMessage' : 'Please Log in first',
              'visibility':'hidden',
             })
    except Exception:
        return render(request,'index.html',{
              'errorMessage' : 'Please Log in first',
              'visibility':'hidden',
          })
    changeURL = 'https://compulynxmeetingrooms.000webhostapp.com/updatebooking.php?old_booking_date={}&old_booking_time={}&old_room={}&new_room={}&username={}&type=1'.format(date,time,oldroom,newroom,username)
    changeResults =  json.loads(requests.get(changeURL).text)
    print(changeURL)
    if(changeResults['success'] == 1):
        request.session['updated'] = "Booking Updated"
    else:
        request.session['updated'] = "Booking Not Updated. Try again later"
    return redirect(adminSettings,username=admin)

def manage(request,username):
    try:
        user = UserInfo.objects.get(username = username)
        if(user.loggedIn):
            fullname = user.fullname
            username = user.username
            role = user.role
        else:
            return render(request,'index.html',{
              'errorMessage' : 'Please Log in first',
              'visibility':'hidden',
          })
    except Exception:
        return render(request,'index.html',{
              'errorMessage' : 'Please Log in first',
              'visibility':'hidden',
          })

    upcomingURL = 'https://compulynxmeetingrooms.000webhostapp.com/getbooking.php?username={}'.format(username)
    upcomingResults =  json.loads(requests.get(upcomingURL).text)
    upcomingBookings = upcomingResults['bookings']
    if request.session.has_key('deleted'):
        deleted = request.session['deleted']
        del request.session['deleted']
        return render(request,'manage.html',{
            'fullname':fullname.title(),
            'username':username,
            'bookings':upcomingBookings,
            'role' : role,
            'deleted':deleted,
        })
    else:
        return render(request,'manage.html',{
            'fullname':fullname.title(),
            'username':username,
            'bookings':upcomingBookings,
            'role' : role,
        })

def delete(request,username,date,time,room):
    try:
        user = UserInfo.objects.get(username = username)
        if(user.loggedIn):
            fullname = user.fullname
            username = user.username
        else:
            return render(request,'index.html',{
              'errorMessage' : 'Please Log in first',
              'visibility':'hidden',
          })
    except Exception:
        return render(request,'index.html',{
              'errorMessage' : 'Please Log in first',
              'visibility':'hidden',
          })
    deleteURL = 'https://compulynxmeetingrooms.000webhostapp.com/cancelbooking.php?username={}&room={}&booking_date={}&booking_time={}'.format(username,room,date,time)
    deleteResults =  json.loads(requests.get(deleteURL).text)
    if(deleteResults['success'] == 1):
        request.session['deleted'] = "Booking Deleted"
        return redirect(manage,username=username)
    else:
        request.session['deleted'] = "Unable to delete booking. Try again later"
        return redirect(manage,username=username) # Change later

def logout(request,username):
    try:
        user = UserInfo.objects.get(username = username)
        if(user.loggedIn):
            fullname = user.fullname
            username = user.username
        else:
            return render(request,'index.html',{
              'errorMessage' : 'Please Log in first',
              'visibility':'hidden',
          })
    except Exception:
        return render(request,'index.html',{
              'errorMessage' : 'Please Log in first',
              'visibility':'hidden',
          })

    user.loggedIn=False
    user.save()
    return redirect(index)

def deleteOld(request,username):
    try:
        user = UserInfo.objects.get(username = username)
        if(user.loggedIn):
            fullname = user.fullname
            username = user.username
            role = user.role
            if(role != 'admin'):
                return redirect(homepage,username = username)
        else:
            return render(request,'index.html',{
              'errorMessage' : 'Please Log in first',
              'visibility':'hidden',
             })
    except Exception:
        return render(request,'index.html',{
              'errorMessage' : 'Please Log in first',
              'visibility':'hidden',
          })

    deleteURL = 'https://compulynxmeetingrooms.000webhostapp.com/deleteOldBooking.php?username={}'.format(username)
    deleteResults =  json.loads(requests.get(deleteURL).text)
    if(deleteResults['success'] == 1):
        request.session['deleted'] = "Old Bookings Deleted"
        return redirect(manage,username=username)
    else:
        request.session['deleted'] = "Unable to delete old bookings. Try again later"
        return redirect(manage,username=username) # Change later
