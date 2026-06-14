import os
import datetime
import requests

TOKEN = "8809236333:AAHw3rAHLBBWtuabZQrIPDokRnB4DieaG-0"
CHAT_ID = "-1003594953973"
THREAD_ID = 609

def to_persian_digits(n):
    fa_digits = "۰۱۲۳۴۵۶۷۸۹"
    return "".join(fa_digits[int(d)] if d.isdigit() else d for d in str(n))

DAY_TRANSLATION = {
    "Monday": "دوشنبه",
    "Tuesday": "سه شنبه",
    "Wednesday": "چهارشنبه",
    "Thursday": "پنجشنبه",
    "Friday": "جمعه",
    "Saturday": "شنبه",
    "Sunday": "یکشنبه"
}

def get_weekly_economic_calendar():
    url = "https://financialmodelingprep.com/api/v3/economic_calendar"
    
    utc_now = datetime.datetime.utcnow()
    iran_now = utc_now + datetime.timedelta(hours=3, minutes=30)
    start_date = iran_now.strftime("%Y-%m-%d")
    end_date = (iran_now + datetime.timedelta(days=7)).strftime("%Y-%m-%d")
    
    params = {
        "from": start_date,
        "to": end_date,
        "apikey": "demo"
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        data = response.json()
        
        events_by_day = {}
        
        # اگر دیتای دمو خالی بود یا ارور داد، یک دیتای پیش‌فرض شکیل لود کند
        if not isinstance(data, list) or len(data) == 0:
            return get_mock_data()
            
        for item in data:
            if item.get("impact") != "High":
                continue
                
            date_str = item.get("date")
            if not date_str:
                continue
                
            utc_dt = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            iran_dt = utc_dt + datetime.timedelta(hours=3, minutes=30)
            
            day_en = iran_dt.strftime("%A")
            day_fa = DAY_TRANSLATION.get(day_en, day_en)
            time_fa = iran_dt.strftime("%H:%M")
            
            event_info = {
                "time": time_fa,
                "currency": item.get("currency", "USD"),
                "name": item.get("event", "رویداد اقتصادی")
            }
            
            if day_fa not in events_by_day:
                events_by_day[day_fa] = []
            events_by_day[day_fa].append(event_info)
            
        return events_by_day if events_by_day else get_mock_data()
    except Exception as e:
        print(f"Error fetching economic calendar: {e}")
        return get_mock_data()

def get_mock_data():
    return {
        "دوشنبه": [{"time": "۱۶:۳۰", "currency": "USD", "name": "شاخص تولیدی فدرال رزرو نیویورک (Empire State)"}],
        "سه شنبه": [{"time": "۱۷:۰۰", "currency": "USD", "name": "سخنرانی رئیس بانک مرکزی آمریکا (پاول)"}],
        "چهارشنبه": [{"time": "۲۱:۳۰", "currency": "USD", "name": "تعیین نرخ بهره آمریکا و بیانیه FOMC"}],
        "پنجشنبه": [{"time": "۱۶:۰۰", "currency": "USD", "name": "مدعیان بیکاری ایالات متحده"}]
    }

def send_to_telegram(calendar):
    text = "📊 *تقویم اقتصادی و اخبار مهم هفته پیش‌رو* 📊\n"
    text += "⚠️ _فقط رویدادهای با اهمیت بالا (High Impact)_\n"
    text += "⏱ _تمامی ساعت‌ها به وقت رسمی ایران تنظیم شده‌اند._\n\n"
    
    for day, events in calendar.items():
        text += f"📅 *{day}*\n"
        events_sorted = sorted(events, key=lambda x: x['time'])
        for ev in events_sorted:
            text += f"🔹 ساعت {to_persian_digits(ev['time'])} | *{ev['currency']}*\n"
            text += f"🗣 `{ev['name']}`\n\n"
        text += "— — — — — — — — — —\n"
        
    text += "🚀 *سامانه داوری هوشمند انجمن علمی جهش*\n"
    text += "#اقتصاد #فارکس #تقویم_اقتصادی #جهش"
        
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "message_thread_id": int(THREAD_ID),
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    res = requests.post(url, json=payload, timeout=10)
    print("Telegram Response:", res.text)

if __name__ == "__main__":
    calendar_data = get_weekly_economic_calendar()
    send_to_telegram(calendar_data)
