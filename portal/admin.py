from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import Profile, Topic, AITask, Submission, Analytics, Feedback


# ==============================
# PROFILE INLINE
# ==============================
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    extra = 0

    fields = (
        "image_preview",
        "image",
        "phone_number",
        "school",
        "grade",
        "bio",
        "total_points",
    )

    readonly_fields = ("image_preview", "total_points")

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:80px;height:80px;border-radius:50%;object-fit:cover;border:3px solid #4f46e5;" />',
                obj.image.url
            )
        return "Rasm yo'q"

    image_preview.short_description = "Profil rasmi"


# ==============================
# USER ADMIN
# ==============================
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "date_joined",
    )

    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "date_joined",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    ordering = ("-date_joined",)


try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, CustomUserAdmin)


# ==============================
# PROFILE ADMIN
# ==============================
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "image_preview",
        "user",
        "phone_number",
        "school",
        "grade",
        "total_points",
    )

    list_filter = (
        "school",
        "grade",
    )

    search_fields = (
        "user__username",
        "user__email",
        "phone_number",
        "school",
        "grade",
    )

    readonly_fields = (
        "image_preview",
        "total_points",
    )

    fieldsets = (
        ("Foydalanuvchi", {
            "fields": (
                "user",
            )
        }),
        ("Profil ma'lumotlari", {
            "fields": (
                "image_preview",
                "image",
                "phone_number",
                "school",
                "grade",
                "bio",
            )
        }),
        ("Ball statistikasi", {
            "fields": (
                "total_points",
            )
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:60px;height:60px;border-radius:50%;object-fit:cover;border:2px solid #6366f1;" />',
                obj.image.url
            )
        return "Rasm yo'q"

    image_preview.short_description = "Rasm"


# ==============================
# TOPIC ADMIN
# ==============================
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "tasks_count",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    fieldsets = (
        ("Mavzu ma'lumotlari", {
            "fields": (
                "title",
                "description",
            )
        }),
        ("Vaqt", {
            "fields": (
                "created_at",
            )
        }),
    )

    def tasks_count(self, obj):
        return obj.tasks.count()

    tasks_count.short_description = "Topshiriqlar soni"


# ==============================
# SUBMISSION INLINE
# ==============================
class SubmissionInline(admin.TabularInline):
    model = Submission
    extra = 0

    fields = (
        "student",
        "ai_score",
        "is_evaluated",
        "submitted_at",
    )

    readonly_fields = (
        "student",
        "ai_score",
        "is_evaluated",
        "submitted_at",
    )

    can_delete = False
    show_change_link = True


# ==============================
# AI TASK ADMIN
# ==============================
@admin.register(AITask)
class AITaskAdmin(admin.ModelAdmin):
    list_display = (
        "topic",
        "level_badge",
        "created_by",
        "submissions_count",
        "created_at",
    )

    list_filter = (
        "level",
        "topic",
        "created_at",
    )

    search_fields = (
        "topic__title",
        "prompt_used",
        "content",
        "correct_solution",
        "created_by__username",
    )

    readonly_fields = (
        "created_at",
    )

    autocomplete_fields = (
        "topic",
        "created_by",
    )

    ordering = (
        "-created_at",
    )

    inlines = (
        SubmissionInline,
    )

    fieldsets = (
        ("Topshiriq sozlamalari", {
            "fields": (
                "topic",
                "level",
                "created_by",
            )
        }),
        ("AI so'rov va natija", {
            "fields": (
                "prompt_used",
                "content",
                "correct_solution",
            )
        }),
        ("Vaqt", {
            "fields": (
                "created_at",
            )
        }),
    )

    def level_badge(self, obj):
        colors = {
            "oson": "#22c55e",
            "o?rta": "#f59e0b",
            "murakkab": "#ef4444",
        }

        color = colors.get(obj.level, "#6366f1")

        return format_html(
            '<span style="background:{};color:white;padding:5px 12px;border-radius:999px;font-weight:700;">{}</span>',
            color,
            obj.get_level_display()
        )

    level_badge.short_description = "Daraja"

    def submissions_count(self, obj):
        return obj.submissions.count()

    submissions_count.short_description = "Javoblar soni"

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


# ==============================
# SUBMISSION ADMIN
# ==============================
@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "task_topic",
        "score_badge",
        "is_evaluated",
        "submitted_at",
    )

    list_filter = (
        "is_evaluated",
        "task__topic",
        "submitted_at",
    )

    search_fields = (
        "student__username",
        "student__email",
        "task__topic__title",
        "student_answer",
        "ai_feedback",
    )

    readonly_fields = (
        "submitted_at",
    )

    autocomplete_fields = (
        "task",
        "student",
    )

    ordering = (
        "-submitted_at",
    )

    fieldsets = (
        ("O'quvchi va topshiriq", {
            "fields": (
                "task",
                "student",
            )
        }),
        ("O'quvchi javobi", {
            "fields": (
                "student_answer",
            )
        }),
        ("AI baholash", {
            "fields": (
                "ai_score",
                "ai_feedback",
                "is_evaluated",
            )
        }),
        ("Vaqt", {
            "fields": (
                "submitted_at",
            )
        }),
    )

    def task_topic(self, obj):
        return obj.task.topic.title

    task_topic.short_description = "Mavzu"

    def score_badge(self, obj):
        if obj.ai_score is None:
            return format_html(
                '<span style="background:#e5e7eb;color:#374151;padding:5px 12px;border-radius:999px;font-weight:700;">Baholanmagan</span>'
            )

        if obj.ai_score >= 80:
            color = "#22c55e"
        elif obj.ai_score >= 50:
            color = "#f59e0b"
        else:
            color = "#ef4444"

        return format_html(
            '<span style="background:{};color:white;padding:5px 12px;border-radius:999px;font-weight:700;">{} ball</span>',
            color,
            obj.ai_score
        )

    score_badge.short_description = "AI ball"


# ==============================
# ANALYTICS ADMIN
# ==============================
@admin.register(Analytics)
class AnalyticsAdmin(admin.ModelAdmin):
    list_display = (
        "topic",
        "average_score",
        "total_attempts",
        "efficiency_badge",
    )

    list_filter = (
        "topic",
    )

    search_fields = (
        "topic__title",
    )

    autocomplete_fields = (
        "topic",
    )

    fieldsets = (
        ("Mavzu", {
            "fields": (
                "topic",
            )
        }),
        ("Natijalar", {
            "fields": (
                "average_score",
                "total_attempts",
                "efficiency_rate",
            )
        }),
    )

    def efficiency_badge(self, obj):
        if obj.efficiency_rate >= 80:
            color = "#22c55e"
        elif obj.efficiency_rate >= 50:
            color = "#f59e0b"
        else:
            color = "#ef4444"

        return format_html(
            '<span style="background:{};color:white;padding:5px 12px;border-radius:999px;font-weight:700;">{}%</span>',
            color,
            obj.efficiency_rate
        )

    efficiency_badge.short_description = "Samaradorlik"


# ==============================
# FEEDBACK ADMIN
# ==============================
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "subject",
        "rating_stars",
        "created_at",
    )

    list_filter = (
        "rating",
        "created_at",
    )

    search_fields = (
        "user__username",
        "subject",
        "message",
    )

    readonly_fields = (
        "created_at",
    )

    autocomplete_fields = (
        "user",
    )

    ordering = (
        "-created_at",
    )

    fieldsets = (
        ("Foydalanuvchi", {
            "fields": (
                "user",
            )
        }),
        ("Fikr-mulohaza", {
            "fields": (
                "subject",
                "message",
                "rating",
            )
        }),
        ("Vaqt", {
            "fields": (
                "created_at",
            )
        }),
    )

    def rating_stars(self, obj):
        stars = "★" * obj.rating + "☆" * (5 - obj.rating)

        return format_html(
            '<span style="color:#f59e0b;font-size:16px;font-weight:700;">{}</span>',
            stars
        )

    rating_stars.short_description = "Reyting"


# ==============================
# ADMIN PANEL NOMLARI
# ==============================
admin.site.site_header = "EduAI Admin Panel"
admin.site.site_title = "EduAI Admin"
admin.site.index_title = "EduAI boshqaruv paneli"