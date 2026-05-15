from portal.models import Topic, Quiz, Question


# 1. Mavzu yaratamiz yoki bor bo'lsa olib kelamiz
topic, created = Topic.objects.get_or_create(
    title="Informatika asoslari",
    defaults={
        "description": "Informatika faniga oid asosiy tushunchalar, kompyuter, internet va dasturlash bo'yicha testlar."
    }
)

if created:
    print("✅ Yangi mavzu yaratildi:", topic.title)
else:
    print("ℹ️ Mavzu oldin bor ekan:", topic.title)


# 2. Quiz yaratamiz yoki bor bo'lsa olib kelamiz
quiz, created = Quiz.objects.get_or_create(
    topic=topic,
    title="Informatika asoslari bo'yicha 10 ta test",
    defaults={
        "description": "Ushbu test informatika fanining boshlang'ich tushunchalarini tekshirish uchun tuzilgan."
    }
)

if created:
    print("✅ Yangi quiz yaratildi:", quiz.title)
else:
    print("ℹ️ Quiz oldin bor ekan:", quiz.title)


# 3. Eski savollarni o'chirib, qaytadan toza qo'shamiz
quiz.questions.all().delete()


questions = [
    {
        "text": "Kompyuterning asosiy vazifasi nima?",
        "option_a": "Faqat o'yin o'ynash",
        "option_b": "Ma'lumotlarni qayta ishlash",
        "option_c": "Faqat rasm chizish",
        "option_d": "Faqat internetga kirish",
        "correct_answer": "B",
    },
    {
        "text": "CPU nimani anglatadi?",
        "option_a": "Markaziy protsessor",
        "option_b": "Doimiy xotira",
        "option_c": "Monitor turi",
        "option_d": "Klaviatura qurilmasi",
        "correct_answer": "A",
    },
    {
        "text": "RAM qanday xotira hisoblanadi?",
        "option_a": "Doimiy xotira",
        "option_b": "Tashqi xotira",
        "option_c": "Tezkor xotira",
        "option_d": "Faqat video xotira",
        "correct_answer": "C",
    },
    {
        "text": "Operatsion tizimga qaysi biri misol bo'ladi?",
        "option_a": "Google Chrome",
        "option_b": "Microsoft Word",
        "option_c": "Windows",
        "option_d": "Telegram",
        "correct_answer": "C",
    },
    {
        "text": "Internet nima?",
        "option_a": "Faqat bitta kompyuter",
        "option_b": "Global kompyuter tarmog'i",
        "option_c": "Faqat rasm ko'rish dasturi",
        "option_d": "Printer turi",
        "correct_answer": "B",
    },
    {
        "text": "Brauzer nima uchun ishlatiladi?",
        "option_a": "Veb sahifalarni ko'rish uchun",
        "option_b": "Kompyuterni yoqish uchun",
        "option_c": "Monitorni sozlash uchun",
        "option_d": "Klaviaturani almashtirish uchun",
        "correct_answer": "A",
    },
    {
        "text": "Algoritm nima?",
        "option_a": "Tasodifiy matn",
        "option_b": "Kompyuter qurilmasi",
        "option_c": "Muammoni yechish uchun ketma-ket amallar tartibi",
        "option_d": "Faqat internet manzili",
        "correct_answer": "C",
    },
    {
        "text": "Python nima?",
        "option_a": "Dasturlash tili",
        "option_b": "Operatsion tizim",
        "option_c": "Printer turi",
        "option_d": "Monitor dasturi",
        "correct_answer": "A",
    },
    {
        "text": "HTML nima uchun ishlatiladi?",
        "option_a": "Ma'lumotlar bazasini boshqarish uchun",
        "option_b": "Veb sahifa tuzilmasini yaratish uchun",
        "option_c": "Kompyuter virusini o'chirish uchun",
        "option_d": "Internet tezligini oshirish uchun",
        "correct_answer": "B",
    },
    {
        "text": "Fayl kengaytmasi nimani bildiradi?",
        "option_a": "Fayl egasining ismini",
        "option_b": "Fayl hajmini faqat",
        "option_c": "Fayl turini",
        "option_d": "Kompyuter modelini",
        "correct_answer": "C",
    },
]


# 4. ORM orqali Question obyektlarini yaratamiz
question_objects = []

for item in questions:
    question_objects.append(
        Question(
            quiz=quiz,
            text=item["text"],
            option_a=item["option_a"],
            option_b=item["option_b"],
            option_c=item["option_c"],
            option_d=item["option_d"],
            correct_answer=item["correct_answer"],
        )
    )

Question.objects.bulk_create(question_objects)

print("✅ 10 ta test savol muvaffaqiyatli qo'shildi!")
print("📌 Quiz:", quiz.title)
print("📌 Mavzu:", topic.title)
print("📌 Savollar soni:", quiz.questions.count())