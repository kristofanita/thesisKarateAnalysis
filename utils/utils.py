def go_to_previous_window(current_window, previous_window):
    previous_window.show()
    current_window.close()


def open_new_window(current_window, next_window):
    current_window.new_window = next_window(current_window)
    current_window.new_window.show()
    current_window.hide()


def open_dialog(current_window, dialog):
    current_window.new_dialog = dialog(current_window)
    current_window.new_dialog.show()


def send_new_password(username):
    # TODO generate a new password
    # TODO send an email to the user

    print(f"A new password was sent. {username}")
