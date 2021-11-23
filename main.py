from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    search_term = website_entry.get()

    try:
        with open('data.json', 'r') as data_file:
            # Reading data
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title='Error Exception', message='No Data File Found')
    else:
        # Checks if search term key matches keys in data dictionary
        if search_term in data:
            print(data[search_term])
            email = data[search_term]['email']
            password = data[search_term]['password']
            messagebox.showinfo(title='Password Manager', message=f'{search_term}\nEmail: {email}\nPassword: {password}')
        else:
            print('data not found')
            messagebox.showwarning(title='Password Manager', message=f'{search_term} does not exist.')


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_list_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_list_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_list_letters + password_list_symbols + password_list_numbers
    shuffle(password_list)

    password = ''.join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)
    messagebox.showinfo(title='Password Manager', message='The newly generated password has been copied to the '
                                                          'clipboard.')

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    user_website = website_entry.get()
    user_email_username = email_username_entry.get()
    user_password = password_entry.get()
    user_notes = notes_entry.get("1.0", END)
    new_data = {
        user_website: {
            'email': user_email_username,
            'password': user_password,
            'notes': user_notes,
        }
    }

    if len(user_website) > 0 and len(user_email_username) > 0 and len(user_password) > 0:
        try:
            with open('data.json', 'r') as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open('data.json', 'w') as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open('data.json', 'w') as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            notes_entry.delete("1.0",'end-1c')
            messagebox.showinfo(title='Password Manager', message='Data entries saved to file data.txt')
    else:
        messagebox.showerror(title='User Error', message='Entry fields must not be empty.')


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title('Password Manager')
window.config(padx=50, pady=50)

# Canvas --------------------
canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Label for website --------------------
website_label = Label(text='Website:')
website_label.grid(column=0, row=1)

# Label for email/username --------------------
email_username_label = Label(text='Email/Username:')
email_username_label.grid(column=0, row=2)

# Label for password --------------------
password_label = Label(text='Password:')
password_label.grid(column=0, row=3)

# Entry box for website --------------------
website_entry = Entry()
# Gets text in website_entry
print(website_entry.get())
website_entry.grid(column=1, row=1, columnspan=1, sticky="EW")
website_entry.focus()

# Button for search --------------------
# calls search() when pressed
search_button = Button(text="Search", command=find_password)
search_button.grid(column=2, row=1, sticky=EW)

# Entry box for email/username --------------------
email_username_entry = Entry()
# Gets text in email_username_entry
print(email_username_entry.get())
email_username_entry.grid(column=1, row=2, columnspan=2, sticky="EW")
email_username_entry.insert(0, 'test@test.com')  # TODO have code pull most used email

# Entry box for password --------------------
password_entry = Entry()
# Gets text in password_entry
print(password_entry.get())
password_entry.grid(column=1, row=3, sticky="EW")

# Label for notes --------------------
password_label = Label(text='Notes:')
password_label.grid(column=0, row=4)

# Multi-line Text entry box for notes
notes_entry = Text(height=5, width=30)
# Adds some text to begin with.
notes_entry.insert(END, "")
# Get's current value in textbox at line 1, character 0
# print(notes_entry.get("1.0", END))
notes_entry.grid(column=1, row=4)


# Button for generate password --------------------
# calls generate_password() when pressed
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(column=2, row=3)

# Button for Add --------------------
# calls save() when pressed
add_button = Button(text="Add", command=save)
add_button.grid(column=1, row=5, columnspan=2, sticky="EW")

window.mainloop()  # Keeps window on screen
