import google.generativeai as genai
from django.conf import settings

# API sozlamalari
genai.configure(api_key=settings.GEMINI_API_KEY)


def get_working_model_name():
    """API kalit ruxsat bergan birinchi ishlovchi model nomini qaytaradi"""
    try:
        # Kalit ruxsat bergan modellarni ko'ramiz
        available_models = [
            m.name for m in genai.list_models()
            if 'generateContent' in m.supported_generation_methods
        ]

        # Ustuvorlik bo'yicha qidirish
        for target in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']:
            if target in available_models:
                return target

        # Agar biz kutganlar yo'q bo'lsa, borini olamiz
        if available_models:
            return available_models[0]

    except Exception as e:
        print(f"Modellarni olishda xato: {e}")

    # Hech narsa bo'lmasa, standart variant
    return 'models/gemini-pro'


def ai_generate_task(topic_name, level):
    """2.1-§: Topshiriq yaratish"""
    try:
        model_name = get_working_model_name()
        model = genai.GenerativeModel(model_name)

        prompt = f"""
        Siz informatika fani o'qituvchisisiz. 
        Mavzu: {topic_name}. Daraja: {level}.
        Vazifa: O'quvchi uchun 1 ta qiziqarli interaktiv topshiriq va uning to'g'ri yechimini yarating.
        Javobni quyidagi formatda qaytaring:
        TOPXIRIQ: [topshiriq matni]
        YECHIM: [to'g'ri javob yoki kod]
        """

        response = model.generate_content(prompt)
        return response.text if response.text else "AI bo'sh javob qaytardi."

    except Exception as e:
        return f"Xatolik yuz berdi: {str(e)}"


def ai_evaluate_answer(task_content, correct_solution, student_answer):
    """2.2-§: Baholash va Feedback"""
    try:
        model_name = get_working_model_name()
        model = genai.GenerativeModel(model_name)

        prompt = f"""
        Topshiriq: {task_content}
        To'g'ri yechim: {correct_solution}
        O'quvchi javobi: {student_answer}

        Vazifa: O'quvchining javobini 100 ballik tizimda baholang va xatolarini tushuntirib feedback bering.
        Javobni faqat shu formatda qaytaring:
        BALL: [faqat raqam]
        FEEDBACK: [izohingiz]
        """

        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"BALL: 0 FEEDBACK: AI xatosi: {str(e)}"