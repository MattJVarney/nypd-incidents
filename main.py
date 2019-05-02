## Matthew Varney
# NYPD Traffic Data

import os
import tarfile
import sqlite3
import csv
import pandas as pd
import matplotlib.pyplot as plt

from dateutil import parser


# This function intializes the project for the first time.
# It unzips the csv that was cloned into the project
# It creates a SQL lite database with data/
# It creates a table called `collisions` and it imports the data
def setup():
    exists = os.path.isfile("data/sqllite/collision.db")
    if not exists:
        print "Unzipping collision data..."

        tar = tarfile.open("data/NYPD_Motor_Vehicle_Collisions.csv.tar.gz")
        tar.extractall('data/')
        tar.close()

        c = conn.cursor()

        c.execute(''' DROP TABLE IF EXISTS collisions''')
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
                count += 1
                if (count == 1):
                    continue

                #normalizes the data
                dt = parser.parse(row[0])
                row[0] = dt.strftime('%Y-%m-%d')

                # normalizes the time
                dt = parser.parse(row[1]);
                row[1] = dt.strftime('%H:%M')

                c.execute("INSERT INTO collisions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
                          "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", row)
                if (count % 10000 == 0):
                    print "processed " + str(count) + " records (out of 1.45M)"
                    conn.commit()
    else:
        conn = sqlite3.connect('data/sqllite/collision.db')
        conn.commit()
        conn.close()
def generateCrashsByMonth():
    conn = sqlite3.connect('data/sqllite/collision.db')
    df = pd.read_sql_query(
        '''SELECT
            count(*) as count,
            strftime("%m", date) as 'month' 
        FROM collisions
        GROUP BY strftime("%m", date)
        ''',
    conn)

    df.plot()
    plt.title('Crashes By Month')
    plt.xlabel("Month")
    plt.ylabel("Crashes")
    plt.savefig("crashesByMonth.png")


def generateCrashByBorough():
    conn = sqlite3.connect('data/sqllite/collision.db')
    myQ = pd.read_sql_query(
        '''SELECT borough, COUNT(borough) as frequency
        FROM collisions
        GROUP BY borough
        ORDER BY COUNT(*) ASC;
        ''',
        conn)
    hist = myQ.plot.bar(x = 'borough', y = 'frequency', rot = 0)
    plt.title('Crashes By Burough')
    plt.xlabel('Borough')
    plt.ylabel('Total of Crashes')
    plt.savefig('crashesByBoroughBar')

def scatterNYC():
    conn = sqlite3.connect('data/sqllite/collision.db')
    myQ = pd.read_sql_query(
    '''
    SELECT CAST(latitude AS NUMERIC) AS lat, CAST(longitude AS NUMERIC) AS long
    FROM collisions
    WHERE lat > 40
    '''
    , conn)
    scatter = myQ.plot.scatter(x = 'long', y = 'lat')
    plt.savefig('crashesByLatLong')

def generateCrashsByTimeOfDay():
    conn = sqlite3.connect('data/sqllite/collision.db')
    df = pd.read_sql_query(
        '''SELECT
            sum(num_killed) as sum,
            count(*) as count,
            strftime("%H", time) hour
        FROM collisions
        GROUP BY strftime("%H", time)
        ''',
        conn)

    df.plot()
    plt.title('Crashes By Time Of Day')
    plt.xlabel("Time")
    plt.ylabel("Crashes")

    plt.savefig("crashesByTimeOfDay.png")

def generateCrashesByDayOfWeek():
    conn = sqlite3.connect('data/sqllite/collision.db')
    myQ = pd.read_sql_query(
        '''
            SELECT 
                strftime('%w', date) day,
                round(count(*) / (SELECT cast (COUNT(*) as real) FROM collisions) * 100, 1) perc
            FROM collisions
            GROUP by strftime('%w', date);
        ''',
        conn)

    bars = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')

    hist = myQ.plot.bar(x = 'day', y = 'perc', rot = 0)
    plt.xticks([0,1,2,3,4,5,6], bars, color='black')
    plt.title('Crashes By Day Of Week')
    plt.xlabel('Day')
    plt.ylabel('Percentage')
    plt.savefig('crashesByDayOfWeekBar')

# def generateCrashesWithDeathsByContributingFactor():
#     conn = sqlite3.connect('data/sqllite/collision.db')
#     myQ = pd.read_sql_query(
#         '''
#             SELECT
#                 contributing_factor_veh_1,
#                 sum(num_motor_killed) deaths
#             FROM collisions
#             GROUP by strftime('%w', date);
#         ''',
#         conn)
#
#     bars = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')
#
#     hist = myQ.plot.bar(x = 'day', y = 'perc', rot = 0)
#     plt.xticks([0,1,2,3,4,5,6], bars, color='black')
#     plt.title('Crashes By Day Of Week')
#     plt.xlabel('Day')
#     plt.ylabel('Percentage')
#     plt.savefig('crashesByDayOfWeekBar')


def generateAlcoholCrashesByDayOfWeek():
    conn = sqlite3.connect('data/sqllite/collision.db')
    myQ = pd.read_sql_query(
        '''
            SELECT 
                strftime('%w', date) day,
                round(count(*) / (SELECT cast (COUNT(*) as real) FROM collisions WHERE contributing_factor_veh_1 = 'Alcohol Involvement') * 100, 1) perc
            FROM collisions
            WHERE contributing_factor_veh_1 = 'Alcohol Involvement'
            GROUP by strftime('%w', date);
        ''',
        conn)

    bars = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')

    hist = myQ.plot.bar(x='day', y='perc', rot=0)
    plt.xticks([0, 1, 2, 3, 4, 5, 6], bars, color='black')
    plt.title('Alcohol Crashes By Day Of Week')
    plt.xlabel('Day')
    plt.ylabel('Percentage')
    plt.savefig('alcoholCrashesByDayOfWeekBar')


def generateDeathsByMonth():
    conn = sqlite3.connect('data/sqllite/collision.db')
    df = pd.read_sql_query(
        '''SELECT
            sum(num_killed) as sum,
            strftime("%m", date) as 'month' 
        FROM collisions
        GROUP BY strftime("%m", date)
        ''',
    conn)

    df.plot()
    plt.title('Traffic Deaths By Month')
    plt.xlabel("Month")
    plt.ylabel("Deaths")
    plt.savefig("deathsByMonth.png")


if __name__ == '__main__':
    setup()
    generateAlcoholCrashesByDayOfWeek()
    generateCrashesByDayOfWeek()
    generateCrashsByMonth()
    generateDeathsByMonth()
    generateCrashsByTimeOfDay()
    generateCrashByBorough()
    scatterNYC()