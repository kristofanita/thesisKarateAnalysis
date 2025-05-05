import sqlite3
import pandas as pd
import uuid


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        conn = sqlite3.connect('karate.db')
        cur = conn.cursor()

        sql_delete_table = "DROP TABLE IF EXISTS Users;"
        cur.execute(sql_delete_table)

        sql_command = """
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
        );         
        """
        cur.execute(sql_command)

        sql_delete_table = "DROP TABLE IF EXISTS Trainings;"
        cur.execute(sql_delete_table)
        sql_command2 = """
            CREATE TABLE Trainings(
                user_id VARCHAR NOT NULL,
                session_id VARCHAR,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                punch_count INTEGER,
                max_training_score INTEGER,
                humidity REAL,
                temperature REAL,
                raw_data_filename VARCHAR,
                info_filename VARCHAR,
                PRIMARY KEY(session_id),
                FOREIGN KEY(user_id) REFERENCES Users(user_id)
            );
        """
        cur.execute(sql_command2)

        sql_delete_table = "DROP TABLE IF EXISTS Punches;"
        cur.execute(sql_delete_table)
        sql_command2 = """
                    CREATE TABLE Punches(
                        user_id INTEGER NOT NULL,
                        session_id INTEGER NOT NULL,
                        max_acc REAL,
                        min_acc REAL,
                        x_peak REAL,
                        x_resultant_percentage REAL,
                        punchTime TIMESTAMP,
                        push1Period TIMESTAMP,
                        secondaryPushAmpl REAL,
                        secondaryPushDiff REAL,
                        std REAL,	
                        mean REAL,
                        skewness REAL,
                        kurtosis REAL,
                        max_phase REAL,
                        dominant_frequency REAL,
                        total_energy REAL,
                        spectral_centroid REAL,
                        max_spectral_density REAL,
                        mean_spectral_density REAL,
                        mean_frequency_gaps REAL,
                        max_acc_2 REAL,
                        min_acc_2 REAL,
                        punchTime2 TIMESTAMP,
                        std2 REAL,
                        mean2 REAL,
                        skewness2 REAL,
                        kurtosis2 REAL,
                        max_phase2 REAL,
                        dominant_frequency2 REAL,
                        total_energy2 REAL,
                        spectral_centroid2 REAL,
                        max_spectral_density2 REAL,
                        mean_spectral_density2 REAL,
                        mean_frequency_gaps2 REAL,
                        Score INTEGER,
                        FOREIGN KEY(user_id) REFERENCES Users(user_id),
                        FOREIGN KEY(session_id) REFERENCES Trainings(session_id)
                    );
                """
        cur.execute(sql_command2)
        conn.commit()

    except sqlite3.Error as error:
        print("Failed to execute the above query", error)

    finally:
        if conn:
            conn.close()

    # check if db creation was successful
    try:
        db_connection = sqlite3.connect('karate.db')
        db_cursor = db_connection.cursor()
        # sql_master_command = """
        #     SELECT name FROM sqlite_master WHERE type='table';
        # """
        sql_try = """
            SELECT * FROM Punches;
        """
        db_cursor.execute(sql_try)
        print(db_cursor.fetchall())
    except sqlite3.Error as error:
        print("Failed to connect to db or execute query", error)

    finally:
        if db_connection:
            db_connection.close()

    makiwara = pd.read_csv("makiwaraPunches.csv", index_col=False)
    scores = pd.read_excel("makiwaraPunches_with_multiple_models.xlsx")

    makiwara.drop(columns="Unnamed: 0", inplace=True)
    #print(makiwara.head)
    cols = makiwara.columns

    try:
        conn = sqlite3.connect('karate.db')
        cur = conn.cursor()

        cur.execute(f"PRAGMA table_info(Users)")
        columns = [row[1] for row in cur.fetchall()]
        column_str = ', '.join(columns)
        placeholders = ', '.join(['?' for _ in columns])
        query = f"INSERT INTO Users ({column_str}) VALUES ({placeholders})"
        print(query)

        # name, email, birth_date, height, weight, user_id, password, latest_score, latest_score_time, best_score, best_score_time
        cur.execute(query, ("Laszlo", None, None, None, None, str(uuid.uuid1()), "0000", None, None, None, None))
        cur.execute(query, ("Dori", None, None, None, None, str(uuid.uuid1()), "0000", None, None, None, None))
        cur.execute(query, ("Tom", None, None, None, None, str(uuid.uuid1()), "0000", None, None, None, None))
        cur.execute(query, ("Reni", None, None, None, None, str(uuid.uuid1()), "0000", None, None, None, None))
        cur.execute(query, ("GLaci", None, None, None, None, str(uuid.uuid1()), "0000", None, None, None, None))
        conn.commit()

        sql_punches = "SELECT user_id, name FROM Users"
        cur.execute(sql_punches)
        all_user_ids = cur.fetchall()
        print(all_user_ids)
        print(type(all_user_ids[0][0]))

        cur.execute(f"PRAGMA table_info(Trainings)")
        columns = [row[1] for row in cur.fetchall()]
        column_str = ', '.join(columns)
        placeholders = ', '.join(['?' for _ in columns])
        query_T = f"INSERT INTO Trainings ({column_str}) VALUES ({placeholders})"
        print(query_T)

        cur.execute(f"PRAGMA table_info(Punches)")
        punches_columns = [row[1] for row in cur.fetchall()]
        print(punches_columns)
        punches_columns_str = ', '.join(punches_columns)
        punches_placeholders = ', '.join(['?' for _ in punches_columns])
        query = f"INSERT INTO Punches ({punches_columns_str}) VALUES ({punches_placeholders})"

        for user in all_user_ids:
            name = user[1]
            if name == "Reni":
                reni_df = scores[(scores.name == "ReniBalkez") | (scores.name == "ReniJobbkez")]
                reni_punch_count = reni_df["name"].count()
                reni_max_score = reni_df["Score"].max()
                reni_session_id = str(uuid.uuid1())
                print(reni_max_score)
                cur.execute(query_T, (user[0], reni_session_id, None, None, reni_punch_count, reni_max_score, None, None, None, None))
                # TODO: Renit meg be kell fejezni
                reni_df.insert(0, "user_id", user[0])
                reni_df.insert(1, "session_id", reni_session_id)
                reni_punches = reni_df[punches_columns]
                cur.executemany(query, reni_punches.values)
            else:
                user_df = scores[scores.name == name]
                punch_count = user_df["name"].count()
                max_score = user_df["Score"].max()
                session_id = str(uuid.uuid1())
                print("!!!!!!!!!!!!!! user [0]=", user[0])
                cur.execute(query_T, (user[0], session_id, None, None, punch_count, max_score, None, None, None, None))
                # itt kell rogton feltolteni a makiwarabol az adatokat a punches tablaba
                user_df.insert(0, "user_id", user[0])
                user_df.insert(1, "session_id", session_id)
                punches = user_df[punches_columns]
                cur.executemany(query, punches.values)
                #cur.execute(query, punches.iloc[0].values)

        conn.commit()

        cur.execute(f"SELECT * FROM Trainings")
        print(cur.fetchall())

        cur.execute(f"SELECT * FROM Punches")
        print(cur.fetchall())

    except Exception as e:
        print("Exception occured:", e)
    finally:
        if conn:
            conn.close()

