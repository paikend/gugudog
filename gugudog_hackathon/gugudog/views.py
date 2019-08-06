from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from .forms import AddForm
from .models import *
from django.contrib.auth.decorators import login_required
from dal import autocomplete
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
import json

# Create your views here.
@login_required(login_url='signup')
def home(request):

    gudog = GuDogService.objects.filter(user=request.user)

    total_price = 0
    
    for service in gudog.values():
        gudogService = Service.objects.get(pk=service['service_id'])
        total_price += gudogService.price

    context = {
        'gudog': gudog,
        'total_price': total_price,
    }
    return render(request, 'home.html', context)

@login_required(login_url='signup')
def service_all(request):
    services = Service.objects.all()

    context = {
        'services': services,
    }
    return render(request, 'service_all.html', context)

def hot(request):
    services = Service.objects.all()

    context = {
        'services': services,
    }
    return render(request, 'hot.html', context)

def tag(request):
    services = Service.objects.all()

    context = {
        'services': services,
    }
    return render(request, 'tag.html', context)

@login_required(login_url='signup')
def recommendation(request):
    return render(request, 'recommendation.html')


def signup(request):
    return render(request, 'registration/signup.html')

@login_required(login_url='signup')
def mypage(request):
    return render(request, 'mypage.html')

def logout(request):
    auth.logout(request)
    return redirect('signup')

@login_required(login_url='signup')
def add(request):
    model = GuDogService.objects.all()
    form = AddForm()
    context = {
        'form': form,
        'models': model,
    }

    if request.method == "POST": 
        try:
            service_pk = request.POST.get('pk', False)
            service = get_object_or_404(Service, pk=service_pk)
            print(service)
            print(service.price)
            return HttpResponse(json.dumps(service.price))
        except:  
            gudog_added, created = GuDogService.objects.get_or_create(
                user=request.user,
                service=Service.objects.get(pk=request.POST['service']),
                register_date=request.POST['register_date']
            )
            
            print(gudog_added)
            gudog_qs = GuDog.objects.filter(user=request.user)
            if gudog_qs.exists():
                gudog = gudog_qs[0]
                # 이미 해당 서비스를 구독했으면
                if gudog.services.filter(service__pk=gudog_added.service.pk).exists():
                    gudog_added.delete()
                    return redirect('add')
                else:
                    gudog.services.add(gudog_added)
                    service = Service.objects.get(pk=gudog_added.service.pk)
                    service.gudog_users.add(request.user)
                    return redirect('home')
            else:
                gudog_added.save()
                gudog = GuDog.objects.create(user=request.user)
                gudog.services.add(gudog_added)
                service = Service.objects.get(pk=gudog_added.service.pk)
                service.gudog_users.add(request.user)
                return redirect('home')
    else:
        # GET 방식으로 요청이 들어오면
        # ajax 요청이면 try 실행
        # try:
        #     pk = request.GET.get('pk')
        #     service = get_object_or_404(Service, pk=pk)
        #     print(service)
        #     context['service']=service
        #     print(context.service.price)
        #     return JsonResponse(context['service'])
        # # ajax 요청이 아니면 그냥 add 페이지 render
        # except:
        return render(request, 'add.html', context)

@login_required(login_url='signup')
def delete_service(request, gudog_service_pk, model_service_pk):
    deletingService = GuDogService.objects.get(pk=gudog_service_pk)

    service = Service.objects.get(pk=model_service_pk)

    service.gudog_users.remove(request.user)
    service.zzim_users.remove(request.user)

    deletingService.delete()
    return redirect('home')

@login_required(login_url='signup')
def service_detail(request, service_pk):
    service = Service.objects.get(pk=service_pk)
    context = {
        'service': service,
    }
    if request.user in service.gudog_users.all():
        context['isGuDoged'] = "구독하고 있는 서비스에요!"
    elif request.user in service.zzim_users.all():
        context['isZzimed'] = "찜한 구독 서비스에요!"
    
    return render(request, 'service_detail.html', context)


@login_required(login_url='signup')
def zzim(request):
    context = {
        'zzim':"찜했어용",
    }
    if request.method == "POST":
        pk = request.POST.get('pk', None)
        service = get_object_or_404(Service, pk=pk)
        zzim_service, created = ZzimService.objects.get_or_create(
            user=request.user,
            service = Service.objects.get(pk=request.POST.get('pk')),
        )

        if not created:
            zzim_service.delete()
            context['zzim']="찜"
            return HttpResponse(json.dumps(context))
    
        zzim_qs = Zzim.objects.filter(user=request.user)
        if zzim_qs.exists():
            zzim = zzim_qs[0]
            if zzim.services.filter(service__pk=zzim_service.service.pk):
                zzim_service.delete()
                context['zzim']="찜"
                return HttpResponse(json.dumps(context))
            else:
                zzim_service.save()
                zzim.services.add(zzim_service)
                service = Service.objects.get(pk=zzim_service.service.pk)
                service.zzim_users.add(request.user)
                return HttpResponse(json.dumps(context))
        else:
            zzim_service.save()
            zzim = Zzim.objects.create(user=request.user)
            zzim.services.add(zzim_service)
            service = Service.objects.get(pk=zzim_service.service.pk)
            service.zzim_users.add(request.user)
    
    return HttpResponse(json.dumps(context))

@login_required(login_url='signup')
def mp(request):
    zzim = ZzimService.objects.filter(user=request.user)
    context = {
        'zzim': zzim,
    }
    return render(request, "mp.html", context)

@login_required(login_url='signup')
def delete_zzim(request, zzim_service_pk, model_service_pk):
    deletingService = ZzimService.objects.get(pk=zzim_service_pk)
    deletingService.delete()

    service = Service.objects.get(pk=model_service_pk)
    service.zzim_users.remove(request.user)

    return redirect('home')

@login_required(login_url='signup')
def test(request):
    categories = Category.objects.all()
    my_interests = InterestService.objects.filter(user=request.user)
    my_inter_list = []
    for i in my_interests:
        my_inter_list.append(i.interest_cate.name)

    context = {
        'categories':categories,
        'my_inter_list':my_inter_list
    }
    return render(request, 'test.html', context)

@login_required(login_url='signup')
def test2(request):
    interest_pk = request.POST.getlist('cate_checked')

    if request.method == 'POST':
        deleting = InterestService.objects.filter(user=request.user)
        deleting.delete()

        for pks in interest_pk:
            interest_add, created = InterestService.objects.get_or_create(
                user = request.user,
                interest_cate = Category.objects.get(pk=pks)
            )
            inter_qs = Interest.objects.filter(
                user = request.user
            )
            if inter_qs.exists():
                inter_cate = inter_qs[0]
                if inter_cate.interests.filter(interest_cate__pk=interest_add.interest_cate.pk).exists():
                    interest_add.save()
                else:
                    inter_cate.interests.add(interest_add)
            else:
                inter_cate = Interest.objects.create(user=request.user)
                inter_cate.interests.add(interest_add)

        interests = InterestService.objects.filter(user=request.user)
        return redirect('test2')

    else:
        interests = InterestService.objects.filter(user=request.user)
        context = {
            'interests':interests
        }
        return render(request, 'test2.html', context)

@login_required(login_url='signup')
def test3(request):
    my_interest = InterestService.objects.filter(user=request.user)
    my_inter_list = []
    for i in my_interest:
        my_inter_list.append(i.interest_cate.name)
    # print(my_inter_list)

    my_reco = []
    for i in my_inter_list:
        a = Service.objects.filter(category__name=i).values()
        for element in a :
            my_reco.append(element)

    context = {
        'my_reco':my_reco
    }
    return render(request, 'test3.html', context)