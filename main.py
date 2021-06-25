import telebot
import cv2
from telebot.types import MessageID

TOKEN = '1874958731:AAGwwVIrF3OYxg22kACmuEWqmooQPg7q0Eo'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_message(message):
    bot.reply_to(message, "отправьте фотографию человека для поиска")

@bot.message_handler(content_types=["photo"])
def photo(message):

    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    src = 'photo.jpg'
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    path_to_image = 'photo.jpg'

    face_cascade_db = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    img = cv2.imread(path_to_image)

    faces = face_cascade_db.detectMultiScale(img, 1.1, 19)
    print(faces)


    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0),2)

    cv2.imwrite('withface.jpg', img)

    bot.send_photo(message.chat.id, photo=open('withface.jpg', 'rb'))    

bot.polling(none_stop=True)