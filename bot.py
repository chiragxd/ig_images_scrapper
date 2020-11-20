import telebot
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  

#web_browser modeule part
CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
CHROMEDRIVER_PATH = 'C:\\APPDATA\\Python\\chromedriver.exe'
WINDOW_SIZE = "1920,1080"
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.binary_location = CHROME_PATH
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,chrome_options=chrome_options)

#bot token
bot_token ="1471730304:AAGqL9p0aUBstl3q9qEV1GxRa2BbJ4DaD08"
bot = telebot.TeleBot(token=bot_token)


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
    #if message.text ==r"/stop":
        #bot.reply_to(message,'Execution Stopped....\nTo Download Pictures Again\nEnter URL Or Username')
        #driver.close()
    if 'instagram.com' not in message.text:
        driver.get(url)   
    else:
        driver.get(message.text)
    imgs_src = driver.find_elements_by_class_name('_bz0w')    #.get_attribute("src") # defining img text obj
    if len(imgs_src)==0:
        bot.reply_to(message,'⚠️⚠️⚠️Profile is Private⚠️⚠️⚠️')
        driver.close()
    images_href=[]
    for img in imgs_src:

        href = img.find_element_by_tag_name('a').get_attribute("href")
        images_href.append(href)
    
    for href in images_href:
        driver.get(href)
        img_id=driver.find_element_by_xpath('//div/img').get_attribute('src')
        print("img_id",img_id)
        #extlist =[]
        #extlist.append(str(random.randint(0,1000)))
        #img_name = img_id.text.join(str(extlist))
        #print(img_name)
        if img_id.endswith('.jpg'):
            bot.send_photo(message.chat.id,photo = img_id)#, caption=img_name
        else:
            bot.send_photo(message.chat.id,photo = img_id)
    #url,caption= get_ig_img(message.text)
    #print(url)
    

while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(15)

        