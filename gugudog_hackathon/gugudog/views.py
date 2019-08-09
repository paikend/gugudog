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

    sorted_gudog = sorted(GuDogService.objects.filter(user=request.user), key=lambda a: a.remained_date)

    context = {
        'total_price': total_price,
        'gudog':sorted_gudog
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
    # gudog_users 내림차순으로 services를 정렬하는 코드
    services = Service.objects.order_by('-gudog_users')

    context = {
        'services': services,
    }
    return render(request, 'hot.html', context)

def tag(request):
    my_interest = InterestService.objects.filter(user=request.user).values()
    tags = Category.objects.all()

    context = {
        'tags':tags,
        'services':''
    }

    if request.method == 'POST':
        tag_checked = request.POST.get('tag_checked')
        services = Service.objects.filter(category__name=tag_checked)
        context['services'] = services
        return render(request, 'tag.html', context)
    else:
        services = Service.objects.all()
        context['services'] = services
        return render(request, 'tag.html', context)

@login_required(login_url='signup')
def recommendation(request):
    my_interest = InterestService.objects.filter(user=request.user)
    my_inter_list = []
    for i in my_interest:
        my_inter_list.append(i.interest_cate.name)

    my_reco = []
    for i in my_inter_list:
        sorted_data = sorted(Service.objects.filter(category__name=i), key=lambda k: k.count_gudog_users)
        for element in sorted_data:
            my_reco.append(element)
    sorted_my_reco = sorted(my_reco, reverse=True, key=lambda k: k.count_gudog_users)

    context = {
        'my_reco':sorted_my_reco
    }
    return render(request, 'recommendation.html', context)

def signup(request):
    return render(request, 'registration/signup.html')

@login_required(login_url='signup')
def mypage(request):
    interest_pk = request.POST.getlist('cate_checked')
    zzim = ZzimService.objects.filter(user=request.user)

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
        return redirect('mypage')

    else:
        interests = InterestService.objects.filter(user=request.user)
        context = {
            'interests':interests,
            'zzim': zzim
        }
        return render(request, 'mypage.html', context)


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
            return HttpResponse(json.dumps(service.price))

        except:

            # 구독한 날짜를 기입하지 않았을 경우 error를 띄운다.
            if request.POST['register_date'] == "":
                context['error_date'] = "구독한 날짜를 입력해주세요"
                return render(request, 'add.html', context)

            gudog_added, created = GuDogService.objects.get_or_create(
                user=request.user,
                service=Service.objects.get(pk=request.POST['service']),
                register_date=request.POST['register_date']
            )
  
            gudog_qs = GuDog.objects.filter(user=request.user)
            if gudog_qs.exists():
                gudog = gudog_qs[0]
  
                # 이미 해당 서비스를 구독했으면
                if gudog.services.filter(service__pk=gudog_added.service.pk).exists():
                    if created:
                        gudog_added.delete()
                
                    return render(request, 'add.html', context)
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

        context['yes'] = True
        context['isGuDoged'] = "구독하고 있는 서비스에요!"
        context['myDelete'] = "삭제하기"

    elif request.user in service.zzim_users.all():
        context['isZzimed'] = "찜한 구독 서비스에요!"
        context['yes'] = False
    
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
            print(zzim_service)
            zzim_service.delete()
            service.zzim_users.remove(request.user)
            # print(service.get_zzim_users)
            context['get_zzim_users'] = service.count_zzim_users
            context['zzim']="찜 취소"
            print('취소됐어요')
            print(context)
            return HttpResponse(json.dumps(context))
    
        zzim_qs = Zzim.objects.filter(user=request.user)
        if zzim_qs.exists():
            zzim = zzim_qs[0]
            if zzim.services.filter(service__pk=zzim_service.service.pk):
                zzim_service.delete()
                print('hello')
                context['zzim']="찜 취소"
                # context['get_zzim_users']
                return HttpResponse(json.dumps(context))
            else:
                zzim_service.save()
                zzim.services.add(zzim_service)
                service = Service.objects.get(pk=zzim_service.service.pk)
                service.zzim_users.add(request.user)
                context['get_zzim_users'] = service.count_zzim_users
                return HttpResponse(json.dumps(context))
        else:
            zzim_service.save()
            zzim = Zzim.objects.create(user=request.user)
            zzim.services.add(zzim_service)
            service = Service.objects.get(pk=zzim_service.service.pk)
            service.zzim_users.add(request.user)
            context['get_zzim_users'] = service.count_zzim_users
    
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
    print(my_inter_list)

    my_reco = []
    for i in my_inter_list:
        # a = Service.objects.filter(category__name=i).values()
        sorted_data = sorted(Service.objects.filter(category__name=i), key=lambda k: k.count_gudog_users)
        for element in sorted_data:
            my_reco.append(element)
    sorted_my_reco = sorted(my_reco, reverse=True, key=lambda k: k.count_gudog_users)
    print(sorted_my_reco)

    context = {
        'my_reco':sorted_my_reco
    }
    return render(request, 'test3.html', context)

@login_required(login_url='signup/')
def service_new(request):
    return render(request, 'service_new.html')
