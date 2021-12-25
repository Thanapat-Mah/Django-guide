# Initialize Virtual Environment
### create virtual environment in folder named `venv`
```commandline
virtualenv -p python3 venv
```

### activate virtual environment
```commandline
Set-ExecutionPolicy Unrestricted -Scope Process
.\venv\Scripts\activate
Set-ExecutionPolicy Default -Scope Process
```
`Set-ExecutionPolicy` is used in case if you can't run `Scripts\activate`  
Note: **Always** activate the virtual environment before development.

### select interpreter of virtual environment
in pycharm > setting > (this project) > project interpreter > select virtual env path  

### install django in virtual env
```commandline
pip install django
```

# Set Up Django Project
### create django project
```commandline
django-admin startproject project_name
```

### create django app
```commandline
cd project_name
python manage.py startapp app_name
```
Then, modify the app!

#### example
Add the following code to `models.py` in app folder.
```python
class Question(models.Model):
    question_text = models.CharField(max_length=100)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # foreign key to Question

    def __str__(self):
        return self.choice_text
```

### run server
```commandline
python manage.py runserver port_number
```
`port_number` is optional, default is 8000  
Terminate the server anytime by pressing ***ctrl + c***

### add apps to django project
in `project_name` folder > `settings.py` > add `'app_name'` to `INSTALLED_APPS`

### migrate app
 Terminate the server, then migrate the app.
```commandline
python manage.py makemigrations app_name
python manage.py migrate
```
The `db.sqlite3` file will be updated.  

# Populate Database
## Way 1: Using Django Shell
### open shell
```commandline
python manage.py shell
```

### set up django
```python
import django
django.setup()
from app_name.models import model_name
```

### fill the data
Check if data in `model_name` is empty or not.
```python
model_name.objects.all()
```
Then, just fill the data in.
####example
* add question
```python
from django.utils import timezone
q = Question(question_text="what's your name", pub_date=timezone.now())
q.save()
```
* add choice
```python
q = Question.objects.get(pk=1)
q.choice_set.create(choice_text="ca", votes=0)
q.choice_set.create(choice_text="py", votes=0)
q.choice_set.create(choice_text="bara", votes=0)
q.save()
```
`pk` is a primary key (id).

###exit shell
```python
exit()
```

## Way 2: Using Admin Tools
### create superuser
```commandline
python manage.py createsuperuser
```
Then, fill whatever it asks for.

### enter the admin page
```commandline
python manage.py runserver
```
It should return url like `http://127.0.0.1:8000/`  
Then, enter the admin page using url like `http://127.0.0.1:8000/admin` and log in as a superuser.

### regist the app
Go to `admin.py` inside the app folder and add following code.
```python
from .models import Question, Choice

admin.site.register(Question)
admin.site.register(Choice)
```
Then, refresh the admin page and the app will be appeared.  
Finally, manage the database with the power of **superuser**!

# Route the URLs
### add URLs router of the app to the project
Go to `urls.py` in project folder and modify code using `include` as following.
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
]
```
Any request to `http://127.0.0.1:8000/polls` will be handled by `polls` app using `urls.py`.  
Note: Always add `/` at the end of the path.

### create URLs handler of the app
Create `urls.py` in app folder using following code.
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
]
```
Handle request for `127.0.0.1/polls/` with `index` function in `views.py`.  

### add the views
The views in django is some kind of **request handler**, not actually a **view** as a front-end web page.  
Add the following `index` function to `views.py`.
```python
from django.http import HttpResponse

def index(request):
    return HttpResponse("Awesome job guys! This is the index page, of our polls application")
```
Use the URL `http://127.0.0.1:8000/polls` to preview the result of the web page right away!

### add routes with parameter
Add route with parameter using `<type:parameter_name>` in the `urlpatterns` in `urls.py` of the app.  
Use following code as an example.
```python
path('<int:question_id>/', views.detail, name="detail"),            # 127.0.0.1/polls/1 (last int is question_id)
path('<int:question_id>/results/', views.results, name="results"),  # 127.0.0.1/polls/1/results
path('<int:question_id>/vote/', views.vote, name="vote"),           # 127.0.0.1/polls/1/vote
```

### using regular expression
The regular expression `(?P<name>pattern)` can be use with `re_path`.
```python
from django.urls import path
from . import views

urlpatterns = [
    path('<int:question_id>/vote/', views.vote, name="vote"),
]
```
will be replaced with
```python
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name="vote"),
]
```
Notes (from understanding of myself, maybe incorrect) :
* `r` indicate the string formatting
* `^` indicate the beginning
* `$` indicate the end

### handle parameter
Use following example code in `views.py` of the the app.
```python
def detail(request, question_id):
    return HttpResponse("This is the detail view of the question: %s" % question_id)

def results(request, question_id):
    return HttpResponse("These are the results of the question: %s" % question_id)

def vote(request, question_id):
    return HttpResponse("Vote on question: %s" % question_id)
```

### display data from database
Modify `index` in the same `views.py` file to display information from the database.
```python
def index(request):
    latest_questions = Question.objects.order_by("-pub_date")[:5]
    output = ", ".join(q.question_text for q in latest_questions)
    return HttpResponse(output)
```

# Create Templates
Django template is a html web page rendering for user.
### create html file
For example, create file named `index.html` inside the `app_name` folder as the path `app_name/templates/app_name/index.html`  
The second `app_name` (inner folder) is for **namespacing**, to prevent some error.

### basic Django Template Language (DTL) syntax
Use these DTL syntax to manipulate the Python in HTML file.
#### if statement
```html
{% if latest_questions %}
  do something
{% else %}
  do something else
{% endif %}
```
Note: Using `{%` and `%}` to cover the Python code.
#### for loop
```html
{% for question in latest_questions %}
  <a href="/polls/{{ question.id }}"><b>{{ question.question_text }}</b></a>
{% endfor %}
```
Note: Using `{{` and `}}` to cover the Python variable.
#### example
Add follow code to the `body` of `index.html`
```html
{% if latest_questions %}
  <ul>
    {% for question in latest_questions %}
      <li><a href="/polls/{{ question.id }}"><b>{{ question.question_text }}</b></a><li>
    {% endfor %}
  </ul>
{% else %}
  <p>You don't have any questions. Please add some.</p>
{% endif %}
```
### quick tip
Using url **template tag** `{% url 'some_url_name' variables %}` can simplify the routing.  
The `url` will be mapped to whatever its URL before.
```html
<li><a href="/polls/{{ question.id }}"><b>{{ question.question_text }}</b></a></li>
```  
can be replaced with
```html
<li><a href={% url "detail" question.id %}><b>{{ question.question_text }}</b></a></li>
```

# Render the Templates
Rendering the template via `views.py` in the app folder using following methods.
## Way 1: Using `HttpResponse` with template`.render`
```python
from django.http import HttpResponse
from .models import Question
from django.template import loader

def index(request):
    latest_questions = Question.objects.order_by("-pub_date")[:5]
    template = loader.get_template("polls/index.html")
    context = {"latest_questions": latest_questions}
    return HttpResponse(template.render(context))
```
## Way 2: Using `render` from `django.shortcuts`
```python
from django.shortcuts import render
from .models import Question

def index(request):
    latest_questions = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_questions": latest_questions}
    return render(request, "polls/index.html", context)
```
### example
```python
from django.http import HttpResponse

def detail(request, question_id):
    return HttpResponse("This is the detail view of the question: %s" % question_id)
```
may be modified to
```python
from django.shortcuts import render
from .models import Question

def detail(request, question_id):
    question = Question.objects.get(pk=question_id)
    return render(request, "polls/detail.html", {"question": question})
```
using `get_object_or_404` can return error 404 when there is no object match with the `pk`
```python
from django.shortcuts import render, get_object_or_404
from .models import Question

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})
```

# Reuse the HTML
Notes: There are 3 important tag for reusing the HTML
* block
* include
* extents
### example
in the `footer.html`
```html
<footer>
<p>Footer</p>
</footer>
```
`{% block block_name %}` and `{% include template_name %}` in the `base.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

{% block main_content %}
{% endblock %}
{% include "polls/footer.html" %}

</body>
</html>
```
`{% extends template_name %}` in the extent file
```html
{% extends 'polls/base.html' %}
{% block main_content %}

<h1>{{ question.question_text }}</h1>
<ul>
  {% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }}</li>
  {% endfor %}
</ul>

{% endblock %}
```

# Use namespace
In case if there are many apps with the same views name. It would be better to specify the **namespace**.  
In the `urls.py` of the project
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
]
```
specify the namespace as below
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls', namespace='polls')),
]
```
in the `urls.py` of the app, add variable 
```python
app_name = 'polls'
``` 
in the HTML
```html
<a href={% url "detail" question.id %}> </a>
```
use `polls:detail` instead of `detail` to indicate that this `detail` view name belong to `polls` app.

# Create the Forms
### voting form
Modify the `detail.html` to be like this.
```html
{% extends 'polls/base.html' %}
{% block main_content %}

<h1>{{ question.question_text }}</h1>

{% if error_message %} <p><strong>{{ error_message }}</strong></p> {% endif %}

<form action="{% url 'polls:vote' question.id %}" method="post">
  {% csrf_token %}  <!-- to make sure data is storing(?) or something -->
  {% for choice in question.choice_set.all %}
    <input type="radio" name="choice" id="choice{{forloop.counter}}" value="{{choice.id}}">
    <label for="choice{{forloop.counter}}">{{ choice.choice_text }}</label><br>
  {% endfor %}
  <input type="submit" value="vote">
</form>

{% endblock %}
```
### modify the views
Modify `vote` function in `views.py` to be like this.
```python
from django.urls import reverse
from django.http import HttpResponseRedirect

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except:
        return render(request, "polls/detail.html", {"question": question, "error_message": "Please select a choice"})
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
```
and modify `results` function to be like this.
```python
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})
```
### show result view
Create `results.html` with these code.
```html
{% extends 'polls/base.html' %}
{% block main_content %}

<h1>{{ question.question_text }}</h1>

<ul>
  {% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }} -- {{ choice.votes }} vote{{ choice.votes|pluralize }}</li>
  {% endfor %}
</ul>

<a href="{% url 'polls:detail' question.id %}">Vote Again</a>

{% endblock %}
```

# Add External CSS and Image
In django, CSS and image are considered as a static file. So, they should be contained in the seperate `static` directory.  
### create static directory
1. Create the directory named  `static` inside the app directory.  
2. Then, create directory one step inside with the same name of the app `app_name` (again, it's name spacing)  
3. Finally, create an static file such as CSS file inside this directory.  
<!-- just mark the end of a list -->
The final path to CSS file should be something like `app_name/static/app_name/some_style.css`  
For example `polls/static/polls/style.css` and `polls/static/polls/images/background.png`  
Embeded the image `images/background.png` as a background in `style.css` as the example below.
```css
body {
    background: white url("images/background.png") no-repeat;
}
```

### load and link CSS to HTML
In the top of the HTML file, load static.
```html
{% load static %}
```
In the `head` of the HTML, link the CSS as usual.
```html
<link rel="stylesheet" type="text/css" href="{% static 'polls/style.css' %}">
```
***Finally, just use the Bootstrap or whatever you want on the front-end side!***
