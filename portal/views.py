from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm, FeedbackForm
from .models import Topic, AITask, Submission, Analytics, Profile, Feedback
from .utils import ai_generate_task, ai_evaluate_answer
from urllib.parse import urlparse, parse_qs, urlencode
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.shortcuts import render, redirect
from django.db.models import Avg, Max
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Topic, VideoLesson, Quiz, Question, QuizSubmission, Submission
from django.db.models import Avg, Sum, Max


# Bosh sahifa
def home(request):
    topics = Topic.objects.all()
    return render(request, 'portal/home.html', {'topics': topics})


def login_view(request):
    # Agar foydalanuvchi oldin login qilgan bo'lsa, home sahifaga yuboramiz
    if request.user.is_authenticated:
        return redirect('home')

    # Middleware login sahifaga ?next=/qaysidir-sahifa/ qilib yuboradi
    next_url = request.GET.get("next") or request.POST.get("next") or "home"

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(
                request,
                f"Xush kelibsiz, {username}! Tizimga muvaffaqiyatli kirdingiz."
            )

            # Login bo'lgandan keyin avval kirmoqchi bo'lgan sahifasiga qaytaradi
            return redirect(next_url)
        else:
            messages.error(
                request,
                "Foydalanuvchi nomi yoki parol noto'g'ri!"
            )

    return render(request, 'registration/login.html', {
        "next": next_url
    })


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


# --- 1. VIDEODARSLAR BO'LIMI ---

@login_required
def video_list_view(request):
    """Barcha videodarslar ro'yxati"""
    videos = VideoLesson.objects.all().order_by('-created_at')
    topics = Topic.objects.all()

    # Mavzu bo'yicha filtr qilish
    topic_id = request.GET.get('topic')
    if topic_id:
        videos = videos.filter(topic_id=topic_id)

    return render(request, 'portal/video_list.html', {
        'videos': videos,
        'topics': topics
    })

import re

def extract_youtube_id(url):
    if not url:
        return None

    parsed = urlparse(url)
    host = parsed.netloc.lower().replace("www.", "").replace("m.", "")
    path = parsed.path.strip("/")

    video_id = None

    if host == "youtu.be":
        video_id = path.split("/")[0]

    elif host in ["youtube.com", "youtube-nocookie.com"]:
        query = parse_qs(parsed.query)

        if path == "watch":
            video_id = query.get("v", [None])[0]

        elif path.startswith("embed/"):
            parts = path.split("/")
            video_id = parts[1] if len(parts) > 1 else None

        elif path.startswith("shorts/"):
            parts = path.split("/")
            video_id = parts[1] if len(parts) > 1 else None

    if not video_id:
        match = re.search(r"([a-zA-Z0-9_-]{11})", url)
        video_id = match.group(1) if match else None

    if video_id and re.fullmatch(r"[a-zA-Z0-9_-]{11}", video_id):
        return video_id

    return None


@login_required
def video_detail_view(request, pk):
    video = get_object_or_404(VideoLesson, pk=pk)

    video_id = extract_youtube_id(video.video_url)

    embed_url = None
    watch_url = None

    if video_id:
        params = {
            "rel": "0",
            "playsinline": "1",
        }

        embed_url = f"https://www.youtube-nocookie.com/embed/{video_id}?{urlencode(params)}"
        watch_url = f"https://www.youtube.com/watch?v={video_id}"
    else:
        messages.error(request, "Video havolasi noto'g'ri kiritilgan!")

    response = render(request, "portal/video_detail.html", {
        "video": video,
        "video_id": video_id,
        "embed_url": embed_url,
        "watch_url": watch_url,
    })

    response["Referrer-Policy"] = "strict-origin-when-cross-origin"

    return response
# --- 2. TESTLAR (QUIZ) BO'LIMI ---

@login_required
def quiz_list_view(request):
    """Mavjud barcha testlar ro'yxati"""
    quizzes = Quiz.objects.all().order_by('-created_at')
    return render(request, 'portal/quiz_list.html', {'quizzes': quizzes})


@login_required
def quiz_detail_view(request, pk):
    """Testni ishlash sahifasi va natijani hisoblash"""
    quiz = get_object_or_404(Quiz, pk=pk)
    questions = quiz.questions.all()

    if request.method == "POST":
        score = 0
        total = questions.count()

        for q in questions:
            # Har bir savol uchun tanlangan javobni olamiz
            selected_option = request.POST.get(f'question_{q.id}')
            if selected_option == q.correct_answer:
                score += 1

        # Natijani bazaga saqlash
        QuizSubmission.objects.create(
            student=request.user,
            quiz=quiz,
            score=score,
            total_questions=total
        )

        messages.success(request, f"Tabriklaymiz! Siz {quiz.title} testidan {score}/{total} natija qayd etdingiz.")
        return redirect('profile')  # Natijani ko'rish uchun profilga yuboramiz

    return render(request, 'portal/quiz_detail.html', {
        'quiz': quiz,
        'questions': questions
    })


# --- 3. PROFILNI YANGILASH (TEST NATIJALARI BILAN) ---

@login_required
def profile_view(request):
    # Agar userda profile yo'q bo'lsa avtomatik yaratamiz
    if not hasattr(request.user, "profile"):
        Profile.objects.create(user=request.user)

    # Profilni yangilash formasi
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profilingiz muvaffaqiyatli yangilandi!")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    # AI topshiriqlar natijalari
    ai_submissions = (
        Submission.objects
        .filter(student=request.user)
        .select_related("task", "task__topic")
        .order_by("-submitted_at")
    )

    # Quiz / test natijalari
    quiz_results = (
        QuizSubmission.objects
        .filter(student=request.user)
        .select_related("quiz", "quiz__topic")
        .order_by("-completed_at")
    )

    # AI statistikalar
    total_ai_tasks = ai_submissions.count()
    avg_ai_score = round(
        ai_submissions.aggregate(avg=Avg("ai_score"))["avg"] or 0,
        1
    )
    best_ai_score = ai_submissions.aggregate(best=Max("ai_score"))["best"] or 0
    total_ai_score = ai_submissions.aggregate(total=Sum("ai_score"))["total"] or 0

    # Quiz statistikalar
    total_quizzes = quiz_results.count()
    total_questions = quiz_results.aggregate(total=Sum("total_questions"))["total"] or 0
    total_correct = quiz_results.aggregate(total=Sum("score"))["total"] or 0

    if total_questions > 0:
        accuracy_percent = round((total_correct / total_questions) * 100, 1)
    else:
        accuracy_percent = 0

    quiz_percentages = [result.percentage for result in quiz_results]

    if quiz_percentages:
        avg_quiz_score = round(sum(quiz_percentages) / len(quiz_percentages), 1)
        best_quiz_score = round(max(quiz_percentages), 1)
    else:
        avg_quiz_score = 0
        best_quiz_score = 0

    # Umumiy progress
    total_activities = total_ai_tasks + total_quizzes

    if total_activities > 0:
        overall_score = round((avg_ai_score + avg_quiz_score) / 2, 1)
    else:
        overall_score = 0

    # Tavsiya matni
    if overall_score >= 85:
        recommendation_title = "Ajoyib natija!"
        recommendation_text = "Siz juda yaxshi natija ko'rsatyapsiz. Endi murakkabroq topshiriqlar va testlar bilan ishlashni tavsiya qilamiz."
    elif overall_score >= 60:
        recommendation_title = "Yaxshi ketayapsiz!"
        recommendation_text = "Natijalaringiz yaxshi. Barqaror o'sish uchun har kuni kamida bitta test va bitta AI topshiriq bajarib boring."
    elif total_activities > 0:
        recommendation_title = "Ko'proq mashq kerak"
        recommendation_text = "Natijalarni oshirish uchun videodarslarni ko'rib, keyin test va AI topshiriqlarni qayta ishlashni tavsiya qilamiz."
    else:
        recommendation_title = "Boshlash vaqti keldi!"
        recommendation_text = "Hali natijalar mavjud emas. Avval videodarslarni ko'ring, keyin test va AI topshiriqlardan boshlang."

    # Grafik uchun oxirgi 7 ta quiz
    recent_quiz_for_chart = list(quiz_results[:7])
    recent_quiz_for_chart.reverse()

    quiz_chart_labels = [
        item.quiz.title[:22] + ("..." if len(item.quiz.title) > 22 else "")
        for item in recent_quiz_for_chart
    ]
    quiz_chart_values = [
        round(item.percentage, 1)
        for item in recent_quiz_for_chart
    ]

    # Grafik uchun oxirgi 7 ta AI topshiriq
    recent_ai_for_chart = list(ai_submissions[:7])
    recent_ai_for_chart.reverse()

    ai_chart_labels = [
        item.task.topic.title[:22] + ("..." if len(item.task.topic.title) > 22 else "")
        for item in recent_ai_for_chart
    ]
    ai_chart_values = [
        item.ai_score or 0
        for item in recent_ai_for_chart
    ]

    # Mavzu bo'yicha statistika
    topic_map = {}

    for item in ai_submissions:
        topic_name = item.task.topic.title
        if topic_name not in topic_map:
            topic_map[topic_name] = {
                "topic": topic_name,
                "ai_count": 0,
                "quiz_count": 0,
                "score_total": 0,
                "score_count": 0,
            }

        if item.ai_score is not None:
            topic_map[topic_name]["ai_count"] += 1
            topic_map[topic_name]["score_total"] += item.ai_score
            topic_map[topic_name]["score_count"] += 1

    for item in quiz_results:
        topic_name = item.quiz.topic.title
        if topic_name not in topic_map:
            topic_map[topic_name] = {
                "topic": topic_name,
                "ai_count": 0,
                "quiz_count": 0,
                "score_total": 0,
                "score_count": 0,
            }

        topic_map[topic_name]["quiz_count"] += 1
        topic_map[topic_name]["score_total"] += item.percentage
        topic_map[topic_name]["score_count"] += 1

    topic_stats = []

    for data in topic_map.values():
        if data["score_count"] > 0:
            percent = round(data["score_total"] / data["score_count"], 1)
        else:
            percent = 0

        topic_stats.append({
            "topic": data["topic"],
            "ai_count": data["ai_count"],
            "quiz_count": data["quiz_count"],
            "percent": percent,
        })

    topic_stats = sorted(topic_stats, key=lambda x: x["percent"], reverse=True)[:6]

    context = {
        "u_form": u_form,
        "p_form": p_form,

        # AI
        "ai_submissions": ai_submissions[:5],
        "total_ai_tasks": total_ai_tasks,
        "avg_ai_score": avg_ai_score,
        "best_ai_score": best_ai_score,
        "total_ai_score": total_ai_score,

        # Quiz
        "quiz_results": quiz_results[:5],
        "total_quizzes": total_quizzes,
        "avg_quiz_score": avg_quiz_score,
        "best_quiz_score": best_quiz_score,
        "total_questions": total_questions,
        "total_correct": total_correct,
        "accuracy_percent": accuracy_percent,

        # Umumiy
        "total_activities": total_activities,
        "overall_score": overall_score,
        "recommendation_title": recommendation_title,
        "recommendation_text": recommendation_text,

        # Grafik
        "quiz_chart_labels": quiz_chart_labels,
        "quiz_chart_values": quiz_chart_values,
        "ai_chart_labels": ai_chart_labels,
        "ai_chart_values": ai_chart_values,

        # Mavzular
        "topic_stats": topic_stats,
    }

    return render(request, "portal/profile.html", context)