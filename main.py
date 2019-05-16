#!/usr/bin/env python

## Matthew Varney
# NYPD Traffic Data

import os
import tarfile
import sqlite3
import csv
import numpy as np
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

        conn = sqlite3.connect('data/sqllite/collision.db')
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

def printInjuryRateOfAlcoholVsNonAlcohol():
    conn = sqlite3.connect('data/sqllite/collision.db')
    df = pd.read_sql_query(
        '''
        SELECT
            alcohol_total,
            non_alcohol_total,
            alcohol_injuries,
            non_alcohol_injuries,
            alcohol_injuries * 1.0 / alcohol_total as al_inj_rate,
            non_alcohol_injuries * 1.0 / non_alcohol_total as non_al_inj_rate,
            alcohol_killed,
            non_alcohol_killed,
            alcohol_killed * 1.0 / alcohol_total as al_killed_rate,
            non_alcohol_killed * 1.0 / non_alcohol_total as non_al_killed_rate
        FROM (
            SELECT
                (SELECT count(1) FROM collisions WHERE contributing_factor_veh_1 = 'Alcohol Involvement' AND num_injured > 0) as alcohol_injuries,
                (SELECT count(1) FROM collisions WHERE contributing_factor_veh_1 != 'Alcohol Involvement' AND num_injured > 0) as non_alcohol_injuries,
                (SELECT count(1) FROM collisions WHERE contributing_factor_veh_1 = 'Alcohol Involvement' AND num_killed > 0) as alcohol_killed,
                (SELECT count(1) FROM collisions WHERE contributing_factor_veh_1 != 'Alcohol Involvement' AND num_killed > 0) as non_alcohol_killed,
                (SELECT count(1) FROM collisions WHERE contributing_factor_veh_1 = 'Alcohol Involvement') as alcohol_total,
                (SELECT count(1) FROM collisions WHERE contributing_factor_veh_1 != 'Alcohol Involvement') as non_alcohol_total
            FROM collisions
            LIMIT 1
        )
        ''',
        conn)

    print "---"
    print "PRINTING ALCOHOL INJURY RATES"
    print df
    print "---\n"

def generateCrashesByMonth():
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
    plt.savefig("charts/crashesByMonth.png")

def generateCrashesByYear():
    conn = sqlite3.connect('data/sqllite/collision.db')
    df = pd.read_sql_query(
        '''SELECT
            count(*) as count,
            strftime("%J", date) - 2456108.5 as day
        FROM collisions
        GROUP BY strftime("%J", date) - 2456108.5
        ''',
    conn)

    df.plot()
    plt.title('Crashes Over Time')
    plt.xlabel("Day")
    plt.ylabel("Crashes")
    plt.savefig("charts/crashesOverTime.png")


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
    plt.savefig('charts/crashesByBoroughBar')

def heatmapNYC():
    conn = sqlite3.connect('data/sqllite/collision.db')
    df = pd.read_sql_query(
        '''
        SELECT CAST(latitude AS NUMERIC) AS lat, CAST(longitude AS NUMERIC) AS long
        FROM collisions
        WHERE lat > 40
        AND lat < 41
        AND long > -74.4
        AND long < -73
        '''
        , conn)

    heatmap, xedges, yedges = np.histogram2d(df.long, df.lat, bins=50)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    plt.clf()
    plt.imshow(heatmap.T, extent=extent, origin='lower')
    plt.savefig('charts/crashesByLatLongHeatmap')

def scatterNYC():
    conn = sqlite3.connect('data/sqllite/collision.db')
    myQ = pd.read_sql_query(
    '''
    SELECT CAST(latitude AS NUMERIC) AS lat, CAST(longitude AS NUMERIC) AS long
    FROM collisions
    WHERE lat > 40
        AND lat < 41
        AND long > -74.4
        AND long < -73
    '''
    , conn)
    scatter = myQ.plot.scatter(x = 'long', y = 'lat')
    plt.savefig('charts/crashesByLatLongPlot')

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

    plt.savefig("charts/crashesByTimeOfDay.png")

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
    plt.savefig('charts/crashesByDayOfWeekBar')

def generateCrashesByFactorPie():
    conn = sqlite3.connect('data/sqllite/collision.db')
    df = pd.read_sql_query(
        '''SELECT
            count(*) as count,
            contributing_factor_veh_1 
        FROM collisions
        GROUP BY contributing_factor_veh_1
        HAVING count > 24000
        ORDER BY count DESC
        ''',
        conn)


    # Data to plot
    plt.pie(
        # using data total arrests
        df['count'],
        # with the labels being officer names
        labels=df['contributing_factor_veh_1'],
        # with no shadows
        shadow=False,
        # with the start angle at 90%
        startangle=60,
        # with the percent listed as a fraction
        autopct='%1.1f%%',
        # rotatelabels=1,
        labeldistance=1.1,
        radius=3,
        textprops={'fontsize': 10}
    )

    # View the plot drop above
    plt.axis('equal')
    plt.subplots_adjust(left=.3, right=.7)
    plt.title('Crash Contributing Factors')
    plt.savefig('charts/crashesByContributingFactorPie', dpi=300)

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
#     plt.savefig('charts/crashesByDayOfWeekBar')


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
    plt.savefig('charts/alcoholCrashesByDayOfWeekBar')

def generateAlcoholCrashesByHour():
    conn = sqlite3.connect('data/sqllite/collision.db')
    myQ = pd.read_sql_query(
        '''
            SELECT 
                strftime("%H", time) hour,
                round(count(*) / (SELECT cast (COUNT(*) as real) FROM collisions WHERE contributing_factor_veh_1 = 'Alcohol Involvement') * 100, 1) perc
            FROM collisions
            WHERE contributing_factor_veh_1 = 'Alcohol Involvement'
            GROUP by strftime("%H", time);
        ''',
        conn)

    hist = myQ.plot.bar(x='hour', y='perc', rot=0)
    plt.title('Alcohol Crashes By Hour of Day')
    plt.xlabel('Hour')
    plt.ylabel('Percentage')
    plt.savefig('charts/alcoholCrashesByHourBar')

def generateAlcoholCrashesByDayOfWeekTimeShifted():
    conn = sqlite3.connect('data/sqllite/collision.db')
    myQ = pd.read_sql_query(
        '''
            SELECT 
                strftime('%w', DATE(date, '-10 hour')) day,
                round(count(*) / (SELECT cast (COUNT(*) as real) FROM collisions WHERE contributing_factor_veh_1 = 'Alcohol Involvement') * 100, 1) perc
            FROM collisions
            WHERE contributing_factor_veh_1 = 'Alcohol Involvement'
            GROUP by strftime('%w', DATE(date, '-7 hour'));
        ''',
        conn)

    bars = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')

    hist = myQ.plot.bar(x='day', y='perc', rot=0)
    plt.xticks([0, 1, 2, 3, 4, 5, 6], bars, color='black')
    plt.title('Alcohol Crashes By Day Of Week Time Shifted')
    plt.xlabel('Day')
    plt.ylabel('Percentage')
    plt.savefig('charts/alcoholCrashesByDayOfWeekTimeShiftedBar')

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
    plt.savefig("charts/deathsByMonth.png")

def printAverages():
    conn = sqlite3.connect('data/sqllite/collision.db')
    df = pd.read_sql_query(
        '''SELECT
            strftime("%Y", date) as year,
            count(*) as crash_count,
            count(*)/365 as crash_daily_avg,
            SUM(num_killed) sum_killed,
            SUM(num_injured) sum_injured
        FROM collisions
        WHERE strftime("%Y", date) != '2012'
            AND strftime("%Y", date) != '2019'
        GROUP BY strftime("%Y", date)
        ''',
    conn)

    print "---"
    print "PRINTING YEARLY AVERAGES"
    print df
    print "---\n"

    df = pd.read_sql_query(
        '''SELECT
            count(*)/365/6 as crash_daily_avg,
            SUM(num_killed)/365/6 killed_daily_avg,
            SUM(num_injured)/365/6 injured_daily_avg
        FROM collisions
        WHERE strftime("%Y", date) != '2012'
            AND strftime("%Y", date) != '2019'
        ''',
        conn)

    print "---"
    print "PRINTING SUMMARY"
    print df
    print "---\n"

def printBoroughCounts():
    conn = sqlite3.connect('data/sqllite/collision.db')
    df = pd.read_sql_query(
        '''SELECT
            borough,
            count(*) as count
        FROM collisions
        GROUP BY borough
        ''',
    conn)

    print "---"
    print "PRINTING BOROUGH TALLY"
    print df
    print "---\n"


if __name__ == '__main__':
    setup()
    printAverages()
    printBoroughCounts()
    printInjuryRateOfAlcoholVsNonAlcohol()
    generateCrashesByFactorPie()
    generateAlcoholCrashesByDayOfWeek()
    generateAlcoholCrashesByHour()
    generateAlcoholCrashesByDayOfWeekTimeShifted()
    generateCrashesByDayOfWeek()
    generateCrashesByMonth()
    generateCrashesByYear()
    generateDeathsByMonth()
    generateCrashsByTimeOfDay()
    generateCrashByBorough()
    scatterNYC()
    heatmapNYC()


    # add cell crashes over time