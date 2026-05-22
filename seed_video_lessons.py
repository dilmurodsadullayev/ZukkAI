# -*- coding: utf-8 -*-

"""
seed_video_lessons.py

Bu fayl hozir saytda mavjud bo'lgan 11 ta mavzu uchun
VideoLesson modeliga ORM orqali bittadan videodars qo'shadi.

Ishlatish:
    python seed_video_lessons.py

Eslatma:
    Agar settings faylingiz "config.settings" bo'lmasa,
    DJANGO_SETTINGS_MODULE qiymatini o'zingizdagi settings nomiga almashtiring.

Masalan:
    core.settings
    config.settings
    project.settings
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.db import transaction
from portal.models import Topic, VideoLesson


# True bo'lsa: shu mavzulardagi eski videodarslarni o'chirib,
# har bir mavzuga bittadan yangi darslik qo'shadi.
DELETE_OLD_VIDEOS_FOR_THESE_TOPICS = True


VIDEO_LESSONS = [
    {
        "topic_title": "Python dasturlash tili",
        "topic_description": "Python dasturlash tili orqali o‘quvchilar dasturlash asoslari, o‘zgaruvchilar, shart operatorlari, sikllar, funksiyalar va oddiy dasturlar yaratishni o‘rganadilar.",
        "title": "Python dasturlash tili | Kirish darsi",
        "video_url": "https://www.youtube.com/watch?v=fj_GLU344bQ",
        "duration": "15:00",
        "description": "Ushbu videodarsda Python dasturlash tiliga kirish, Python dasturini o‘rnatish, birinchi dastur yozish va asosiy tushunchalar tushuntiriladi.",
    },
    {
        "topic_title": "Ma’lumotlar bazasi (SQL)",
        "topic_description": "Ma’lumotlar bazasi mavzusida jadvallar, ustunlar, yozuvlar, SQL so‘rovlari, SELECT, INSERT, UPDATE, DELETE va ma’lumotlar bilan ishlash asoslari o‘rganiladi.",
        "title": "SQL va ma’lumotlar bazasi asoslari",
        "video_url": "https://www.youtube.com/watch?v=1ztYVUetfr0",
        "duration": "60:00",
        "description": "Ushbu darsda SQL tili, ma’lumotlar bazasi tushunchasi, jadval yaratish va oddiy so‘rovlar bilan ishlash ko‘rsatiladi.",
    },
    {
        "topic_title": "Kompyuter tarmoqlari",
        "topic_description": "Kompyuter tarmoqlari mavzusida lokal va global tarmoqlar, IP manzillar, DNS, router, server, mijoz va internet orqali ma’lumot almashish jarayoni o‘rganiladi.",
        "title": "Kompyuter tarmoqlari va ularning turlari",
        "video_url": "https://www.youtube.com/watch?v=vv0EI_H5cnM",
        "duration": "12:00",
        "description": "Videodarsda kompyuter tarmoqlari nima ekanligi, ularning turlari va internet ishlashining asosiy tamoyillari tushuntiriladi.",
    },
    {
        "topic_title": "Axborot xavfsizligi",
        "topic_description": "Axborot xavfsizligi mavzusida shaxsiy ma’lumotlarni himoyalash, parollar xavfsizligi, zararli dasturlar, viruslar, fishing hujumlari va himoya usullari o‘rganiladi.",
        "title": "Axborot xavfsizligi va uni himoyalash usullari",
        "video_url": "https://www.youtube.com/watch?v=R4b371U2blw",
        "duration": "20:52",
        "description": "Ushbu videodars axborot xavfsizligi, axborotlarni himoyalash va xavfsizlik usullari haqida boshlang‘ich tushuncha beradi.",
    },
    {
        "topic_title": "Operatsion tizimlar",
        "topic_description": "Operatsion tizimlar mavzusida Windows, Linux, fayllar tizimi, jarayonlar, xotira boshqaruvi, dasturlarni ishga tushirish va tizim resurslarini boshqarish o‘rganiladi.",
        "title": "Operatsion sistema haqida",
        "video_url": "https://www.youtube.com/watch?v=e_pE7rFrC1k",
        "duration": "10:00",
        "description": "Videodarsda operatsion tizim nima, uning vazifalari va kompyuter ishlashidagi o‘rni haqida ma’lumot beriladi.",
    },
    {
        "topic_title": "10-sinf informatika",
        "topic_description": "10-sinf informatika mavzusida algoritmlash, dasturlash, axborot texnologiyalari, internet, ma’lumotlar bilan ishlash va kompyuter savodxonligi bo‘yicha bilimlar beriladi.",
        "title": "10-sinf informatika | Kompyuterning rivojlanish tarixi",
        "video_url": "https://www.youtube.com/watch?v=EIaSAV6winQ",
        "duration": "12:00",
        "description": "Ushbu dars 10-sinf informatika fani bo‘yicha kompyuterning rivojlanish tarixi va boshlang‘ich tushunchalarni o‘rganishga yordam beradi.",
    },
    {
        "topic_title": "Elektron jadvallar",
        "topic_description": "Elektron jadvallar mavzusida Excel yoki Google Sheets dasturlarida jadval yaratish, kataklar bilan ishlash, formulalar, funksiyalar va diagrammalar tuzish o‘rganiladi.",
        "title": "Excelda jadval yaratish | Elektron jadvallar",
        "video_url": "https://www.youtube.com/watch?v=DC3n3PKfa6U",
        "duration": "15:00",
        "description": "Ushbu videodarsda elektron jadvallar tushunchasi, Excelda jadval yaratish, kataklarga ma’lumot kiritish va oddiy hisob-kitoblar bajarish o‘rganiladi.",
    },
    {
        "topic_title": "3D modellashtirish",
        "topic_description": "3D modellashtirish mavzusida uch o‘lchamli obyektlar, shakllar, modellar yaratish, obyektlarni tahrirlash va grafik muhitda ishlash asoslari o‘rganiladi.",
        "title": "Blender 3D | Interfeys va navigatsiya",
        "video_url": "https://www.youtube.com/watch?v=sWGpibbNNsw",
        "duration": "15:00",
        "description": "Videodarsda Blender dasturi interfeysi, 3D muhitda harakatlanish va uch o‘lchamli obyektlar bilan ishlash asoslari tushuntiriladi.",
    },
    {
        "topic_title": "Video ma'lumotlar bilan ishlash",
        "topic_description": "Video ma’lumotlar bilan ishlash mavzusida video fayllar, ularni ochish, tahrirlash, kesish, montaj qilish, formatlar va saqlash usullari o‘rganiladi.",
        "title": "Adobe Spark dasturida yangi video yaratish",
        "video_url": "https://www.youtube.com/watch?v=t2IF8Ur2YQU",
        "duration": "15:00",
        "description": "Ushbu darsda video yaratish, videoga elementlar qo‘shish va video ma’lumotlar bilan ishlash bo‘yicha amaliy tushunchalar beriladi.",
    },
    {
        "topic_title": "Veb dizayn.CSS",
        "topic_description": "Veb dizayn.CSS mavzusida CSS yordamida web sahifalarni bezash, ranglar, shriftlar, margin, padding, flexbox, bloklar va responsiv dizayn asoslari o‘rganiladi.",
        "title": "CSS 1-dars | HTML tuzilishi va Live Server",
        "video_url": "https://www.youtube.com/watch?v=R54iX3Icf64",
        "duration": "15:00",
        "description": "Videodarsda CSS asoslari, HTML sahifaga dizayn berish, ranglar, shriftlar va web dizaynning boshlang‘ich tushunchalari ko‘rsatiladi.",
    },
    {
        "topic_title": "Sun’iy intellekt va zamonaviy texnologiyalar",
        "topic_description": "Sun’iy intellekt va zamonaviy texnologiyalar mavzusida AI tushunchasi, aqlli tizimlar, zamonaviy raqamli texnologiyalar, avtomatlashtirish va ularning hayotdagi qo‘llanilishi o‘rganiladi.",
        "title": "Sun’iy intellekt | Qo‘llanilish sohalari va turlari",
        "video_url": "https://www.youtube.com/watch?v=xiD4uq5zBw4",
        "duration": "20:00",
        "description": "Ushbu videodarsda sun’iy intellekt, uning qo‘llanilish sohalari, turlari va zamonaviy texnologiyalardagi o‘rni tushuntiriladi.",
    },
]


@transaction.atomic
def run():
    created_topics = 0
    updated_topics = 0
    deleted_videos = 0
    created_videos = 0

    for item in VIDEO_LESSONS:
        topic, topic_created = Topic.objects.get_or_create(
            title=item["topic_title"],
            defaults={
                "description": item["topic_description"]
            }
        )

        if topic_created:
            created_topics += 1
            print(f"Mavzu yaratildi: {topic.title}")
        else:
            updated_topics += 1

            if topic.description != item["topic_description"]:
                topic.description = item["topic_description"]
                topic.save(update_fields=["description"])
                print(f"Mavzu tavsifi yangilandi: {topic.title}")
            else:
                print(f"Mavzu oldin bor: {topic.title}")

        if DELETE_OLD_VIDEOS_FOR_THESE_TOPICS:
            old_count = VideoLesson.objects.filter(topic=topic).count()

            if old_count > 0:
                VideoLesson.objects.filter(topic=topic).delete()
                deleted_videos += old_count
                print(f"Eski videodarslar o‘chirildi: {topic.title} | {old_count} ta")

        video = VideoLesson.objects.create(
            topic=topic,
            title=item["title"],
            video_url=item["video_url"],
            description=item["description"],
            duration=item["duration"],
        )

        created_videos += 1
        print(f"Videodars qo‘shildi: {video.title}")

    print("\n==============================")
    print("Video darsliklar bazaga qo‘shildi!")
    print(f"Yangi yaratilgan mavzular: {created_topics}")
    print(f"Oldin bor/yangi tavsif berilgan mavzular: {updated_topics}")
    print(f"O‘chirilgan eski videodarslar: {deleted_videos}")
    print(f"Yangi qo‘shilgan videodarslar: {created_videos}")
    print(f"Jami videodarslar soni: {VideoLesson.objects.count()}")
    print("==============================")


if __name__ == "__main__":
    run()