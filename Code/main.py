#from ast import keyword
#from cgi import test
#from inspect import getsource
#from numpy import append
import tweepy
import configparser
import pandas as pd
from tkinter import *
from tkinter import scrolledtext
import tkinter as tk
import matplotlib as plt
#import random
import matplotlib.pyplot as plt
import botometer
import numpy as np
import statistics
#from matplotlib.animation import FuncAnimation




config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']
access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']
rapidapi_key = config['RapidAPI']['rapidapi_key']

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit = True)


twitter_app_auth = {
    'consumer_key': api_key,
    'consumer_secret': api_key_secret,
    'access_token': access_token,
    'access_token_secret': access_token_secret,
  }

analyzer = botometer.Botometer(wait_on_ratelimit = True, rapidapi_key = rapidapi_key, **twitter_app_auth)



global search_keyword, df2
df2 = pd.read_csv('accounts_scores.csv')

global  bots_score, bots_binary, bot_type, langList     
bots_score, bots_binary, bot_type, langList = ([] for i in range(4))

'''df2 = pd.DataFrame(columns = ['cap.english','cap.universal', 'display_scores.english.astroturf', 'display_scores.english.fake_follower', 'display_scores.english.financial'
, 'display_scores.english.other','display_scores.english.overall','display_scores.english.self_declared', 'display_scores.english.spammer',
'display_scores.universal.astroturf', 'display_scores.universal.fake_follower', 'display_scores.universal.financial',
 'display_scores.universal.other', 'display_scores.universal.overall', 'display_scores.universal.self_declared', 'display_scores.universal.spammer', 'raw_scores.english.astroturf',
  'raw_scores.english.fake_follower', 'raw_scores.english.financial', 'raw_scores.english.other', 'raw_scores.english.overall', 'raw_scores.english.self_declared',
   'raw_scores.english.spammer', 'raw_scores.universal.astroturf', 'raw_scores.universal.fake_follower', 'raw_scores.universal.financial', 'raw_scores.universal.other',
    'raw_scores.universal.overall', 'raw_scores.universal.self_declared', 'raw_scores.universal.spammer', 'user.majority_lang', 'user.user_data.id_str', 'user.user_data.screen_name'])'''

class Linstener(tweepy.StreamListener):
    def on_status(self, status):

        if(status.text).find(search_keyword) != -1:

            df = pd.DataFrame(columns = ['account_id','account_name', 'tweet_time', 'tweet', 'keyword', 'account_lang','fake_follower','political_bot', 'spammer','bot_score'])
            result = analyzer.check_account('@' + status.user.screen_name)
            df2 = pd.json_normalize(result)
            df2.to_csv('accounts_scores.csv', index=False, mode='a', header=False)

            print(status.id)
            print('@' + status.user.screen_name)
            print(status.created_at)
            print(status.text)
            print(search_keyword)
            print(result)

            df.loc[df.shape[0]] = [status.id, '@' + status.user.screen_name, status.created_at, status.text, search_keyword, df2["user.majority_lang"].item(), 
            df2["raw_scores.universal.fake_follower"].item(), df2["raw_scores.universal.astroturf"].item(), df2["raw_scores.universal.spammer"].item(), df2["raw_scores.universal.overall"].item()]
        
            df.to_csv('History.csv', mode='a', index=False, header=False)

            score_as_string = str(df2["raw_scores.universal.overall"].item()) + '  '
            str_on_frame = df2["user.user_data.screen_name"].item() +' '+ score_as_string + '\n' + status.text + '\n\n'
            text_area1.insert(INSERT, str_on_frame)

            if df2["raw_scores.universal.overall"].item() > 0.5:
                bots_binary.append('Bot')
            else:
                bots_binary.append('account')
            bots_score.append(df2["raw_scores.universal.overall"].item())

            if df2["raw_scores.universal.astroturf"].item() > 0.5:
                bot_type.append('Politcal_bot')
        
            if df2["raw_scores.universal.spammer"].item() > 0.5:
                bot_type.append('Spammer_bot')
        
            if df2["raw_scores.universal.fake_follower"].item() > 0.5:
                bot_type.append('FakeFollower_Bot')
        
            langList.append(df2["user.majority_lang"].item())


            lbl4['text'] = 'عدد التغريدات التي تم تحليلها حتى الان: ' + str(len(bots_binary))
            lbl5['text'] = 'متوسط الحسابات المحللة حتى الان: ' + str(round(np.mean(bots_score), 2))
            lbl6['text'] = 'عدد الحسابات الوهمية: ' + str(bots_binary.count('Bot'))
            lbl7['text'] = 'عدد الحسابات الوهمية السياسية: ' + str(bot_type.count('Politcal_bot'))
            lbl8['text'] = 'عدد الحسابات الوهمية المكررة للمحتوى: ' + str(bot_type.count('Spammer_bot'))
            lbl9['text'] = 'عدد المتابعين الوهميين: ' + str(bot_type.count('FakeFollower_Bot')) 
            lbl10['text'] =  str(statistics.mode(langList)) + ' :لغة الحسابات التي تغرد' 

            if bots_binary.count('Bot') > bots_binary.count('account'):
                lbl11['text'] = 'تصنيف الهاشتاق: وهمي' 
            else:
                lbl11['text'] = 'تصنيف الهاشتاق: حقيقي' 


            window.update()

        
        
def streamTweets():
    myStreamListener = Linstener()
    myStreamListener = tweepy.Stream(auth = api.auth, listener = myStreamListener)
    myStreamListener.filter(languages=['ar'], track = search_keyword)
    


def mainFrame():
        global text_area1, window, lbl3, lbl4, lbl5, lbl6, lbl7, lbl8, lbl9, lbl10, lbl11
        
        window = tk.Tk()
        window.title('TWITFAKE')
        window.geometry('1920x1080')
        window.config(background='black')
        window.iconbitmap("images/image1.ico")
        img = PhotoImage(file='images/image2.png')
        Label(window,image=img, background ='black', width = 200, height=180).place(x = 850-200, y = 45)

        #lbl1 = Label(text = ':ادخل الكلمه المفتاحية')
        #lbl1.config(foreground = 'white', background = 'black')
        #lbl1.place(x = 890-200, y = 250)

        #search_keyword = Text(width = 20, height = 1)
        #search_keyword.place(x = 870, y = 270)

        #bserch = Button(text = 'استماع')
        #bserch.config(foreground = 'white', background = 'black', width = 10, height = 2)
        #bserch.place(x = 910-200, y = 300)
        
        lbl2 = Label(text = ' بث وتحليل مباشر للتغريدات المتعلقة بـ ' + str(search_keyword) )
        lbl2.config(foreground = 'white', background = '#082054', font=("Times New Roman", 20))
        lbl2.config()
        lbl2.place(x = 1320-350, y = 130-50)

        lbl3 = Label(text = 'النتائج')
        lbl3.config(foreground = 'white', background = '#082054', font=("Times New Roman", 25), width=26, anchor='center')
        lbl3.place(x = 500-350, y = 180-50)

        lbl4 = Label(text = '0 :عدد التغريدات التي تم تحليلها حتى الان')
        lbl4.config(foreground = 'white', background = '#082054', font=("Times New Roman", 25), width=26, anchor='e')
        lbl4.place(x = 500-350, y = 270-50)

        lbl5 = Label(text = ':متوسط الحسابات المحللة حتى الان')
        lbl5.config(foreground = 'white', background = '#22355c', font=("Times New Roman", 25), width=26, anchor='e')
        lbl5.place(x = 500-350, y = 320-50)

        lbl6 = Label(text = ':عدد الحسابات الوهمية')
        lbl6.config(foreground = 'white', background = '#22355c', font=("Times New Roman", 25), width=26, anchor='e')
        lbl6.place(x = 500-350, y = 370-50)

        lbl7 = Label(text = ':عدد الحسابات الوهمية السياسية')
        lbl7.config(foreground = 'white', background = '#082054', font=("Times New Roman", 25), width=26, anchor='e')
        lbl7.place(x = 500-350, y = 420-50)

        lbl8 = Label(text = ':عدد الحسابات الوهمية المكررة للمحتوى')
        lbl8.config(foreground = 'white', background = '#22355c', font=("Times New Roman", 25), width=26, anchor='e')
        lbl8.place(x = 500-350, y = 470-50)

        lbl9 = Label(text = ':عدد المتابعين الوهميين')
        lbl9.config(foreground = 'white', background = '#082054', font=("Times New Roman", 25), width=26, anchor='e')
        lbl9.place(x = 500-350, y = 520-50)

        lbl10 = Label(text = ':لغة الحسابات التي تغرد')
        lbl10.config(foreground = 'white', background = '#22355c', font=("Times New Roman", 25), width=26, anchor='e')
        lbl10.place(x = 500-350, y = 570-50)

        lbl11 = Label(text = ':تصنيف الهاشتاق' )
        lbl11.config(foreground = 'white', background = '#082054', font=("Times New Roman", 25), width=26, anchor='e')
        lbl11.place(x = 500-350, y = 620-50)

        
        

        text_area1 = scrolledtext.ScrolledText(window,  wrap = tk.WORD,  width = 55, height = 28,  font = ("Times New Roman",     15))
        text_area1.place(x = 1250-350, y = 180-50)
        text_area1.see(tk.END)
        text_area1.after(2500, streamTweets)
        mainloop()
 
search_keyword = input("ادخل الهاشتاق المراد تحليله: ")
print('Welcome to TwitFake!')
mainFrame()