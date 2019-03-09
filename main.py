## Matthew Varney
# NYPD Traffic Data

import os
import tarfile
import sqlite3
import csv

def setup():
    exists = os.path.isfile('data/NYPD_Motor_Vehicle_Collisions.csv')
    if not exists:
        print "Unzipping collision data..."
        tar = tarfile.open("data/NYPD_Motor_Vehicle_Collisions.csv.tar.gz")
        tar.extractall('data/')
        tar.close()

    conn = sqlite3.connect('data/sqllite/collision.db')

    c = conn.cursor()

    # Create table
    c.execute('''
        CREATE TABLE IF NOT EXISTS collisions (
            date date,
            time text,
            borough text,
            zip int,
            latitude real ,
            longitude real ,
            location text,
            on_street_name text,
            off_street_name text,
            cross_street_name text,
            num_injured int,
            num_killed int,
            num_ped_injured int,
            num_ped_killed text,
            num_cycle_injured text,
            num_cycle_killed text,
            num_motor_injured text,
            num_motor_killed text,
            contributing_factor_veh_1 text,
            contributing_factor_veh_2 text,
            contributing_factor_veh_3 text,
            contributing_factor_veh_4 text,
            contributing_factor_veh_5 text,
            unique_key int,
            veh_type_code_1 text,
            veh_type_code_2 text,
            veh_type_code_3 text,
            veh_type_code_4 text,
            veh_type_code_5 text
        )
    ''')


    print "PROCESSING CSV INTO SQL LITE"
    with open('data/NYPD_Motor_Vehicle_Collisions.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        count = 0;
        for row in readCSV:
            c.execute("INSERT INTO collisions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
                      "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", row)
            if (count % 10000 == 0):
                print "processed " + str(count) + " records (out of 1.4M)"
                conn.commit()
            count += 1
    # Save (commit) the changes
    conn.commit()

    conn.close()


if __name__ == '__main__':
    setup()