import telebot,os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from flask import Flask, request

chrome_options = Options()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("GOgitOGLE_CHROME_BIN"),chrome_options=chrome_options)


bot_token ="1471730304:AAGqL9p0aUBstl3q9qEV1GxRa2BbJ4DaD08"
bot = telebot.TeleBot(token=bot_token)
server = Flask(__name__)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,"Welcome To Instagram Image Downloader Bot\n     Only Send Username Or Profile Link  ")
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message,'Use //stop Command to stop downloading Pictures \nDon\'t Send Private Profiles')

@bot.message_handler(commands=['xstop'])
def send_stop(message):
    bot.reply_to(message,'Stopped Downloading Images')

@bot.message_handler(func = lambda msg: msg.text!="stop" and msg.text!="Stop" and msg.text!="STOP" )
def at_answer(message):
    print(message.text)
    url="https://www.instagram.com" +"/" + message.text
    if 'instagram.com' not in message.text:
        driver.get(url)   
    else:
        driver.get(message.text)

    imgs_src = driver.find_elements_by_class_name('_bz0w')

    if len(imgs_src)==0:
        bot.reply_to(message,'⚠️⚠️⚠️Profile is Private⚠️⚠️⚠️')
        driver.close()

    images_href=[]
    for img in imgs_src[0:10]:
        href = img.find_element_by_tag_name('a').get_attribute("href")
        images_href.append(href)

    for i,href in enumerate(images_href):
        driver.get(href)
        img_id=driver.find_element_by_xpath('//div/img').get_attribute('src')
        print("img_id",img_id)
        img_name = message.text+"("+str(i+1)+")"
        if img_id.endswith('.jpg'):
            bot.send_photo(message.chat.id,photo = img_id,caption=img_name)#, caption=img_name
        else:
            bot.send_photo(message.chat.id,photo = img_id,caption=img_name)
    bot.reply_to(message,'NOICE')
    

@server.route('/' +'' 1471730304:AAGqL9p0aUBstl3q9qEV1GxRa2BbJ4DaD08', methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200   

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://ig-scrap.herokuapp.com/' + '1471730304:AAGqL9p0aUBstl3q9qEV1GxRa2BbJ4DaD08')
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))