from django.shortcuts import render
from django.http import HttpResponse
from .forms import User_Form
from .models import LicensePlates, LicensePlatesUser, LicensePlatesParking, ParkingHistory, StaffParking, Staff, User
from django.views import View
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.http import JsonResponse, HttpResponseServerError, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
import random, string
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
import base64, time
import requests
from datetime import datetime
from django.utils.dateparse import parse_time, parse_date
import json
from django.views.decorators.csrf import csrf_exempt

# import detect
import home.detect.detect_dropplate as detect_dropplate
import os, numpy as np, cv2
from PIL import Image
from ultralytics import YOLO

def generate_random_user_id():
    random_number = random.randint(0, 999999)
    return f"user{random_number:08d}"  # Định dạng thành số có 4 chữ số

def generate_random_staff_id():
    random_number = random.randint(0, 999999)
    return f"user{random_number:08d}"  # Định dạng thành số có 4 chữ số

def generate_random_parking_history_id():
    random_number = random.randint(0, 999999)
    return f"park{random_number:08d}"  # Định dạng thành số có 4 chữ số

def generate_random_plate_number_id():
    random_number = random.randint(0, 999999)
    return f"pl{random_number:08d}"  # Định dạng thành số có 4 chữ số

def index(request):
    try:
        # release_camera()
        context = {}
        return render(request, 'app/index.html', context)
    except Exception as e:
        # Ghi log hoặc in ra console để theo dõi lỗi
        print(f"Error in 'index' view: {e}")
        # Trả về một trang lỗi có thể hiển thị cho người dùng
        return HttpResponseServerError("Internal Server Error")
    
def managerStaff_User(request):
    if request.method == 'POST':
        try:

            user_id = request.POST.get('user_id_manage')
            user = User.objects.get(id=user_id)
            
            lp = LicensePlatesUser.objects.get(userID=user_id)
            # platesNumber =  LicensePlates.objects.get(lp)
            all_users = User.objects.filter(role='user')

            context = {
                'User': user,
                'Lp' : lp.license_plates.license_plates,
                'all_users': all_users
            }
            return render(request, 'app/manager_update_staff.html', context)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Parking history with the given ID does not exist'})
    return JsonResponse({'error': 'Invalid request'})

def manager_staff(request):
    if request.method == "POST" and "backButton" in request.POST:
        return render(request, 'app/manager_staff.html', context)
    all_users = User.objects.filter(role='user')
    context = {'all_users': []}
    for user in all_users:
        plate_numbers = LicensePlatesUser.objects.filter(userID=user.id).values_list('license_plates', flat=True)
        context['all_users'].append({'user': user, 'plate_numbers': plate_numbers})
    return render(request, 'app/manager_staff.html', context)

def managerStaff_delete(request):
    if request.method == 'POST':
        try:
            user_id = request.POST.get('user_id_delete')
            user_to_delete = User.objects.get(id=user_id)
            user_to_delete.delete()
            # messages.success(request, 'Xóa thành công')
            return redirect('managerStaff')  # Chuyển hướng đến trang chính sau khi xóa thành công

        except User.DoesNotExist:
            # messages.error(request, 'Không tìm thấy người dùng cần xóa')
            return redirect('managerStaff')  # Chuyển hướng trở lại trang chính nếu không tìm thấy người dùng cần xóa

    return render(request, 'manager_staff_delete.html')

def historyStaff_delete(request):
    if request.method == 'POST':
        try:
            history_id = request.POST.get('history_id_delete')
            history_to_delete = ParkingHistory.objects.get(parking_historyID=history_id)
            history_to_delete.delete()
            # messages.success(request, 'Xóa thành công')
            return redirect('historyStaff')  # Chuyển hướng đến trang chính sau khi xóa thành công

        except User.DoesNotExist:
            # messages.error(request, 'Không tìm thấy người dùng cần xóa')
            return redirect('historyStaff')  # Chuyển hướng trở lại trang chính nếu không tìm thấy người dùng cần xóa

    return render(request, 'manager_staff_delete.html')

def managerStaff_register(request):
    if request.method == 'POST':
        id = generate_random_user_id()
        username = request.POST['username']
        password = request.POST['password']
        fullname = request.POST['fullname']
        email = request.POST['email']
        date_of_birth = request.POST['date_of_birth']
        position = request.POST['position']
        phone = request.POST['phone']
        account_balance = request.POST['account_balance']
        license_plates = request.POST['plate_number']

        try :
            new_user = User(id=id, username=username, password=password, fullname=fullname, email=email, date_of_birth=date_of_birth, position=position, phone=phone, account_balance=account_balance, role='user')
            new_user.save()

            lp = LicensePlates(license_platesID=license_plates, license_plates=license_plates)
            lp.save()

            lp_new = LicensePlates.objects.get(license_platesID = license_plates)

            lpUser = LicensePlatesUser(userID=id, license_plates=lp_new)
            lpUser.save()

            # messages.success(request, 'Đăng ký thành công')
            return redirect('managerStaff')  # Chuyển hướng đến trang chính sau khi đăng ký

        except ObjectDoesNotExist:
            # messages.error(request, 'Mật khẩu không khớp')
            return redirect('register')  # Chuyển hướng trở lại trang đăng ký nếu mật khẩu không khớp

    return render(request, 'register.html')

def update_staff(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            user.username = request.POST['username']
            user.password = request.POST['password']
            user.fullname = request.POST['fullname']
            user.email = request.POST['email']
            user.date_of_birth = request.POST['date_of_birth']
            user.position = request.POST['position']
            user.phone = request.POST['phone']

            user.account_balance = float(request.POST['account_balance'])  # Chuyển đổi account_balance sang float
            user.save()
            return redirect('managerStaff')
        except (User.DoesNotExist, ValueError) as e:
            # Xử lý trường hợp không tìm thấy người dùng hoặc lỗi chuyển đổi dữ liệu
            # In hoặc xử lý lỗi theo cách mong muốn
            print(f"Có lỗi xảy ra: {e}")
            # Hoặc thêm mã để thông báo lỗi đến người dùng

    else:
        user_id = request.GET.get('user_id')  # Sử dụng request.GET để trích xuất user_id từ yêu cầu GET
        try:
            user = User.objects.get(id=user_id)
            context = {'user': user}
            return render(request, 'app/update_user.html', context)
        except User.DoesNotExist:
            # Xử lý trường hợp không tìm thấy người dùng
            # Hoặc thêm mã để thông báo lỗi đến người dùng
            pass  # Có thể thêm mã để xử lý trường hợp này



# def historyStaff1(request):
#     if request.method == 'POST':
#         try:
#             parking_history = ParkingHistory.objects.filter(license_plates__in=LicensePlates.objects.all())

#             history_id = request.POST.get('history_id')
#             history = ParkingHistory.objects.get(parking_historyID=history_id)
#             time_in = history.time_in
#             time_out = history.time_out
#             date_in = history.date_in
#             date_out = history.date_out
#             total_price = history.total
#             license_plate_number = history.license_plates.license_plates

#             try:    
#                 user = User.objects.get(id=history.license_plates.licenseplatesuser_set.first().userID)
#                 full_name = user.fullname
#                 phone_number = user.phone
#                 address = user.position

#                 context = {
#                     'full_name': full_name,
#                     'license_plate_number': license_plate_number,
#                     'phone_number': phone_number,
#                     'address': address,
#                     'time_in': time_in,
#                     'date_in': date_in,
#                     'time_out': time_out,
#                     'date_out': date_out,
#                     'total_price': total_price,
#                     'parking_history': parking_history
#                 }
#             except User.DoesNotExist:
#                 context = {
#                     'full_name': 'Chưa đăng ký',
#                     'license_plate_number': license_plate_number,
#                     'phone_number': '',
#                     'address': '',
#                     'time_in': time_in,
#                     'date_in': date_in,
#                     'time_out': time_out,
#                     'date_out': date_out,
#                     'total_price': total_price,
#                     'parking_history': parking_history
#                 }
#             return render(request, 'app/history_staff_full.html', context)
#         except ObjectDoesNotExist:
#             return JsonResponse({'error': 'Parking history with the given ID does not exist'})
#     return JsonResponse({'error': 'Invalid request'})

def historyStaff1(request):
    if request.method == 'POST':
        try:
            parking_history = ParkingHistory.objects.filter(license_plates__in=LicensePlates.objects.all())
            history_id = request.POST.get('history_id')
            history = ParkingHistory.objects.get(parking_historyID=history_id)
            time_in = history.time_in
            time_out = history.time_out
            date_in = history.date_in
            date_out = history.date_out
            total_price = history.total
            license_plate_number = history.license_plates.license_plates
            license_plate_user = history.license_plates.licenseplatesuser_set.first()
            if license_plate_user:
                user = User.objects.get(id=license_plate_user.userID)
                full_name = user.fullname
                phone_number = user.phone
                address = user.position
            else:
                full_name = 'Chưa đăng ký'
                phone_number = ''
                address = ''
            context = {
                'full_name': full_name,
                'license_plate_number': license_plate_number,
                'phone_number': phone_number,
                'address': address,
                'time_in': time_in,
                'date_in': date_in,
                'time_out': time_out,
                'date_out': date_out,
                'total_price': total_price,
                'parking_history': parking_history
            }
            return render(request, 'app/history_staff_full.html', context)
        except ParkingHistory.DoesNotExist:
            return JsonResponse({'error': 'Parking history with the given ID does not exist'})
    return JsonResponse({'error': 'Invalid request'})



def history_staff(request):
    parking_history = ParkingHistory.objects.filter(license_plates__in=LicensePlates.objects.all())
    context = {'parking_history': parking_history}
    return render(request, 'app/history_staff.html', context)

def index_staff(request): 
    global camera_in
    global camera_out
    if camera_in is None or camera_out is None:
        # Gọi các hàm chỉ một lần sau khi người dùng đăng nhập
        initialize_camera()
        # has_functions_been_called = True

    # response_data = request.GET.get('data', '')
    all_users = User.objects.filter(role='user')
    context = {'all_users': []}
    for user in all_users:
        plate_numbers = LicensePlatesUser.objects.filter(userID=user.id).values_list('license_plates', flat=True)
        context['all_users'].append({'user': user, 'plate_numbers': plate_numbers})

    return render(request, 'app/index_staff.html', context)

@csrf_exempt
def historyIn(request): 
    if request.method == 'POST':
        user_plate_in = request.POST.get('userPlateIn', None)
        id = generate_random_parking_history_id()

        try:
            user_plates = LicensePlates.objects.get(license_plates=user_plate_in)
            if user_plates:
                try:
                    pk_old = ParkingHistory.objects.filter(license_plates=user_plates, state=0)
                    if(not pk_old):
                        user_time_in = request.POST.get('userTimeIn', '')
                        user_date_in = request.POST.get('userDateIn', '')
                        state = 0
                        pkHistory = ParkingHistory(parking_historyID=id, license_plates=user_plates, time_in=user_time_in, date_in=user_date_in, state=state)
                        pkHistory.save()
                        response_data = 'Đăng ký xe vào thành công'
                    else:
                        response_data = 'Đăng ký xe vào không thành công'
                except ParkingHistory.DoesNotExist:
                    response_data = 'Đăng ký xe vào không thành công'
                return HttpResponse(response_data)
        except LicensePlates.DoesNotExist:
            lp = LicensePlates(license_platesID=user_plate_in, license_plates=user_plate_in)
            lp.save()

            try:
                pk_old = ParkingHistory.objects.filter(license_plates=lp, state=0)
                if(not pk_old):
                    user_time_in = request.POST.get('userTimeIn', '')
                    user_date_in = request.POST.get('userDateIn', '')
                    state = 0
                    pkHistory = ParkingHistory(parking_historyID=id, license_plates=lp, time_in=user_time_in, date_in=user_date_in, state=state)
                    pkHistory.save()
                    response_data = 'Đăng ký xe vào tạm thời'
                else:
                    response_data = 'Đăng ký xe vào không thành công'
            except ParkingHistory.DoesNotExist:
                user_time_in = request.POST.get('userTimeIn', '')
                user_date_in = request.POST.get('userDateIn', '')
                state = 0
                pkHistory = ParkingHistory(parking_historyID=id, license_plates=lp, time_in=user_time_in, date_in=user_date_in, state=state)
                pkHistory.save()
                response_data = 'Đăng ký xe vào tạm thời'
            return HttpResponse(response_data)
            

@csrf_exempt
def historyOut(request): 
    if request.method == 'POST':
        user_plate_out = request.POST.get('userPlateOut', None)
        if not user_plate_out:
            response_data = 'Đăng ký xe ra không thành công'
            return HttpResponse(response_data)
            
        try:
            user_plate = LicensePlates.objects.get(license_plates=user_plate_out)
        except LicensePlates.DoesNotExist:
            response_data = 'Đăng ký xe ra không thành công'
            return HttpResponse(response_data)

        try:
            history = ParkingHistory.objects.get(license_plates=user_plate, state='0')

            user_time_in = history.time_in
            user_date_in = history.date_in
            user_time_out = request.POST.get('userTimeOut', '')
            user_date_out = request.POST.get('userDateOut', '')

            user_time_out = parse_time(user_time_out)
            user_date_out = parse_date(user_date_out)

            datetime_in = datetime.combine(user_date_in, user_time_in)
            datetime_out = datetime.combine(user_date_out, user_time_out)
            # Tính khoảng thời gian giữa datetime_out và datetime_in
            time_difference = datetime_out - datetime_in
            minutes = time_difference.total_seconds() / 60

            history.time_out = user_time_out
            history.date_out = user_date_out
            if minutes <= 30:
                total = 10000
            elif minutes > 30 and minutes <= 120:
                total = 10000 + int(minutes) * 200
            elif minutes > 120:
                total = 10000 + int(minutes) * 100

            # minutes = time_difference.total_seconds()
            # total = minutes
    
            history.total = total

            try:
                userID = LicensePlatesUser.objects.get(license_plates=user_plate)
                user = User.objects.get(id = userID.userID)
                if user.account_balance >= total:
                    user.account_balance -= total
                    history.state = 1
                    history.save()
                    response_data = 'Thanh toán thành công'
                    return HttpResponse(response_data)
                else:
                    history.state = 1
                    history.save()
                    response_data = 'Tài khoản không đủ!\n Vui lòng thanh toán bằng tiền mặt'
                    return HttpResponse(response_data)
            except LicensePlatesUser.DoesNotExist:
                history.state = 1
                history.save()
                response_data = 'Thanh toán bằng tiền mặt'
                return HttpResponse(response_data)   
            except User.DoesNotExist:
                history.state = 1
                history.save()
                response_data = 'Thanh toán bằng tiền mặt'
                return HttpResponse(response_data)          

        except ParkingHistory.DoesNotExist:
            response_data = 'Đăng ký xe ra không thành công'
            return HttpResponse(response_data)

@csrf_exempt
def getTotal(request): 
    if request.method == 'POST':
        user_plate_out = request.POST.get('userPlateOut', None)
        try:
            user_plate = LicensePlates.objects.get(license_plates=user_plate_out)
            history = ParkingHistory.objects.get(license_plates=user_plate, state='0')

            user_time_in = history.time_in
            user_date_in = history.date_in
            user_time_out = request.POST.get('userTimeOut', '')
            user_date_out = request.POST.get('userDateOut', '')

            user_time_out = parse_time(user_time_out)
            user_date_out = parse_date(user_date_out)

            datetime_in = datetime.combine(user_date_in, user_time_in)
            datetime_out = datetime.combine(user_date_out, user_time_out)
            # Tính khoảng thời gian giữa datetime_out và datetime_in
            time_difference = datetime_out - datetime_in
            minutes = time_difference.total_seconds() / 60

            history.time_out = user_time_out
            history.date_out = user_date_out
            if minutes <= 30:
                total = 10000
            elif minutes > 30 and minutes <= 120:
                total = 10000 + int(minutes) * 200
            elif minutes > 120:
                total = 10000 + int(minutes) * 100

            # minutes = time_difference.total_seconds()
            # total = minutes

            response_data = total
            return HttpResponse(response_data)

        except ParkingHistory.DoesNotExist:
            response_data = 0
            return HttpResponse(response_data)
        except LicensePlates.DoesNotExist:
            response_data = 0
            return HttpResponse(response_data)
        
# response_data = f"{frame_out_base64_data}|{new_img_base64_data}|{kitu}|{'none'}|{'Chưa đăng ký'}|{kitu}"
@csrf_exempt
def checkTotal(request): 
    if request.method == 'POST':
        user_plate = request.POST.get('userPlateOut', None)
        getTotal = request.POST.get('getTotal', None)
        user_plate = LicensePlates.objects.get(license_plates=user_plate)
        user_plates = LicensePlatesUser.objects.get(license_plates=user_plate)

        users = User.objects.get(id=user_plates.userID)
        
        if float(getTotal) > users.account_balance:
            response_data = "Tài khoản không đủ!!! Vui lòng thanh toán bằng tiền mặt!"
        else:
            response_data = "Thực hiện thanh toán!"
        return HttpResponse(response_data)
        


#def index_user(request):
#    context = {}
#    return render(request, 'app/index_user.html', context)
def index_user(request):
    user_id = request.session.get('user', None)  # Lấy thông tin người dùng từ session
    if user_id is not None:
        user = User.objects.get(id=user_id)
        license_plates = LicensePlatesUser.objects.filter(userID=user_id)
        context = {'user': user, 'license_plates':license_plates}
        return render(request, 'app/index_user.html', context)
    else:
        return redirect('login')

def update_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        user.fullname = request.POST['fullname']
        user.email = request.POST['email']
        user.date_of_birth = request.POST['date_of_birth']
        user.phone = request.POST['phone']
        user.position = request.POST['position']
        user.save()

        return redirect('indexUser')
    else:
        user_id = request.POST.get('user_id') # Kiểm tra nếu cần trích xuất user_id từ yêu cầu GET
        user = User.objects.get(id=user_id)
        context = {'user': user}
        return render(request, 'app/update_user.html', context)
    
def addLicensePlate_User(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        license_plates = request.POST.get('license_plates')
        lp = LicensePlates(license_platesID=license_plates, license_plates=license_plates)
        lp.save()

        lp_new = LicensePlates.objects.get(license_platesID = license_plates)

        lpUser = LicensePlatesUser(userID=user_id, license_plates=lp_new)
        lpUser.save()
        # messages.success(request, 'Đăng ký thành công')

        return redirect('indexUser')  # Chuyển hướng đến trang chính sau khi đăng ký
    
    else:
        user_id = request.POST.get('user_id') # Kiểm tra nếu cần trích xuất user_id từ yêu cầu GET
        user = User.objects.get(id=user_id)
        context = {'user': user}
        return render(request, 'app/index_user.html', context)


def history_user(request):
    user_id = request.session.get('user', None)  # Lấy thông tin người dùng từ session
    if user_id is not None:
        parking_history = ParkingHistory.objects.filter(license_plates__licenseplatesuser__userID=user_id)
        context = {'parking_history': parking_history}
        return render(request, 'app/history_user.html', context)
    else:
        return redirect('login')

class contact(View):
    def get(self, request):
        context = {'cf': User_Form}
        return render(request, 'contact/contact.html', context)

    def post(self, request):
        if request.method == "POST":
            cf = User_Form(request.POST)
            if cf.is_valid():
                cf.save()
                return HttpResponse("save success")
        else:
            return HttpResponse("no post")
def contactDetail(request):
    cV = User.objects.all()
    context = {'cV':cV}
    return render(request, 'contact/contactDetail.html', context)
def contactView(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        cD = User.objects.get(id = id)
        context = {'cD':cD}
        return render(request, 'contact/contactView.html', context)
    return render(request, 'contact/contactDetail.html', {})
""""""


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        users =  User.objects.filter(username=username)
        if users.exists():
            for user in users:
                if password == user.password:
                    if user.role == 'user':
                        request.session['user'] = user.id  # Lưu thông tin người dùng vào session
                        return redirect('indexUser')  # Chuyển hướng đến indexUser
                    if user.role == 'staff':
                        request.session['user'] = user.id  # Lưu thông tin người dùng vào session
                        # initialize_camera()
                        return redirect('indexStaff')  # Chuyển hướng đến indexStaff
            return render(request, 'app/index.html', {'error_message': 'Invalid login'})
        else:
            # Return an 'invalid login' error message.
            return render(request, 'app/index.html', {'error_message': 'Invalid login'})
    else:
        return render(request, 'app/index.html')

def register_user(request):
    if request.method == 'POST':
        id = generate_random_user_id()
        username = request.POST['registerUsername']
        password = request.POST['registerPassword']
        confirm_password = request.POST['registerPasswordConfirm']
        registerName = request.POST['registerName']
        registerEmail = request.POST['registerEmail']
        registerDob = request.POST['registerDob']
        registerAddress = request.POST['registerAddress']
        registerPhone = request.POST['registerPhone']


        if password == confirm_password:
            new_user = User(id=id, username=username, password=password, confirm_password=confirm_password,registerName=registerName, registerEmail=registerEmail ,
                            registerDob=registerDob, registerAddress=registerAddress, registerPhone=registerPhone, role='user')
            new_user.save()
            # messages.success(request, 'Đăng ký thành công')
            return redirect('index')  # Chuyển hướng đến trang chính sau khi đăng ký

        else:
            # messages.error(request, 'Mật khẩu không khớp')
            return redirect('register')  # Chuyển hướng trở lại trang đăng ký nếu mật khẩu không khớp

    return render(request, 'register.html')


# oad
esp32_cam_in_ip = '192.168.43.24'
esp32_cam_out_ip = '192.168.43.78'

camera_in = None
camera_out = None
model_plates_path = os.path.abspath('D:/HK5/HK5_h/pbl4/be/PBL4 - Bao - Test/PBL4/myweb/home/detect/best_plates.pt')
model_charaters_path = os.path.abspath('D:/HK5/HK5_h/pbl4/be/PBL4 - Bao - Test/PBL4/myweb/home/detect/best_characters.pt')
# Load a model
model_plates = YOLO(model_plates_path)  # load a plates model
model_charaters = YOLO(model_charaters_path)

camera_in_url = f'http://{esp32_cam_in_ip}:81/stream'
camera_out_url = f'http://{esp32_cam_out_ip}:81/stream'
capture_photo_url_in = f'http://{esp32_cam_in_ip}/capture'
capture_photo_url_out = f'http://{esp32_cam_out_ip}/capture'

def initialize_camera():
    global camera_in
    global camera_out

    if camera_in is None:
        try:
            camera_in = cv2.VideoCapture(camera_in_url)
            # camera_in = cv2.VideoCapture(0)
        except cv2.error as e:
            print(f"Lỗi khi khởi tạo camera_in: {str(e)}")

    if camera_out is None:
        try:
            camera_out = cv2.VideoCapture(camera_out_url)
            # camera_out = cv2.VideoCapture(0)
        except cv2.error as e:
            print(f"Lỗi khi khởi tạo camera_in: {str(e)}")


# def video_feed_in(request):
#     # initialize_camera()
#     try:
#         response = StreamingHttpResponse(get_frame_in(camera_in), content_type="multipart/x-mixed-replace;boundary=frame")
#         return response
#     except Exception as e:
#         print(f"Error in 'video_feed_in': {e}")
#         return HttpResponseServerError("Internal Server Error")

# def video_feed_out(request):
#     # initialize_camera()
#     try:
#         response = StreamingHttpResponse(get_frame_out(camera_out), content_type="multipart/x-mixed-replace;boundary=frame")
#         return response
#     except Exception as e:
#         print(f"Error in 'video_feed_in': {e}")
#         return HttpResponseServerError("Internal Server Error")

def video_feed_in(request):
    try:
        response = StreamingHttpResponse(get_frame_in(camera_in), content_type="multipart/x-mixed-replace;boundary=frame")
        return response
    except cv2.error as e:
        # Không thể khởi tạo hoặc load lại camera
        print(f"Lỗi khi load camera: {str(e)}")
        # Thử khởi tạo lại camera
        try:
            initialize_camera()
            response = StreamingHttpResponse(get_frame_in(camera_in), content_type="multipart/x-mixed-replace;boundary=frame")
            return response
        except cv2.error as e:
            print(f"Lỗi khi load lại camera: {str(e)}")
        return HttpResponseServerError("Internal Server Error")
    except Exception as e:
        print(f"Lỗi trong 'video_feed_in': {e}")
        return HttpResponseServerError("Internal Server Error")
    
def video_feed_out(request):
    try:
        response = StreamingHttpResponse(get_frame_out(camera_out), content_type="multipart/x-mixed-replace;boundary=frame")
        return response
    except cv2.error as e:
        # Không thể khởi tạo hoặc load lại camera
        print(f"Lỗi khi load camera: {str(e)}")
        # Thử khởi tạo lại camera
        try:
            initialize_camera()
            response = StreamingHttpResponse(get_frame_out(camera_out), content_type="multipart/x-mixed-replace;boundary=frame")
            return response
        except cv2.error as e:
            print(f"Lỗi khi load lại camera: {str(e)}")
        return HttpResponseServerError("Internal Server Error")
    except Exception as e:
        print(f"Lỗi trong 'video_feed_in': {e}")
        return HttpResponseServerError("Internal Server Error")

def release_camera():
    global camera_in
    global camera_out
    if camera_in is not None:
        camera_in.release()
        camera_in = None
    if camera_out is not None:
        camera_out.release()
        camera_out = None

# def get_frame_in(camera):
#     while True:
#         success, frame = camera.read()
#         if not success:
#             time.sleep(1)
#             continue  # Bỏ qua frame nếu không thành công trong việc đọc
#         # Chuyển đổi frame thành định dạng JPEG
#         is_success, buffer = cv2.imencode('.jpg', frame)
#         if is_success:
#             frame_bytes = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

# def get_frame_out(camera):
#     while True:
#         success, frame = camera.read()
#         if not success:
#             time.sleep(1)
#             continue  # Bỏ qua frame nếu không thành công trong việc đọc
#         # Chuyển đổi frame thành định dạng JPEG
#         is_success, buffer = cv2.imencode('.jpg', frame)
#         if is_success:
#             frame_bytes = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

def get_frame_in(camera):
    while True:
        success, frame = camera.read()
        if not success:
            time.sleep(1)
            # Load lại camera nếu không thành công trong việc đọc
            try:
                camera = cv2.VideoCapture(camera_in_url)
                continue
            except cv2.error as e:
                print(f"Lỗi khi khởi tạo camera_in: {str(e)}")
                break  # Thoát khỏi vòng lặp nếu không thể khởi tạo lại camera
        is_success, buffer = cv2.imencode('.jpg', frame)
        if is_success:
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

def get_frame_out(camera):
    while True:
        success, frame = camera.read()
        if not success:
            time.sleep(1)
            # Load lại camera nếu không thành công trong việc đọc
            try:
                camera = cv2.VideoCapture(camera_out_url)
                continue
            except cv2.error as e:
                print(f"Lỗi khi khởi tạo camera_in: {str(e)}")
                break  # Thoát khỏi vòng lặp nếu không thể khởi tạo lại camera
        is_success, buffer = cv2.imencode('.jpg', frame)
        if is_success:
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')


# Hàm để chuyển đổi dữ liệu MJPEG thành ảnh OpenCV
def convert_mjpeg_to_image(mjpeg_data):
    try:
        image_data = b''
        for chunk in mjpeg_data.iter_content(chunk_size=1024):
            if chunk:
                image_data += chunk
                a = image_data.find(b'\xff\xd8')
                b = image_data.find(b'\xff\xd9')
                if a != -1 and b != -1:
                    jpg = image_data[a:b + 2]
                    image_data = image_data[b + 2:]
                    return cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
    except Exception as e:
        print(f"Error in 'convert_mjpeg_to_image': {e}")
    # success, image = camera_in.read()
    # if not success:
    #     return HttpResponse("Cannot capture image from camera.")

def capture_image_in(request):
    global camera_in
    try:
        if camera_in is None:
            return HttpResponse("Camera is not initialized.")
        
        # Thực hiện yêu cầu để lấy frame từ luồng video MJPEG
        response = requests.get(capture_photo_url_in, stream=True)

        # Kiểm tra trạng thái kết quả của yêu cầu MJPEG
        if response.status_code != 200:
            print(f"Error retrieving MJPEG frame. Status code: {response.status_code}")
            raise Exception("Error retrieving MJPEG frame.")

        # Chuyển đổi frame từ dữ liệu MJPEG
        frame = convert_mjpeg_to_image(response)

        # Kiểm tra xem frame có hợp lệ hay không
        if frame is None:
            print("Error converting MJPEG to image.")
            raise Exception("Error converting MJPEG to image.")

        # ret, frame = camera_in.read()

        # Xử lý frame
        frame_out, new_img, kitu = detect_dropplate.get_Frame(True, frame, model_plates, model_charaters)

        # Kiểm tra xem kết quả xử lý frame có hợp lệ hay không
        if frame_out is None or new_img is None or kitu is None:
            return HttpResponse("Error character")


        # Chuyển đổi frame kết quả thành dạng base64 để trả về
        ret, frame_out = cv2.imencode('.jpg', frame_out)
        ret, new_img = cv2.imencode('.jpg', new_img)
        frame_out_base64_data = base64.b64encode(frame_out).decode('utf-8')
        new_img_base64_data = base64.b64encode(new_img).decode('utf-8')

        # Trả về dữ liệu như là một chuỗi văn bản
        try:
            lp_in = LicensePlates.objects.get(license_plates=kitu)
            user_in_id = LicensePlatesUser.objects.get(license_plates=lp_in.license_platesID)
            user_in = User.objects.get(id=user_in_id.userID)
            response_data = f"{frame_out_base64_data}|{new_img_base64_data}|{kitu}|{user_in.id}|{user_in.fullname}|{lp_in.license_plates}"
        except LicensePlates.DoesNotExist:
            # Xử lý khi LicensePlates không tồn tại
            response_data = f"{frame_out_base64_data}|{new_img_base64_data}|{kitu}|{'none'}|{'Chưa đăng ký'}|{kitu}"
        except LicensePlatesUser.DoesNotExist:
            # Xử lý khi LicensePlatesUser không tồn tại
            response_data = f"{frame_out_base64_data}|{new_img_base64_data}|{kitu}|{'none'}|{'Chưa đăng ký'}|{kitu}"
        except User.DoesNotExist:
            # Xử lý khi User không tồn tại
            response_data = f"{frame_out_base64_data}|{new_img_base64_data}|{kitu}|{'none'}|{'Chưa đăng ký'}|{kitu}"

        # Trả về dữ liệu như là một chuỗi văn bản
        return HttpResponse(response_data)
    except Exception as e:
        print(f"Error in 'capture_image_in': {e}")
        return HttpResponseServerError("Internal Server Error")

@csrf_exempt
def capture_image_data(request):
    if request.method == 'POST':
        response_data = request.POST.get('capturedData', '')  
        # Xử lý dữ liệu nếu cần

        # Chuyển hướng đến trang index.html với dữ liệu truyền qua query parameter
        return HttpResponseRedirect(f'/indexStaff/?data={response_data}')

    return HttpResponse('Invalid method', status=400)


def capture_image_out(request):
    global camera_out
    try:
        if camera_out is None:
            return HttpResponse("Camera is not initialized.")

        # Thực hiện yêu cầu để lấy frame từ luồng video MJPEG
        response = requests.get(capture_photo_url_out, stream=True)

        # Kiểm tra trạng thái kết quả của yêu cầu MJPEG
        if response.status_code != 200:
            print(f"Error retrieving MJPEG frame. Status code: {response.status_code}")
            raise Exception("Error retrieving MJPEG frame.")

        # Chuyển đổi frame từ dữ liệu MJPEG
        frame = convert_mjpeg_to_image(response)

        # Kiểm tra xem frame có hợp lệ hay không
        if frame is None:
            print("Error converting MJPEG to image.")
            raise Exception("Error converting MJPEG to image.")

        # ret, frame = camera_out.read()

        frame_out, new_img, kitu = detect_dropplate.get_Frame(True, frame, model_plates, model_charaters)

        # Kiểm tra xem kết quả xử lý frame có hợp lệ hay không
        if frame_out is None or new_img is None or kitu is None:
            return HttpResponse("Error character")
        
        ret, frame_out = cv2.imencode('.jpg', frame_out)
        ret, new_img = cv2.imencode('.jpg', new_img)
        # frame = jpeg.tobytes()
        frame_out_base64_data = base64.b64encode(frame_out).decode('utf-8')
        new_img_base64_data = base64.b64encode(new_img).decode('utf-8')

        try:
            lp_in = LicensePlates.objects.get(license_plates = kitu)
            user_in_id = LicensePlatesUser.objects.get(license_plates = lp_in.license_platesID)
            user_in = User.objects.get(id = user_in_id.userID)

            history = ParkingHistory.objects.get(license_plates=lp_in, state='0')
            
            # Trong hàm capture_image_in của bạn
            response_data = f"{frame_out_base64_data}|{new_img_base64_data}|{kitu}|{user_in.id}|{user_in.fullname}|{lp_in.license_plates}|{'In'}"
        except LicensePlates.DoesNotExist:
            # Xử lý khi LicensePlates không tồn tại
            response_data = f"{frame_out_base64_data}|{new_img_base64_data}|{kitu}|{'none'}|{'Chưa đăng ký'}|{kitu}|{'Out'}"
        except LicensePlatesUser.DoesNotExist:
            try:
                history = ParkingHistory.objects.get(license_plates=lp_in, state='0')
                if history:
                    # Xử lý khi LicensePlatesUser không tồn tại
                    response_data = f"  {frame_out_base64_data}|{new_img_base64_data}|{kitu}|{'none'}|{'Chưa đăng ký'}|{kitu}|{'In'}"
            except ParkingHistory.DoesNotExist:
                response_data = f"{frame_out_base64_data}|{new_img_base64_data}|{kitu}|{'none'}|{'Chưa đăng ký'}|{kitu}|{'Out'}"

        except User.DoesNotExist:
            # Xử lý khi User không tồn tại
            response_data = f"{frame_out_base64_data}|{new_img_base64_data}|{kitu}|{'none'}|{'Chưa đăng ký'}|{kitu}|{'Out'}"

        # Trả về dữ liệu như là một chuỗi văn bản
        return HttpResponse(response_data)
    except Exception as e:
        print(f"Error in 'capture_image_out': {e}")
        return HttpResponseServerError("Internal Server Error")

def crop_image(image, x, y, width, height):
    cropped_image = image[y:y+height, x:x+width]
    return cropped_image


@csrf_exempt
def module1_api(request):
    if request.method == 'GET' or request.method == 'POST':
        try:
            if request.method == 'POST':
                # Trích xuất giá trị của tham số "module1" từ yêu cầu POST
                module_value = request.POST.get("module1")
            elif request.method == 'GET':
                # Trích xuất giá trị của tham số "module1" từ yêu cầu GET
                module_value = request.GET.get("module1")

            # Kiểm tra xem giá trị "module1" có phải là "1" hay không
            if module_value == "1":
                # Trả về thành công
                return HttpResponse("success")
            else:
                # Trả về thông báo lỗi
                return HttpResponse("error: Giá trị module1 không hợp lệ")
        except Exception as e:
            # Trả về thông báo lỗi
            return HttpResponse(f"error: {str(e)}")
    else:
        # Trả về thông báo lỗi nếu không phải là yêu cầu GET hoặc POST
        return HttpResponse("error: Chỉ có yêu cầu GET và POST được phép")
