"""
NIGORA DETOX Marketplace - Backend API & Web Application
"""
import os
import json
import uuid
import datetime
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="NIGORA DETOX Marketplace API",
    description="Detoks va ozdiruvchi kompleks mahsulotlar savdosi, Click to'lov, Nigora AI Konsultant va Admin boshqaruvi",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for pictures and frontend assets
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)
ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")
CHATS_FILE = os.path.join(DATA_DIR, "chats.json")

def load_json(filepath: str, default: Any):
    if not os.path.exists(filepath):
        return default
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def save_json(filepath: str, data: Any):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

COURSES = [
    {
        "id": "course-5-days",
        "name": "5 Kunlik Ekspress Detoks Kursi",
        "days": 5,
        "base_price": 370000,
        "discount_percent": 5,
        "final_price": 351500,
        "badge": "5% Chegirma",
        "is_popular": False,
        "short_desc": "Organizm shlaklarini yuvish, ichaklarni yengillashtirish va boshlang'ich 2-3 kg vazn tashlash uchun ajoyib boshlanish.",
        "daily_set": [
            "Block Fit Detox Tea (1 saşe)",
            "Detox Kofe (1 saşe)",
            "Yashil Parashok Fit Komponenti"
        ]
    },
    {
        "id": "course-10-days",
        "name": "10 Kunlik Optimal Detoks & Ozish Kursi",
        "days": 10,
        "base_price": 740000,
        "discount_percent": 8,
        "final_price": 680800,
        "badge": "Eng ommabop (8% Chegirma)",
        "is_popular": True,
        "short_desc": "Moddalar almashinuvini (metabolizm) to'liq qayta yuklash, oshqozon-ichak trakti (JKT) faoliyatini normallashtirish va mustahkam natija.",
        "daily_set": [
            "Block Fit Detox Tea (2 saşe kunlik)",
            "Detox Kofe (1 saşe energiya va yog' yoqish)",
            "Yashil Parashok Kunlik Kompleks"
        ]
    },
    {
        "id": "course-20-days",
        "name": "20 Kunlik Maksimal Kompleks Transformatsiya",
        "days": 20,
        "base_price": 1480000,
        "discount_percent": 10,
        "final_price": 1332000,
        "badge": "Super Natija (10% Chegirma)",
        "is_popular": False,
        "short_desc": "To'liq tana yangilanishi, chuqur yog' qatlamlarini eritish, yoshartirish va metabolizmni maksimal tezlashtirish.",
        "daily_set": [
            "Block Fit Detox Tea (To'liq kurs)",
            "Detox Kofe (To'liq kurs)",
            "Yashil Parashok Fit To'plami",
            "Shaxsiy Nigora AI 24/7 nazorat hamrohligi"
        ]
    }
]

PRODUCTS = [
    {
        "id": "block-fit-tea",
        "name": "BLOCK FIT DETOX Tea (Premium Formula)",
        "category": "Detox Choy",
        "image": "/static/media_1791473015839.jpg",
        "package_info": "3g x 10 saşe germetik paketlarda",
        "target": "Ichaklarni tozalash, ich qotishni yo'qotish, toksinlarni haydash",
        "description": "Tabiiy o'simliklar asosidagi maxsus formula. Oshqozon-ichak faoliyatini yumshoq yaxshilaydi, shishlarni ketkazadi va qorin sohasidagi ortiqcha santimetrlarni qisqartiradi."
    },
    {
        "id": "detox-coffee",
        "name": "Detox Energy Coffee (Zanjabil & L-Karnitin)",
        "category": "Detox Kofe",
        "image": "/static/media_1791472996762.png",
        "package_info": "Kunlik porsiya (qaynoq suvda damlanadi)",
        "target": "Yog' yoqish, energiya berish, ishtahani bloklash",
        "description": "Ertalabki metabolizmni uyg'otuvchi va tanadagi chuqur yog' to'qimalarini eritishga yo'naltirilgan xushbo'y tabiiy kofe kompleksi."
    },
    {
        "id": "green-powder",
        "name": "Yashil Fit Parashok (Detox Kasha)",
        "category": "Fit Kasha / Parashok",
        "image": "/static/media_1791472996762.png",
        "package_info": "Kuniga 2 mahal iste'mol qilinadi",
        "target": "Kletchatka, to'qlik hissi, ichki organlarni shlaklardan tozalash",
        "description": "Suvga solinib bo'tqa (kasha) holatida ichiladi. Oshqozonni to'ldirib, ortiqcha ovqatlanishdan saqlaydi va ichki mikroflorani tiklaydi."
    }
]

DAILY_SCHEDULE = [
    {
        "step": 1,
        "time": "07:00",
        "title": "Hojatxonaga kirish",
        "desc": "Tongda uyg'ongach darhol ichaklarni bo'shatish zarur.",
        "icon": "🚽"
    },
    {
        "step": 2,
        "time": "07:15",
        "title": "Bir qultum suv ichmasdan taroziga chiqish",
        "desc": "Tarozini kafelga (tekis qattiq joyga) qo'ying va och qoringa vazningizni o'lchab qayd qiling.",
        "icon": "⚖️"
    },
    {
        "step": 3,
        "time": "07:30",
        "title": "Yashil Parashok (Kasha holatida)",
        "desc": "Yashil parashokni idishga solib, ustiga suv quyib kasha holatida tayyorlab ichasiz. Orqasidan yarim piyola iliq suv iching. Yarim soatdan keyin yana iliq suv sekin-sekin ho'plab ichiladi.",
        "icon": "🥣"
    },
    {
        "step": 4,
        "time": "09:30",
        "title": "Qo'lingizdagi Kofe (2 soatdan keyin)",
        "desc": "Yarim piyola qaynoq suvda tayyorlab ichasiz. Kofedan keyin chanqasangiz, yarim soatdan so'ng iliq suv iching.",
        "icon": "☕"
    },
    {
        "step": 5,
        "time": "11:30 - 12:30",
        "title": "To'yimli Tushlik",
        "desc": "2 ta qaynatilgan tuxum oqi + ozgina go'sht (tovuq yoki mol go'shti) + 2 ta bodring. Ovqatdan keyin paketdagi choyni damlab iching.",
        "icon": "🥩"
    },
    {
        "step": 6,
        "time": "13:00 - 15:00",
        "title": "Perekus (Soat 15:00 gacha ruxsat)",
        "desc": "Faqat ruxsat etilgan mevalar: Yashil olma, apelsin, kivi, bodring, nok.",
        "icon": "🍏"
    },
    {
        "step": 7,
        "time": "16:00",
        "title": "2-marta Yashil Parashok",
        "desc": "Parashokni og'izga solib, orqasidan yarim piyola iliq suv ichasiz. 30 daqiqadan keyin yana iliq suv ho'plang.",
        "icon": "🥄"
    },
    {
        "step": 8,
        "time": "18:00",
        "title": "Kechki Yengil Taom",
        "desc": "Mumkin bo'lgan ovqatlardan iste'mol qilasiz (dimlangan go'sht, baliq, qaynatilgan tuxum oqi, salat).",
        "icon": "🥗"
    },
    {
        "step": 9,
        "time": "21:00",
        "title": "Kun oxirida Paketdagi Choy",
        "desc": "Block Fit Detox Tea choyini damlab xotirjam ichasiz. U kechasi bilan oshqozon va yog'larni eritish ustida ishlaydi.",
        "icon": "🍵"
    }
]

ALLOWED_FOODS = [
    {"name": "Bodring", "category": "Sabzavot", "calories": "15 kkal"},
    {"name": "Apelsin", "category": "Meva", "calories": "47 kkal"},
    {"name": "Kivi", "category": "Meva", "calories": "61 kkal"},
    {"name": "Nok", "category": "Meva", "calories": "57 kkal"},
    {"name": "Lavlagi", "category": "Sabzavot", "calories": "43 kkal"},
    {"name": "Yashil Olma", "category": "Meva", "calories": "52 kkal"},
    {"name": "Mol go'shti (yog'siz)", "category": "Protein", "calories": "140 kkal"},
    {"name": "Baqlajon", "category": "Sabzavot", "calories": "25 kkal"},
    {"name": "Ko'katlar (kashnich, shivit, kashnich)", "category": "Ko'kat", "calories": "20 kkal"},
    {"name": "Tovuq go'shti (ko'krak qismi)", "category": "Protein", "calories": "120 kkal"},
    {"name": "Brokkoli (Birkling)", "category": "Sabzavot", "calories": "34 kkal"},
    {"name": "Gul karam", "category": "Sabzavot", "calories": "25 kkal"},
    {"name": "Jigar", "category": "Protein", "calories": "130 kkal"},
    {"name": "Zaytun yog'i (bir necha tomchi)", "category": "Yog'", "calories": "80 kkal"},
    {"name": "Go'sht say", "category": "Issiq taom", "calories": "150 kkal"},
    {"name": "Tovuq file", "category": "Protein", "calories": "110 kkal"},
    {"name": "Lavlagili uy soki", "category": "Ichimlik", "calories": "40 kkal"},
    {"name": "Qulupnay", "category": "Meva", "calories": "33 kkal"},
    {"name": "Tuxum oqi (faqat oqi!)", "category": "Protein", "calories": "17 kkal"},
    {"name": "Baliqning hamma turlari", "category": "Protein", "calories": "100 kkal"},
    {"name": "Apelsin yangi siqilgan soki", "category": "Ichimlik", "calories": "45 kkal"},
    {"name": "Yashil olma soki", "category": "Ichimlik", "calories": "46 kkal"},
    {"name": "Qulupnay va lavlagi aralashmasi", "category": "Ichimlik", "calories": "42 kkal"}
]

class OrderCreateRequest(BaseModel):
    customer_name: str
    phone: str
    region: str
    address: str
    course_id: str
    delivery_note: Optional[str] = ""

class AIChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    user_context: Optional[Dict[str, Any]] = None

class ClickPrepareRequest(BaseModel):
    click_trans_id: int
    service_id: int
    click_paydoc_id: int
    merchant_trans_id: str
    amount: float
    action: int
    error: int
    error_note: str
    sign_time: str
    sign_string: str

@app.get("/api/catalog")
def get_catalog():
    return {
        "courses": COURSES,
        "products": PRODUCTS,
        "daily_schedule": DAILY_SCHEDULE,
        "allowed_foods": ALLOWED_FOODS,
        "consultant": {
            "name": "Nigora",
            "title": "Detoks & Sog'lom ozish bo'yicha ekspert",
            "avatar": "/static/media_1791472969574.png",
            "status": "Online (24/7 yordamda)"
        }
    }

@app.post("/api/orders")
def create_order(req: OrderCreateRequest):
    course = next((c for c in COURSES if c["id"] == req.course_id), None)
    if not course:
        raise HTTPException(status_code=400, detail="Noto'g'ri kurs tanlandi!")

    order_id = f"NIG-{datetime.datetime.now().strftime('%y%m%d')}-{uuid.uuid4().hex[:5].upper()}"
    new_order = {
        "order_id": order_id,
        "created_at": datetime.datetime.now().isoformat(),
        "customer_name": req.customer_name,
        "phone": req.phone,
        "region": req.region,
        "address": req.address,
        "course_id": course["id"],
        "course_name": course["name"],
        "course_days": course["days"],
        "base_price": course["base_price"],
        "discount_percent": course["discount_percent"],
        "final_price": course["final_price"],
        "status": "waiting_payment",
        "delivery_note": req.delivery_note,
        "payment_method": "Click"
    }

    orders = load_json(ORDERS_FILE, [])
    orders.append(new_order)
    save_json(ORDERS_FILE, orders)

    service_id = "55512"
    merchant_id = "22134"
    click_url = f"https://my.click.uz/services/pay?service_id={service_id}&merchant_id={merchant_id}&amount={new_order['final_price']}&transaction_param={order_id}&return_url=https://nigora-detox.uz/order-success?order_id={order_id}"

    return {
        "status": "success",
        "order": new_order,
        "click_url": click_url,
        "message": f"Buyurtma qabul qilindi! To'lov miqdori: {new_order['final_price']:,} so'm".replace(",", " ")
    }

@app.get("/api/orders")
def get_orders():
    orders = load_json(ORDERS_FILE, [])
    return {"orders": list(reversed(orders))}

@app.patch("/api/orders/{order_id}/status")
def update_order_status(order_id: str, payload: Dict[str, str]):
    new_status = payload.get("status")
    orders = load_json(ORDERS_FILE, [])
    found = False
    for o in orders:
        if o["order_id"] == order_id:
            o["status"] = new_status
            found = True
            break
    if not found:
        raise HTTPException(status_code=404, detail="Order topilmadi")
    save_json(ORDERS_FILE, orders)
    return {"status": "success", "order_id": order_id, "new_status": new_status}

@app.post("/api/click/prepare")
def click_prepare(req: ClickPrepareRequest):
    orders = load_json(ORDERS_FILE, [])
    order = next((o for o in orders if o["order_id"] == req.merchant_trans_id), None)
    if not order:
        return {"error": -5, "error_note": "User/Order does not exist"}
    if abs(float(req.amount) - float(order["final_price"])) > 1.0:
        return {"error": -2, "error_note": "Incorrect parameter amount"}
    return {
        "click_trans_id": req.click_trans_id,
        "merchant_trans_id": req.merchant_trans_id,
        "merchant_prepare_id": int(datetime.datetime.now().timestamp()),
        "error": 0,
        "error_note": "Success"
    }

@app.post("/api/click/complete")
def click_complete(req: ClickPrepareRequest):
    orders = load_json(ORDERS_FILE, [])
    order = next((o for o in orders if o["order_id"] == req.merchant_trans_id), None)
    if not order:
        return {"error": -5, "error_note": "Order does not exist"}
    order["status"] = "paid"
    order["click_trans_id"] = req.click_trans_id
    order["paid_at"] = datetime.datetime.now().isoformat()
    save_json(ORDERS_FILE, orders)
    return {
        "click_trans_id": req.click_trans_id,
        "merchant_trans_id": req.merchant_trans_id,
        "merchant_confirm_id": int(datetime.datetime.now().timestamp()),
        "error": 0,
        "error_note": "Success"
    }

def nigora_ai_engine(user_msg: str, history: List[Dict[str, str]]) -> Dict[str, Any]:
    msg = user_msg.lower().strip()
    
    if any(w in msg for w in ["narx", "qancha", "nechpul", "summa", "narxi", "qimmat"]):
        return {
            "reply": """Salom azizam! 🌸 Men Nigoraman. Sizga hozirgi eng foydali kurslarimiz narxlarini ma'lum qilaman:

✨ **5 kunlik ekspress kurs:** 370 000 so'm ➔ **5% chegirma bilan: 351 500 so'm**
🔥 **10 kunlik to'liq kurs:** 740 000 so'm ➔ **8% chegirma bilan: 680 800 so'm** (Eng ko'p tanlanadigani!)
💎 **20 kunlik super transformatsiya:** 1 480 000 so'm ➔ **10% chegirma bilan: 1 332 000 so'm**

Butun O'zbekiston bo'ylab yetkazib beramiz! Siz necha kg vazn tashlashni reja qilyapsiz? Hozirgi vazningiz necha kg?""",
            "suggested_actions": ["10 kunlik kursga buyurtma", "Vaznim 75 kg, maslahat bering", "Ichish tartibini ko'rish"]
        }

    if any(w in msg for w in ["tartib", "qanday ichiladi", "ichish", "reja", "soat", "kasha", "parashok", "qachon"]):
        return {
            "reply": """Jonim, tartib juda oddiy va qat'iy intizom talab qiladi. Qarang:

⏰ **07:00** — Hojatxonaga kirasiz.
⚖️ **07:15** — Bir qultum ham suv ichmasdan, tarozini kafelga qo'yib o'lchanasiz.
🥣 **07:30** — **Yashil parashokni** idishga solib suv bilan kasha qilib ichasiz, orqasidan yarim piyola iliq suv.
☕ **09:30** — 2 soat o'tgach, **Detox Kofeni** yarim piyola qaynoq suvda ichasiz.
🥩 **11:30** — Tushlik: 2 ta tuxum oqi + go'sht + 2 bodring. Orqasidan **paketli choy**!
🍏 **15:00 gacha** — Perekus (yashil olma, kivi, nok, bodring).
🥄 **16:00** — 2-marta Yashil parashok + iliq suv.
🥗 **18:00** — Kechki yengil taom (go'sht/baliq).
🍵 **21:00** — Yotishdan oldin **Block Fit Choy**.

Hech qiyin joyi yo'q, kun bo'yi yoningizda bo'lib eslatib turaman! Buyurtma berishga tayyormisiz?""",
            "suggested_actions": ["Ruxsat etilgan taomlar ro'yxati", "10 kunlik kursni tanlash", "Men ham ozsam bo'ladimi?"]
        }

    if any(w in msg for w in ["ovqat", "nima yesam", "taom", "diyeta", "menyu", "mumkin"]):
        return {
            "reply": """Detoks paytida och qolmaysiz! Faqat to'g'ri mahsulotlarni yeysiz:

🥗 **Sabzavot va mevalar:** Bodring, yashil olma, kivi, nok, apelsin, lavlagi, brokkoli, gulkaram, baqlajon, yangi ko'katlar.
🍗 **Proteinlar:** Yog'siz mol go'shti, tovuq filesi, tovuq ko'kragi, qaynatilgan tuxum OQI (sarig'isiz!), baliqning barcha turlari, jigar.
🥤 **Ichimliklar:** O'zimiz uyda siqqan yangi soklar (apelsin, olma, lavlagi), toza iliq suv.

🚫 **Qat'iy taqiqlanadi:** Qand, non, pishiriqlar, qovurilgan yog'li taomlar, gazli ichimliklar!""",
            "suggested_actions": ["5 kunlik kurs", "10 kunlik kurs", "Yetkazib berish qancha?"]
        }

    if any(w in msg for w in ["homilador", "emizikli", "kasal", "mumkin emas", "yaramaydi", "zarar", "yosh"]):
        return {
            "reply": """Sog'lig'ingiz biz uchun birinchi o'rinda! 🌿
Quyidagi holatlarda kurs tavsiya etilmaydi:
- Homilador ayollar va 6 oygacha bo'lgan emizikli onalar;
- Oshqozon yarasining (yazva) o'tkir bosqichida bo'lganlar;
- Og'ir surunkali buyrak va jigar yetishmovchiligi bo'lganlar;
- 16 yoshdan kichiklar.

Agar sizda bunday holatlar bo'lmasa, metabolizmingizni tozalash va yengillashish uchun kursimiz 100% to'g'ri keladi!""",
            "suggested_actions": ["Menga to'g'ri keladi, buyurtma qilaman", "10 kunlik kurs narxi"]
        }

    if any(w in msg for w in ["necha kg", "ozaman", "natija", "kafolat", "kg", "ozish"]):
        return {
            "reply": """Mijozlarimizning 98% foizida tartibga 100% amal qilinganda:
- **5 kunlik kursda:** 2 kg dan 4 kg gacha shish va toksinlar ketadi.
- **10 kunlik kursda:** 4 kg dan 7 kg gacha metabolik vazn tashlanadi, oshqozon qisqaradi!
- **20 kunlik kursda:** 7 kg dan 12 kg gacha to'liq tana o'zgarishi yuz beradi.

Eng muhimi — qayta vazn to'planmaydi, chunki moddalar almashinuvini (JKT) joyiga qo'yib beramiz! Qaysi kursdan boshlaymiz?""",
            "suggested_actions": ["10 kunlik kursni tanlash", "5 kunlik bilan sinab ko'rish", "To'lov Click orqali"]
        }

    return {
        "reply": f"""Assalomu alaykum! Men Nigoraman — sizning shaxsiy detoks va ozish bo'yicha hamrohingizman 💖.

Sizga qaysi masala bo'yicha yordam beray?
1. Qaysi kurs sizning bo'yingiz va vazningizga eng mos kelishini hisoblab beraymi?
2. Kunlik 9 bosqichli ichish jadvalini tushuntiraymi?
3. 5, 10 yoki 20 kunlik to'plamga **10% gacha chegirma** bilan buyurtma beramizmi?

Savolingizni bering, batafsil yordam beraman!""",
        "suggested_actions": ["Narxlar va chegirmalar", "Kunlik ichish tartibi", "Buyurtma berish"]
    }

@app.post("/api/ai/chat")
def ai_chat(req: AIChatRequest):
    chats = load_json(CHATS_FILE, [])
    session_id = req.session_id or str(uuid.uuid4())
    
    user_record = {
        "id": str(uuid.uuid4()),
        "session_id": session_id,
        "sender": "user",
        "text": req.message,
        "timestamp": datetime.datetime.now().isoformat()
    }
    chats.append(user_record)

    engine_res = nigora_ai_engine(req.message, [])

    bot_record = {
        "id": str(uuid.uuid4()),
        "session_id": session_id,
        "sender": "nigora_ai",
        "text": engine_res["reply"],
        "suggested_actions": engine_res.get("suggested_actions", []),
        "timestamp": datetime.datetime.now().isoformat()
    }
    chats.append(bot_record)
    save_json(CHATS_FILE, chats)

    return {
        "session_id": session_id,
        "reply": engine_res["reply"],
        "suggested_actions": engine_res.get("suggested_actions", [])
    }

@app.get("/api/ai/chats")
def get_all_chats():
    chats = load_json(CHATS_FILE, [])
    return {"chats": list(reversed(chats))}

@app.get("/", response_class=HTMLResponse)
def index_page():
    index_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>NIGORA DETOX Marketplace API running</h1>"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
