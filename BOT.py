from TKN_reader import token_get
import telebot

TOKEN = token_get()


if __name__ == '__main__':
    print(TOKEN)
    print(type(TOKEN))
