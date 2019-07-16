class Development:
    DEBUG = True
    SECRET_KEY = 'hard to guess string'
    MONGODB_SETTINGS = {
        'db': 'Wang',
        'host': '127.0.0.1',
        'port': 27017
    }
    port = 9001

    # 自己的配置
    LWG_HOST = "http://127.0.0.1:9001"

    CHAT_ROOM_MAX_NUM = 100
