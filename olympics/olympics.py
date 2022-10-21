'''
    olympics.py
    Zack Dong, 20 October 2022
'''

import sys
import argparse
import psycopg2
import config

def print_usage():
     print('usage: python3 [-h] [-a ATHLETES] [-m [MEDALS]] [-y YEAR]')

def get_connection():
    ''' Returns a database connection object with which you can create cursors,
        issue SQL queries, etc. This function is extremely aggressive about
        failed connections--it just prints an error message and kills the whole
        program. Sometimes that's the right choice, but it depends on your
        error-handling needs. '''
    try:
        return psycopg2.connect(database=config.database,
                                user=config.user,
                                password=config.password)
    except Exception as e:
        print(e, file=sys.stderr)
        exit()

def get_country_noc(noc):
    ''' Returns country from NOC code'''
    noc = noc.upper()
    try:
        query =  '''SELECT country 
                    FROM regions
                    WHERE regions.noc = %s
                    '''
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (noc,))
        country = cursor.fetchone()[0] #Retrieves the country from the cursor

    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()

    return country
    
    

def get_country_athletes(noc):
    ''' Returns a list of the full names of all athletes in the database
        from NOC country code. '''
    noc = noc.upper()
    athletes = []
    try:
        query =  '''SELECT athletes.firstname, athletes.lastname 
                    FROM athletes, regions, event_results
                    WHERE athletes.id = event_results.athlete_id 
                    AND regions.id = event_results.regions_id 
                    AND regions.noc = %s
                    GROUP BY athletes.firstname, athletes.lastname;'''
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (noc,))
        for row in cursor:
            firstname = row[0]
            lastname = row[1]
            athletes.append(f'{firstname} {lastname}')

    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return athletes

def get_country_medals(medal):
    ''' Returns a full list of countries and the number of medals, with gold being the default. '''
    medal = medal.lower()
    medals = []
    try:
        query =  '''SELECT regions.noc, COUNT(event_results.medal) AS medal_count
                    FROM regions, event_results
                    WHERE regions.id = event_results.regions_id
                    AND LOWER(event_results.medal) = %s
                    GROUP BY regions.noc
                    ORDER By medal_count DESC;'''
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (medal,))
        for row in cursor:
            country = row[0]
            medal_count = row[1]
            medals.append(f'{country}:  {medal_count}')

    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return medals

def get_top_athletes(year):
    ''' Returns a list of top 10 athletes and their respective countries, main event, and their medal counts. '''
    athletes = []

    try:
        query =  '''SELECT athletes.firstname, athletes.lastname, athletes.team, event_categories.name, COUNT(event_results.medal) AS medal_count
                    FROM athletes, games, event_results, events, event_categories
                    WHERE athletes.id = event_results.athlete_id
                    AND games.id = event_results.games_id
                    AND games.year = %s
                    AND events.id = event_results.event_id
                    AND event_categories.id = events.event_category_id
                    AND event_results.medal !='NA'
                    GROUP BY athletes.lastname, athletes.firstname, athletes.team, event_categories.name
                    ORDER BY medal_count DESC
                    LIMIT 10;''' 
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query,(year,))
        for row in cursor:
            firstname = row[0]
            lastname = row[1]
            country = row[2]
            event = row[3]
            medal_count = row[4]
            athletes.append(f'{firstname} {lastname} ({country}): {medal_count} medals in {event}')

    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return athletes


def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--athletes", help = "Lists names of all athletes from a specified NOC", type = str)
    parser.add_argument("-m", "--medals", nargs='?', const = 'gold', help = " List all the NOCs and the number of medals they have won," 
                                            " in decreasing order of the number of medals. The default is gold")
    parser.add_argument("-y", "--year", help = " Lists the top 10 athletes with the most medals in the specified year " 
                                            " as well their respetive countries and events", type = int)                                            
    args = parser.parse_args()
    arguments = sys.argv

    if(len(arguments)==1): #If no arguments typed, print usage statement
        return print_usage()

    if args.medals:
        medal = args.medals
        medal = medal.lower().capitalize()
        if medal not in ['Gold', 'Silver', 'Bronze']:
            print('Not a valid medal color. Choose from gold, silver, or bronze')
            return 
        medals = get_country_medals(medal)
        print('--------------------------------------------------------')
        print(f'========== {medal} Medal counts by Country ==========')
        for country in medals:
            print(country)
        print('======================================================== \n')
    elif args.athletes:
        noc = args.athletes
        if len(noc) != 3:
            print('Not a valid NOC. Please enter a 3 letter country code.')
            return
        country = get_country_noc(noc)
        athletes = get_country_athletes(noc)
        if len(athletes) == 0:
            print('Not a valid NOC. Please try again')
            return
        print('--------------------------------------------------------')
        print(f'========== All athletes from {country} ({noc.upper()}) ==========')
        for athlete in athletes:
            print(athlete)
        print('======================================================== \n')
    elif args.year:
        year = args.year
        if year > 2016 or year % 2 != 0:
            print('Not a valid olympic year in this data set. Please try again')
            return
        country = get_top_athletes(year)
        print()
        print(f'========== Top 10 athletes from the {year} Olympics ==========')
        print('---------------------------------------------')
        for athlete in country:
            print(athlete)
            print('---------------------------------------------')
        print('======================================================== \n')


if __name__ == '__main__':
    main()