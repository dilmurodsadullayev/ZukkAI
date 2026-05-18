# -*- coding: utf-8 -*-

import os
import django

# Agar project settings noming boshqacha bo'lsa, config.settings ni almashtirasan
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.db import transaction
from portal.models import Topic, Quiz, Question


TOPICS = [
    {
        "title": "Algoritmlash asoslari",
        "description": "Algoritm tushunchasi, blok-sxemalar, masalalarni bosqichma-bosqich yechish va dasturlashga tayyorlash asoslari o‘rganiladi.",
    },
    {
        "title": "Python dasturlash tili",
        "description": "Python dasturlash tilining sintaksisi, o‘zgaruvchilar, shart operatorlari, sikllar, funksiyalar va amaliy dasturlar yaratish o‘rganiladi.",
    },
    {
        "title": "Ma’lumotlar bazasi (SQL)",
        "description": "Ma’lumotlar bazasi tushunchasi, jadvallar, SQL so‘rovlari, SELECT, INSERT, UPDATE, DELETE va bog‘langan jadvallar bilan ishlash o‘rganiladi.",
    },
    {
        "title": "Ob’ektga yo‘naltirilgan dasturlash",
        "description": "Class, object, meros olish, inkapsulyatsiya, polimorfizm va real loyihalarda OOP yondashuvlaridan foydalanish o‘rganiladi.",
    },
    {
        "title": "Kompyuter tarmoqlari",
        "description": "Kompyuter tarmoqlari, IP manzillar, DNS, HTTP/HTTPS, router, server va mijoz o‘rtasidagi aloqa asoslari o‘rganiladi.",
    },
    {
        "title": "Sun’iy intellekt va mashinaviy o‘rganish",
        "description": "Sun’iy intellekt tushunchasi, mashinaviy o‘rganish asoslari, ma’lumotlar bilan ishlash, model o‘qitish va bashorat qilish jarayonlari o‘rganiladi.",
    },
    {
        "title": "Web-dasturlash (Frontend)",
        "description": "HTML, CSS, JavaScript, sahifa tuzilmasi, dizayn, responsiv interfeys va foydalanuvchi bilan ishlovchi web sahifalar yaratish o‘rganiladi.",
    },
    {
        "title": "Axborot xavfsizligi",
        "description": "Axborotlarni himoyalash, parollar xavfsizligi, shifrlash, tarmoq xavfsizligi, zararli dasturlar va himoya usullari o‘rganiladi.",
    },
    {
        "title": "Kompyuter grafikasi",
        "description": "Grafik obyektlar, ranglar, tasvirlar bilan ishlash, 2D/3D grafika asoslari va kompyuter grafikasi dasturlari haqida bilim beriladi.",
    },
    {
        "title": "Operatsion tizimlar",
        "description": "Operatsion tizim tushunchasi, fayl tizimi, jarayonlar, xotira boshqaruvi, Linux va Windows tizimlarining asosiy ishlash prinsiplari o‘rganiladi.",
    },
    {
        "title": "10-sinf informatika",
        "description": "10-sinf informatika fanida algoritmlash, dasturlash asoslari, ma’lumotlar bilan ishlash, kompyuter tizimlari, internet texnologiyalari va axborot xavfsizligi bo‘yicha asosiy bilimlar o‘rganiladi.",
    },
]


QUIZ_BANK = {
    "Algoritmlash asoslari": [
        ("Algoritm nima?", "Kompyuter qurilmasi", "Muammoni yechish uchun ketma-ket amallar tartibi", "Internet manzili", "Fayl turi", "B"),
        ("Algoritmning asosiy xossalaridan biri qaysi?", "Noaniqlik", "Cheksizlik", "Aniqlik", "Tasodifiylik", "C"),
        ("Blok-sxemada boshlash va tugatish belgisi qanday shaklda bo‘ladi?", "To‘rtburchak", "Romb", "Oval", "Uchburchak", "C"),
        ("Shart tekshirish blok-sxemada qaysi shakl bilan ifodalanadi?", "Romb", "Aylana", "To‘g‘ri chiziq", "Oval", "A"),
        ("Chiziqli algoritm nima?", "Amallar ketma-ket bajariladigan algoritm", "Faqat shartli algoritm", "Faqat sikl", "Faqat grafik", "A"),
        ("Tarmoqlanuvchi algoritmda nima ishlatiladi?", "Faqat print", "Shart", "Faqat fayl", "Faqat jadval", "B"),
        ("Takrorlanuvchi algoritm nima?", "Amallar bir necha marta bajariladigan algoritm", "Faqat bitta amal", "Faqat matn yozish", "Faqat rasm chizish", "A"),
        ("Algoritm ijrochisi kim yoki nima bo‘lishi mumkin?", "Faqat inson", "Faqat kompyuter", "Buyruqlarni bajara oladigan obyekt", "Faqat printer", "C"),
        ("Psevdokod nima?", "Dasturga o‘xshash soddalashtirilgan yozuv", "Virus turi", "Operatsion tizim", "Monitor sozlamasi", "A"),
        ("Algoritm natijaviylik xossasi nimani bildiradi?", "Algoritm oxirida natija berishi kerak", "Algoritm cheksiz davom etishi kerak", "Algoritm faqat rasm bo‘lishi kerak", "Algoritm internetga ulanishi kerak", "A"),
    ],

    "Python dasturlash tili": [
        ("Python qanday til hisoblanadi?", "Dasturlash tili", "Operatsion tizim", "Brauzer", "Antivirus", "A"),
        ("Python’da ekranga ma’lumot chiqarish uchun qaysi funksiya ishlatiladi?", "input()", "print()", "len()", "type()", "B"),
        ("Python’da foydalanuvchidan ma’lumot olish uchun qaysi funksiya ishlatiladi?", "print()", "input()", "range()", "str()", "B"),
        ("Python’da butun son turi qanday nomlanadi?", "str", "float", "int", "bool", "C"),
        ("Python’da matnli ma’lumot turi qaysi?", "str", "int", "float", "list", "A"),
        ("Python’da shart operatori qaysi kalit so‘z bilan boshlanadi?", "for", "while", "if", "def", "C"),
        ("Python’da sikl yaratish uchun qaysi operatorlardan foydalaniladi?", "if va else", "for va while", "try va except", "class va object", "B"),
        ("Python’da funksiya yaratish uchun qaysi kalit so‘z ishlatiladi?", "func", "def", "function", "return", "B"),
        ("Python’da ro‘yxat qanday belgilar bilan yoziladi?", "()", "{}", "[]", "<>", "C"),
        ("Python’da kommentariya qaysi belgi bilan yoziladi?", "#", "//", "/* */", "@", "A"),
    ],

    "Ma’lumotlar bazasi (SQL)": [
        ("Ma’lumotlar bazasi nima?", "Ma’lumotlarni tartibli saqlash tizimi", "Faqat rasm chizish dasturi", "Operatsion tizim", "Brauzer", "A"),
        ("SQL nimaga xizmat qiladi?", "Ma’lumotlar bazasi bilan ishlashga", "Rasm tahrirlashga", "Kompyuterni o‘chirishga", "Video montajga", "A"),
        ("SELECT buyrug‘i nima qiladi?", "Ma’lumot qo‘shadi", "Ma’lumotlarni tanlab ko‘rsatadi", "Jadvalni o‘chiradi", "Parol o‘zgartiradi", "B"),
        ("INSERT buyrug‘i nima uchun ishlatiladi?", "Ma’lumot qo‘shish uchun", "Ma’lumot o‘chirish uchun", "Jadvalni ko‘rish uchun", "Bazani yopish uchun", "A"),
        ("UPDATE buyrug‘i nima qiladi?", "Ma’lumotni yangilaydi", "Kompyuterni yangilaydi", "Internetni yoqadi", "Faylni siqadi", "A"),
        ("DELETE buyrug‘i nima qiladi?", "Ma’lumotni o‘chiradi", "Ma’lumotni chiqaradi", "Ma’lumotni nusxalaydi", "Jadval chizadi", "A"),
        ("Jadvaldagi ustun nima deb ataladi?", "Row", "Column", "Database", "Server", "B"),
        ("Jadvaldagi satr nima deb ataladi?", "Record", "Column", "Field", "Query", "A"),
        ("PRIMARY KEY nimani bildiradi?", "Jadvaldagi noyob identifikator", "Oddiy matn", "Parol turi", "Brauzer nomi", "A"),
        ("WHERE sharti nima uchun ishlatiladi?", "Ma’lumotlarni shart asosida filtrlash uchun", "Jadval rangini o‘zgartirish uchun", "Baza yaratish uchun", "Kompyuter tezligini oshirish uchun", "A"),
    ],

    "Ob’ektga yo‘naltirilgan dasturlash": [
        ("OOP nimani anglatadi?", "Ob’ektga yo‘naltirilgan dasturlash", "Operatsion tizim protokoli", "Online ochiq platforma", "Oddiy o‘yin paketi", "A"),
        ("Class nima?", "Obyektlar yaratish uchun qolip", "Faqat son", "Fayl kengaytmasi", "Internet tarmog‘i", "A"),
        ("Object nima?", "Class asosida yaratilgan nusxa", "Faqat jadval", "Brauzer", "Printer", "A"),
        ("Inkapsulyatsiya nima?", "Ma’lumot va metodlarni bir obyekt ichida birlashtirish", "Internetga ulanish", "Faylni o‘chirish", "Matnni tarjima qilish", "A"),
        ("Meros olish nima?", "Bir class boshqa class xususiyatlarini olishi", "Fayl ko‘chirish", "Xotirani tozalash", "Rasmni ochish", "A"),
        ("Polimorfizm nima?", "Bir xil nomdagi metodlarning turlicha ishlashi", "Faqat bitta amal bajarish", "Faqat matn chiqarish", "Jadval yaratish", "A"),
        ("Constructor odatda nima uchun kerak?", "Obyekt yaratilganda boshlang‘ich qiymat berish uchun", "Kompyuterni o‘chirish uchun", "Bazani tozalash uchun", "Internetni ulash uchun", "A"),
        ("Python’da class yaratish uchun qaysi kalit so‘z ishlatiladi?", "def", "class", "object", "new", "B"),
        ("Metod nima?", "Class ichidagi funksiya", "Faqat o‘zgaruvchi", "Fayl turi", "Server nomi", "A"),
        ("self kalit so‘zi nimani bildiradi?", "Joriy obyektga murojaatni", "Kompyuter xotirasini", "Internet manzilini", "Operatsion tizimni", "A"),
    ],

    "Kompyuter tarmoqlari": [
        ("Kompyuter tarmog‘i nima?", "Kompyuterlarning o‘zaro bog‘lanishi", "Faqat bitta monitor", "Matn muharriri", "Fayl kengaytmasi", "A"),
        ("LAN nima?", "Mahalliy tarmoq", "Global tarmoq", "Video karta", "Dasturlash tili", "A"),
        ("WAN nima?", "Keng hududli tarmoq", "Klaviatura turi", "Xotira turi", "Printer dasturi", "A"),
        ("IP manzil nima?", "Tarmoqdagi qurilma manzili", "Fayl nomi", "Rasm formati", "Parol turi", "A"),
        ("DNS nima vazifa bajaradi?", "Domen nomini IP manzilga aylantiradi", "Kompyuterni sovitadi", "Rasm yaratadi", "Fayl siqadi", "A"),
        ("HTTP nima?", "Veb ma’lumot almashish protokoli", "Grafik dastur", "Xotira turi", "Operatsion tizim", "A"),
        ("HTTPS nimasi bilan xavfsizroq?", "Ma’lumotlarni shifrlab uzatadi", "Faqat tezroq ishlaydi", "Faqat rasm ko‘rsatadi", "Faqat offline ishlaydi", "A"),
        ("Router nima qiladi?", "Tarmoq trafikini yo‘naltiradi", "Matn yozadi", "Faylni o‘chiradi", "Monitorni yoqadi", "A"),
        ("Server nima?", "Mijozlarga xizmat ko‘rsatuvchi kompyuter yoki dastur", "Faqat klaviatura", "Rasm turi", "O‘yin turi", "A"),
        ("Client nima?", "Server xizmatidan foydalanuvchi qurilma yoki dastur", "Faqat printer", "Antivirus", "BIOS turi", "A"),
    ],

    "Sun’iy intellekt va mashinaviy o‘rganish": [
        ("Sun’iy intellekt nima?", "Kompyuterning aqlli vazifalarni bajarish texnologiyasi", "Faqat printer sozlamasi", "Fayl kengaytmasi", "Monitor turi", "A"),
        ("Mashinaviy o‘rganish nima?", "Ma’lumotlar asosida o‘rganadigan algoritmlar yo‘nalishi", "Faqat qo‘lda yozish", "Internetni o‘chirish", "Kompyuter yig‘ish", "A"),
        ("Dataset nima?", "Model o‘qitish uchun ma’lumotlar to‘plami", "Faylni o‘chirish dasturi", "Monitor sozlamasi", "Router turi", "A"),
        ("Model nima?", "Ma’lumotlardan o‘rgangan matematik tuzilma", "Faqat rasm", "Fayl nomi", "Parol", "A"),
        ("Training nima?", "Modelni ma’lumotlar asosida o‘qitish", "Kompyuterni formatlash", "Faylni siqish", "Brauzerni yopish", "A"),
        ("Prediction nima?", "Model tomonidan bashorat qilish", "Matnni o‘chirish", "Tarmoq uzilishi", "Printer sozlamasi", "A"),
        ("Classification vazifasi nima?", "Ma’lumotni sinflarga ajratish", "Faylni nusxalash", "Monitorni sozlash", "Bazani yopish", "A"),
        ("Regression vazifasi nima?", "Sonli qiymatni bashorat qilish", "Faqat rasm chizish", "Parol almashtirish", "Tizimni o‘chirish", "A"),
        ("Overfitting nima?", "Model o‘quv ma’lumotiga haddan tashqari moslashib qolishi", "Internet tezlashishi", "Fayl ochilmasligi", "Monitor o‘chishi", "A"),
        ("AI tavsiya tizimi nimaga xizmat qiladi?", "Foydalanuvchiga mos tavsiyalar berishga", "Kompyuterni tozalashga", "Faqat musiqa eshitishga", "Kabel ulashga", "A"),
    ],

    "Web-dasturlash (Frontend)": [
        ("Frontend nima?", "Foydalanuvchi ko‘radigan web qism", "Serverdagi baza", "Operatsion tizim", "Router", "A"),
        ("HTML nima uchun ishlatiladi?", "Veb sahifa tuzilmasini yaratish uchun", "Dizayn rangini avtomatik tanlash uchun", "Ma’lumotlar bazasi uchun", "Serverni boshqarish uchun", "A"),
        ("CSS nima uchun kerak?", "Veb sahifani bezash uchun", "Baza yaratish uchun", "Kompyuterni formatlash uchun", "Faylni shifrlash uchun", "A"),
        ("JavaScript nima qiladi?", "Veb sahifaga interaktivlik qo‘shadi", "Faqat rasm saqlaydi", "Internet kabelini ulaydi", "BIOS sozlaydi", "A"),
        ("Responsiv dizayn nima?", "Sahifaning turli ekranlarga moslashishi", "Faqat katta ekranda ishlashi", "Faqat qora rang", "Faylni o‘chirish", "A"),
        ("HTML’da havola yaratish uchun qaysi teg ishlatiladi?", "<a>", "<p>", "<div>", "<img>", "A"),
        ("HTML’da rasm chiqarish uchun qaysi teg ishlatiladi?", "<img>", "<link>", "<table>", "<script>", "A"),
        ("CSS’da rang berish uchun qaysi xossa ishlatiladi?", "color", "size", "print", "select", "A"),
        ("React nima?", "Frontend kutubxonasi", "Ma’lumotlar bazasi", "Operatsion tizim", "Router protokoli", "A"),
        ("API frontend uchun nima beradi?", "Backend bilan ma’lumot almashish imkonini", "Monitorni tozalashni", "Faylni siqishni", "Kompyuterni o‘chirishni", "A"),
    ],

    "Axborot xavfsizligi": [
        ("Axborot xavfsizligi nima?", "Ma’lumotlarni himoya qilish sohasi", "Faqat rasm yaratish", "Kompyuter o‘yini", "Matn bezash", "A"),
        ("Kuchli parol qanday bo‘lishi kerak?", "Uzun, murakkab va taxmin qilish qiyin", "Faqat 12345", "Faqat ism", "Faqat tug‘ilgan yil", "A"),
        ("Phishing nima?", "Soxta xabar yoki sayt orqali ma’lumot o‘g‘irlash", "Rasm chizish", "Faylni siqish", "Internetni tezlatish", "A"),
        ("Antivirus nima uchun kerak?", "Zararli dasturlardan himoyalash uchun", "Matn tarjima qilish uchun", "Rasm ko‘rish uchun", "Monitorni yoqish uchun", "A"),
        ("Shifrlash nima?", "Ma’lumotni maxfiy ko‘rinishga o‘tkazish", "Faylni o‘chirish", "Kompyuterni yoqish", "Brauzer ochish", "A"),
        ("Ikki bosqichli autentifikatsiya nima?", "Kirishda qo‘shimcha tasdiqlash usuli", "Faqat rang tanlash", "Fayl nomlash", "Printer ulash", "A"),
        ("Zararli dastur nima?", "Kompyuterga zarar yetkazuvchi dastur", "Foydali jadval", "Brauzer belgisi", "Oddiy rasm", "A"),
        ("Firewall nima qiladi?", "Tarmoq trafikini nazorat qiladi", "Matn yozadi", "Video ko‘rsatadi", "Rasm chizadi", "A"),
        ("Backup nima?", "Ma’lumotlarning zaxira nusxasi", "Virus turi", "Monitor sozlamasi", "Fayl kengaytmasi", "A"),
        ("Maxfiy ma’lumotlarni himoya qilishda eng muhim narsa nima?", "Parol va kirish huquqlarini ehtiyot qilish", "Hamma bilan ulashish", "Parolni oddiy qilish", "Public joyga yozib qo‘yish", "A"),
    ],

    "Kompyuter grafikasi": [
        ("Kompyuter grafikasi nima?", "Tasvirlarni kompyuterda yaratish va qayta ishlash sohasi", "Faqat matn yozish", "Tarmoq sozlash", "Baza yaratish", "A"),
        ("Rastr grafika nimadan tashkil topadi?", "Piksellardan", "Faqat chiziqlardan", "Faqat matndan", "Faqat jadvaldan", "A"),
        ("Vektor grafika nimaga asoslanadi?", "Matematik chiziq va shakllarga", "Piksellar sonigagina", "Faqat matnga", "Faqat ovozga", "A"),
        ("Piksel nima?", "Raqamli tasvirning eng kichik nuqtasi", "Printer turi", "Fayl papkasi", "Tarmoq protokoli", "A"),
        ("RGB rang modeli qaysi ranglardan iborat?", "Qizil, yashil, ko‘k", "Oq, qora, sariq", "Ko‘k, qora, oq", "Sariq, yashil, oq", "A"),
        ("2D grafika nima?", "Ikki o‘lchamli tasvirlar", "Uch o‘lchamli obyekt", "Faqat ovoz", "Faqat matn", "A"),
        ("3D grafika nima?", "Uch o‘lchamli obyektlar bilan ishlash", "Faqat jadval", "Faqat matn", "Faqat parol", "A"),
        ("Grafik fayl formatiga qaysi biri misol bo‘ladi?", "PNG", "DOCX", "SQL", "PY", "A"),
        ("Resolution nimani bildiradi?", "Tasvir aniqligi yoki o‘lcham darajasi", "Internet tezligi", "Parol uzunligi", "Fayl egasi", "A"),
        ("Adobe Photoshop asosan nima uchun ishlatiladi?", "Rastr tasvirlarni tahrirlash uchun", "Server yaratish uchun", "Python kod yozish uchun", "SQL baza boshqarish uchun", "A"),
    ],

    "Operatsion tizimlar": [
        ("Operatsion tizim nima?", "Kompyuter resurslarini boshqaruvchi dastur", "Faqat brauzer", "Fayl kengaytmasi", "Router", "A"),
        ("Windows nima?", "Operatsion tizim", "Dasturlash tili", "Ma’lumotlar bazasi", "Antivirus", "A"),
        ("Linux nima?", "Operatsion tizim", "Monitor turi", "SQL so‘rovi", "Video karta", "A"),
        ("Fayl tizimi nima?", "Fayllarni saqlash va tartiblash usuli", "Internet tezligi", "Rasm rangi", "Klaviatura turi", "A"),
        ("Jarayon nima?", "Ishlayotgan dastur holati", "Fayl kengaytmasi", "Parol turi", "Printer modeli", "A"),
        ("RAM operatsion tizimda nima uchun kerak?", "Dasturlarni vaqtincha ishlatish uchun", "Faqat rasm saqlash uchun", "Internet kabeli uchun", "Monitorni tozalash uchun", "A"),
        ("Drayver nima?", "Qurilma bilan tizim orasida aloqa qiluvchi dastur", "Fayl o‘chirish belgisi", "Parol", "Brauzer oynasi", "A"),
        ("GUI nima?", "Grafik foydalanuvchi interfeysi", "Tarmoq kabeli", "SQL jadval", "Video format", "A"),
        ("CLI nima?", "Buyruq satri interfeysi", "Rasm muharriri", "Printer turi", "Brauzer sahifasi", "A"),
        ("Operatsion tizimning asosiy vazifasi qaysi?", "Xotira, fayl, qurilma va dasturlarni boshqarish", "Faqat rasm chizish", "Faqat internet ko‘rsatish", "Faqat o‘yin o‘ynatish", "A"),
    ],

    "10-sinf informatika": [
        ("10-sinf informatika fanida nimalar o‘rganiladi?", "Algoritm, dasturlash, axborot va texnologiyalar", "Faqat sport", "Faqat musiqa", "Faqat rasm", "A"),
        ("Axborot nima?", "Qabul qilinadigan, saqlanadigan va uzatiladigan ma’lumot", "Faqat kompyuter", "Faqat printer", "Faqat monitor", "A"),
        ("Kompyuterning asosiy qurilmalariga qaysilar kiradi?", "Protsessor, xotira, monitor, klaviatura", "Faqat stol va stul", "Faqat modem", "Faqat kabel", "A"),
        ("Dasturlash nima?", "Kompyuterga buyruqlar yozish jarayoni", "Faqat rasm chizish", "Faqat fayl o‘chirish", "Faqat internetga kirish", "A"),
        ("Algoritmni tasvirlash usullaridan biri qaysi?", "Blok-sxema", "Monitor", "Printer", "Router", "A"),
        ("Elektron jadval dasturiga qaysi biri misol?", "Microsoft Excel", "Paint", "Chrome", "Telegram", "A"),
        ("Matn muharririga qaysi biri misol bo‘ladi?", "Microsoft Word", "BIOS", "Router", "CPU", "A"),
        ("Internetdan xavfsiz foydalanishda nima muhim?", "Shaxsiy ma’lumotlarni himoya qilish", "Parolni hammaga aytish", "Begona linklarni bosish", "Soxta saytlarga kirish", "A"),
        ("Domen nomi nima?", "Saytning internetdagi nomi", "Kompyuter xotirasi", "Klaviatura tugmasi", "Printer qog‘ozi", "A"),
        ("Dasturdagi xatolik nima deb ataladi?", "Bug", "Tag", "Host", "Link", "A"),
    ],
}


@transaction.atomic
def run():
    total_topics = 0
    total_quizzes = 0
    total_questions = 0

    for topic_data in TOPICS:
        topic, topic_created = Topic.objects.get_or_create(
            title=topic_data["title"],
            defaults={
                "description": topic_data["description"]
            }
        )

        # Agar mavzu oldin bor bo'lsa, description bo'sh bo'lsa to'ldirib qo'yamiz
        if not topic.description:
            topic.description = topic_data["description"]
            topic.save(update_fields=["description"])

        total_topics += 1

        questions = QUIZ_BANK.get(topic.title, [])

        quiz_title = f"{topic.title} bo'yicha 10 ta test"
        quiz_description = f"Ushbu test {topic.title} mavzusi bo‘yicha bilimlarni tekshirish uchun tuzilgan."

        quiz, quiz_created = Quiz.objects.get_or_create(
            topic=topic,
            title=quiz_title,
            defaults={
                "description": quiz_description
            }
        )

        # Agar quiz oldin bor bo'lsa, description yangilab qo'yamiz
        if quiz.description != quiz_description:
            quiz.description = quiz_description
            quiz.save(update_fields=["description"])

        # Shu quizdagi eski savollarni tozalaymiz
        quiz.questions.all().delete()

        question_objects = []

        for text, option_a, option_b, option_c, option_d, correct_answer in questions:
            question_objects.append(
                Question(
                    quiz=quiz,
                    text=text,
                    option_a=option_a,
                    option_b=option_b,
                    option_c=option_c,
                    option_d=option_d,
                    correct_answer=correct_answer,
                )
            )

        Question.objects.bulk_create(question_objects)

        total_quizzes += 1
        total_questions += len(question_objects)

        status = "Yangi yaratildi" if quiz_created else "Oldin bor edi, savollari yangilandi"
        print(f"✅ {status}: {quiz.title} | Savollar: {len(question_objects)}")

    print("\n==============================")
    print("✅ Barcha testlar qo'shildi!")
    print(f"📚 Mavzular soni: {total_topics}")
    print(f"📝 Quizlar soni: {total_quizzes}")
    print(f"❓ Savollar soni: {total_questions}")
    print("==============================")


if __name__ == "__main__":
    run()