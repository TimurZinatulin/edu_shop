# complete
from django.shortcuts import render
from .models import *
from django.urls import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.paginator import Paginator


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])    
            # Save the User object
            new_user.save()
            Cart.objects.create(owner=new_user)
            Balance.objects.create(profile=new_user, amount=7000)
            BoughtedCourse.objects.create(profile=new_user)
            return render(request, 'dadova/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'dadova/register.html', {'user_form': user_form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'dadova/login_done.html', {'user': user})
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'dadova/login.html', {'form': form})


def home(request):

	c = Course.objects.order_by('-id')[:6]

	return render(request, 'dadova/home.html', {'courses': c})


def features(request):

	c = Course.objects.filter(is_featured=True)

	paginator = Paginator(c, 3)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	return render(request, 'dadova/features.html', {'courses': c, 'page_obj': page_obj})


def categories(request):

	try:
		c = Category.objects.all()
	except:
		raise Http404()

	return render(request, 'dadova/categories.html', {'categories': c})


def events(request):

	e = Event.objects.order_by('-id')[:5]

	return render(request, 'dadova/events.html', {'events': e})


def courses(request, cat_id):

	try:
		c = Category.objects.get(id=cat_id)
	except:
		raise Http404()

	courses = c.course_set.all()

	paginator = Paginator(courses, 3)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	return render(request, 'dadova/courses.html', {'category': c, 'courses': courses, 'page_obj': page_obj})


def detail(request, cour_id):

	try:
		c = Course.objects.get(id=cour_id)
	except:
		raise Http404()

	categories = Category.objects.all()
	reviews = c.review_set.order_by('-id')[:10]

	return render(request, 'dadova/detail.html', {'course': c, 'categories': categories, 'reviews': reviews})


def leave_review(request, cour_id, user_id):

	try:
		c = Course.objects.get(id=cour_id)
	except:
		raise Http404()

	c.review_set.create(author=User.objects.get(id=user_id) , text=request.POST['text'])
	return HttpResponseRedirect(reverse('dadova:detail', args=(c.id, )))


def cart(request, user_id):

	courses = Cart.objects.get(owner=User.objects.get(id=user_id)).courses.all()

	paginator = Paginator(courses, 3)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	return render(request, 'dadova/cart.html', {'page_obj': page_obj})


def add_to_cart(request, cour_id, user_id):

	try:
		cart = Cart.objects.get(owner=User.objects.get(id=user_id))
		course = Course.objects.get(id=cour_id)
	except:
		raise Http404()

	cart.courses.add(course)
	return HttpResponseRedirect(reverse('dadova:detail', args=(course.id, )))


def profile(request, user_id):

	balance = Balance.objects.get(profile=User.objects.get(id=user_id))

	courses = BoughtedCourse.objects.get(profile=User.objects.get(id=user_id)).courses.all()

	paginator = Paginator(courses, 3)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	return render(request, 'dadova/profile.html', {'courses': courses, 'balance': balance, 'page_obj': page_obj})


def buy(request, cour_id, user_id):

	try:
		bougthed_course = BoughtedCourse.objects.get(profile=User.objects.get(id=user_id))
		balance = Balance.objects.get(profile=User.objects.get(id=user_id))
		course = Course.objects.get(id=cour_id)
	except:
		raise Http404()

	if balance.amount < course.price:
		return HttpResponseRedirect(reverse('dadova:detail', args=(course.id, )))
	balance.amount -= course.price
	balance.save()
	bougthed_course.courses.add(course)
	return HttpResponseRedirect(reverse('dadova:detail', args=(course.id, )))