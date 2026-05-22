# -*- coding: utf-8 -*-

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.db import transaction
from portal.models import Topic, Quiz, Question


DELETE_OLD_QUIZZES_FOR_THESE_TOPICS = True


TOPICS = [
    {
        "title": "Python dasturlash tili",
        "description": "Python dasturlash tili orqali o‘quvchilar dasturlash asoslari, o‘zgaruvchilar, shart operatorlari, sikllar, funksiyalar va oddiy dasturlar yaratishni o‘rganadilar.",
    },
    {
        "title": "Ma’lumotlar bazasi (SQL)",
        "description": "Ma’lumotlar bazasi mavzusida jadvallar, ustunlar, yozuvlar, SQL so‘rovlari, SELECT, INSERT, UPDATE, DELETE va ma’lumotlar bilan ishlash asoslari o‘rganiladi.",
    },
    {
        "title": "Kompyuter tarmoqlari",
        "description": "Kompyuter tarmoqlari mavzusida lokal va global tarmoqlar, IP manzillar, DNS, router, server, mijoz va internet orqali ma’lumot almashish jarayoni o‘rganiladi.",
    },
    {
        "title": "Axborot xavfsizligi",
        "description": "Axborot xavfsizligi mavzusida shaxsiy ma’lumotlarni himoyalash, parollar xavfsizligi, zararli dasturlar, viruslar, fishing hujumlari va himoya usullari o‘rganiladi.",
    },
    {
        "title": "Operatsion tizimlar",
        "description": "Operatsion tizimlar mavzusida Windows, Linux, fayllar tizimi, jarayonlar, xotira boshqaruvi, dasturlarni ishga tushirish va tizim resurslarini boshqarish o‘rganiladi.",
    },
    {
        "title": "10-sinf informatika",
        "description": "10-sinf informatika mavzusida algoritmlash, dasturlash, axborot texnologiyalari, internet, ma’lumotlar bilan ishlash va kompyuter savodxonligi bo‘yicha bilimlar beriladi.",
    },
    {
        "title": "Elektron jadvallar",
        "description": "Elektron jadvallar mavzusida Excel yoki Google Sheets dasturlarida jadval yaratish, kataklar bilan ishlash, formulalar, funksiyalar va diagrammalar tuzish o‘rganiladi.",
    },
    {
        "title": "3D modellashtirish",
        "description": "3D modellashtirish mavzusida uch o‘lchamli obyektlar, shakllar, modellar yaratish, obyektlarni tahrirlash va grafik muhitda ishlash asoslari o‘rganiladi.",
    },
    {
        "title": "Video ma'lumotlar bilan ishlash",
        "description": "Video ma’lumotlar bilan ishlash mavzusida video fayllar, ularni ochish, tahrirlash, kesish, montaj qilish, formatlar va saqlash usullari o‘rganiladi.",
    },
    {
        "title": "Veb dizayn.CSS",
        "description": "Veb dizayn.CSS mavzusida CSS yordamida web sahifalarni bezash, ranglar, shriftlar, margin, padding, flexbox, bloklar va responsiv dizayn asoslari o‘rganiladi.",
    },
    {
        "title": "Sun’iy intellekt va zamonaviy texnologiyalar",
        "description": "Sun’iy intellekt va zamonaviy texnologiyalar mavzusida AI tushunchasi, aqlli tizimlar, zamonaviy raqamli texnologiyalar, avtomatlashtirish va ularning hayotdagi qo‘llanilishi o‘rganiladi.",
    },
]


QUIZ_BANK = {
    "Python dasturlash tili": [
        ("Python qanday turdagi til hisoblanadi?", "Dasturlash tili", "Operatsion tizim", "Brauzer", "Antivirus", "A"),
        ("Python’da ekranga ma’lumot chiqarish uchun qaysi funksiya ishlatiladi?", "input()", "print()", "len()", "type()", "B"),
        ("Python’da foydalanuvchidan ma’lumot olish uchun qaysi funksiya ishlatiladi?", "print()", "input()", "range()", "str()", "B"),
        ("Python’da butun son ma’lumot turi qaysi?", "str", "float", "int", "bool", "C"),
        ("Python’da matnli ma’lumot turi qanday nomlanadi?", "str", "int", "float", "list", "A"),
        ("Python’da shart operatori qaysi kalit so‘z bilan boshlanadi?", "for", "while", "if", "def", "C"),
        ("Python’da sikllar uchun qaysi operatorlar ishlatiladi?", "if va else", "for va while", "try va except", "class va object", "B"),
        ("Python’da funksiya yaratish uchun qaysi kalit so‘z ishlatiladi?", "func", "def", "function", "return", "B"),
        ("Python’da ro‘yxat qaysi belgilar bilan yoziladi?", "()", "{}", "[]", "<>", "C"),
        ("Python’da izoh yozish uchun qaysi belgi ishlatiladi?", "#", "//", "/* */", "@", "A"),
    ],

    "Ma’lumotlar bazasi (SQL)": [
        ("Ma’lumotlar bazasi nima?", "Ma’lumotlarni tartibli saqlash tizimi", "Faqat rasm chizish dasturi", "Operatsion tizim", "Brauzer", "A"),
        ("SQL nima uchun ishlatiladi?", "Ma’lumotlar bazasi bilan ishlash uchun", "Video tahrirlash uchun", "Kompyuterni o‘chirish uchun", "Rasm chizish uchun", "A"),
        ("SELECT buyrug‘i nima qiladi?", "Ma’lumot qo‘shadi", "Ma’lumotlarni tanlab ko‘rsatadi", "Jadvalni o‘chiradi", "Parolni almashtiradi", "B"),
        ("INSERT buyrug‘i nima uchun ishlatiladi?", "Ma’lumot qo‘shish uchun", "Ma’lumot o‘chirish uchun", "Jadvalni ko‘rish uchun", "Bazani yopish uchun", "A"),
        ("UPDATE buyrug‘i nima qiladi?", "Ma’lumotni yangilaydi", "Kompyuterni yangilaydi", "Internetni yoqadi", "Faylni siqadi", "A"),
        ("DELETE buyrug‘i nima qiladi?", "Ma’lumotni o‘chiradi", "Ma’lumotni chiqaradi", "Ma’lumotni nusxalaydi", "Jadval chizadi", "A"),
        ("Jadvaldagi ustun inglizcha qanday ataladi?", "Row", "Column", "Database", "Server", "B"),
        ("Jadvaldagi satr odatda qanday ataladi?", "Record", "Column", "Field", "Query", "A"),
        ("PRIMARY KEY nimani bildiradi?", "Jadvaldagi noyob identifikator", "Oddiy matn", "Parol turi", "Brauzer nomi", "A"),
        ("WHERE sharti nima uchun ishlatiladi?", "Ma’lumotlarni shart asosida filtrlash uchun", "Jadval rangini o‘zgartirish uchun", "Baza yaratish uchun", "Kompyuter tezligini oshirish uchun", "A"),
    ],

    "Kompyuter tarmoqlari": [
        ("Kompyuter tarmog‘i nima?", "Kompyuterlarning o‘zaro bog‘lanishi", "Faqat bitta monitor", "Matn muharriri", "Fayl kengaytmasi", "A"),
        ("LAN nima?", "Mahalliy tarmoq", "Global tarmoq", "Video karta", "Dasturlash tili", "A"),
        ("WAN nima?", "Keng hududli tarmoq", "Klaviatura turi", "Xotira turi", "Printer dasturi", "A"),
        ("IP manzil nima?", "Tarmoqdagi qurilma manzili", "Fayl nomi", "Rasm formati", "Parol turi", "A"),
        ("DNS nima vazifa bajaradi?", "Domen nomini IP manzilga aylantiradi", "Kompyuterni sovitadi", "Rasm yaratadi", "Fayl siqadi", "A"),
        ("HTTP nima?", "Veb ma’lumot almashish protokoli", "Grafik dastur", "Xotira turi", "Operatsion tizim", "A"),
        ("HTTPS nima sababdan xavfsizroq?", "Ma’lumotlarni shifrlab uzatadi", "Faqat tezroq ishlaydi", "Faqat rasm ko‘rsatadi", "Faqat offline ishlaydi", "A"),
        ("Router nima qiladi?", "Tarmoq trafikini yo‘naltiradi", "Matn yozadi", "Faylni o‘chiradi", "Monitorni yoqadi", "A"),
        ("Server nima?", "Mijozlarga xizmat ko‘rsatuvchi kompyuter yoki dastur", "Faqat klaviatura", "Rasm turi", "O‘yin turi", "A"),
        ("Client nima?", "Server xizmatidan foydalanuvchi qurilma yoki dastur", "Faqat printer", "Antivirus", "BIOS turi", "A"),
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

    "Elektron jadvallar": [
        ("Elektron jadval nima?", "Ma’lumotlarni jadval ko‘rinishida saqlash va hisoblash dasturi", "Faqat rasm chizish dasturi", "Video ko‘rish dasturi", "Operatsion tizim", "A"),
        ("Microsoft Excel qanday dastur?", "Elektron jadval dasturi", "Brauzer", "Antivirus", "Video montaj dasturi", "A"),
        ("Elektron jadvaldagi kichik bo‘lim nima deb ataladi?", "Katak", "Papka", "Disk", "Oyna", "A"),
        ("Excel’da formula odatda qaysi belgi bilan boshlanadi?", "=", "#", "@", "$", "A"),
        ("SUM funksiyasi nima qiladi?", "Sonlarni yig‘adi", "Matnni o‘chiradi", "Rasm chizadi", "Faylni yopadi", "A"),
        ("A1 nimani bildiradi?", "A ustun va 1-satr kesishmasidagi katakni", "Fayl nomini", "Diagramma turini", "Dastur versiyasini", "A"),
        ("Diagramma nima uchun ishlatiladi?", "Ma’lumotlarni grafik ko‘rinishda tasvirlash uchun", "Parol yaratish uchun", "Fayl o‘chirish uchun", "Internetga ulanish uchun", "A"),
        ("Elektron jadvalda ustunlar odatda qanday belgilanadi?", "Harflar bilan", "Faqat raqamlar bilan", "Faqat ranglar bilan", "Faqat belgilar bilan", "A"),
        ("Elektron jadvalda satrlar odatda qanday belgilanadi?", "Raqamlar bilan", "Harflar bilan", "Ranglar bilan", "Fayl nomlari bilan", "A"),
        ("AVERAGE funksiyasi nima qiladi?", "O‘rtacha qiymatni hisoblaydi", "Eng katta sonni o‘chiradi", "Matnni tarjima qiladi", "Jadvalni yopadi", "A"),
    ],

    "3D modellashtirish": [
        ("3D modellashtirish nima?", "Uch o‘lchamli obyektlarni yaratish jarayoni", "Faqat matn yozish", "Faqat jadval tuzish", "Internet tezligini o‘lchash", "A"),
        ("3D obyekt nechta asosiy o‘lchamga ega?", "3 ta", "1 ta", "2 ta", "5 ta", "A"),
        ("3D modellashtirishda kenglik, balandlik va yana nima ishlatiladi?", "Chuqurlik", "Parol", "Ustun", "Brauzer", "A"),
        ("Blender qanday dastur hisoblanadi?", "3D modellashtirish dasturi", "Matn muharriri", "Antivirus", "Brauzer", "A"),
        ("3D model nima?", "Uch o‘lchamli obyektning raqamli ko‘rinishi", "Faqat rasm nomi", "Parol turi", "SQL so‘rovi", "A"),
        ("Rendering nima?", "3D sahnani yakuniy tasvirga aylantirish", "Faylni o‘chirish", "Matnni nusxalash", "Tarmoqni uzish", "A"),
        ("3D modellashtirish qayerlarda ishlatiladi?", "O‘yin, arxitektura, animatsiya va dizaynda", "Faqat kalkulyatorda", "Faqat parol yaratishda", "Faqat xat yozishda", "A"),
        ("3D obyektni aylantirish amali qanday maqsadda ishlatiladi?", "Obyekt ko‘rinishini o‘zgartirish uchun", "Faylni yopish uchun", "Internetni sozlash uchun", "Matnni tarjima qilish uchun", "A"),
        ("Material nima?", "3D obyekt yuzasining rangi va ko‘rinishi", "Faqat fayl hajmi", "Klaviatura turi", "Tarmoq nomi", "A"),
        ("3D sahnada yorug‘lik nima uchun kerak?", "Obyektlarni ko‘rinadigan va realroq qilish uchun", "Kod yozish uchun", "Bazani o‘chirish uchun", "Parol almashtirish uchun", "A"),
    ],

    "Video ma'lumotlar bilan ishlash": [
        ("Video ma’lumot nima?", "Harakatlanuvchi tasvir va ovozdan iborat raqamli ma’lumot", "Faqat matnli fayl", "Faqat jadval", "Faqat parol", "A"),
        ("Video montaj nima?", "Videoni kesish, birlashtirish va tahrirlash jarayoni", "Faylni shifrlash", "Kompyuterni o‘chirish", "Internet tezligini oshirish", "A"),
        ("MP4 qanday format?", "Video fayl formati", "Matn formati", "Jadval formati", "Dasturlash tili", "A"),
        ("Video fayl hajmiga nimalar ta’sir qiladi?", "Sifat, davomiylik va format", "Faqat klaviatura", "Faqat parol", "Faqat sichqoncha", "A"),
        ("Videoni kesish nima uchun kerak?", "Keraksiz qismlarni olib tashlash uchun", "Parolni tiklash uchun", "Jadval yaratish uchun", "Tarmoqni uzish uchun", "A"),
        ("Frame nima?", "Videodagi bitta kadr", "Fayl papkasi", "SQL jadval", "Router turi", "A"),
        ("FPS nimani bildiradi?", "Bir soniyada ko‘rsatiladigan kadrlar sonini", "Fayl parolini", "Internet nomini", "Monitor rangini", "A"),
        ("Video tahrirlash dasturiga qaysi biri misol bo‘ladi?", "Adobe Premiere Pro", "Microsoft Excel", "Notepad", "Calculator", "A"),
        ("Videoga matn qo‘shish nima uchun ishlatiladi?", "Izoh, sarlavha yoki subtitr berish uchun", "Kompyuterni formatlash uchun", "Faylni yashirish uchun", "Parol yaratish uchun", "A"),
        ("Videoni eksport qilish nimani bildiradi?", "Tayyor videoni kerakli formatda saqlash", "Videoni o‘chirib tashlash", "Kompyuterni qayta yoqish", "Brauzerni yopish", "A"),
    ],

    "Veb dizayn.CSS": [
        ("CSS nima?", "Web sahifaga dizayn beruvchi uslublar tili", "Ma’lumotlar bazasi", "Operatsion tizim", "Antivirus", "A"),
        ("CSS’da rang berish uchun qaysi xossa ishlatiladi?", "color", "print", "select", "query", "A"),
        ("background-color nima qiladi?", "Element orqa fon rangini belgilaydi", "Matnni o‘chiradi", "Fayl yaratadi", "Serverni ishga tushiradi", "A"),
        ("font-size nima uchun ishlatiladi?", "Matn o‘lchamini belgilash uchun", "Internetni ulash uchun", "Jadvalni o‘chirish uchun", "Parol yaratish uchun", "A"),
        ("margin nima?", "Element tashqi bo‘shlig‘i", "Element ichki matni", "Rasm formati", "Tarmoq protokoli", "A"),
        ("padding nima?", "Element ichki bo‘shlig‘i", "Brauzer nomi", "Dastur xatosi", "Fayl turi", "A"),
        ("border nima uchun ishlatiladi?", "Elementga chegara berish uchun", "Ma’lumot o‘chirish uchun", "Server ochish uchun", "Parolni almashtirish uchun", "A"),
        ("CSS’da class selector qanday yoziladi?", ".class_nomi", "#class_nomi", "@class_nomi", "$class_nomi", "A"),
        ("CSS’da id selector qanday yoziladi?", "#id_nomi", ".id_nomi", "@id_nomi", "$id_nomi", "A"),
        ("Responsiv dizayn nima?", "Sahifaning turli ekran o‘lchamlariga moslashishi", "Faqat bitta ekranda ishlashi", "Faqat qora rangda bo‘lishi", "Faylni o‘chirish usuli", "A"),
    ],

    "Sun’iy intellekt va zamonaviy texnologiyalar": [
        ("Sun’iy intellekt nima?", "Kompyuterning aqlli vazifalarni bajarish texnologiyasi", "Faqat printer sozlamasi", "Fayl kengaytmasi", "Monitor turi", "A"),
        ("AI qisqartmasi nimani anglatadi?", "Artificial Intelligence", "Automatic Internet", "Advanced Image", "Application Input", "A"),
        ("Chatbot nima?", "Foydalanuvchi bilan suhbatlasha oladigan dastur", "Faqat rasm chizuvchi qurilma", "Internet kabeli", "Operatsion tizim", "A"),
        ("Zamonaviy texnologiyalarga qaysi biri misol bo‘ladi?", "Sun’iy intellekt, robototexnika va bulutli xizmatlar", "Faqat daftar va ruchka", "Faqat doska", "Faqat oddiy kalkulyator", "A"),
        ("Mashinaviy o‘rganish nima?", "Ma’lumotlar asosida o‘rganadigan algoritmlar yo‘nalishi", "Faqat qo‘lda yozish", "Internetni o‘chirish", "Kompyuter yig‘ish", "A"),
        ("AI qayerlarda qo‘llaniladi?", "Tibbiyot, ta’lim, transport, biznes va dasturlarda", "Faqat chiroq yoqishda", "Faqat qog‘oz kesishda", "Faqat stol tuzatishda", "A"),
        ("Raqamli texnologiya nima?", "Ma’lumotlarni raqamli shaklda qayta ishlovchi texnologiya", "Faqat qog‘oz hujjat", "Faqat mexanik uskuna", "Faqat oddiy daftar", "A"),
        ("Bulutli texnologiya nima?", "Ma’lumot va xizmatlarni internet orqali ishlatish imkoniyati", "Faqat kompyuter ichidagi chang", "Faqat monitor nuri", "Faqat printer siyohi", "A"),
        ("Avtomatlashtirish nima?", "Jarayonlarni inson aralashuvisiz yoki kam aralashuv bilan bajarish", "Faqat qo‘lda yozish", "Faylni butunlay yo‘qotish", "Internetni uzish", "A"),
        ("Sun’iy intellektdan foydalanishda nima muhim?", "Xavfsizlik, ishonchlilik va to‘g‘ri ma’lumotdan foydalanish", "Har qanday javobga ko‘r-ko‘rona ishonish", "Parolni AIga berish", "Manbani tekshirmaslik", "A"),
    ],
}


@transaction.atomic
def run():
    total_topics = 0
    total_quizzes = 0
    total_questions = 0
    deleted_quizzes = 0

    for topic_data in TOPICS:
        topic, topic_created = Topic.objects.get_or_create(
            title=topic_data["title"],
            defaults={
                "description": topic_data["description"]
            }
        )

        if not topic_created:
            if topic.description != topic_data["description"]:
                topic.description = topic_data["description"]
                topic.save(update_fields=["description"])

        questions = QUIZ_BANK.get(topic.title, [])

        if len(questions) != 10:
            raise ValueError(f"{topic.title} mavzusi uchun savollar soni 10 ta emas: {len(questions)} ta")

        if DELETE_OLD_QUIZZES_FOR_THESE_TOPICS:
            old_count = Quiz.objects.filter(topic=topic).count()

            if old_count > 0:
                Quiz.objects.filter(topic=topic).delete()
                deleted_quizzes += old_count
                print(f"Eski quizlar o‘chirildi: {topic.title} | {old_count} ta")

        quiz = Quiz.objects.create(
            topic=topic,
            title=f"{topic.title} bo‘yicha 10 ta test",
            description=f"Ushbu test {topic.title} mavzusi bo‘yicha bilimlarni tekshirish uchun tuzilgan."
        )

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

        total_topics += 1
        total_quizzes += 1
        total_questions += len(question_objects)

        print(f"Quiz qo‘shildi: {quiz.title} | Savollar: {len(question_objects)} ta")

    print("\n==============================")
    print("Barcha quizlar bazaga qo‘shildi!")
    print(f"Mavzular soni: {total_topics}")
    print(f"Yangi quizlar soni: {total_quizzes}")
    print(f"Yangi savollar soni: {total_questions}")
    print(f"O‘chirilgan eski quizlar soni: {deleted_quizzes}")
    print(f"Bazada jami quizlar soni: {Quiz.objects.count()}")
    print(f"Bazada jami savollar soni: {Question.objects.count()}")
    print("==============================")


if __name__ == "__main__":
    run()