def token_get():
    with open('bot/TOKEN.txt', 'r') as file:
        token = file.readline()
        return token
