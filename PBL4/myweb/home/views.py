from django.shortcuts import render
from django.http import HttpResponse
from .forms import LicensePlates_Form, LicensePlatesUser_Form, LicensePlatesParking_Form, ParkingHistory_Form, StaffParking_Form, Staff_Form, User_Form
from .models import LicensePlates, LicensePlatesUser, LicensePlatesParking, ParkingHistory, StaffParking, Staff, User
from django.views import View
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import random, string

# from employee.forms import loginForm
# from employee.models import Login
# Create your views here.

def generate_random_user_id():
    random_number = random.randint(0, 999999)
    return f"user{random_number:08d}"  # Định dạng thành số có 4 chữ số


def generate_random_staff_id():
    random_number = random.randint(0, 999999)
    return f"user{random_number:08d}"  # Định dạng thành số có 4 chữ số

def generate_random_parking_history_id():
    random_number = random.randint(0, 999999)
    return f"park{random_number:08d}"  # Định dạng thành số có 4 chữ số

def index(request):
    context = {}
    return render(request, 'app/index.html', context)

def managerStaff1(request):
    if request.method == 'POST':
        try:

            user_id = request.POST.get('user_id_manage')
            user = User.objects.get(id=user_id)
            
            all_users = User.objects.filter(role='user')

            context = {
                'User': user,
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
    context = {'all_users': all_users}
    return render(request, 'app/manager_staff.html', context)

def managerStaff_delete(request):
    if request.method == 'POST':
        try:
            user_id = request.POST.get('user_id_delete')
            user_to_delete = User.objects.get(id=user_id)
            user_to_delete.delete()
            messages.success(request, 'Xóa thành công')
            return redirect('managerStaff')  # Chuyển hướng đến trang chính sau khi xóa thành công

        except User.DoesNotExist:
            messages.error(request, 'Không tìm thấy người dùng cần xóa')
            return redirect('managerStaff')  # Chuyển hướng trở lại trang chính nếu không tìm thấy người dùng cần xóa

    return render(request, 'manager_staff_delete.html')

def historyStaff_delete(request):
    if request.method == 'POST':
        try:
            history_id = request.POST.get('history_id_delete')
            history_to_delete = ParkingHistory.objects.get(parking_historyID=history_id)
            history_to_delete.delete()
            messages.success(request, 'Xóa thành công')
            return redirect('historyStaff')  # Chuyển hướng đến trang chính sau khi xóa thành công

        except User.DoesNotExist:
            messages.error(request, 'Không tìm thấy người dùng cần xóa')
            return redirect('historyStaff')  # Chuyển hướng trở lại trang chính nếu không tìm thấy người dùng cần xóa

    return render(request, 'manager_staff_delete.html')

def managerStaff_register(request):
    if request.method == 'POST':
        id = generate_random_user_id()
        fullname = request.POST['fullname']
        email = request.POST['email']
        date_of_birth = request.POST['date_of_birth']
        position = request.POST['position']
        phone = request.POST['phone']
        account_balance = request.POST['account_balance']
        plate_number = request.POST['plate_number']

        try :
            new_user = User(id=id, fullname=fullname, email=email, date_of_birth=date_of_birth, position=position, phone=phone, account_balance=account_balance, role='user')
            new_user.save()
            messages.success(request, 'Đăng ký thành công')
            return redirect('managerStaff')  # Chuyển hướng đến trang chính sau khi đăng ký

        except ObjectDoesNotExist:
            messages.error(request, 'Mật khẩu không khớp')
            return redirect('register')  # Chuyển hướng trở lại trang đăng ký nếu mật khẩu không khớp

    return render(request, 'register.html')

def update_staff(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        try:
            user = User.objects.get(id=user_id)
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


def historyStaff1(request):
    if request.method == 'POST':
        try:
            users = User.objects.all()  # Lấy tất cả người dùng
            parking_history = ParkingHistory.objects.filter(license_plates__licenseplatesuser__userID__in=[user.id for user in users])

            history_id = request.POST.get('history_id')
            history = ParkingHistory.objects.get(parking_historyID=history_id)
            time_in = history.time_in
            time_out = history.time_out
            total_price = history.total
            user = User.objects.get(id=history.license_plates.licenseplatesuser_set.first().userID)
            full_name = user.fullname
            license_plate_number = history.license_plates.license_plates
            phone_number = user.phone
            address = user.position

            context = {
                'full_name': full_name,
                'license_plate_number': license_plate_number,
                'phone_number': phone_number,
                'address': address,
                'time_in': time_in,
                'time_out': time_out,
                'total_price': total_price,
                'parking_history': parking_history
            }
            return render(request, 'app/history_staff_full.html', context)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Parking history with the given ID does not exist'})
    return JsonResponse({'error': 'Invalid request'})

def history_staff(request):
    users = User.objects.all()  # Lấy tất cả người dùng
    parking_history = ParkingHistory.objects.filter(license_plates__licenseplatesuser__userID__in=[user.id for user in users])

    context = {'parking_history': parking_history}
    return render(request, 'app/history_staff.html', context)

def index_staff(request): 
    context = {}
    return render(request, 'app/index_staff.html', context)

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
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            new_user = User(id=id, username=username, password=password, role='user')
            new_user.save()
            messages.success(request, 'Đăng ký thành công')
            return redirect('index')  # Chuyển hướng đến trang chính sau khi đăng ký

        else:
            messages.error(request, 'Mật khẩu không khớp')
            return redirect('register')  # Chuyển hướng trở lại trang đăng ký nếu mật khẩu không khớp

    return render(request, 'register.html')


# def emp(request):
#     if request.method == "POST":
#         form = loginForm(request.POST)
#         if form.is_valid():
#             try:
#                 form.save()
#                 return redirect('/view')
#             except:
#                 pass
#         else:
#             form = loginForm()
#         return render(request, 'index.html', {'form':form})