# -*- coding: utf-8 -*-

"""
seed_video_lessons.py

Bu fayl VideoLesson modeliga har bir mavzu uchun bittadan YouTube video dars qo'shadi.

Ishlatish:
    python seed_video_lessons.py

Eslatma:
    Agar Django project settings nomi "config.settings" bo'lmasa,
    pastdagi DJANGO_SETTINGS_MODULE qiymatini o'zingdagi settings nomiga almashtir.
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.db import transaction
from portal.models import Topic, VideoLesson


# Agar True bo'lsa, shu fayldagi mavzular bo'yicha eski videolarni o'chirib,
# har bir mavzuga bittadan yangi video dars qoldiradi.
# Agar eski videolaring saqlanib qolsin desang, False qilib qo'y.
DELETE_OLD_VIDEOS_FOR_THESE_TOPICS = True


VIDEO_LESSONS = [
    {
        "topic_title": "Algoritmlash asoslari",
        "topic_description": "Algoritm tushunchasi, blok-sxemalar, masalalarni bosqichma-bosqich yechish va dasturlashga tayyorlash asoslari o‘rganiladi.",
        "title": "Algoritm tushunchasi va qo‘llanilishi | Algoritmlash asoslari",
        "video_url": "https://www.youtube.com/watch?v=4VEq3DRfq6I",
        "duration": "10:00",
        "description": "Ushbu videodarsda algoritm tushunchasi, uning vazifasi va dasturlashdagi o‘rni haqida boshlang‘ich ma’lumot beriladi.",
    },
    {
        "topic_title": "Python dasturlash tili",
        "topic_description": "Python dasturlash tilining sintaksisi, o‘zgaruvchilar, shart operatorlari, sikllar, funksiyalar va amaliy dasturlar yaratish o‘rganiladi.",
        "title": "1-dastur | Python dasturlash tili",
        "video_url": "https://www.youtube.com/watch?v=fj_GLU344bQ",
        "duration": "15:00",
        "description": "Python dasturlash tilini boshlash, Python muhitini sozlash va birinchi dastur yozish bo‘yicha o‘zbekcha video dars.",
    },
    {
        "topic_title": "Ma’lumotlar bazasi (SQL)",
        "topic_description": "Ma’lumotlar bazasi tushunchasi, jadvallar, SQL so‘rovlari, SELECT, INSERT, UPDATE, DELETE va bog‘langan jadvallar bilan ishlash o‘rganiladi.",
        "title": "Ma’lumotlar bazasini to‘liq o‘rganish | SQL | MySQL",
        "video_url": "https://www.youtube.com/watch?v=1ztYVUetfr0",
        "duration": "60:00",
        "description": "Ma’lumotlar bazasi nima, SQL nima uchun kerak va MySQL bilan ishlash bo‘yicha o‘zbekcha tushuntirish darsi.",
    },
    {
        "topic_title": "Ob’ektga yo‘naltirilgan dasturlash",
        "topic_description": "Class, object, meros olish, inkapsulyatsiya, polimorfizm va real loyihalarda OOP yondashuvlaridan foydalanish o‘rganiladi.",
        "title": "Class nima? | Ob’ektga yo‘naltirilgan dasturlash",
        "video_url": "https://www.youtube.com/watch?v=BQ2Me5tujRM",
        "duration": "12:00",
        "description": "Ob’ektga yo‘naltirilgan dasturlashda class va object tushunchalari sodda misollar bilan tushuntiriladi.",
    },
    {
        "topic_title": "Kompyuter tarmoqlari",
        "topic_description": "Kompyuter tarmoqlari, IP manzillar, DNS, HTTP/HTTPS, router, server va mijoz o‘rtasidagi aloqa asoslari o‘rganiladi.",
        "title": "Kompyuter tarmoqlari va ularning turlari",
        "video_url": "https://www.youtube.com/watch?v=vv0EI_H5cnM",
        "duration": "12:00",
        "description": "Kompyuter tarmoqlari, ularning vazifasi, turlari va asosiy tushunchalari haqida o‘zbekcha videodars.",
    },
    {
        "topic_title": "Sun’iy intellekt va mashinaviy o‘rganish",
        "topic_description": "Sun’iy intellekt tushunchasi, mashinaviy o‘rganish asoslari, ma’lumotlar bilan ishlash, model o‘qitish va bashorat qilish jarayonlari o‘rganiladi.",
        "title": "Sun’iy intellekt nima? | To‘liq obzor",
        "video_url": "https://www.youtube.com/watch?v=XtizkYKT280",
        "duration": "20:00",
        "description": "Sun’iy intellekt nima, qayerlarda ishlatiladi va uning asosiy yo‘nalishlari haqida o‘zbekcha tushuntirish.",
    },
    {
        "topic_title": "Web-dasturlash (Frontend)",
        "topic_description": "HTML, CSS, JavaScript, sahifa tuzilmasi, dizayn, responsiv interfeys va foydalanuvchi bilan ishlovchi web sahifalar yaratish o‘rganiladi.",
        "title": "Frontend dasturlash | HTML | 1-dars",
        "video_url": "https://www.youtube.com/watch?v=-Aj2-o5WiDw",
        "duration": "15:00",
        "description": "Frontend dasturlashga kirish, HTML asoslari va web sahifa yaratishni boshlash bo‘yicha o‘zbekcha video dars.",
    },
    {
        "topic_title": "Axborot xavfsizligi",
        "topic_description": "Axborotlarni himoyalash, parollar xavfsizligi, shifrlash, tarmoq xavfsizligi, zararli dasturlar va himoya usullari o‘rganiladi.",
        "title": "Axborot xavfsizligi va uni himoyalash usullari",
        "video_url": "https://www.youtube.com/watch?v=R4b371U2blw",
        "duration": "12:00",
        "description": "Axborot xavfsizligi, ma’lumotlarni himoyalash va xavfsizlik usullari bo‘yicha boshlang‘ich o‘zbekcha videodars.",
    },
    {
        "topic_title": "Kompyuter grafikasi",
        "topic_description": "Grafik obyektlar, ranglar, tasvirlar bilan ishlash, 2D/3D grafika asoslari va kompyuter grafikasi dasturlari haqida bilim beriladi.",
        "title": "Kompyuter grafikasi tushunchasi va turlari",
        "video_url": "https://www.youtube.com/watch?v=jgFRZxR9fK8",
        "duration": "10:00",
        "description": "Kompyuter grafikasi, rastr va vektor grafika, rang tushunchalari haqida o‘zbekcha video dars.",
    },
    {
        "topic_title": "Operatsion tizimlar",
        "topic_description": "Operatsion tizim tushunchasi, fayl tizimi, jarayonlar, xotira boshqaruvi, Linux va Windows tizimlarining asosiy ishlash prinsiplari o‘rganiladi.",
        "title": "Operatsion sistema haqida",
        "video_url": "https://www.youtube.com/watch?v=e_pE7rFrC1k",
        "duration": "10:00",
        "description": "Operatsion tizim tushunchasi, uning vazifalari va kompyuter ishlashidagi o‘rni haqida o‘zbekcha video dars.",
    },
    {
        "topic_title": "10-sinf informatika",
        "topic_description": "10-sinf informatika fanida algoritmlash, dasturlash asoslari, ma’lumotlar bilan ishlash, kompyuter tizimlari, internet texnologiyalari va axborot xavfsizligi bo‘yicha asosiy bilimlar o‘rganiladi.",
        "title": "10-sinf informatika | 1-dars | Kompyuterning rivojlanish tarixi",
        "video_url": "https://www.youtube.com/watch?v=EIaSAV6winQ",
        "duration": "12:00",
        "description": "10-sinf informatika fanining birinchi mavzularidan biri bo‘lgan kompyuterning rivojlanish tarixi haqida o‘zbekcha videodars.",
    },
]


@transaction.atomic
def run():
    created_topics = 0
    updated_topics = 0
    created_videos = 0
    updated_videos = 0
    deleted_videos = 0

    for item in VIDEO_LESSONS:
        topic, topic_created = Topic.objects.get_or_create(
            title=item["topic_title"],
            defaults={
                "description": item["topic_description"]
            }
        )

        if topic_created:
            created_topics += 1
            print(f"✅ Mavzu yaratildi: {topic.title}")
        else:
            updated_topics += 1

            # Agar description bo'sh bo'lsa yoki yangilash kerak bo'lsa
            if topic.description != item["topic_description"]:
                topic.description = item["topic_description"]
                topic.save(update_fields=["description"])
                print(f"♻️ Mavzu tavsifi yangilandi: {topic.title}")

        if DELETE_OLD_VIDEOS_FOR_THESE_TOPICS:
            old_count = VideoLesson.objects.filter(topic=topic).count()
            if old_count:
                VideoLesson.objects.filter(topic=topic).delete()
                deleted_videos += old_count
                print(f"🧹 Eski videolar o'chirildi: {topic.title} | {old_count} ta")

            video = VideoLesson.objects.create(
                topic=topic,
                title=item["title"],
                video_url=item["video_url"],
                description=item["description"],
                duration=item["duration"],
            )
            created_videos += 1
            print(f"🎬 Video qo'shildi: {video.title}")

        else:
            video, video_created = VideoLesson.objects.update_or_create(
                topic=topic,
                title=item["title"],
                defaults={
                    "video_url": item["video_url"],
                    "description": item["description"],
                    "duration": item["duration"],
                }
            )

            if video_created:
                created_videos += 1
                print(f"🎬 Video yaratildi: {video.title}")
            else:
                updated_videos += 1
                print(f"♻️ Video yangilandi: {video.title}")

    print("\n==============================")
    print("✅ Video darsliklar bazaga qo'shildi!")
    print(f"📚 Yangi mavzular: {created_topics}")
    print(f"📚 Oldin bor/yaxshilangan mavzular: {updated_topics}")
    print(f"🧹 O'chirilgan eski videolar: {deleted_videos}")
    print(f"🎬 Yangi qo'shilgan videolar: {created_videos}")
    print(f"♻️ Yangilangan videolar: {updated_videos}")
    print(f"📌 Jami video darsliklar: {VideoLesson.objects.count()}")
    print("==============================")


if __name__ == "__main__":
    run()