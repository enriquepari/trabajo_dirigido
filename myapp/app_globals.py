class AppGlobals:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppGlobals, cls).__new__(cls)
            cls._instance.user_group = None  # Variable para almacenar el grupo del usuario
        return cls._instance