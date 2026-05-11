from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm, FeedbackForm
from .models import Topic, AITask, Submission, Analytics, Profile, Feedback
from .utils import ai_generate_task, ai_evaluate_answer

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.db.models import Avg, Max
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


# Bosh sahifa
def home(request):
    topics = Topic.objects.all()
    return render(request, 'portal/home.html', {'topics': topics})


def login_view(request):
    # Agar foydalanuvchi allaqachon kirgan bo'lsa, bosh sahifaga yuboramiz
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')

        user = authenticate(username=u, password=p)

        if user is not None:
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {u}! Tizimga muvaffaqiyatli kirdingiz.")
            return redirect('home')
        else:
            # Login yoki parol xato bo'lsa
            messages.error(request, "Foydalanuvchi nomi yoki parol noto'g'ri!")

    return render(request, 'registration/login.html')


@login_required
def profile_view(request):
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Profilingiz muvaffaqiyatli yangilandi!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    my_submissions = Submission.objects.filter(student=request.user).order_by('-submitted_at')

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'submissions': my_submissions[:5],
        'total_tasks': my_submissions.count(),
        'avg_score': round(my_submissions.aggregate(Avg('ai_score'))['ai_score__avg'] or 0, 1),
    }
    return render(request, 'portal/profile.html', context)


# 2.1: Topshiriq yaratish view
@login_required
def create_task(request):
    if request.method == "POST":
        topic_id = request.POST.get('topic')
        level = request.POST.get('level')
        topic = Topic.objects.get(id=topic_id)

        # AI dan natija olish
        ai_response = ai_generate_task(topic.title, level)

        # Natijani bo'laklarga bo'lish (oddiyroq usulda)
        parts = ai_response.split("YECHIM:")
        content = parts[0].replace("TOPSHIRIQ:", "").strip()
        solution = parts[1].strip() if len(parts) > 1 else "Yechim topilmadi"

        # Bazaga saqlash
        task = AITask.objects.create(
            topic=topic,
            level=level,
            prompt_used=f"Mavzu: {topic.title}, Daraja: {level}",
            content=content,
            correct_solution=solution,
            created_by=request.user
        )
        return redirect('task_detail', pk=task.pk)

    topics = Topic.objects.all()
    return render(request, 'portal/create_task.html', {'topics': topics})


def task_detail(request, pk):
    # Topshiriqni bazadan qidiramiz
    task = get_object_or_404(AITask, pk=pk)

    if request.method == "POST":
        student_answer = request.POST.get('answer')

        # AI orqali baholash
        evaluation = ai_evaluate_answer(task.content, task.correct_solution, student_answer)

        # AI javobini bo'laklarga bo'lish
        try:
            score = int(''.join(filter(str.isdigit, evaluation.split("FEEDBACK:")[0])))
            feedback = evaluation.split("FEEDBACK:")[1].strip()
        except:
            score = 0
            feedback = evaluation

        # Javobni saqlash
        Submission.objects.create(
            task=task,
            student=request.user,
            student_answer=student_answer,
            ai_score=score,
            ai_feedback=feedback,
            is_evaluated=True
        )
        return redirect('results')

    # MUHIM: Mana bu qator bo'lishi shart!
    return render(request, 'portal/task_detail.html', {'task': task})


# 2.3: Natijalar va tahlil
def results(request):
    submissions = Submission.objects.filter(student=request.user).order_by('-submitted_at')
    return render(request, 'portal/results.html', {'submissions': submissions})


# 2. RO'YXATDAN O'TISH (Muvaffaqiyatli alert va parolni tekshirish bilan)
def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        p1 = request.POST.get('password')
        p2 = request.POST.get('confirm_password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Bu foydalanuvchi nomi allaqachon mavjud.")
        elif p1 != p2:
            messages.error(request, "Parollar bir-biriga mos kelmadi!")
        elif len(p1) < 6:
            messages.error(request, "Parol juda qisqa (kamida 6 ta belgi).")
        else:
            # create_user parolni shifrlab saqlaydi
            user = User.objects.create_user(username=username, email=email, password=p1)
            user.save()
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {username}! Ro'yxatdan muvaffaqiyatli o'tdingiz.")
            return redirect('home')

    return render(request, 'registration/register.html')


@login_required
def feedback_view(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(request, "Rahmat! Fikringiz muvaffaqiyatli qabul qilindi.")
            return redirect('feedback')

    feedbacks = Feedback.objects.all().order_by('-created_at')[:10]
    form = FeedbackForm()
    return render(request, 'portal/feedback.html', {'form': form, 'feedbacks': feedbacks})


@login_required
def all_tasks_view(request):
    # Qidiruv va filtr logikasi
    query = request.GET.get('q')
    topic_id = request.GET.get('topic')

    tasks = AITask.objects.all().order_by('-created_at')

    if query:
        tasks = tasks.filter(content__icontains=query)
    if topic_id:
        tasks = tasks.filter(topic_id=topic_id)

    topics = Topic.objects.all()

    return render(request, 'portal/all_tasks.html', {
        'tasks': tasks,
        'topics': topics
    })