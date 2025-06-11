# Libraries
import tkinter as tk
import sqlite3
import threading
import bcrypt


# Form
def Menu():
    form=tk.Tk()
    form.title("Full SQL Account System")
    form.geometry("300x175")
    
    userLabel=tk.Label(form, text="Kullanıcı Adı")
    userLabel.pack(side="top")

    userEntry=tk.Entry(form)
    userEntry.pack(side="top", pady=10)

    userPLabel=tk.Label(form, text="Kullanıcı Şifresi")
    userPLabel.pack(side="top")

    userPEntry=tk.Entry(form, show="*")
    userPEntry.pack(side="top", pady=10)

    frame=tk.Frame(form)
    frame.pack(side="top")

    KayitOl=tk.Button(frame, text="Kayıt Ol", command=lambda: SQL(userEntry.get(), userPEntry.get().encode("utf-8"), True))
    GirisYap=tk.Button(frame, text="Giriş Yap", command=lambda: SQL(userEntry.get(), userPEntry.get().encode("utf-8"), False))

    KayitOl.pack(side="left", padx=5, pady=5)
    GirisYap.pack(side="left", padx=5, pady=5)

    form.mainloop()



# SQL Operations
def SQL(username, password, method=True):
    db=sqlite3.connect("database.db")
    cursor=db.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS Users(
                   ID INTEGER PRIMARY KEY,
                   NAME VARCHAR(255) UNIQUE,
                   PASSWORD VARCHAR(255)
                   )""")
    db.commit()

    if method:
        try:
            cursor.execute("INSERT INTO Users(NAME, PASSWORD) VALUES(?, ?)", (username, bcrypt.hashpw(password, bcrypt.gensalt())))
            print("Saved!")

        except sqlite3.IntegrityError:
            print("This user already saved!")

    else:
        data=cursor.execute("SELECT * FROM Users WHERE NAME=?", (username, ))
        data=data.fetchall()

        if  username == data[0][1] and bcrypt.checkpw(password, data[0][2]):
            print("Login Successful!")
        
        else:
            print("Login Failed!")

    db.commit()
    cursor.close()
    db.close()



# Start Code
if __name__=="__main__":
    mth=threading.Thread(target=Menu, daemon=True)
    mth.start()

    mth.join()
