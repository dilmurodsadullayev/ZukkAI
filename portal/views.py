from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Topic, AITask, Submission, Analytics, Profile
from .utils import ai_generate_task, ai_evaluate_answer

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.db.models import Avg, Max
from django.contrib.auth.decorators import login_required


# Bosh sahifa
def home(request):
    topics = Topic.objects.all()
    return render(request, 'portal/home.html', {'topics': topics})


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

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})