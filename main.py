from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
import pandas


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_real_passwords():
    generate_passwords(password_entry)


def generate_real_new_passwords():
    generate_passwords(new_password_entry)


def generate_passwords(new_password):
    new_password.delete(0, END)
    # Password Generator Project
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers

    random.shuffle(password_list)

    password = "".join(password_list)
    new_password.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_file():
    data_cvs = pandas.read_csv("do not delete it or your data will lost.cvs")
    datas_index = {"index": index for (index, row) in data_cvs.iterrows()}
    datas = {row.website: {"email": row.email, "password": row.password} for (index, row) in data_cvs.iterrows()}
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        },
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty! except new password.")
    else:
        try:
            with open('data.json', mode='r') as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open('data.json', mode='w') as data_file:
                json.dump(datas, data_file, indent=2)

            with open('data.json', mode='r') as data_file:
                data = json.load(data_file)
                for _ in range(0, datas_index['index']):
                    data.update(datas)
                data.update(new_data)

            with open('data.json', mode='w') as data_file:
                json.dump(data, data_file, indent=2)
        else:
            data.update(new_data)
            with open('data.json', mode='w') as data_file:
                json.dump(data, data_file, indent=2)
        finally:
            with open('do not delete it or your data will lost.cvs', mode='a') as data_file:
                data_file.write(f"\n{website},{email},{password}")
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #


def find_password():
    website = website_entry.get()
    email = email_entry.get()
    try:
        with open('data.json', mode='r') as data_file:
            loaded_data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title='Error', message="No Data File Found")
    else:
        if len(email) == 0 or len(website) == 0:
            messagebox.showinfo(title="Oops", message="Please don't leave email and website fields empty!")
        else:
            try:
                loaded_data[website]
            except KeyError:
                messagebox.showinfo(title="Oops",
                                    message=f"No details for {website} exists.")
            else:
                if email != loaded_data[website]['email']:
                    messagebox.showinfo(title="Oops",
                                        message=f"No details for {email} exists.")
                else:
                    messagebox.showinfo(title=website, message=f"Email: {loaded_data[website]['email']}\n"
                                                               f"Password: {loaded_data[website]['password']}")


# ---------------------------- REPLACE PASSWORD ------------------------------- #

def replace_password():
    data_cvs = pandas.read_csv("do not delete it or your data will lost.cvs")
    website = website_entry.get()
    new_password = new_password_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    if len(website) == 0 or len(new_password) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open('data.json', 'r'):
                pass
        except FileNotFoundError:
            with open('data.json', 'w'):
                pass
        else:
            with open('data.json', 'r') as data_file:
                data = json.load(data_file)
            try:
                data[website]
            except KeyError:
                messagebox.showinfo(title="Oops",
                                    message=f"No details for {website} exists.")
            else:
                if email != data[website]["email"]:
                    messagebox.showinfo(title="Oops",
                                        message=f"No details for {email} exists.")
                else:
                    if email == data[website]['email']:
                        data[website]["password"] = new_password
                        with open('data.json', 'w') as data_file:
                            json.dump(data, data_file, indent=2)
                        data_cvs.loc[data_cvs.password == password, "password"] = new_password
                        data_cvs.to_csv("do not delete it or your data will lost.cvs", index=False)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)
                new_password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Canvas
logo_canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
logo_canvas.create_image(100, 100, image=logo_img)
logo_canvas.grid(column=1, row=0)

# Label
website_name = Label(text="Website:")
website_name.grid(column=0, row=1)

user_email = Label(text="Email/Username:")
user_email.grid(column=0, row=2)

user_password = Label(text="Password:")
user_password.grid(column=0, row=3)

new_user_password = Label(text="New Password:")
new_user_password.grid(column=0, row=4)

# Entry
website_entry = Entry(width=21)
website_entry.grid(column=1, row=1)
website_entry.focus()

email_entry = Entry(width=44)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "astonLeonardlo22@gmail.com")

password_entry = Entry(width=21)
password_entry.grid(column=1, row=3)

new_password_entry = Entry(width=21)
new_password_entry.grid(column=1, row=4)

# Button
generate_password = Button(text="Generate Password", command=generate_real_passwords)
generate_password.grid(column=2, row=3)
new_generate_password = Button(text="Generate Password", command=generate_real_new_passwords)
new_generate_password.grid(column=2, row=4)

search = Button(text="Search", width=14, command=find_password)
search.grid(column=2, row=1)

add = Button(text="Add", width=18, command=save_file)
add.grid(column=1, row=5)

replace = Button(text="Replace", width=18, command=replace_password)
replace.grid(column=2, row=5)

window.mainloop()
