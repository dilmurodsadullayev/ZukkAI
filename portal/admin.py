from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.db.models import Count

from .models import (
    Profile,
    Topic,
    AITask,
    Submission,
    Analytics,
    Feedback,
    VideoLesson,
    Quiz,
    Question,
    QuizSubmission,
)


# ==============================
# ADMIN SITE CUSTOMIZATION
# ==============================

admin.site.site_header = "FSociety Admin Panel"
admin.site.site_title = "FSociety Admin"
admin.site.index_title = "Boshqaruv paneliga xush kelibsiz"


# ==============================
# PROFILE INLINE FOR USER
# ==============================

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    extra = 0
    readonly_fields = ("image_preview", "total_points")

    fieldsets = (
        ("Asosiy ma'lumotlar", {
            "fields": ("image", "image_preview", "phone_number", "school", "grade")
        }),
        ("Qo‘shimcha", {
            "fields": ("bio", "total_points")
        }),
    )

    @admin.display(description="Profil rasmi")
    def image_preview(self, obj):
        if obj and obj.image:
            try:
                return format_html(
                    '<img src="{}" width="90" height="90" '
                    'style="object-fit:cover; border-radius:50%; border:3px solid #2563eb;" />',
                    obj.image.url
                )
            except Exception:
                return "Rasm topilmadi"
        return "Rasm yo‘q"


class CustomUserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "profile_points",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "date_joined")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("-date_joined",)

    @admin.display(description="Jami ball")
    def profile_points(self, obj):
        try:
            points = obj.profile.total_points
            return format_html(
                '<span style="background:#16a34a; color:white; padding:4px 10px; '
                'border-radius:12px; font-weight:bold;">{} ball</span>',
                points
            )
        except Profile.DoesNotExist:
            return format_html(
                '<span style="background:#dc2626; color:white; padding:4px 10px; '
                'border-radius:12px;">Profil yo‘q</span>'
            )


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
        "user",
        "image_preview_small",
        "phone_number",
        "school",
        "grade",
        "total_points_badge",
    )
    list_filter = ("school", "grade")
    search_fields = (
        "user__username",
        "user__email",
        "phone_number",
        "school",
        "grade",
    )
    readonly_fields = ("image_preview",)
    list_select_related = ("user",)

    fieldsets = (
        ("Foydalanuvchi", {
            "fields": ("user",)
        }),
        ("Profil ma'lumotlari", {
            "fields": ("image", "image_preview", "phone_number", "school", "grade", "bio")
        }),
        ("Ball", {
            "fields": ("total_points",)
        }),
    )

    @admin.display(description="Rasm")
    def image_preview_small(self, obj):
        if obj.image:
            try:
                return format_html(
                    '<img src="{}" width="45" height="45" '
                    'style="object-fit:cover; border-radius:50%; border:2px solid #2563eb;" />',
                    obj.image.url
                )
            except Exception:
                return "Yo‘q"
        return "Yo‘q"

    @admin.display(description="Profil rasmi")
    def image_preview(self, obj):
        if obj.image:
            try:
                return format_html(
                    '<img src="{}" width="140" height="140" '
                    'style="object-fit:cover; border-radius:18px; border:3px solid #2563eb;" />',
                    obj.image.url
                )
            except Exception:
                return "Rasm topilmadi"
        return "Rasm yo‘q"

    @admin.display(description="Jami ball")
    def total_points_badge(self, obj):
        return format_html(
            '<span style="background:#0f766e; color:white; padding:5px 12px; '
            'border-radius:15px; font-weight:bold;">{} ball</span>',
            obj.total_points
        )


# ==============================
# TOPIC ADMIN
# ==============================

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "task_count",
        "video_count",
        "quiz_count",
        "created_at",
    )
    search_fields = ("title", "description")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
    date_hierarchy = "created_at"

    fieldsets = (
        ("Mavzu ma'lumotlari", {
            "fields": ("title", "description")
        }),
        ("Vaqt", {
            "fields": ("created_at",)
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            tasks_total=Count("tasks", distinct=True),
            videos_total=Count("videos", distinct=True),
            quizzes_total=Count("quizzes", distinct=True),
        )

    @admin.display(description="AI topshiriqlar")
    def task_count(self, obj):
        return format_html(
            '<span style="background:#7c3aed; color:white; padding:4px 10px; '
            'border-radius:12px;">{}</span>',
            obj.tasks_total
        )

    @admin.display(description="Videodarslar")
    def video_count(self, obj):
        return format_html(
            '<span style="background:#2563eb; color:white; padding:4px 10px; '
            'border-radius:12px;">{}</span>',
            obj.videos_total
        )

    @admin.display(description="Testlar")
    def quiz_count(self, obj):
        return format_html(
            '<span style="background:#ea580c; color:white; padding:4px 10px; '
            'border-radius:12px;">{}</span>',
            obj.quizzes_total
        )


# ==============================
# AI TASK ADMIN
# ==============================

class SubmissionInline(admin.TabularInline):
    model = Submission
    extra = 0
    readonly_fields = (
        "student",
        "student_answer",
        "ai_score",
        "ai_feedback",
        "submitted_at",
        "is_evaluated",
    )
    can_delete = False
    show_change_link = True


@admin.register(AITask)
class AITaskAdmin(admin.ModelAdmin):
    list_display = (
        "short_content",
        "topic",
        "level_badge",
        "created_by",
        "submission_count",
        "created_at",
    )
    list_filter = ("level", "topic", "created_at")
    search_fields = (
        "content",
        "correct_solution",
        "prompt_used",
        "topic__title",
        "created_by__username",
    )
    readonly_fields = ("created_at",)
    list_select_related = ("topic", "created_by")
    inlines = (SubmissionInline,)
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    fieldsets = (
        ("Asosiy", {
            "fields": ("topic", "level", "created_by")
        }),
        ("AI so‘rovi va topshiriq", {
            "fields": ("prompt_used", "content", "correct_solution")
        }),
        ("Vaqt", {
            "fields": ("created_at",)
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(submissions_total=Count("submissions", distinct=True))

    @admin.display(description="Topshiriq")
    def short_content(self, obj):
        return obj.content[:70] + "..." if len(obj.content) > 70 else obj.content

    @admin.display(description="Daraja")
    def level_badge(self, obj):
        colors = {
            "oson": "#16a34a",
            "o?rta": "#f59e0b",
            "murakkab": "#dc2626",
        }
        color = colors.get(obj.level, "#6b7280")
        return format_html(
            '<span style="background:{}; color:white; padding:5px 12px; '
            'border-radius:14px; font-weight:bold;">{}</span>',
            color,
            obj.get_level_display()
        )

    @admin.display(description="Javoblar soni")
    def submission_count(self, obj):
        return format_html(
            '<span style="background:#0891b2; color:white; padding:4px 10px; '
            'border-radius:12px;">{}</span>',
            obj.submissions_total
        )


# ==============================
# SUBMISSION ADMIN
# ==============================

@admin.action(description="Tanlangan javoblarni baholangan deb belgilash")
def mark_as_evaluated(modeladmin, request, queryset):
    queryset.update(is_evaluated=True)


@admin.action(description="Tanlangan javoblarni baholanmagan deb belgilash")
def mark_as_not_evaluated(modeladmin, request, queryset):
    queryset.update(is_evaluated=False)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "task_topic",
        "score_badge",
        "evaluated_badge",
        "submitted_at",
    )
    list_filter = ("is_evaluated", "submitted_at", "task__topic")
    search_fields = (
        "student__username",
        "student__email",
        "student_answer",
        "ai_feedback",
        "task__topic__title",
    )
    readonly_fields = ("submitted_at",)
    list_select_related = ("student", "task", "task__topic")
    actions = (mark_as_evaluated, mark_as_not_evaluated)
    date_hierarchy = "submitted_at"
    ordering = ("-submitted_at",)

    fieldsets = (
        ("O‘quvchi va topshiriq", {
            "fields": ("student", "task")
        }),
        ("Javob", {
            "fields": ("student_answer",)
        }),
        ("AI baholash", {
            "fields": ("ai_score", "ai_feedback", "is_evaluated")
        }),
        ("Vaqt", {
            "fields": ("submitted_at",)
        }),
    )

    @admin.display(description="Mavzu")
    def task_topic(self, obj):
        return obj.task.topic.title

    @admin.display(description="Ball")
    def score_badge(self, obj):
        if obj.ai_score is None:
            return format_html(
                '<span style="background:#6b7280; color:white; padding:5px 12px; '
                'border-radius:15px;">Baholanmagan</span>'
            )

        if obj.ai_score >= 80:
            color = "#16a34a"
        elif obj.ai_score >= 50:
            color = "#f59e0b"
        else:
            color = "#dc2626"

        return format_html(
            '<span style="background:{}; color:white; padding:5px 12px; '
            'border-radius:15px; font-weight:bold;">{} ball</span>',
            color,
            obj.ai_score
        )

    @admin.display(description="Holat")
    def evaluated_badge(self, obj):
        if obj.is_evaluated:
            return format_html(
                '<span style="background:#16a34a; color:white; padding:5px 12px; '
                'border-radius:15px;">Baholangan</span>'
            )
        return format_html(
            '<span style="background:#dc2626; color:white; padding:5px 12px; '
            'border-radius:15px;">Kutilmoqda</span>'
        )


# ==============================
# ANALYTICS ADMIN
# ==============================

@admin.register(Analytics)
class AnalyticsAdmin(admin.ModelAdmin):
    list_display = (
        "topic",
        "average_score_badge",
        "total_attempts",
        "efficiency_badge",
    )
    list_filter = ("topic",)
    search_fields = ("topic__title",)
    list_select_related = ("topic",)

    fieldsets = (
        ("Mavzu", {
            "fields": ("topic",)
        }),
        ("Statistika", {
            "fields": ("average_score", "total_attempts", "efficiency_rate")
        }),
    )

    @admin.display(description="O‘rtacha ball")
    def average_score_badge(self, obj):
        return format_html(
            '<span style="background:#2563eb; color:white; padding:5px 12px; '
            'border-radius:15px; font-weight:bold;">{:.1f}</span>',
            obj.average_score
        )

    @admin.display(description="Samaradorlik")
    def efficiency_badge(self, obj):
        if obj.efficiency_rate >= 80:
            color = "#16a34a"
        elif obj.efficiency_rate >= 50:
            color = "#f59e0b"
        else:
            color = "#dc2626"

        return format_html(
            '<span style="background:{}; color:white; padding:5px 12px; '
            'border-radius:15px; font-weight:bold;">{}%</span>',
            color,
            obj.efficiency_rate
        )


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
    list_filter = ("rating", "created_at")
    search_fields = (
        "user__username",
        "user__email",
        "subject",
        "message",
    )
    readonly_fields = ("created_at",)
    list_select_related = ("user",)
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    fieldsets = (
        ("Foydalanuvchi", {
            "fields": ("user",)
        }),
        ("Xabar", {
            "fields": ("subject", "message", "rating")
        }),
        ("Vaqt", {
            "fields": ("created_at",)
        }),
    )

    @admin.display(description="Reyting")
    def rating_stars(self, obj):
        rating = max(1, min(obj.rating, 5))
        stars = "★" * rating + "☆" * (5 - rating)
        return format_html(
            '<span style="color:#f59e0b; font-size:18px; font-weight:bold;">{}</span>',
            stars
        )


# ==============================
# VIDEO LESSON ADMIN
# ==============================

@admin.register(VideoLesson)
class VideoLessonAdmin(admin.ModelAdmin):
    list_display = (
        "thumbnail_preview_small",
        "title",
        "topic",
        "duration",
        "video_link",
        "created_at",
    )
    list_filter = ("topic", "created_at")
    search_fields = ("title", "description", "video_url", "topic__title")
    readonly_fields = ("thumbnail_preview", "created_at")
    list_select_related = ("topic",)
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    fieldsets = (
        ("Mavzu va sarlavha", {
            "fields": ("topic", "title", "description")
        }),
        ("Video", {
            "fields": ("video_url", "duration")
        }),
        ("Muqova", {
            "fields": ("thumbnail", "thumbnail_preview")
        }),
        ("Vaqt", {
            "fields": ("created_at",)
        }),
    )

    @admin.display(description="Muqova")
    def thumbnail_preview_small(self, obj):
        if obj.thumbnail:
            try:
                return format_html(
                    '<img src="{}" width="70" height="45" '
                    'style="object-fit:cover; border-radius:8px; border:2px solid #2563eb;" />',
                    obj.thumbnail.url
                )
            except Exception:
                return "Yo‘q"
        return "Yo‘q"

    @admin.display(description="Video muqovasi")
    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            try:
                return format_html(
                    '<img src="{}" width="240" height="140" '
                    'style="object-fit:cover; border-radius:14px; border:3px solid #2563eb;" />',
                    obj.thumbnail.url
                )
            except Exception:
                return "Rasm topilmadi"
        return "Rasm yo‘q"

    @admin.display(description="Havola")
    def video_link(self, obj):
        if obj.video_url:
            return format_html(
                '<a href="{}" target="_blank" '
                'style="background:#dc2626; color:white; padding:5px 12px; '
                'border-radius:15px; text-decoration:none;">YouTube</a>',
                obj.video_url
            )
        return "Yo‘q"


# ==============================
# QUIZ / QUESTION ADMIN
# ==============================

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = (
        "text",
        "option_a",
        "option_b",
        "option_c",
        "option_d",
        "correct_answer",
    )
    show_change_link = True


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "topic",
        "question_count",
        "created_at",
    )
    list_filter = ("topic", "created_at")
    search_fields = ("title", "description", "topic__title")
    readonly_fields = ("created_at",)
    list_select_related = ("topic",)
    inlines = (QuestionInline,)
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    fieldsets = (
        ("Test ma'lumotlari", {
            "fields": ("topic", "title", "description")
        }),
        ("Vaqt", {
            "fields": ("created_at",)
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(questions_total=Count("questions", distinct=True))

    @admin.display(description="Savollar soni")
    def question_count(self, obj):
        return format_html(
            '<span style="background:#ea580c; color:white; padding:5px 12px; '
            'border-radius:15px; font-weight:bold;">{} ta</span>',
            obj.questions_total
        )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "short_question",
        "quiz",
        "correct_answer_badge",
    )
    list_filter = ("quiz", "correct_answer")
    search_fields = (
        "text",
        "option_a",
        "option_b",
        "option_c",
        "option_d",
        "quiz__title",
        "quiz__topic__title",
    )
    list_select_related = ("quiz", "quiz__topic")
    ordering = ("quiz", "id")

    fieldsets = (
        ("Test", {
            "fields": ("quiz",)
        }),
        ("Savol", {
            "fields": ("text",)
        }),
        ("Variantlar", {
            "fields": ("option_a", "option_b", "option_c", "option_d")
        }),
        ("To‘g‘ri javob", {
            "fields": ("correct_answer",)
        }),
    )

    @admin.display(description="Savol")
    def short_question(self, obj):
        return obj.text[:80] + "..." if len(obj.text) > 80 else obj.text

    @admin.display(description="To‘g‘ri javob")
    def correct_answer_badge(self, obj):
        return format_html(
            '<span style="background:#16a34a; color:white; padding:5px 12px; '
            'border-radius:15px; font-weight:bold;">{}</span>',
            obj.correct_answer
        )


# ==============================
# QUIZ SUBMISSION ADMIN
# ==============================

@admin.register(QuizSubmission)
class QuizSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "quiz",
        "score_result",
        "percentage_badge",
        "completed_at",
    )
    list_filter = ("quiz", "completed_at")
    search_fields = (
        "student__username",
        "student__email",
        "quiz__title",
        "quiz__topic__title",
    )
    readonly_fields = ("percentage_view", "completed_at")
    list_select_related = ("student", "quiz", "quiz__topic")
    date_hierarchy = "completed_at"
    ordering = ("-completed_at",)

    fieldsets = (
        ("O‘quvchi va test", {
            "fields": ("student", "quiz")
        }),
        ("Natija", {
            "fields": ("score", "total_questions", "percentage_view")
        }),
        ("Vaqt", {
            "fields": ("completed_at",)
        }),
    )

    @admin.display(description="Natija")
    def score_result(self, obj):
        return format_html(
            '<span style="background:#2563eb; color:white; padding:5px 12px; '
            'border-radius:15px; font-weight:bold;">{}/{}</span>',
            obj.score,
            obj.total_questions
        )

    @admin.display(description="Foiz")
    def percentage_badge(self, obj):
        percent = obj.percentage

        if percent >= 80:
            color = "#16a34a"
        elif percent >= 50:
            color = "#f59e0b"
        else:
            color = "#dc2626"

        return format_html(
            '<span style="background:{}; color:white; padding:5px 12px; '
            'border-radius:15px; font-weight:bold;">{:.1f}%</span>',
            color,
            percent
        )

    @admin.display(description="Foiz ko‘rinishi")
    def percentage_view(self, obj):
        return self.percentage_badge(obj)