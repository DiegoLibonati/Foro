from foro import create_app
from flask_socketio import SocketIO,send
from flask_login import login_required, current_user

app = create_app()
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('message')
@login_required
def handleMessage(msg):
    send(f'<img src="/static/profilephotos/{current_user.profile_photo}" class="element_of_message_chat" alt="{current_user.username}"/> <h2 class="element_of_message_chat" >{current_user.username}:</h2> <p class="message element_of_message_chat">{msg}</p>', broadcast=True)

if __name__ == "__main__":
    socketio.run(app,debug=True)