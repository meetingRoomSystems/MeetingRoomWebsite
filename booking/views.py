from django.shortcuts import render
from django.http import HttpResponse
from .forms import GetRegister, GetLogin
import json,requests,datetime
from django.shortcuts import redirect
from .models import UserInfo

# url of the php file and database
url = 'https://compulynxmeetingrooms.000webhostapp.com/'
# url = 'http://localhost:3000/compulynx/'

def index(request):
    """ Renders the index page of the application """
    return render(request,'index.html',{
            'errorMessage' : '',
            'visibility':'hidden',
        })

def login(request):
    """ When user logins it this function checks if the username and password is correct """
    username = ''
    password = ''
    if request.method == 'POST':
        form = GetLogin(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
    loginURL = url + 'login.php?username={}&user_password={}'.format(username,password)
    loginResults =  json.loads(requests.get(loginURL).text)
    successCode = loginResults['success']
    if(successCode == 1):
        # check if we have the username in the local django database. If not add it
        fullname = loginResults['fullname']
        role = loginResults['role']
        try:
            database = UserInfo.objects.get(username = username)
            if(database.loggedIn):
                return render(request,'index.html',{
                        'errorMessage' : 'Already logged in. Please log out first',
                        'visibility':'visible',
                    })
            database.loggedIn = True
            database.role = role
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
    """ This function is used to register a user and add the user to the local and MySQL database """
    username = ''
    password = ''
    fullname = ''
    if request.method == 'POST':
        form = GetRegister(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            fullname = form.cleaned_data['fullname']
    punctuations = ['&','$','+',',','/',':',';','=','?','@','#','<','>','{','}','|','\\','^','%',' ']
    if any(x in username for x in punctuations) :
        return render(request,'index.html',{
            'errorMessage' : 'Wrong punctuation(s) used in username',
            'visibility':'hidden',
        })
    # add user to MySQL database
    fullname.title()
    loginURL = url + 'register.php?fullname={}&username={}&user_password={}'.format(fullname,username,password)
    loginResults =  json.loads(requests.get(loginURL).text)
    successCode = loginResults['success']
    if(successCode == 1):
        # add user to local database
        createUser = UserInfo(username = username,fullname=fullname,loggedIn=True,role='user')
        createUser.save()
        return redirect(homepage,username=username)
    else:
        return render(request,'index.html',{
                'errorMessage' : 'Username already exists',
                'visibility':'hidden',

            })

def logOutAll(request):
    """ log out a user from all browsers """
    username = ''
    password = ''
    if request.method == 'POST':
        form = GetLogin(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
    loginURL = url + 'login.php?username={}&user_password={}'.format(username,password)
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
    """ gets all the upcoming bookings for a user and all the bookings for today """
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

    # get all upcoming bookings for the user
    upcomingURL = url + 'getbooking.php?username={}'.format(username)
    upcomingResults =  json.loads(requests.get(upcomingURL).text)

    upcomingBookings = upcomingResults['bookings']

    # get all bookings for today
    allBookingURL = url + 'getbooking.php?booking_date={}'.format(datetime.datetime.today().strftime('%Y-%m-%d'))
    allBookingResults =  json.loads(requests.get(allBookingURL).text)
    allBookings = allBookingResults['bookings']
    
    # if there is a message to be shown as toast
    if request.session.has_key('message'):
        message = request.session['message']
        del request.session['message']
        if request.session.has_key('deleted'):
            deleted = request.session['deleted']
            del request.session['deleted']
            return render(request,'homepage.html',{
                'fullname':fullname.title(),
                'username':username,
                'bookings':upcomingBookings,
                'allBookings':allBookings,
                'today' : datetime.datetime.today().strftime('%Y-%m-%d'),
                'message': message,
                'role' : role,
                'deleted':deleted,
            })
        else:
            return render(request,'homepage.html',{
                'fullname':fullname.title(),
                'username':username,
                'bookings':upcomingBookings,
                'allBookings':allBookings,
                'today' : datetime.datetime.today().strftime('%Y-%m-%d'),
                'message': message,
                'role' : role,
            })
    else:
        if request.session.has_key('deleted'):
            deleted = request.session['deleted']
            del request.session['deleted']
            return render(request,'homepage.html',{
                'fullname':fullname.title(),
                'username':username,
                'bookings':upcomingBookings,
                'allBookings':allBookings,
                'today' : datetime.datetime.today().strftime('%Y-%m-%d'),
                'role' : role,
                'deleted':deleted,
            })
        else:
            return render(request,'homepage.html',{
                'fullname':fullname.title(),
                'username':username,
                'bookings':upcomingBookings,
                'allBookings':allBookings,
                'today' : datetime.datetime.today().strftime('%Y-%m-%d'),
                'role' : role,
             })

def rooms(request,username):
    """ used to show information about each meeting rooms """
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
    """ Used to show all available timings """
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

    # if an ajax call is made get all available bookings and send back as json format
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
            allBookingURL = url + 'getbooking.php?booking_date={}&room=0'.format(date)
            allBookingResults =  json.loads(requests.get(allBookingURL).text)
            namesURL = url + 'getAllUsers.php?username={}'.format(username)
            namesResults = json.loads(requests.get(namesURL).text)
            userList = namesResults['names']
            names = []
            for user in userList:
                names.append({'fullname':user['fullname'],'username':user['username']})

            allTimings = ["08:00:00","08:30:00","09:00:00","09:30:00","10:00:00","10:30:00","11:00:00","11:30:00","12:00:00","12:30:00","13:00:00","13:30:00","14:00:00","14:30:00","15:00:00","15:30:00","16:00:00", "16:30:00", "17:00:00","17:30:00"]
            booked_room1 = []
            booked_room2 = []
            booked_room3 = []
            booked_room4 = []
            available_room1 = []
            available_room2 = []
            available_room3 = []
            available_room4 = []
            # put all booked timings for each room in their respective arrays
            if(allBookingResults['success'] == 2):
                for booking_time in allBookingResults['room1']:
                    booked_room1.append(booking_time)
                for booking_time in allBookingResults['room2']:
                    booked_room2.append(booking_time)
                for booking_time in allBookingResults['room3']:
                    booked_room3.append(booking_time)
                for booking_time in allBookingResults['room4']:
                    booked_room4.append(booking_time)
                # add timings from allTimings into each available_room array only if that timing is not in booked_time
                for time in allTimings:
                    if time not in booked_room1:
                        available_room1.append(time)
                    if time not in booked_room2:
                        available_room2.append(time)
                    if time not in booked_room3:
                        available_room3.append(time)
                    if time not in booked_room4:
                        available_room4.append(time)
            response_data = {'room1':available_room1,'room2':available_room2,'room3':available_room3,'room4':available_room4,'names':names}
            #  send the data back in json
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
    """ Once user has given all booking details and confirmed booking, this function makes the booking """
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
    duration = request.GET.get('duration')
    if not duration:
        duration=30
    tags = request.GET.getlist('tags')
    # date and time in url is as a singe number. Parse and make them into the correct format
    date = date[0:4] + '-' + date[4:6] + '-' + date[6:]
    time = time[0:2]+ ":" + time[2:4] + ":" + time[4:]
    makeBookingURL = url + 'setbooking.php?fullname={}&username={}&capacity={}&room={}&booking_date={}&booking_time={}&length={}'.format(fullname,username,capacity,room,date,time,duration)
    if tags != []:
        for tag in tags:
            makeBookingURL += '&tags[]={}'.format(tag)
    else:
        makeBookingURL += '&tags[]=none'
    makeBookingResults =  json.loads(requests.get(makeBookingURL).text)
    checkIfMade = makeBookingResults['success']
    if(checkIfMade == 1):
        request.session['message'] = "Booking has been made"
        return redirect(homepage,username=username)
    else:
        request.session['message'] = "Booking has not been made. Try again later"
        return redirect(homepage,username=username)

def allBookings(request,username):
    """ get all bookings for a certain day and display it """
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

    allBookingURL = url + 'getbooking.php?all=2'
    allBookingResults =  json.loads(requests.get(allBookingURL).text)
    allBookings = allBookingResults['bookings']
    return render(request,'allBookings.html',{
        'fullname':fullname.title(),
        'username':username,
        'bookings':allBookings,
        'date':'2',
        'role' : role,
    })

def adminSettings(request,username):
    """ this page allows an admin to change the room of any booking or make any user an admin """
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

    # get all bookings
    allBookingURL = url + 'getbooking.php?all=1'
    allBookingResults =  json.loads(requests.get(allBookingURL).text)
    allBookings = allBookingResults['bookings']
    results = []
    if allBookingResults['bookings'] != '[]':
        # for each booking see which other rooms are available
        for book in allBookings:
            availableRoomsURL = url + 'getbooking.php?booking_date={}&booking_time={}&room={}'.format(book['booking_date'],book['booking_start'],book['room'])
            availableRoomsResults =  json.loads(requests.get(availableRoomsURL).text)
            if(availableRoomsResults['success'] == 1):
                rooms = availableRoomsResults['rooms']
                # see if rooms is a list or not
                if(isinstance(rooms, list)):
                    availableRooms = rooms
                else:
                    availableRooms = list(rooms.values())
            else:
                availableRooms = ['1','2','3','4']
            bookingDetails = {'username':book['username'],'fullname':book['fullname'],'duration':book['duration'],'booking_date':book['booking_date'],'booking_start':book['booking_start'],'booking_end':book['booking_end'],'room':book['room'],'capacity':int(book['capacity']),'availabeRooms':availableRooms,'others':book['others']}
            results.append(bookingDetails)
    bookingCountURL = url + 'getNumberOfBookings.php'
    bookingCountResults = json.loads(requests.get(bookingCountURL).text)
    bookingCount = bookingCountResults['results']
    updated = ''
    deleteOld = ''
    makeAdmin = ''
    if request.session.has_key('updated'):
        updated = request.session['updated']
        del request.session['updated']
    if request.session.has_key('deleteOld'):
        deleteOld = request.session['deleteOld']
        del request.session['deleteOld']
    if request.session.has_key('makeAdmin'):
        makeAdmin = request.session['makeAdmin']
        del request.session['makeAdmin']

    return render(request,'admin.html',{
        'fullname':fullname.title(),
        'username':username,
        'bookings':results,
        'updated': updated,
        'deleteOld':deleteOld,
        'makeAdmin':makeAdmin,
        'bookingCount':bookingCount,
        'role' : role,
   })

def changeRoom(request,admin,username,date,time,oldroom,newroom):
    """ change the room for a booking """
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

    changeURL = url + 'updatebooking.php?old_booking_date={}&old_booking_time={}&old_room={}&new_room={}&username={}&type=1'.format(date,time,oldroom,newroom,username)
    changeResults =  json.loads(requests.get(changeURL).text)
    if(changeResults['success'] == 1):
        request.session['updated'] = "Booking Updated"
    else:
        request.session['updated'] = "Booking Not Updated. Try again later"
    return redirect(adminSettings,username=admin)

def manage(request,username):
    """ show all bookings for a user with the option to delete their bookings """
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

    upcomingURL = url + 'getbooking.php?username={}'.format(username)
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
    """ function call to delete a booking """
    # see where the delete call was made from (can be from homepage or manage)
    referer = request.META.get('HTTP_REFERER')
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
    deleteURL = url + 'cancelbooking.php?username={}&room={}&booking_date={}&booking_time={}'.format(username,room,date,time)
    deleteResults =  json.loads(requests.get(deleteURL).text)
    if(deleteResults['success'] == 1):
        # if call is from homepage then redirect to homepage
        request.session['deleted'] = "Booking Deleted"
        if referer[-9:-1] == "homepage":
            return redirect(homepage,username=username)
        else:
            return redirect(manage,username=username)
    else:
        request.session['deleted'] = "Unable to delete booking. Try again later"
        return redirect(manage,username=username) # Change later

def logout(request,username):
    """ function call to log out """
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
    """ delete all old bookings from the MySQL database. Old bookings are all bookings on dates before today """
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

    deleteURL = url + 'deleteOldBooking.php?username={}'.format(username)
    deleteResults =  json.loads(requests.get(deleteURL).text)
    if(deleteResults['success'] == 1):
        request.session['deleteOld'] = "Old Bookings Deleted"
        return redirect(adminSettings,username=username)
    else:
        request.session['deleteOld'] = "Unable to delete old bookings. Try again later"
        return redirect(adminSettings,username=username) # Change later

def makeAdmin(request,username,name):
    """ function to make an user an admin """
    try:
        user = UserInfo.objects.get(username = username)
        if(user.loggedIn):
            fullname = user.fullname
            admin = user.username
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

    adminURL = url + 'makeAdmin.php?username={}'.format(name)
    adminResults =  json.loads(requests.get(adminURL).text)
    if(adminResults['success'] == 1):
        request.session['makeAdmin'] = name + " is now an admin"
        return redirect(adminSettings,username=username)
    else:
        request.session['makeAdmin'] = "Unable to make " + name + " an admin.Try again later"
        return redirect(adminSettings,username=username) # Change later
