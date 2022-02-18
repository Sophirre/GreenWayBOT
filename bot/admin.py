from config import bot, dp, types

ADMINS = ['SophireS', ]


def admin_check(message: types.Message):
    if message.from_user.username in ADMINS:
        return True
    else:
        return False


