from ursina import *
from minecraft import Minecraft
from login import Login

if __name__ == "__main__" :
    login = Login()
    
    if login.login_success :
        app = Ursina()
        game = Minecraft()
        app.run()