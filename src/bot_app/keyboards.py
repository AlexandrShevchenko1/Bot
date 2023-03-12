from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_button_week_events = InlineKeyboardButton("Week events", callback_data="Week events")
inline_button_day_events = InlineKeyboardButton("Day events", callback_data="Day events")
inline_kb = InlineKeyboardMarkup()

inline_kb.add(inline_button_week_events)
inline_kb.add(inline_button_day_events)

# inline_button_log_in = InlineKeyboardButton("Log In", callback_data="Log In")
# inline_button_register = InlineKeyboardButton("Register", callback_data="Register")

# inline_kb_lr = InlineKeyboardMarkup()
# inline_kb_lr.add(inline_button_log_in)
# inline_kb_lr.add(inline_button_register)