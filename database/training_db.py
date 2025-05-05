import sqlite3
import pandas as pd
import numpy as np
import uuid

from backend import global_vars


def save_training_session():
    try:
        conn = sqlite3.connect('/home/karate/karateProjectFullstack/database/karate.db')
        cur = conn.cursor()

        cur.execute(f"PRAGMA table_info(Trainings)")
        columns = [row[1] for row in cur.fetchall()]
        column_str = ', '.join(columns)
        placeholders = ', '.join(['?' for _ in columns])
        query = f"INSERT INTO Trainings ({column_str}) VALUES ({placeholders})"
        
        user_id = global_vars.current_user.get_user_id()
        session_id = str(uuid.uuid1())
        start_time = global_vars.time_vector[0]
        end_time = global_vars.time_vector[-1]
        punch_count = len(global_vars.currentMeasurementStats)
        max_training_score = np.max(global_vars.currentMeasurementStats.Score)

        name = global_vars.current_user.get_name()
        time = global_vars.time_vector[0].strftime("%y.%m.%d-%H:%M:%S.%f")
        raw_data_filename = name + "rawData" + time + ".csv"

        query_vals = [None] * len(columns)
        query_vals[0] = user_id
        query_vals[1] = session_id
        query_vals[2] = start_time
        query_vals[3] = end_time
        query_vals[4] = punch_count
        query_vals[5] = max_training_score
        query_vals[8] = raw_data_filename


        cur.execute(query, query_vals)
        conn.commit()

        #sql_trainings = "SELECT * FROM Trainings"
        #cur.execute(sql_trainings)
        #all_trainings = cur.fetchall()
        #print(all_trainings)

        """
        save all punches of this session as well, into Punches table
        """
        #print("!!!!!!!!!!!!!!!!")
        cur.execute(f"PRAGMA table_info(Punches)")
        columns_P = [row[1] for row in cur.fetchall()]
        column_str_P = ', '.join(columns_P)
        placeholders_P = ', '.join(['?' for _ in columns_P])
        query = f"INSERT INTO Punches ({column_str_P}) VALUES ({placeholders_P})"
        #print(columns_P)
        #print(query)
        #print(column_str_P)
        #print(global_vars.currentMeasurementStats.columns)

        user_df = global_vars.currentMeasurementStats.copy()
        user_df.insert(0, "user_id", user_id)
        user_df.insert(1, "session_id", session_id)
        punches_db = user_df[columns_P]
        #print("punches_db cols:")
        #print(punches_db.columns)
        #print(punches_db)

        cur.executemany(query, punches_db.values)
        conn.commit()

        #sql_punches = "SELECT * FROM Punches"
        #cur.execute(sql_punches)
        #all_punches = cur.fetchall()
        #print(all_punches)

    except sqlite3.Error as error:
        print("Failed to execute the above query", error)

    finally:
        if conn:
            conn.close()
