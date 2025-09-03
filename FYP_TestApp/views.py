import calendar
from datetime import datetime
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.core import serializers
from django.core.mail import EmailMessage
from django.db.models import OuterRef, Exists
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import *
from .tokens import account_activation_token

User = get_user_model()

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        signupForm = SignupForm()  # Reinitialize forms
        loginForm = LoginForm()
        return render(request, 'signUp.html', {'signupForm': signupForm, 'loginForm': loginForm})
    else:
        return HttpResponse('Activation link is invalid!')

    # return redirect('/home')

def activateEmail(request , user, to_email):
    mail_subject = "Activate your UniCompanion Account"
    message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,  # if set up server/port forwarding, change this to server ip
        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()
    # if email.send():
    #     messages.success(request, f'Dear <b>{user}</b>, Please go to your email <b>{to_email}</b>'
    #                             f'inbox and click on received activation link to confirm and'
    #                             f'complete your registration.\n'
    #                             f'<b>Note:</b> Check your spam folder')
    # else:
    #     messages.error(request, f'Dear <b>{user}</b>, There was a problem sending email to {to_email}'
    #                             f'\nPlease check if you types it correctly.')

def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data['stu_email']
        password = data['password']
        user = authenticate(request, stu_email=email, password=password)
        if user is not None:
            if not user.is_active:  # if user acc is not active
                # messages.error(request, "Your account is not enabled.")
                return JsonResponse({'success': "verify-needed"})

            if user.is_banned:
                return JsonResponse({'success': "success", 'redirect_url': '/banned/'})

            login(request, user)
            return JsonResponse({'success': "success", 'redirect_url': '/home/'})
        else:
            return JsonResponse({'success': "failure"})

def check_email_exists(request):
    email = request.GET.get('email', None)
    exists = Users.objects.filter(stu_email=email).exists()
    return JsonResponse({'exists': exists})

def signUp_view(request):
    signupForm = SignupForm()
    loginForm = LoginForm()
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        username = data['username']
        password = data['password']
        email = data['stu_email']
        user = User.objects.create_user(username=username,stu_email=email, password=password)
        activateEmail(request, user, email)
        login(request, user)
        print(f"user {username} created with password {password}")

        return render(request, 'signUp.html', {"signupForm": signupForm, 'loginForm': loginForm})

    print("No post request, sending normal signup.html")
    return render(request, 'signUp.html', {"signupForm": signupForm, 'loginForm': loginForm})

def logout_view(request):
    logout(request)
    return redirect(reverse('signup'))

def banned_view(request):

    return render(request, 'banPage.html')

def addAppeal_view(request):
    if request.method != "POST":
        return HttpResponse(status=400)

    email = request.POST.get('email')
    reason = request.POST.get('reason')

    user = User.objects.filter(stu_email=email)
    if not user or not user[0].is_banned:
        return HttpResponse(status=400)

    user = user[0]
    reason = reason.strip()
    reason = reason.replace('\n', ' ')
    if Appeals.objects.filter(user=user).exists():
        Appeals.objects.filter(user=user).update(reason=reason)
    else:
        Appeals.objects.create(user=user, reason=reason)

    return HttpResponse(status=200)

""" Admin Views """
@login_required
def adminDashboard_view(request):
    if not request.user.is_superuser:
        return redirect(reverse('home'))

    post_reports = ReportPost.objects.all().count()
    comment_reports = ReportComment.objects.all().count()
    user_reports = ReportUser.objects.all().count()
    total = post_reports + comment_reports + user_reports

    post_percentage = int(post_reports/total*100)
    comment_percentage = int(comment_reports/total*100)
    user_percentage = int(user_reports/total*100)

    context = {
        'user': request.user,
        'post_reports': post_reports,
        'comment_reports': comment_reports,
        'user_reports': user_reports,
        'total': total,
        'post_percentage': post_percentage,
        'comment_percentage': comment_percentage,
        'user_percentage': user_percentage,
    }
    return render(request, 'adminDashboard.html', context)

@login_required
def adminReportedContent_view(request):
    if not request.user.is_superuser:
        return redirect(reverse('home'))

    # print(ReportComment.objects.all().select_related('comment__post').query)

    post_reports = ReportPost.objects.all()
    comment_reports = ReportComment.objects.all().select_related('comment__post')
    user_reports = ReportUser.objects.all().select_related('target')

    if user_reports.exists():
        print(user_reports[0].__dict__)
        print(user_reports[0].__dict__["_state"].__dict__)

    context = {
        'user': request.user,
        'post_reports': post_reports,
        'comment_reports': comment_reports,
        'user_reports': user_reports,
    }
    return render(request, 'adminReportedContent.html', context)

@login_required
def adminReportedContentDelete_view(request):
    if not request.user.is_superuser:
        return redirect(reverse('home'))
    if request.method != "POST":
        return redirect(reverse('admin_reported'))

    id = request.POST.get('id')  # good luck trying to re-read this
    if id[0] == 'P' or id[0] == 'p':
        post = Posts.objects.filter(post_id = id[1:])
        post.delete()
    if id[0] == 'C' or id[0] == 'c':
        comment = PostComments.objects.filter(post_comment_id = id[1:])
        comment.delete()
    if id[0] == 'U' or id[0] == 'u':
        user = Users.objects.filter(user_id = id[1:])
        user.update(is_banned = True)
        ReportUser.objects.filter(target_id = id[1:]).delete()

    return HttpResponse(status=200)

@login_required
def adminReportedContentDismiss_view(request):
    if not request.user.is_superuser:
        return redirect(reverse('home'))
    if request.method != "POST":
        return redirect(reverse('admin_reported'))

    id = request.POST.get('id')
    if id[0] == 'P' or id[0] == 'p':
        post = ReportPost.objects.filter(post_id = id[1:])
        post.delete()
    if id[0] == 'C' or id[0] == 'c':
        comment = ReportComment.objects.filter(comment_id = id[1:])
        comment.delete()
    if id[0] == 'U' or id[0] == 'u':
        user = ReportUser.objects.filter(target_id = id[1:])
        user.delete()

    return HttpResponse(status=200)

@login_required
def adminFlair_view(request):
    if not request.user.is_superuser:
        return redirect(reverse('home'))

    flairForm = EditFlairForm()
    flairs = Flair.objects.all()

    return render(request, 'adminFlair.html', {'flairForm': flairForm, 'flairs': flairs, 'user': request.user})

@login_required
def adminAddFlair_view(request):
    if not request.user.is_superuser:
        return redirect(reverse('home'))

    # if invalid request
    if request.method != "POST":
        return redirect(reverse('admin_flair'))

    flairForm = EditFlairForm(request.POST)

    # kick them out if form is invalid
    if not flairForm.is_valid():
        return redirect(reverse('admin_flair'))

    flair_name = flairForm.cleaned_data['flair_name']
    flair_color = flairForm.cleaned_data['flair_color']

    Flair.objects.create(
        flair_name=flair_name,
        flair_color=flair_color,
    )

    return redirect(reverse('admin_flair'))

@login_required
def adminDelFlair_view(request):
    if not request.user.is_superuser:
        return redirect(reverse('home'))

    if request.method == "GET" and len(request.GET) == 0 or request.GET.get("id") is None:
        return redirect(reverse('admin_flair'))

    flair_id = request.GET.get("id")
    flair = Flair.objects.filter(flair_id=flair_id)

    # checks if the event exists
    if len(flair) == 0:
        return redirect(reverse('admin_flair'))  #  if they not creator, kick them

    flair.delete()

    return redirect(reverse('admin_flair'))

@login_required
def adminEditFAQ_view(request):
    if not request.user.is_superuser:
        return redirect(reverse('home'))


    context = {
        'AddFaqForm': AddFAQForm(),
        'faqs': CompanionFAQ.objects.all(),
    }
    return render(request, 'adminChatbotFAQ.html', context)

@login_required
def adminEditFAQAdd_view(request):
    if not request.user.is_superuser:
        return redirect(reverse('home'))

    add_faq = AddFAQForm(request.POST)
    if request.method != "POST" and not add_faq.is_valid():
        print(add_faq.errors)
        return redirect(reverse('admin_faq'))

    category_id = add_faq.data['category']
    question = add_faq.data['question']
    answer = add_faq.data['answer']
    keywords = add_faq.data['keywords']

    CompanionFAQ.objects.create(category_id=category_id, question=question, answer=answer, keywords=keywords)

    return redirect(reverse('admin_faq'))

@login_required
def adminEditFAQDelete_view(request):
    if not request.user.is_superuser:
        return redirect(reverse('home'))

    if request.method == "POST" and len(request.POST) == 0:
        return redirect(reverse('admin_faq'))

    faq_id = request.GET.get('id')
    CompanionFAQ.objects.filter(id=faq_id).delete()

    return redirect(reverse('admin_faq'))

@login_required
def adminAppeal_view(request):

    appeals = Appeals.objects.all()

    return render(request, 'adminAppeal.html', {'appeals': appeals})

@login_required
def adminAppealApprove_view(request):
    if not request.user.is_superuser:
        return redirect(reverse('home'))
    if request.method != "POST":
        return redirect(reverse('admin_appeal'))

    userId = request.POST.get('userId')

    Appeals.objects.filter(user_id=userId).delete()
    Users.objects.filter(user_id=userId).update(is_banned = False)

    return redirect(reverse('admin_appeal'))

@login_required
def adminAppealDeny_view(request):
    if not request.user.is_superuser:
        return redirect(reverse('home'))
    if request.method != "POST":
        return redirect(reverse('admin_appeal'))

    userId = request.POST.get('userId')

    Appeals.objects.filter(user_id=userId).delete()

    return redirect(reverse('admin_appeal'))

""" Home Views """
@login_required
def home_view(request):
    postForms = PostForm()
    # posts = Posts.objects.all().order_by('-created_at')

    posts = Posts.objects.all().order_by('-created_at').annotate(
        isUpvoted=Exists(PostVotes.objects.filter(post_id=OuterRef("post_id"), user_id=request.user.pk, post_upvote=True)),
        isDownvoted=Exists(PostVotes.objects.filter(post_id=OuterRef("post_id"), user_id=request.user.pk, post_upvote=False))
    )

    # posts = Post.objects.annotate(
    #     isUpvoted=Exists(
    #         Post.objects.filter(id=OuterRef('id'), liked_by=request.user)
    #     )
    # )
    # posts = Posts.objects.all().order_by('-created_at').annotate(
    #     isDownvoted=PostVotes.objects.filter(user_id=request.user.pk, post_upvote=False)
    # )

    # print(posts)
    # print(Posts.objects.all().order_by('-created_at').annotate(isDownvoted=Exists(PostVotes.objects.filter(post_id=OuterRef("post_id"), user_id=request.user.pk, post_upvote=False))).query)

    context = {
        'PostForm': postForms,
        'posts': posts,
        'searchForm': SearchForm(),
    }
    return render(request, 'home.html', context)

@login_required
def search_view(request):
    # if not post request or form not valid
    if request.method != "POST" or request.POST.get("searchQuery") is None or len(request.POST.get("searchQuery")) == 0:
        return render(request, 'search.html')

    searchQuery = request.POST.get("searchQuery")
    postSearch = Posts.objects.filter(title__icontains=searchQuery).order_by('-created_at').annotate(
        isUpvoted=Exists(PostVotes.objects.filter(post_id=OuterRef("post_id"), user_id=request.user.pk, post_upvote=True)),
        isDownvoted=Exists(PostVotes.objects.filter(post_id=OuterRef("post_id"), user_id=request.user.pk, post_upvote=False))
    )
    profileSearch = Users.objects.filter(username__icontains=searchQuery, is_active=True).order_by('-created_at')

    context = {
        'postSearch': postSearch,
        'profileSearch': profileSearch,
        'searchQuery': searchQuery,
    }
    return render(request, 'search.html', context)

@login_required
def home_createPost_view(request):
    if request.method != "POST":
        print("not a post request")
        return redirect(reverse('home'))

    postForm = PostForm(request.POST)

    # kick them out if form is invalid
    if not postForm.is_valid():
        print(postForm.errors)
        return redirect(reverse('home'))

    title = postForm.data['title']
    description = postForm.data['description']
    flair_id = postForm.data['flair']
    user_id = request.user.pk

    Posts.objects.create(
        title=title,
        description=description,
        flair_id=flair_id,
        user_id=user_id,
    )

    return redirect(reverse('home'))

@login_required
def post_like_view(request):
    if request.method != "POST" or not request.POST.get("postId") or not request.POST.get("vote"):
        print("not a post request or no postId")
        return HttpResponse(status=400)

    upvote = request.POST.get('vote') == "like"
    post_id = request.POST.get('postId')
    user_id = request.user.pk

    postVote = PostVotes.objects.filter(post_id=post_id, user_id=user_id)
    post = Posts.objects.get(pk=post_id)
    notif = Notification.objects.filter(user_id=user_id)

    # print("received": upvote)
    # print("db:", "none" if not postVote else postVote[0].post_upvote)

    # notify target
    if upvote:
        Notification.objects.create(user_id=user_id, target_id=post.user.pk, type='post_like',
                                    vote=upvote, title=post.title)
    else:
        Notification.objects.create(user_id=user_id, target_id=post.user.pk, type='post_dislike',
                                    vote=upvote, title=post.title)

    # update db
    if not postVote:
        PostVotes.objects.create(post_upvote=upvote, user_id=user_id, post_id=post_id)

    elif postVote[0].post_upvote == upvote:  # if it's a dislike
        postVote.delete()
    else:
        postVote.update(post_upvote=upvote)


    return HttpResponse(status=200)

@login_required
def indivPost_view(request):
    if request.method != "GET" or not request.GET.get("postId"):
        print("invalid query")
        return redirect(reverse('home'))

    postId = request.GET.get("postId")
    posts = Posts.objects.filter(post_id=postId).order_by('-created_at').annotate(
        isUpvoted=Exists(
            PostVotes.objects.filter(post_id=OuterRef("post_id"), user_id=request.user.pk, post_upvote=True)),
        isDownvoted=Exists(
            PostVotes.objects.filter(post_id=OuterRef("post_id"), user_id=request.user.pk, post_upvote=False))
    )

    if posts is None:
        print("post does not exist")
        return redirect(reverse('home'))

    commentForm = IndivPostCommentForm()
    comments = PostComments.objects.filter(post_id=postId).order_by('-created_at').annotate(
        isUpvoted=Exists(
            PostcVotes.objects.filter(post_comment_id=OuterRef("post_comment_id"), user_id=request.user.pk, postc_upvote=True)),
        isDownvoted=Exists(
            PostcVotes.objects.filter(post_comment_id=OuterRef("post_comment_id"), user_id=request.user.pk, postc_upvote=False))
    )
    # commentUpvotes = PostcVotes.objects.filter(post_id=postId)

    context ={
        'post': posts[0],
        'commentForm': commentForm,
        'comments': comments,
        'searchForm': SearchForm(),
    }

    return render(request, 'indivPost.html', context)

@login_required
def indivPost_addComment_view(request):
    if request.method != "POST" or not request.GET.get("postId") or not request.POST.get("content"):
        print("invalid query")

        return redirect(reverse('home'))

    content = request.POST.get("content")
    postId = request.GET.get("postId")
    posts = Posts.objects.filter(post_id=postId)

    if posts is None:
        print("post does not exist")
        return redirect(reverse('home'))

    # notify target
    Notification.objects.create(user_id=request.user.pk, target_id=posts[0].user.pk, type='comment_add',
                                title=posts[0].title)

    PostComments.objects.create(content=content, post_id=postId, user_id=request.user.pk)

    return redirect(f"{reverse('indivPost')}?postId={postId}")

@login_required
def comment_like_view(request):
    if request.method != "POST" or not request.POST.get("commentId") or not request.POST.get("vote"):
        print("not a post request or no commentId")
        return HttpResponse(status=400)

    upvote = request.POST.get('vote') == "like"
    comment_id = request.POST.get('commentId')
    user_id = request.user.pk
    comment = PostComments.objects.filter(post_comment_id=comment_id)

    if not comment.exists():
        print("no such comment")
        return HttpResponse(status=400)

    # print(comment_id)
    # print(request.POST.get('vote'))
    postcVote = PostcVotes.objects.filter(post_comment_id=comment_id, user_id=user_id)
    notif = Notification.objects.filter(user_id=user_id)

    # print("received": upvote)
    # print("db:", "none" if not postVote else postVote[0].post_upvote)

    # notify target
    target_id = comment[0].post.user.pk
    title = comment[0].post.title
    if upvote:
        Notification.objects.create(user_id=user_id, target_id=target_id, type='comment_like',
                                    vote=upvote, title=title)
    else:
        Notification.objects.create(user_id=user_id, target_id=target_id, type='comment_dislike',
                                    vote=upvote, title=title)

    # the upvote/downvote holy grail, I should've made 2 views instead maybe idk maybe that might be even longer
    if not postcVote:
        PostcVotes.objects.create(postc_upvote=upvote, user_id=user_id, post_comment_id=comment_id)

    elif postcVote[0].postc_upvote == upvote:  # if it's a dislike
        postcVote.delete()
    else:
        postcVote.update(postc_upvote=upvote)

    return HttpResponse(status=200)

""" Report Views """
@login_required
def report_post_view(request):
    if request.method != "POST" or not request.POST.get("id") or not request.POST.get("content"):
        print("invalid query")

        return redirect(reverse('home'))

    content = request.POST.get("content")
    postId = request.POST.get("id")
    posts = Posts.objects.filter(post_id=postId)

    if posts is None:
        print("post does not exist")
        return redirect(reverse('home'))

    content = content.strip()
    content = content.replace('\n', ' ')
    ReportPost.objects.create(content=content, post_id=postId, user_id=request.user.pk)

    return HttpResponse(status=200)

@login_required
def report_comment_view(request):
    if request.method != "POST" or not request.POST.get("id") or not request.POST.get("content"):
        print("invalid query")

        return redirect(reverse('home'))

    content = request.POST.get("content")
    commentId = request.POST.get("id")
    comments = PostComments.objects.filter(post_comment_id=commentId)

    if comments is None:
        print("comment does not exist")
        return redirect(reverse('home'))

    content = content.strip()
    content = content.replace('\n', ' ')
    ReportComment.objects.create(content=content, comment_id=commentId, user_id=request.user.pk)

    return HttpResponse(status=200)

@login_required
def report_user_view(request):
    if request.method != "POST" or not request.POST.get("id") or not request.POST.get("content"):
        print("invalid query")

        return redirect(reverse('home'))

    content = request.POST.get("content")
    userId = request.POST.get("id")
    users = Users.objects.filter(user_id=userId)

    if users is None:
        print("user does not exist")
        return redirect(reverse('home'))

    content = content.strip()
    content = content.replace('\n', ' ')
    ReportUser.objects.create(content=content, target_id=userId, user_id=request.user.pk)

    return HttpResponse(status=200)

""" Calendar Views """
@login_required
def events_view(request):
    # Get the current year and month
    year = int(request.GET.get('year')) if request.GET.get('year') else datetime.now().year
    month = int(request.GET.get('month')) if request.GET.get('month') else datetime.now().month

    user_id = request.user.pk
    eventEditForm = EventEditForm()
    eventForm = EventForm()

    # Convert to integers
    year = int(year)
    month = int(month)

    # Get month info
    calendar.setfirstweekday(calendar.SUNDAY)
    first_day, days_in_month = calendar.monthrange(year, month)
    month_name = calendar.month_name[month]
    first_day = (first_day + 1) % 7

    # Get events
    events = CalendarEvent.objects.filter(user_id=user_id, start_time__year=year, start_time__month=month).order_by('start_time')
    events_json = serializers.serialize('json', events)

    user = request.user
    # print(events[0].start_time)
    # Pass data to template
    context = {
        'user': user,
        'month_name': month_name,
        'year': year,
        'first_day': first_day,
        'days_in_month': days_in_month,
        'eventForm': eventForm,
        'eventEditForm': eventEditForm,
        'events': events,
        'events_json': events_json,
        'searchForm': SearchForm(),
    }
    return render(request, 'calendar.jinja', context)

@login_required
def event_add_view(request):
    # kick them out if no post request
    if request.method != "POST":
        return redirect(reverse('calendar'))

    eventForm = EventForm(request.POST)
    user_id = request.user.pk

    # kick them out if form is invalid
    if not eventForm.is_valid():
        return redirect(reverse('calendar'))

    category = eventForm.cleaned_data['category']
    title = eventForm.cleaned_data['title']
    date = eventForm.cleaned_data['date']
    start_time = eventForm.cleaned_data['start_time']
    end_time = eventForm.cleaned_data['end_time']
    location = eventForm.cleaned_data['location']
    desc = eventForm.cleaned_data['description']
    color = eventForm.cleaned_data['color']

    color = color.split('-')[1]

    start = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M:%S")


    CalendarEvent.objects.create(
        user_id=user_id,
        category=category,
        title=title,
        start_time=start,
        end_time=end,
        location=location,
        description=desc,
        color=color
    )

    # redirect back with month and year
    if request.GET.get('year'):
        month = int(request.GET.get('month'))
        year = int(request.GET.get('year'))
        return redirect(f"{reverse('calendar')}?month={month}&year={year}")
    return redirect(reverse('calendar'))

@login_required
def event_edit_view(request):
    # kick them out if they somehow get here
    if request.method != "POST" or len(request.GET) == 0 or request.GET.get("id") is None:
        print("no get or post, kicking")
        return redirect(reverse('calendar'))

    # check if they can delete
    user_id = request.user.pk
    event_id = request.GET.get("id")
    eventForm = EventForm(request.POST)
    event = CalendarEvent.objects.filter(user_id=user_id, event_id=event_id)

    if len(event) == 0:
        print("can't edit/find event, kicking")
        return redirect(reverse('calendar'))  # if they not creator, kick them

    # processing form field to fit db field
    date=eventForm.cleaned_data['date']
    start_time=eventForm.cleaned_data['start_time']
    end_time=eventForm.cleaned_data['end_time']
    color=eventForm.cleaned_data['color']

    color = color.split('-')[1]
    start = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M:%S")

    # update db
    event.update(
        category=eventForm.cleaned_data['category'],
        title=eventForm.cleaned_data['title'],
        start_time=start,
        end_time=end,
        location=eventForm.cleaned_data['location'],
        description=eventForm.cleaned_data['description'],
        color=color,
    )

    # redirect back to calendar page
    print("successfully edited, redirecting")
    if request.GET.get('year'):
        month = int(request.GET.get('month'))
        year = int(request.GET.get('year'))
        return redirect(f"{reverse('calendar')}?month={month}&year={year}")
    return redirect(reverse('calendar'))

@login_required
def event_delete_view(request):
    # kick them out if they somehow get here
    if request.method == "GET" and len(request.GET) == 0 or request.GET.get("id") is None:
        return redirect(reverse('calendar'))

    # check if they can delete
    user_id = request.user.pk
    event_id = request.GET.get("id")
    events = CalendarEvent.objects.filter(user_id=user_id, event_id=event_id)

    # checks if the event exists
    if len(events) == 0:
        return redirect(reverse('calendar'))  #  if they not creator, kick them

    # delete from db
    events.delete()

    # redirect back to calendar page
    if request.GET.get('year'):
        month = int(request.GET.get('month'))
        year = int(request.GET.get('year'))
        return redirect(f"{reverse('calendar')}?month={month}&year={year}")
    return redirect(reverse('calendar'))

""" Saved Views """
@login_required
def saved_view(request):

    context = {
        'searchForm': SearchForm(),
    }
    return render(request, 'saved.html', context)

""" Profile Views """
@login_required
def profile_view(request):
    profileForm = ProfileForm()
    editProfileForm = EditProfileForm()
    editProfileImageForm = EditProfileImageForm()

    # gets email from url, or default to login user's email
    if request.method == "GET" and len(request.GET) > 0 and request.GET.get("email") is not None:
        email = request.GET.get("email")
    else:
        email = request.user.stu_email

    # check if url email is valid, or else it'll default to login user's email
    target_user_email = Users.objects.filter(stu_email=email).values("stu_email")
    if len(target_user_email) == 0:
        target_user_email = Users.objects.filter(stu_email=request.user.stu_email).values("stu_email")

    target_user_email = target_user_email[0]["stu_email"]  # getting the profile user email

    target_profile = Users.objects.filter(stu_email=target_user_email).values("user_id", "username", "stu_email", "image", "description")[0]  # own profile
    upvotes = int(UserComments.objects.filter(profile_user_email=target_user_email, profile_upvote=True).count())
    downvotes = int(UserComments.objects.filter(profile_user_email=target_user_email, profile_upvote=False).count())
    comments = UserComments.objects.filter(profile_user_email=target_user_email)
    ownProfile = target_user_email == request.user.stu_email

    context = {
        'profileForm': profileForm,
        'editProfileForm': editProfileForm,
        'editProfileImageForm': editProfileImageForm,
        'profile': target_profile,
        'upvotes': upvotes,
        'downvotes': downvotes,
        'comments': comments,
        'ownProfile': ownProfile,
        'searchForm': SearchForm(),
    }
    return render(request, 'profile.html', context)

@login_required
def profile_add_view(request):
    # invalid query
    if request.method == "GET" and len(request.GET) == 0 or request.GET.get("email") is None:
        print("no get or invalid email, kicking")
        return redirect(reverse('profile'))

    # invalid email | additional error handling
    email = request.GET.get("email")
    profile_user = Users.objects.filter(stu_email=email)
    if profile_user.count() == 0:
        print("user not found, kicking")
        if request.GET.get('email'):
            return redirect(f"{reverse('profile')}?email={email}")
        return redirect(reverse('profile'))

    # invalid post request form
    profileForm = ProfileForm(request.POST)
    if not profileForm.is_valid():
        print("invalid form")
        return redirect(f"{reverse('profile')}?email={email}")

    commenter_id = request.user.pk
    vote = True if profileForm.data["votes"] == "upvote" else False
    comment = UserComments.objects.filter(commenter_id=commenter_id)

    # notify target
    if vote:
        Notification.objects.create(user_id=commenter_id, target_id=profile_user[0].pk, type='profile_like', vote=vote)
    else:
        Notification.objects.create(user_id=commenter_id, target_id=profile_user[0].pk, type='profile_dislike', vote=vote)

    #check if they're adding review to their own profile
    if commenter_id == profile_user[0].pk:
        print("User cannot comment on own profile, kicking")
        return redirect(f"{reverse('profile')}?email={email}")

    # insert to db
    if comment.count() == 0:
        UserComments.objects.create(profile_feedback=profileForm.data["profile_feedback"], profile_upvote=vote,
                                    profile_user_email=email, commenter_id=commenter_id)
    else:
        comment.update(profile_feedback=profileForm.data["profile_feedback"], profile_upvote=vote,
                                    profile_user_email=email, commenter_id=commenter_id)

    return redirect(f"{reverse('profile')}?email={email}")

@login_required
def profile_edit_view(request):
    # invalid query
    if request.method == "GET" and len(request.GET) == 0 or request.GET.get("email") is None:
        print("no get or invalid email, kicking")
        return redirect(reverse('profile'))

    # invalid email | additional error handling
    email = request.GET.get("email")
    editor = Users.objects.filter(stu_email=email)
    if editor.count() == 0:
        print("user not found, kicking")
        if request.GET.get('email'):
            return redirect(f"{reverse('profile')}?email={email}")
        return redirect(reverse('profile'))
    # editor = editor[0]

    # invalid post request form
    editProfileForm = EditProfileForm(request.POST)
    editProfileImageForm = EditProfileImageForm(request.POST, request.FILES, instance=request.user)
    if not editProfileForm.is_valid() and not editProfileImageForm.is_valid():
        print("invalid edit form")
        print(editProfileForm.errors)
        print("invalid image form")
        print(editProfileImageForm.errors)
        return redirect(f"{reverse('profile')}?email={email}")

    # check if they're editing their own profile
    if editor[0].stu_email != request.user.stu_email:
        print("User cannot edit on other's profile, kicking")
        return redirect(f"{reverse('profile')}?email={email}")

    if editProfileForm.is_valid():
        editor.update(username=editProfileForm.data["username"], description=editProfileForm.data["description"])

        return redirect(f"{reverse('profile')}?email={email}")

    elif editProfileImageForm.is_valid():
        editProfileImageForm.save()  # save image

        return redirect(f"{reverse('profile')}?email={email}")
    else:
        print("how did you get here")
        return redirect(f"{reverse('profile')}?email={email}")

""" FAQ this Chat Bot"""
@login_required
def companion_view(request):

    context = {
        'faqs': CompanionFAQ.objects.all(),
        'faq_category': CompanionFAQCategory.objects.all(),
    }
    return render(request, 'companion.html', context)

""" Help Views """
@login_required
def help_center_view(request):
    return render(request, 'helpCenter.html')

""" Notification Views """
@login_required
def notification_view(request):
    notif = Notification.objects.filter(target_id=request.user.pk).order_by("-created_at")

    return render(request, 'notification.html', {'notifications': notif, 'searchForm': SearchForm()})

@login_required
def mark_notification_view(request):
    if request.method == "POST" and len(request.POST) == 0 or request.POST.get("user_id") is None:
        return HttpResponse(status=400)

    user_id = int(request.POST.get("user_id"))
    Notification.objects.filter(target_id=user_id).update(is_seen=True)

    return HttpResponse(status=200)

""" App Settings """
@login_required
def app_settings_view(request):
    return render(request, 'appSettings.html')

@login_required
def app_settings_checkPass_view(request):
    if (request.method != "POST" or not request.POST.get("currentPass")):
        print("not post")
        return JsonResponse({'pass': False})

    passw = request.POST.get("currentPass")
    stu_email = Users.objects.filter(username=request.user).values("stu_email")[0]["stu_email"]
    user = authenticate(request, stu_email=stu_email, password=passw)

    if user is None:
        print("password error")
        return JsonResponse({'pass': False})

    return JsonResponse({'pass': True})

@login_required
def app_settings_editPass_view(request):
    if request.method != "POST" or not request.POST.get("newPass"):
        return redirect(reverse('app_settings'))

    new_pass = make_password(request.POST.get("newPass"))
    User.objects.filter(user_id=request.user.pk).update(password=new_pass)

    return redirect(reverse('signup'))

@login_required
def app_settings_deleteAcc_view(request):
    if request.method != "POST" or not request.POST.get("user_id"):
        print("not post")
        return redirect(reverse("app_settings"))

    if request.POST.get("user_id") != str(request.user.pk):
        print("safety feature")
        return redirect(reverse("app_settings"))

    print("account deleted")
    user = Users.objects.get(pk=request.user.pk)
    user.delete()
    logout(request)

    return redirect(reverse("signup"))



