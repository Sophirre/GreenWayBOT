def token_get():
    with open('TOKEN.txt', 'r') as file:
        token = file.readline()
        return token
