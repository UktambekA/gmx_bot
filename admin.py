# admin.py
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from html import escape

# Logging sozlamalari
logger = logging.getLogger(__name__)

# Admin holatlari
ADMIN_STATES = {
    "MAIN_MENU": "admin_main_menu",
    "PHARMACY_MENU": "admin_pharmacy_menu",
    "EMPLOYEE_MENU": "admin_employee_menu",
    "MEDICINE_MENU": "admin_medicine_menu",
    "ADD_PHARMACY_NAME": "admin_add_pharmacy_name",
    "ADD_PHARMACY_ADDRESS": "admin_add_pharmacy_address",
    "ADD_PHARMACY_INN": "admin_add_pharmacy_inn",
    "ADD_PHARMACY_OWNER": "admin_add_pharmacy_owner",
    "ADD_PHARMACY_CONTRACT": "admin_add_pharmacy_contract",
    "ADD_PHARMACY_DOGOVOR": "admin_add_pharmacy_dogovor",
    "ADD_PHARMACY_RS": "admin_add_pharmacy_rs",
    "ADD_PHARMACY_MFO": "admin_add_pharmacy_mfo",
    "ADD_PHARMACY_PHONE": "admin_add_pharmacy_phone",
    "EDIT_PHARMACY_SELECT": "admin_edit_pharmacy_select",
    "EDIT_PHARMACY_FIELD": "admin_edit_pharmacy_field",
    "DELETE_PHARMACY_SELECT": "admin_delete_pharmacy_select",
    "ADD_EMPLOYEE_NAME": "admin_add_employee_name",
    "ADD_EMPLOYEE_PHONE": "admin_add_employee_phone",
    "ADD_EMPLOYEE_POSITION": "admin_add_employee_position",
    "EDIT_EMPLOYEE_SELECT": "admin_edit_employee_select",
    "EDIT_EMPLOYEE_FIELD": "admin_edit_employee_field",
    "DELETE_EMPLOYEE_SELECT": "admin_delete_employee_select",
    "ADD_MEDICINE_NAME": "admin_add_medicine_name",
    "ADD_MEDICINE_PRICE": "admin_add_medicine_price",
    "ADD_MEDICINE_IKPU": "admin_add_medicine_ikpu",
    "ADD_MEDICINE_IMAGE": "admin_add_medicine_image",
    "ADD_MEDICINE_INFO": "admin_add_medicine_info",
    "EDIT_MEDICINE_SELECT": "admin_edit_medicine_select",
    "EDIT_MEDICINE_FIELD": "admin_edit_medicine_field",
    "DELETE_MEDICINE_SELECT": "admin_delete_medicine_select",
    "VIEW_PHARMACIES": "admin_view_pharmacies",
    "VIEW_EMPLOYEES": "admin_view_employees",
    "VIEW_MEDICINES": "admin_view_medicines",
}

# Admin ID'lari (Bu yerga adminlarning Telegram user ID'larini qo'ying)
ADMIN_IDS = [7178547244, 6825463456] # Misol uchun, o'zingizning ID'ingizni qo'ying

# Admin paneli klaviaturalari
def get_admin_main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🏥 Дорихоналар", callback_data="admin_pharmacy_menu")],
        [InlineKeyboardButton("👤 Ходимлар", callback_data="admin_employee_menu")],
        [InlineKeyboardButton("💊 Дорилар", callback_data="admin_medicine_menu")],
        [InlineKeyboardButton("🚪 Чиқиш", callback_data="admin_exit")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_admin_pharmacy_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("➕ Дорихона қўшиш", callback_data="admin_add_pharmacy")],
        # [InlineKeyboardButton("✏️ Дорихона таҳрирлаш", callback_data="admin_edit_pharmacy")],
        # [InlineKeyboardButton("🗑️ Дорихона ўчириш", callback_data="admin_delete_pharmacy")],
        # [InlineKeyboardButton("📋 Барча дорихоналар", callback_data="admin_view_pharmacies")],
        [InlineKeyboardButton("🔙 Орқага", callback_data="admin_main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_admin_employee_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("➕ Ходим қўшиш", callback_data="admin_add_employee")],
        [InlineKeyboardButton("✏️ Ходим таҳрирлаш", callback_data="admin_edit_employee")],
        [InlineKeyboardButton("🗑️ Ходим ўчириш", callback_data="admin_delete_employee")],
        [InlineKeyboardButton("📋 Барча ходимлар", callback_data="admin_view_employees")],
        [InlineKeyboardButton("🔙 Орқага", callback_data="admin_main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_admin_medicine_menu_keyboard():
    keyboard = [
        # [InlineKeyboardButton("➕ Дори қўшиш", callback_data="admin_add_medicine")],
        [InlineKeyboardButton("✏️ Дори таҳрирлаш", callback_data="admin_edit_medicine")],
        [InlineKeyboardButton("🗑️ Дори ўчириш", callback_data="admin_delete_medicine")],
        [InlineKeyboardButton("📋 Барча дорилар", callback_data="admin_view_medicines")],
        [InlineKeyboardButton("🔙 Орқага", callback_data="admin_main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_to_main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔙 Асосий менюга", callback_data="admin_main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_to_pharmacy_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔙 Дорихона менюсига", callback_data="admin_pharmacy_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_to_employee_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔙 Ходимлар менюсига", callback_data="admin_employee_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_to_medicine_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔙 Дорилар менюсига", callback_data="admin_medicine_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Admin buyruqlarini qayta ishlash
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("Сизда бу функциядан фойдаланиш ҳуқуқи йўқ.")
        return

    context.user_data['admin_state'] = ADMIN_STATES["MAIN_MENU"]
    await update.message.reply_text(
        "👨‍💻 Админ панелига хуш келибсиз!",
        reply_markup=get_admin_main_menu_keyboard()
    )

async def admin_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data

    await query.answer()

    if user_id not in ADMIN_IDS:
        await query.edit_message_text("Сизда бу функциядан фойдаланиш ҳуқуқи йўқ.")
        return

    current_state = context.user_data.get('admin_state')

    # Asosiy menyu navigatsiyasi
    if data == "admin_main_menu":
        context.user_data['admin_state'] = ADMIN_STATES["MAIN_MENU"]
        await query.edit_message_text(
            "👨‍💻 Админ панели",
            reply_markup=get_admin_main_menu_keyboard()
        )
    elif data == "admin_pharmacy_menu":
        context.user_data['admin_state'] = ADMIN_STATES["PHARMACY_MENU"]
        await query.edit_message_text(
            "🏥 Дорихоналарни бошқариш",
            reply_markup=get_admin_pharmacy_menu_keyboard()
        )
    elif data == "admin_employee_menu":
        context.user_data['admin_state'] = ADMIN_STATES["EMPLOYEE_MENU"]
        await query.edit_message_text(
            "👤 Ходимларни бошқариш",
            reply_markup=get_admin_employee_menu_keyboard()
        )
    elif data == "admin_medicine_menu":
        context.user_data['admin_state'] = ADMIN_STATES["MEDICINE_MENU"]
        await query.edit_message_text(
            "💊 Дориларни бошқариш",
            reply_markup=get_admin_medicine_menu_keyboard()
        )
    elif data == "admin_exit":
        context.user_data['admin_state'] = None
        await query.edit_message_text(
            "🚪 Админ панелидан чиқдингиз.",
            reply_markup=None
        )
        # Foydalanuvchi botning asosiy menyusiga qaytishi uchun
        # await query.message.reply_text("Асосий менюга қайтиш учун /start буйруғини юборинг.")
        return

    # --- Дорихоналарни бошқариш ---
    elif data == "admin_add_pharmacy":
        context.user_data['admin_state'] = ADMIN_STATES["ADD_PHARMACY_NAME"]
        context.user_data['new_pharmacy_data'] = {}
        await query.edit_message_text(
            "➕ Янги дорихона номини киритинг:",
            reply_markup=get_back_to_pharmacy_menu_keyboard()
        )
    elif data == "admin_edit_pharmacy":
        context.user_data['admin_state'] = ADMIN_STATES["EDIT_PHARMACY_SELECT"]
        pharmacies = context.bot_data['db_manager'].get_all_pharmacies()
        if not pharmacies:
            await query.edit_message_text("Таҳрирлаш учун дорихоналар мавжуд эмас.", reply_markup=get_back_to_pharmacy_menu_keyboard())
            return
        
        keyboard = []
        for p in pharmacies:
            keyboard.append([InlineKeyboardButton(f"{p['dorixona_nomi']} (ИНН: {p['inn']})", callback_data=f"edit_pharmacy_{p['id']}")])
        keyboard.append([InlineKeyboardButton("🔙 Орқага", callback_data="admin_pharmacy_menu")])
        
        await query.edit_message_text(
            "✏️ Таҳрирлаш учун дорихонани танланг:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif data.startswith("edit_pharmacy_") and current_state == ADMIN_STATES["EDIT_PHARMACY_SELECT"]:
        pharmacy_id = int(data.split("_")[2])
        pharmacy = next((p for p in context.bot_data['db_manager'].get_all_pharmacies() if p['id'] == pharmacy_id), None)
        if not pharmacy:
            await query.edit_message_text("Дорихона топилмади.", reply_markup=get_back_to_pharmacy_menu_keyboard())
            return
        
        context.user_data['editing_pharmacy_id'] = pharmacy_id
        context.user_data['admin_state'] = ADMIN_STATES["EDIT_PHARMACY_FIELD"]
        
        keyboard = [
            [InlineKeyboardButton(f"Номи: {pharmacy['dorixona_nomi']}", callback_data="edit_pharmacy_field_dorixona_nomi")],
            [InlineKeyboardButton(f"Манзили: {pharmacy['manzil']}", callback_data="edit_pharmacy_field_manzil")],
            [InlineKeyboardButton(f"ИНН: {pharmacy['inn']}", callback_data="edit_pharmacy_field_inn")],
            [InlineKeyboardButton(f"Эгаси: {pharmacy['dorixona_egasi']}", callback_data="edit_pharmacy_field_dorixona_egasi")],
            [InlineKeyboardButton(f"Телефон: {pharmacy['kontrakt']}", callback_data="edit_pharmacy_field_kontrakt")],
            [InlineKeyboardButton(f"Договор: {pharmacy['dagovor']}", callback_data="edit_pharmacy_field_dagovor")],
            [InlineKeyboardButton(f"Р/с: {pharmacy['rs']}", callback_data="edit_pharmacy_field_rs")],
            [InlineKeyboardButton(f"МФО: {pharmacy['mfo']}", callback_data="edit_pharmacy_field_mfo")],
            [InlineKeyboardButton("🔙 Орқага", callback_data="admin_edit_pharmacy")]
        ]
        await query.edit_message_text(
            f"✏️ *{escape(pharmacy['dorixona_nomi'])}* дорихонаси учун қайси майдонни таҳрирлайсиз?",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif data.startswith("edit_pharmacy_field_") and current_state == ADMIN_STATES["EDIT_PHARMACY_FIELD"]:
        field_name = data.split("_")[3]
        context.user_data['editing_field_name'] = field_name
        context.user_data['admin_state'] = f"admin_edit_pharmacy_value_{field_name}" # Yangi holat
        await query.edit_message_text(
            f"📝 Янги қийматни киритинг: *{field_name}*",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_back_to_pharmacy_menu_keyboard() # Orqaga tugmasi
        )
    elif data == "admin_delete_pharmacy":
        context.user_data['admin_state'] = ADMIN_STATES["DELETE_PHARMACY_SELECT"]
        pharmacies = context.bot_data['db_manager'].get_all_pharmacies()
        if not pharmacies:
            await query.edit_message_text("Ўчириш учун дорихоналар мавжуд эмас.", reply_markup=get_back_to_pharmacy_menu_keyboard())
            return
        
        keyboard = []
        for p in pharmacies:
            keyboard.append([InlineKeyboardButton(f"{p['dorixona_nomi']} (ИНН: {p['inn']})", callback_data=f"delete_pharmacy_{p['id']}")])
        keyboard.append([InlineKeyboardButton("🔙 Орқага", callback_data="admin_pharmacy_menu")])
        
        await query.edit_message_text(
            "🗑️ Ўчириш учун дорихонани танланг:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif data.startswith("delete_pharmacy_") and current_state == ADMIN_STATES["DELETE_PHARMACY_SELECT"]:
        pharmacy_id = int(data.split("_")[2])
        # Tasdiqlash so'rash
        keyboard = [
            [InlineKeyboardButton("✅ Ҳа, ўчириш", callback_data=f"confirm_delete_pharmacy_{pharmacy_id}")],
            [InlineKeyboardButton("❌ Йўқ, бекор қилиш", callback_data="admin_delete_pharmacy")]
        ]
        await query.edit_message_text(
            "❓ Ростдан ҳам бу дорихонани ўчирмоқчимисиз?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif data.startswith("confirm_delete_pharmacy_"):
        pharmacy_id = int(data.split("_")[3])
        success = context.bot_data['db_manager'].delete_pharmacy(pharmacy_id) # delete_pharmacy funksiyasini qo'shish kerak
        if success:
            await query.edit_message_text("✅ Дорихона муваффақиятли ўчирилди.", reply_markup=get_back_to_pharmacy_menu_keyboard())
        else:
            await query.edit_message_text("❌ Дорихонани ўчиришда хатолик юз берди.", reply_markup=get_back_to_pharmacy_menu_keyboard())
        context.user_data['admin_state'] = ADMIN_STATES["PHARMACY_MENU"]
    # elif data == "admin_view_pharmacies":
    #     pharmacies = context.bot_data['db_manager'].get_all_pharmacies()
    #     if not pharmacies:
    #         await query.edit_message_text("Дорихоналар мавжуд эмас.", reply_markup=get_back_to_pharmacy_menu_keyboard())
    #         return
        
    #     message_text = "🏥 *Барча дорихоналар:*\n\n"
    #     for p in pharmacies:
    #         message_text += f"*{escape(p['dorixona_nomi'])}*\n"
    #         message_text += f"  Манзил: {escape(p['manzil'])}\n"
    #         message_text += f"  ИНН: `{escape(p['inn'])}`\n"
    #         message_text += f"  Эгаси: {escape(p['dorixona_egasi'])}\n"
    #         message_text += f"  Телефон: {escape(p['kontrakt'])}\n"
    #         message_text += f"  Договор: {escape(p['dagovor'])}\n"
    #         message_text += f"  Р/с: {escape(p['rs'])}\n"
    #         message_text += f"  МФО: {escape(str(p['mfo']))}\n"
        
    #     await query.edit_message_text(
    #         message_text,
    #         parse_mode=ParseMode.MARKDOWN,
    #         reply_markup=get_back_to_pharmacy_menu_keyboard()
    #     )

    # --- Ходимларни бошқариш ---
    elif data == "admin_add_employee":
        context.user_data['admin_state'] = ADMIN_STATES["ADD_EMPLOYEE_NAME"]
        context.user_data['new_employee_data'] = {}
        await query.edit_message_text(
            "➕ Янги ходимнинг исм-фамилиясини киритинг:",
            reply_markup=get_back_to_employee_menu_keyboard()
        )
    elif data == "admin_edit_employee":
        context.user_data['admin_state'] = ADMIN_STATES["EDIT_EMPLOYEE_SELECT"]
        employees = context.bot_data['db_manager'].get_all_employees() # get_all_employees funksiyasini qo'shish kerak
        if not employees:
            await query.edit_message_text("Таҳрирлаш учун ходимлар мавжуд эмас.", reply_markup=get_back_to_employee_menu_keyboard())
            return
        
        keyboard = []
        for e in employees:
            keyboard.append([InlineKeyboardButton(f"{e['ism_familiya']} ({e['telefon_raqam']})", callback_data=f"edit_employee_{e['id']}")])
        keyboard.append([InlineKeyboardButton("🔙 Орқага", callback_data="admin_employee_menu")])
        
        await query.edit_message_text(
            "✏️ Таҳрирлаш учун ходимни танланг:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif data.startswith("edit_employee_") and current_state == ADMIN_STATES["EDIT_EMPLOYEE_SELECT"]:
        employee_id = int(data.split("_")[2])
        employee = next((e for e in context.bot_data['db_manager'].get_all_employees() if e['id'] == employee_id), None)
        if not employee:
            await query.edit_message_text("Ходим топилмади.", reply_markup=get_back_to_employee_menu_keyboard())
            return
        
        context.user_data['editing_employee_id'] = employee_id
        context.user_data['admin_state'] = ADMIN_STATES["EDIT_EMPLOYEE_FIELD"]
        
        keyboard = [
            [InlineKeyboardButton(f"Исм-фамилия: {employee['ism_familiya']}", callback_data="edit_employee_field_ism_familiya")],
            [InlineKeyboardButton(f"Телефон рақам: {employee['telefon_raqam']}", callback_data="edit_employee_field_telefon_raqam")],
            # [InlineKeyboardButton(f"Лавозим: {employee['lavozim']}", callback_data="edit_employee_field_lavozim")],
            [InlineKeyboardButton("🔙 Орқага", callback_data="admin_edit_employee")]
        ]
        await query.edit_message_text(
            f"✏️ *{escape(employee['ism_familiya'])}* ходими учун қайси майдонни таҳрирлайсиз?",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif data.startswith("edit_employee_field_") and current_state == ADMIN_STATES["EDIT_EMPLOYEE_FIELD"]:
        field_name = data.split("_")[3]
        context.user_data['editing_field_name'] = field_name
        context.user_data['admin_state'] = f"admin_edit_employee_value_{field_name}" # Yangi holat
        await query.edit_message_text(
            f"📝 Янги қийматни киритинг: *{field_name}*",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_back_to_employee_menu_keyboard()
        )
    elif data == "admin_delete_employee":
        context.user_data['admin_state'] = ADMIN_STATES["DELETE_EMPLOYEE_SELECT"]
        employees = context.bot_data['db_manager'].get_all_employees()
        if not employees:
            await query.edit_message_text("Ўчириш учун ходимлар мавжуд эмас.", reply_markup=get_back_to_employee_menu_keyboard())
            return
        
        keyboard = []
        for e in employees:
            keyboard.append([InlineKeyboardButton(f"{e['ism_familiya']} ({e['telefon_raqam']})", callback_data=f"delete_employee_{e['id']}")])
        keyboard.append([InlineKeyboardButton("🔙 Орқага", callback_data="admin_employee_menu")])
        
        await query.edit_message_text(
            "🗑️ Ўчириш учун ходимни танланг:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif data.startswith("delete_employee_") and current_state == ADMIN_STATES["DELETE_EMPLOYEE_SELECT"]:
        employee_id = int(data.split("_")[2])
        # Tasdiqlash so'rash
        keyboard = [
            [InlineKeyboardButton("✅ Ҳа, ўчириш", callback_data=f"confirm_delete_employee_{employee_id}")],
            [InlineKeyboardButton("❌ Йўқ, бекор қилиш", callback_data="admin_delete_employee")]
        ]
        await query.edit_message_text(
            "❓ Ростдан ҳам бу ходимни ўчирмоқчимисиз?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif data.startswith("confirm_delete_employee_"):
        employee_id = int(data.split("_")[3])
        success = context.bot_data['db_manager'].delete_employee(employee_id) # delete_employee funksiyasini qo'shish kerak
        if success:
            await query.edit_message_text("✅ Ходим муваффақиятли ўчирилди.", reply_markup=get_back_to_employee_menu_keyboard())
        else:
            await query.edit_message_text("❌ Ходимни ўчиришда хатолик юз берди.", reply_markup=get_back_to_employee_menu_keyboard())
        context.user_data['admin_state'] = ADMIN_STATES["EMPLOYEE_MENU"]
    elif data == "admin_view_employees":
        employees = context.bot_data['db_manager'].get_all_employees()
        if not employees:
            await query.edit_message_text("Ходимлар мавжуд эмас.", reply_markup=get_back_to_employee_menu_keyboard())
            return
        
        message_text = "👤 *Барча ходимлар:*\n\n"
        for e in employees:
            message_text += f"*{escape(e['ism_familiya'])}*\n"
            message_text += f"  Телефон: `{escape(e['telefon_raqam'])}`\n"
            # message_text += f"  Лавозим: {escape(e['lavozim'])}\n\n"
        
        await query.edit_message_text(
            message_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_back_to_employee_menu_keyboard()
        )

    # --- Дориларни бошқариш ---
    elif data == "admin_add_medicine":
        context.user_data['admin_state'] = ADMIN_STATES["ADD_MEDICINE_NAME"]
        context.user_data['new_medicine_data'] = {}
        await query.edit_message_text(
            "➕ Янги дори номини киритинг:",
            reply_markup=get_back_to_medicine_menu_keyboard()
        )
    elif data == "admin_edit_medicine":
        context.user_data['admin_state'] = ADMIN_STATES["EDIT_MEDICINE_SELECT"]
        medicines = context.bot_data['db_manager'].get_all_medicines()
        if not medicines:
            await query.edit_message_text("Таҳрирлаш учун дорилар мавжуд эмас.", reply_markup=get_back_to_medicine_menu_keyboard())
            return
        
        keyboard = []
        for m in medicines:
            keyboard.append([InlineKeyboardButton(f"{m['dori_nomi']} ({m['narxi']} so'm)", callback_data=f"edit_medicine_{m['id']}")])
        keyboard.append([InlineKeyboardButton("🔙 Орқага", callback_data="admin_medicine_menu")])
        
        await query.edit_message_text(
            "✏️ Таҳрирлаш учун дорини танланг:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif data.startswith("edit_medicine_") and current_state == ADMIN_STATES["EDIT_MEDICINE_SELECT"]:
        medicine_id = int(data.split("_")[2])
        medicine = next((m for m in context.bot_data['db_manager'].get_all_medicines() if m['id'] == medicine_id), None)
        if not medicine:
            await query.edit_message_text("Дори топилмади.", reply_markup=get_back_to_medicine_menu_keyboard())
            return
        
        context.user_data['editing_medicine_id'] = medicine_id
        context.user_data['admin_state'] = ADMIN_STATES["EDIT_MEDICINE_FIELD"]
        
        keyboard = [
            [InlineKeyboardButton(f"Номи: {medicine['dori_nomi']}", callback_data="edit_medicine_field_dori_nomi")],
            [InlineKeyboardButton(f"Нархи: {medicine['narxi']}", callback_data="edit_medicine_field_narxi")],
            [InlineKeyboardButton(f"ИКПУ: {medicine['ikpu']}", callback_data="edit_medicine_field_ikpu")],
            # [InlineKeyboardButton(f"Расм ID: {medicine['image_file_id'] or 'Йўқ'}", callback_data="edit_medicine_field_image_file_id")],
            [InlineKeyboardButton(f"Маълумот: {medicine['info'] or 'Йўқ'}", callback_data="edit_medicine_field_info")],
            [InlineKeyboardButton("🔙 Орқага", callback_data="admin_edit_medicine")]
        ]
        await query.edit_message_text(
            f"✏️ *{escape(medicine['dori_nomi'])}* дориси учун қайси майдонни таҳрирлайсиз?",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif data.startswith("edit_medicine_field_") and current_state == ADMIN_STATES["EDIT_MEDICINE_FIELD"]:
        field_name = data.split("_")[3]
        context.user_data['editing_field_name'] = field_name
        context.user_data['admin_state'] = f"admin_edit_medicine_value_{field_name}" # Yangi holat
        await query.edit_message_text(
            f"📝 Янги қийматни киритинг: *{field_name}*",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_back_to_medicine_menu_keyboard()
        )
    elif data == "admin_delete_medicine":
        context.user_data['admin_state'] = ADMIN_STATES["DELETE_MEDICINE_SELECT"]
        medicines = context.bot_data['db_manager'].get_all_medicines()
        if not medicines:
            await query.edit_message_text("Ўчириш учун дорилар мавжуд эмас.", reply_markup=get_back_to_medicine_menu_keyboard())
            return
        
        keyboard = []
        for m in medicines:
            keyboard.append([InlineKeyboardButton(f"{m['dori_nomi']} ({m['narxi']} so'm)", callback_data=f"delete_medicine_{m['id']}")])
        keyboard.append([InlineKeyboardButton("🔙 Орқага", callback_data="admin_medicine_menu")])
        
        await query.edit_message_text(
            "🗑️ Ўчириш учун дорини танланг:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif data.startswith("delete_medicine_") and current_state == ADMIN_STATES["DELETE_MEDICINE_SELECT"]:
        medicine_id = int(data.split("_")[2])
        # Tasdiqlash so'rash
        keyboard = [
            [InlineKeyboardButton("✅ Ҳа, ўчириш", callback_data=f"confirm_delete_medicine_{medicine_id}")],
            [InlineKeyboardButton("❌ Йўқ, бекор қилиш", callback_data="admin_delete_medicine")]
        ]
        await query.edit_message_text(
            "❓ Ростдан ҳам бу дорини ўчирмоқчимисиз?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif data.startswith("confirm_delete_medicine_"):
        medicine_id = int(data.split("_")[3])
        success = context.bot_data['db_manager'].delete_medicine(medicine_id) # delete_medicine funksiyasini qo'shish kerak
        if success:
            await query.edit_message_text("✅ Дори муваффақиятли ўчирилди.", reply_markup=get_back_to_medicine_menu_keyboard())
        else:
            await query.edit_message_text("❌ Дорини ўчиришда хатолик юз берди.", reply_markup=get_back_to_medicine_menu_keyboard())
        context.user_data['admin_state'] = ADMIN_STATES["MEDICINE_MENU"]
    elif data == "admin_view_medicines":
        medicines = context.bot_data['db_manager'].get_all_medicines()
        if not medicines:
            await query.edit_message_text("Дорилар мавжуд эмас.", reply_markup=get_back_to_medicine_menu_keyboard())
            return
        
        message_text = "💊 *Барча дорилар:*\n\n"
        for m in medicines:
            message_text += f"*{escape(m['dori_nomi'])}*\n"
            message_text += f"  Нархи: {m['narxi']:,} so'm\n"
            message_text += f"  ИКПУ: `{escape(m['ikpu'])}`\n"
            # message_text += f"  Расм ID: `{escape(m['image_file_id'] or 'Йўқ')}`\n"
            message_text += f"  Маълумот: {escape(m['info'] or 'Йўқ')}\n\n"
        
        await query.edit_message_text(
            message_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_back_to_medicine_menu_keyboard()
        )

    # --- Matnli xabarlarni qayta ishlash (admin holatida) ---
async def admin_handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    
    if user_id not in ADMIN_IDS:
        return # Admin bo'lmagan foydalanuvchilarning xabarlarini e'tiborsiz qoldirish
    
    current_state = context.user_data.get('admin_state')
    
    # Дорихона қўшиш
    if current_state == ADMIN_STATES["ADD_PHARMACY_NAME"]:
        context.user_data['new_pharmacy_data']['dorixona_nomi'] = text
        context.user_data['admin_state'] = ADMIN_STATES["ADD_PHARMACY_ADDRESS"]
        await update.message.reply_text("Манзилни киритинг:", reply_markup=get_back_to_pharmacy_menu_keyboard())
    elif current_state == ADMIN_STATES["ADD_PHARMACY_ADDRESS"]:
        context.user_data['new_pharmacy_data']['manzil'] = text
        context.user_data['admin_state'] = ADMIN_STATES["ADD_PHARMACY_INN"]
        await update.message.reply_text("ИНН рақамини киритинг:", reply_markup=get_back_to_pharmacy_menu_keyboard())
    elif current_state == ADMIN_STATES["ADD_PHARMACY_INN"]:
        context.user_data['new_pharmacy_data']['inn'] = text
        context.user_data['admin_state'] = ADMIN_STATES["ADD_PHARMACY_OWNER"]
        await update.message.reply_text("Дорихона эгасининг исмини киритинг:", reply_markup=get_back_to_pharmacy_menu_keyboard())
    elif current_state == ADMIN_STATES["ADD_PHARMACY_OWNER"]:
        context.user_data['new_pharmacy_data']['dorixona_egasi'] = text
        context.user_data['admin_state'] = ADMIN_STATES["ADD_PHARMACY_CONTRACT"]
        await update.message.reply_text("Контакт рақамини киритинг:", reply_markup=get_back_to_pharmacy_menu_keyboard())
    elif current_state == ADMIN_STATES["ADD_PHARMACY_CONTRACT"]:
        context.user_data['new_pharmacy_data']['kontrakt'] = text
        context.user_data['admin_state'] = ADMIN_STATES["ADD_PHARMACY_DOGOVOR"]
        await update.message.reply_text("Договор рақамини киритинг:", reply_markup=get_back_to_pharmacy_menu_keyboard())
    elif current_state == ADMIN_STATES["ADD_PHARMACY_DOGOVOR"]:
        context.user_data['new_pharmacy_data']['dagovor'] = text
        context.user_data['admin_state'] = ADMIN_STATES["ADD_PHARMACY_RS"]
        await update.message.reply_text("Р/с рақамини киритинг:", reply_markup=get_back_to_pharmacy_menu_keyboard())
    elif current_state == ADMIN_STATES["ADD_PHARMACY_RS"]:
        context.user_data['new_pharmacy_data']['rs'] = text
        context.user_data['admin_state'] = ADMIN_STATES["ADD_PHARMACY_MFO"]
        await update.message.reply_text("МФО рақамини киритинг:", reply_markup=get_back_to_pharmacy_menu_keyboard())
    elif current_state == ADMIN_STATES["ADD_PHARMACY_MFO"]:
        context.user_data['new_pharmacy_data']['mfo'] = text
    #     # context.user_data['admin_state'] = ADMIN_STATES["ADD_PHARMACY_PHONE"]
    #     # await update.message.reply_text("Телефон рақамини киритинг:", reply_markup=get_back_to_pharmacy_menu_keyboard())
    # elif current_state == ADMIN_STATES["ADD_PHARMACY_PHONE"]:
    #     context.user_data['new_pharmacy_data']['telefon'] = text
        
        new_pharmacy = context.user_data['new_pharmacy_data']
        success = context.bot_data['db_manager'].add_pharmacy(new_pharmacy) # add_pharmacy funksiyasini qo'shish kerak
        
        if success:
            await update.message.reply_text("✅ Дорихона муваффақиятли қўшилди!", reply_markup=get_admin_pharmacy_menu_keyboard())
        else:
            await update.message.reply_text("❌ Дорихонани қўшишда хатолик юз берди.", reply_markup=get_admin_pharmacy_menu_keyboard())
        context.user_data['admin_state'] = ADMIN_STATES["PHARMACY_MENU"]
        context.user_data.pop('new_pharmacy_data', None)

    # # Дорихона таҳрирлаш қийматини киритиш
    # elif current_state and current_state.startswith("admin_edit_pharmacy_value_"):
    #     field_name = current_state.replace("admin_edit_pharmacy_value_", "")
    #     pharmacy_id = context.user_data.get('editing_pharmacy_id')
        
    #     success = context.bot_data['db_manager'].update_pharmacy(pharmacy_id, field_name, text) # update_pharmacy funksiyasini qo'shish kerak
        
    #     if success:
    #         await update.message.reply_text(f"✅ Дорихонанинг '{field_name}' майдони муваффақиятли таҳрирланди.", reply_markup=get_admin_pharmacy_menu_keyboard())
    #     else:
    #         await update.message.reply_text(f"❌ Дорихонанинг '{field_name}' майдонини таҳрирлашда хатолик юз берди.", reply_markup=get_admin_pharmacy_menu_keyboard())
    #     context.user_data['admin_state'] = ADMIN_STATES["PHARMACY_MENU"]
    #     context.user_data.pop('editing_pharmacy_id', None)
    #     context.user_data.pop('editing_field_name', None)

    # Ходим қўшиш
    elif current_state == ADMIN_STATES["ADD_EMPLOYEE_NAME"]:
        context.user_data['new_employee_data']['ism_familiya'] = text
        context.user_data['admin_state'] = ADMIN_STATES["ADD_EMPLOYEE_PHONE"]
        await update.message.reply_text("Телефон рақамини киритинг (мисол: +998901234567):", reply_markup=get_back_to_employee_menu_keyboard())
    elif current_state == ADMIN_STATES["ADD_EMPLOYEE_PHONE"]:
        context.user_data['new_employee_data']['telefon_raqam'] = text
        context.user_data['admin_state'] = ADMIN_STATES["ADD_EMPLOYEE_POSITION"]
        await update.message.reply_text("ИД рақамини киритинг:", reply_markup=get_back_to_employee_menu_keyboard())
    elif current_state == ADMIN_STATES["ADD_EMPLOYEE_POSITION"]:
        context.user_data['new_employee_data']['id'] = text
        
        new_employee = context.user_data['new_employee_data']
        success = context.bot_data['db_manager'].add_employee(new_employee) # add_employee funksiyasini qo'shish kerak
        
        if success:
            await update.message.reply_text("✅ Ходим муваффақиятли қўшилди!", reply_markup=get_admin_employee_menu_keyboard())
        else:
            await update.message.reply_text("❌ Ходимни қўшишда хатолик юз берди.", reply_markup=get_admin_employee_menu_keyboard())
        context.user_data['admin_state'] = ADMIN_STATES["EMPLOYEE_MENU"]
        context.user_data.pop('new_employee_data', None)

    # Ходим таҳрирлаш қийматини киритиш
    elif current_state and current_state.startswith("admin_edit_employee_value_"):
        field_name = current_state.replace("admin_edit_employee_value_", "")
        employee_id = context.user_data.get('editing_employee_id')
        
        success = context.bot_data['db_manager'].update_employee(employee_id, field_name, text) # update_employee funksiyasini qo'shish kerak
        
        if success:
            await update.message.reply_text(f"✅ Ходимнинг '{field_name}' майдони муваффақиятли таҳрирланди.", reply_markup=get_admin_employee_menu_keyboard())
        else:
            await update.message.reply_text(f"❌ Ходимнинг '{field_name}' майдонини таҳрирлашда хатолик юз берди.", reply_markup=get_admin_employee_menu_keyboard())
        context.user_data['admin_state'] = ADMIN_STATES["EMPLOYEE_MENU"]
        context.user_data.pop('editing_employee_id', None)
        context.user_data.pop('editing_field_name', None)

    # # Дори қўшиш
    # elif current_state == ADMIN_STATES["ADD_MEDICINE_NAME"]:
    #     context.user_data['new_medicine_data']['dori_nomi'] = text
    #     context.user_data['admin_state'] = ADMIN_STATES["ADD_MEDICINE_PRICE"]
    #     await update.message.reply_text("Нархини киритинг (фақат рақам):", reply_markup=get_back_to_medicine_menu_keyboard())
    # elif current_state == ADMIN_STATES["ADD_MEDICINE_PRICE"]:
    #     try:
    #         price = float(text)
    #         context.user_data['new_medicine_data']['narxi'] = price
    #         context.user_data['admin_state'] = ADMIN_STATES["ADD_MEDICINE_IKPU"]
    #         await update.message.reply_text("ИКПУ кодини киритинг:", reply_markup=get_back_to_medicine_menu_keyboard())
    #     except ValueError:
    #         await update.message.reply_text("❌ Нархни тўғри рақам форматида киритинг.", reply_markup=get_back_to_medicine_menu_keyboard())
    # elif current_state == ADMIN_STATES["ADD_MEDICINE_IKPU"]:
    #     context.user_data['new_medicine_data']['ikpu'] = text
    #     context.user_data['admin_state'] = ADMIN_STATES["ADD_MEDICINE_IMAGE"]
    #     await update.message.reply_text("Расм ID'сини киритинг ёки 'йўқ' деб ёзинг:", reply_markup=get_back_to_medicine_menu_keyboard())
    # elif current_state == ADMIN_STATES["ADD_MEDICINE_IMAGE"]:
    #     context.user_data['new_medicine_data']['image_file_id'] = text if text.lower() != 'йўқ' else None
    #     context.user_data['admin_state'] = ADMIN_STATES["ADD_MEDICINE_INFO"]
    #     await update.message.reply_text("Маълумотни киритинг ёки 'йўқ' деб ёзинг:", reply_markup=get_back_to_medicine_menu_keyboard())
    # elif current_state == ADMIN_STATES["ADD_MEDICINE_INFO"]:
    #     context.user_data['new_medicine_data']['info'] = text if text.lower() != 'йўқ' else None
        
    #     new_medicine = context.user_data['new_medicine_data']
    #     success = context.bot_data['db_manager'].add_medicine(new_medicine) # add_medicine funksiyasini qo'shish kerak
        
    #     if success:
    #         await update.message.reply_text("✅ Дори муваффақиятли қўшилди!", reply_markup=get_admin_medicine_menu_keyboard())
    #     else:
    #         await update.message.reply_text("❌ Дорини қўшишда хатолик юз берди.", reply_markup=get_admin_medicine_menu_keyboard())
    #     context.user_data['admin_state'] = ADMIN_STATES["MEDICINE_MENU"]
    #     context.user_data.pop('new_medicine_data', None)

    # Дори таҳрирлаш қийматини киритиш
    elif current_state and current_state.startswith("admin_edit_medicine_value_"):
        field_name = current_state.replace("admin_edit_medicine_value_", "")
        medicine_id = context.user_data.get('editing_medicine_id')
        
        value = text
        if field_name == 'narxi':
            try:
                value = float(text)
            except ValueError:
                await update.message.reply_text("❌ Нархни тўғри рақам форматида киритинг.", reply_markup=get_admin_medicine_menu_keyboard())
                context.user_data['admin_state'] = ADMIN_STATES["MEDICINE_MENU"]
                return
        elif field_name in ['image_file_id', 'info'] and text.lower() == 'йўқ':
            value = None
            
        success = context.bot_data['db_manager'].update_medicine(medicine_id, field_name, value) # update_medicine funksiyasini qo'shish kerak
        
        if success:
            await update.message.reply_text(f"✅ Дорининг '{field_name}' майдони муваффақиятли таҳрирланди.", reply_markup=get_admin_medicine_menu_keyboard())
        else:
            await update.message.reply_text(f"❌ Дорининг '{field_name}' майдонини таҳрирлашда хатолик юз берди.", reply_markup=get_admin_medicine_menu_keyboard())
        context.user_data['admin_state'] = ADMIN_STATES["MEDICINE_MENU"]
        context.user_data.pop('editing_medicine_id', None)
        context.user_data.pop('editing_field_name', None)

