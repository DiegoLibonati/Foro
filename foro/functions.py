from datetime import datetime
import secrets
import os

def get_time_login():
    now = datetime.now()

    current_time = f"{add_zero(now.hour)}:{add_zero(now.minute)}:{add_zero(now.second)} | {add_zero(now.day)}/{add_zero(now.month)}/{now.year}"

    return current_time

def add_zero(value):

    if value < 10:
        return f"0{value}"
    
    return value

def save_images (photo, route, current_app):
    if photo:
        hash_photo = secrets.token_urlsafe(10)
        _, file_extension = os.path.splitext(photo.filename)
        photo_name = hash_photo + file_extension
        file_path = os.path.join(current_app.root_path, f'static/{route}', photo_name)
        photo.save(file_path)
        return photo_name

def check_files_on_update(current_user_img, input_file, current_app, checkbox_delete, folder, default_db_img):
    # IF: Si el usuario tiene una foto de perfil y no se toca el boton para remover la foto y se paso una foto en el input profile photo
    if current_user_img and input_file:
        if not current_user_img == f"{default_db_img}":
            os.remove(os.path.join(current_app.root_path, f'static/{folder}', current_user_img))
        current_user_img = save_images(input_file, f"{folder}", current_app)
        return current_user_img
    # ELIF1: Si el usuario no tiene foto, no quiere borrar su foto y tiene pasada una foto, es decir, un valor en el input file
    elif not current_user_img and input_file:
        current_user_img = save_images(input_file, f"{folder}", current_app)
        return current_user_img
    # ELIF2: Si el usuario tiene una foto de perfil y el checkbox esta activado y no tiene pasada ninguna foto. Elmina la foto y deja el dato default
    elif checkbox_delete == "on":
        os.remove(os.path.join(current_app.root_path, f'static/{folder}', current_user_img))
        current_user_img = f"{default_db_img}"
        return current_user_img
    else:
        return current_user_img