from django.shortcuts import render
from django.http import HttpResponse
# from employee.forms import loginForm
# from employee.models import Login
# Create your views here.

def index(request):
    context = {}
    return render(request, 'app/index.html', context)

def manager(request):
    context = {}
    return render(request, 'app/manager.html', context)

def history_admin(request):
    context = {}
    return render(request, 'app/history.html', context)

def index_staff(request):
    context = {}
    return render(request, 'app/index_staff.html', context)

def indexacc(request):
    context = {}
    return render(request, 'app/indexacc.html', context)

def history_acc(request):
    context = {}
    return render(request, 'app/historyacc.html', context)


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