from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum

# 1. Foydalanuvchi profili (Rasm, telefon, maktab va h.k.)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png', verbose_name="Profil rasmi")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon raqami")
    school = models.CharField(max_length=255, blank=True, null=True, verbose_name="Maktab / OTM nomi")
    grade = models.CharField(max_length=50, blank=True, null=True, verbose_name="Sinf yoki Kurs")
    bio = models.TextField(max_length=500, blank=True, null=True, verbose_name="O'zi haqida qisqacha")
    total_points = models.IntegerField(default=0, verbose_name="To'plangan jami ballar")

    def __str__(self):
        return f"{self.user.username} profili"

    class Meta:
        verbose_name = "Foydalanuvchi profili"
        verbose_name_plural = "Foydalanuvchi profillari"

# --- SIGNALS: User yaratilganda avtomatik Profile yaratish ---
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
# -----------------------------------------------------------


# 2. Informatika fanidagi mavzular (Katalog)
class Topic(models.Model):
    title = models.CharField(max_length=255, verbose_name="Mavzu nomi")
    description = models.TextField(blank=True, null=True, verbose_name="Mavzu haqida qisqacha")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Mavzu"
        verbose_name_plural = "Mavzular"


# 3. AI tomonidan yaratilgan topshiriqlar (2.1-paragraf)
class AITask(models.Model):
    LEVEL_CHOICES = [
        ('oson', 'Oson'),
        ('o’rta', 'O’rta'),
        ('murakkab', 'Murakkab'),
    ]

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="tasks")
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='o’rta')
    prompt_used = models.TextField(verbose_name="AIga berilgan so'rov")
    content = models.TextField(verbose_name="Topshiriq matni")
    correct_solution = models.TextField(verbose_name="To'g'ri javob (AI talqini)")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'is_staff': True})
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.topic.title} - {self.level}"

    class Meta:
        verbose_name = "AI Topshiriq"
        verbose_name_plural = "AI Topshiriqlar"


# 4. O'quvchilar javoblari va AI Baholashi (2.2-paragraf)
class Submission(models.Model):
    task = models.ForeignKey(AITask, on_delete=models.CASCADE, related_name="submissions")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_works")
    student_answer = models.TextField(verbose_name="O'quvchi javobi")

    # AI Feedback qismi
    ai_score = models.IntegerField(null=True, blank=True, verbose_name="AI Bergan Ball")
    ai_feedback = models.TextField(null=True, blank=True, verbose_name="AI Izohi (Feedback)")

    submitted_at = models.DateTimeField(auto_now_add=True)
    is_evaluated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.username} - {self.task.topic.title}"

    # Har safar javob saqlanganda o'quvchining jami ballini yangilash
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.ai_score:
            profile = self.student.profile
            total = Submission.objects.filter(student=self.student).aggregate(Sum('ai_score'))['ai_score__sum']
            profile.total_points = total or 0
            profile.save()

    class Meta:
        verbose_name = "O'quvchi javobi"
        verbose_name_plural = "O'quvchi javoblari"


# 5. Statistika va Tajriba-sinov natijalari (2.3-paragraf)
class Analytics(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    average_score = models.FloatField(default=0.0, verbose_name="O'rtacha ball")
    total_attempts = models.IntegerField(default=0, verbose_name="Urinishlar soni")
    efficiency_rate = models.FloatField(help_text="Samaradorlik ko'rsatkichi % da", verbose_name="Samaradorlik")

    def __str__(self):
        return f"Statistika: {self.topic.title}"

    class Meta:
        verbose_name = "Statistika"
        verbose_name_plural = "Statistikalar"


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    subject = models.CharField(max_length=200, verbose_name="Mavzu")
    message = models.TextField(verbose_name="Xabar matni")
    rating = models.IntegerField(default=5, verbose_name="Baholash (1-5)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.subject}"

    class Meta:
        verbose_name = "Fikr-mulohaza"
        verbose_name_plural = "Fikr-mulohazalar"