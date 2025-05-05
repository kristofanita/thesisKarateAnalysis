import sqlite3
import pandas as pd
import uuid
import bcrypt
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from backend.User import User
from backend import global_vars


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed

def decode_password(hashed, password_typed):
    return hashed == bcrypt.hashpw(password_typed.encode(), hashed)

def send_email_to_new_user(to_email, user_name, user_id):
    sender_email = "makiwara.ai@gmail.com"
    sender_password = "dqwzmexchorwrnkx" #"MakiwarAI25"
    subject = "Successull registration to Makiwara AI"
    body = f"Dear {user_name}!\n\n\tThank you for your registration to MakiwarAI!\n\tWe hope our tool will help you to improve your karate technique!\n\tPlease save your id number:\n\t\t{user_id}\n\nBest regrads,\nMakiwarAI"
    
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print("Email sent to: ", to_email)
    except Exception as e:
        print(e)
        pass

def register_new_user(name, password, email, birth, h, w):
    try:
        conn = sqlite3.connect('/home/karate/karateProjectFullstack/database/karate.db')
        cur = conn.cursor()

        """sql_command = 
        CREATE TABLE Users(
            name VARCHAR,
            email VARCHAR,
            birth_date TIMESTAMP,
            height REAL,
            weight REAL,
            user_id VARCHAR,
            password VARCHAR,
            latest_score INTEGER,
            latest_score_time TIMESTAMP,
            best_score INTEGER,
            best_score_time TIMESTAMP,
            PRIMARY KEY(user_id)
        );   id, name, email, birth_date, height, weight, latest_score,
                 latest_score_time, best_score, best_score_time      
        """

        cur.execute(f"PRAGMA table_info(Users)")
        columns = [row[1] for row in cur.fetchall()]
        column_str = ', '.join(columns)
        placeholders = ', '.join(['?' for _ in columns])
        query = f"INSERT INTO Users ({column_str}) VALUES ({placeholders})"
        print(columns)
        print(query)
        print(column_str)

        query_vals = [None] * len(columns)
        query_vals[0] = name
        query_vals[1] = email
        query_vals[2] = birth
        query_vals[3] = h
        query_vals[4] = w
        query_vals[5] = str(uuid.uuid1())
        pwd = hash_password(password)
        query_vals[6] = pwd

        # name, email, birth_date, height, weight, user_id, password, latest_score, latest_score_time, best_score, best_score_time
        cur.execute(query, query_vals)
        conn.commit()

        sql_users = "SELECT * FROM Users"
        cur.execute(sql_users)
        all_user_ids = cur.fetchall()
        #print(all_user_ids)

        global_vars.current_user = User(query_vals[0],
                                        query_vals[1],
                                        query_vals[2],
                                        query_vals[3],
                                        query_vals[4],
                                        query_vals[5]
                                        )
        global_vars.current_user.print_user()
        send_email_to_new_user(email, name, query_vals[5])

    except sqlite3.Error as error:
        print("Failed to execute the above query", error)

    finally:
        if conn:
            conn.close()


def verify_user(email, password):
    #TODO: itt kell db-ből select * from Users where email=email
    # majd dekódolni a tárolt passwordot, osszehasonlitani a most kapott passworddel
    # ha egyezik, letre kell hozni egy User objektumot azokkal az ertekekkel amit epp lekerdeztem a db-bol
        #global_vars.current_user=User(id, name, email ...)
    # ha nem egyezik, egyelore csak lepjen ki a programbol egy print(verifying user was not successfull)
    ret = False
    try:
        conn = sqlite3.connect('/home/karate/karateProjectFullstack/database/karate.db')
        cur = conn.cursor()
        query = f"SELECT * FROM Users WHERE email= ?"
        cur.execute(query, (email,))
        user_from_db = cur.fetchall()[0]
        print(type(user_from_db))
        if decode_password(user_from_db[6], password):
            print(user_from_db)
            global_vars.current_user = User(user_from_db[0],
                                            user_from_db[1],
                                            user_from_db[2],
                                            user_from_db[3],
                                            user_from_db[4],
                                            user_from_db[5],
                                            user_from_db[7],
                                            user_from_db[8],
                                            user_from_db[9],
                                            user_from_db[10]
                                            )
            global_vars.current_user.print_user()
        else:
            print("verifying user was not successfull")

    except sqlite3.Error as error:
        print("Failed to execute the above query", error)
        return ret

    finally:
        if conn:
            conn.close()
        return ret
    return ret
