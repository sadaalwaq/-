import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# تكوين البوت
TOKEN = "7875474961:AAG5ftUNzRuSK3RdSEqeYMC-ANgjT-nSiOo"
CHANNEL_LINK = "https://t.me/saddaalwak"
CHANNEL_USERNAME = "@saddaalwak"  # بدون @ إذا كنت تريد استخدامه في الروابط
WP_URL = "https://www.sadaalwaqe.com/wp-json/wp/v2/posts"

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# تعريف الأوامر
def start(update: Update, context: CallbackContext) -> None:
    """إرسال رسالة ترحيبية عند استخدام الأمر /start"""
    user = update.effective_user
    welcome_message = (
        f"مرحباً {user.first_name} 👋\n"
        "أنا بوت أساعدك في العثور على أحدث الأخبار.\n\n"
        f"للحصول على آخر الأخبار والتحديثات، تفضل بزيارة قناتنا: {CHANNEL_LINK}"
    )
    
    keyboard = [
        [InlineKeyboardButton("قناة الأخبار 📰", url=CHANNEL_LINK)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(welcome_message, reply_markup=reply_markup)

def help_command(update: Update, context: CallbackContext) -> None:
    """إرسال رسالة المساعدة"""
    help_message = (
        "📋 قائمة الأوامر المتاحة:\n\n"
        "/start - بدء المحادثة مع البوت\n"
        "/help - عرض هذه الرسالة\n"
        "/news - الحصول على رابط القناة الإخبارية\n"
        "/latest - عرض آخر 3 أخبار من الموقع\n\n"
        "💬 يمكنك أيضاً إرسال أي رسالة تحتوي على كلمة 'أخبار' للحصول على رابط القناة."
    )
    
    keyboard = [
        [InlineKeyboardButton("قناة الأخبار 📰", url=CHANNEL_LINK)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(help_message, reply_markup=reply_markup)

def news_command(update: Update, context: CallbackContext) -> None:
    """إرسال رابط القناة الإخبارية"""
    news_message = (
        "📰 قناة الأخبار\n\n"
        f"تابع أحدث الأخبار والتحديثات على قناتنا: {CHANNEL_LINK}\n\n"
        "نقدم تغطية شاملة للأخبار المحلية والعالمية."
    )
    
    keyboard = [
        [InlineKeyboardButton("انضم إلى القناة 📢", url=CHANNEL_LINK)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(news_message, reply_markup=reply_markup)

def latest_articles(update: Update, context: CallbackContext) -> None:
    """أمر /latest - لاستعراض آخر 3 مقالات من الموقع"""
    try:
        user = update.effective_user
        logger.info(f"User {user.id} ({user.username}) requested latest articles")
        
        # إرسال رسالة انتظار
        wait_message = update.message.reply_text("🔄 جاري تحميل آخر الأخبار...")
        
        # جلب آخر 3 مقالات من WordPress
        response = requests.get(WP_URL, params={"per_page": 3}, timeout=10)
        
        if response.status_code == 200:
            posts = response.json()
            
            # حذف رسالة الانتظار
            wait_message.delete()
            
            if posts:
                # إرسال رسالة تمهيدية
                intro_message = "📰 آخر الأخبار من موقع صدى الواقع:\n\n"
                update.message.reply_text(intro_message)
                
                # إرسال كل مقال
                for i, post in enumerate(posts, 1):
                    title = post['title']['rendered']
                    link = post['link']
                    
                    # إزالة HTML tags من العنوان إن وجدت
                    import re
                    title = re.sub('<[^<]+?>', '', title)
                    
                    article_message = (
                        f"📄 <b>{i}. {title}</b>\n\n"
                        f"🔗 <a href='{link}'>قراءة الخبر على الموقع</a>"
                    )
                    
                    keyboard = [
                        [InlineKeyboardButton("قراءة الخبر 📖", url=link)],
                        [InlineKeyboardButton("قناة الأخبار 📢", url=CHANNEL_LINK)]
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    
                    update.message.reply_html(article_message, reply_markup=reply_markup)
            else:
                update.message.reply_text(
                    "❌ لم يتم العثور على أخبار في الوقت الحالي.\n"
                    f"يمكنك زيارة الموقع مباشرة: {WP_URL.replace('/wp-json/wp/v2/posts', '')}"
                )
        else:
            # حذف رسالة الانتظار
            wait_message.delete()
            
            error_message = (
                "❌ عذراً، حدث خطأ في الاتصال بالموقع.\n"
                f"يمكنك زيارة الموقع مباشرة: https://www.sadaalwaqe.com\n\n"
                f"أو تابع قناة الأخبار: {CHANNEL_LINK}"
            )
            
            keyboard = [
                [InlineKeyboardButton("زيارة الموقع 🌐", url="https://www.sadaalwaqe.com")],
                [InlineKeyboardButton("قناة الأخبار 📢", url=CHANNEL_LINK)]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            update.message.reply_text(error_message, reply_markup=reply_markup)
            
    except requests.exceptions.Timeout:
        if 'wait_message' in locals():
            wait_message.delete()
        
        timeout_message = (
            "⏰ انتهت مهلة الاتصال بالموقع.\n"
            f"يمكنك زيارة الموقع مباشرة: https://www.sadaalwaqe.com\n\n"
            f"أو تابع قناة الأخبار: {CHANNEL_LINK}"
        )
        
        keyboard = [
            [InlineKeyboardButton("زيارة الموقع 🌐", url="https://www.sadaalwaqe.com")],
            [InlineKeyboardButton("قناة الأخبار 📢", url=CHANNEL_LINK)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        update.message.reply_text(timeout_message, reply_markup=reply_markup)
        
    except Exception as e:
        logger.error(f"Error fetching latest articles: {e}")
        
        if 'wait_message' in locals():
            wait_message.delete()
            
        error_message = (
            "❌ حدث خطأ غير متوقع.\n"
            f"يمكنك زيارة الموقع مباشرة: https://www.sadaalwaqe.com\n\n"
            f"أو تابع قناة الأخبار: {CHANNEL_LINK}"
        )
        
        keyboard = [
            [InlineKeyboardButton("زيارة الموقع 🌐", url="https://www.sadaalwaqe.com")],
            [InlineKeyboardButton("قناة الأخبار 📢", url=CHANNEL_LINK)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        update.message.reply_text(error_message, reply_markup=reply_markup)

def handle_news_query(update: Update, context: CallbackContext) -> None:
    """الرد على أي رسالة تحتوي على كلمة أخبار"""
    text = update.message.text.lower()
    news_keywords = ['خبر', 'أخبار', 'news', 'تحديثات', 'الاخبارية']
    
    if any(keyword in text for keyword in news_keywords):
        response = (
            "🔍 يبدو أنك تبحث عن أخبار!\n\n"
            f"يمكنك متابعة أحدث الأخبار والتحديثات على قناتنا: {CHANNEL_LINK}\n\n"
            "نقدم تغطية شاملة للأخبار المحلية والعالمية."
        )
        
        keyboard = [
            [InlineKeyboardButton("انضم إلى القناة 📢", url=CHANNEL_LINK)],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        update.message.reply_text(response, reply_markup=reply_markup)
    else:
        # رد عام على الرسائل الأخرى
        general_response = (
            "شكراً لرسالتك! 😊\n\n"
            "أنا بوت مخصص لتقديم الأخبار والتحديثات.\n"
            f"للحصول على آخر الأخبار، تفضل بزيارة قناتنا: {CHANNEL_LINK}\n\n"
            "استخدم /help لمعرفة الأوامر المتاحة."
        )
        
        keyboard = [
            [InlineKeyboardButton("قناة الأخبار 📰", url=CHANNEL_LINK)],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        update.message.reply_text(general_response, reply_markup=reply_markup)

def error_handler(update: Update, context: CallbackContext) -> None:
    """معالجة الأخطاء"""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main() -> None:
    """تشغيل البوت"""
    try:
        # إنشاء updater وتمرير token
        updater = Updater(TOKEN, use_context=True)
        
        # الحصول على dispatcher لتسجيل handlers
        dispatcher = updater.dispatcher

        # معالجات الأوامر
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("help", help_command))
        dispatcher.add_handler(CommandHandler("news", news_command))
        dispatcher.add_handler(CommandHandler("latest", latest_articles))
        
        # معالجة الرسائل النصية
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_news_query))
        
        # معالج الأخطاء
        dispatcher.add_error_handler(error_handler)

        # بدء البوت
        updater.start_polling()
        logger.info("Bot started successfully!")
        
        # تشغيل البوت حتى يتم إيقافه بـ Ctrl-C
        updater.idle()
        
    except Exception as e:
        logger.error(f"Error starting bot: {e}")

if __name__ == '__main__':
    main()