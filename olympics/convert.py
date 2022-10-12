'''
    convert.py
    Zack Dong, 11 Oct 2021

    Illustrating how to use Python dictionaries, etc. to
    start converting the data. This is based on the Kaggle
    Olympics data, and assumes you have a copy of the
    athlete_events.csv and noc_regions.csv file. You can 
    download them at this link:
    https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results    

    CREATE TABLE athletes (
        id SERIAL,
        firstname text,
        nickname text,
        lastname text,
        gender text,
        team text
    );

    CREATE TABLE event_categories (
        id SERIAL,
        name text
    );

    CREATE TABLE events (
        id SERIAL,
        event_category_id int,
        event text
    );

    CREATE TABLE games (
        id SERIAL,
        year int,
        season text,
        city text
    );

    CREATE TABLE regions (
        id SERIAL,
        noc text,
        country text,
        notes text
    );

    CREATE TABLE event_results (
        athlete_id int,
        event_id int,
        games_id int,
        regions_id int,
        medal text
    );

    When I run this code, I end up with six new files: athletes.csv, 
    event_categories.csv events.csv, games.csv, regions.csv, and 
    event_results.csv. 

    One of the rows in athletes.csv is:

       11495,Simone Arianne,,Biles,F,United States

     One of the rows in event_categories.csv is:

       13,Gymnastics

     One of the rows in events.csv is:

       214,13,Gymnastics Women's Individual All-Around

    One of the rows in games.csv is:

        1,2016,Summer,Rio de Janeiro

    One of the rows in regions.csv is:

        69,FIN,Finland,

    And one of the rows in event_results.csv is:

        11495,214,1,69,Gold

    When you combine five of the rows (excluding regions) from the different tables, 
    you can conclude that Simone Biles (From America) won the Gold medal in the
    Gymnastics Women's Individual All-Around in the 2016 Summer Olympic Games 
    in Rio de Janeiro
'''

import csv

# (1) Table for athletes. Create a dictionary that maps athlete_id -> athlete_name
#       and then save the results in athletes.csv. The athlete names are split up
#       by first name, nickname, and lastname.
athletes = {}
with open('athlete_events.csv') as original_data_file,\
        open('athletes.csv', 'w') as athletes_file:
    reader = csv.reader(original_data_file)
    writer = csv.writer(athletes_file)
    heading_row = next(reader) # eat up and ignore the heading row of the data file
    for column in reader:
        athlete_id = column[0]
        athlete_nickname = ""
        if athlete_id not in athletes: #if id number hasn't been found in dictionary
            noNickname = True
            athlete_firstname = ""
            athlete_lastname = ""
            name_parts = column[1].split(" ") # splits up the names by spaces
            for i, name in enumerate(name_parts):
                changed_name = name.strip("\"") 
                changed_name = changed_name.strip("'")
                if changed_name != name: #if this name is a nickname, i.e. if it was stripped of the quotations
                    noNickname = False
                    athlete_nickname = changed_name
                    j = 0
                    while j < i: #takes every part before nickname
                        athlete_firstname += name_parts[j] + " "
                        j += 1
                    athlete_firstname = athlete_firstname.rstrip() #clean up white space
                    athlete_firstname = athlete_firstname.lstrip()
                    if name_parts[-1].startswith("("): #if they changed their last name
                        athlete_lastname = name_parts[-2] + " " + name_parts[-1] 
                        break
                    else:
                        athlete_lastname = name_parts[-1]
                        break
            if noNickname: #If there was no nickname found
                if name_parts[-1].startswith("("): #if they changed their last name
                    athlete_lastname = name_parts.pop(-2) + " " + name_parts.pop(-1) 
                else:
                    athlete_lastname = name_parts.pop(-1)
                for names in name_parts:
                    athlete_firstname += names + " "
                athlete_firstname = athlete_firstname.rstrip()
                athlete_firstname = athlete_firstname.lstrip()
            athlete_name = column[1]
            athlete_gender = column[2]
            athlete_team = column[6]
            athletes[athlete_id] = athlete_name #store in dictionary
            writer.writerow([athlete_id, athlete_firstname, athlete_nickname, athlete_lastname, athlete_gender, athlete_team])

# (2) Table for event categories. Create a dictionary that maps event_name -> event_id
#       and then save the results in event_categories.csv. This dictionary is used for the 
#       events table
event_categories = {}
with open('athlete_events.csv') as original_data_file,\
        open('event_categories.csv', 'w') as events_file:
    reader = csv.reader(original_data_file)
    writer = csv.writer(events_file)
    heading_row = next(reader) # eat up and ignore the heading row of the data file
    for column in reader:
        event_sport = column[12]
        if event_sport not in event_categories:
            event_id = len(event_categories) + 1
            event_categories[event_sport] = event_id
            writer.writerow([event_id, event_sport])

# (2) Table for events. Create a dictionary that maps event_category -> event_id
#       and then save the results in events.csv. The events category dictionary is also 
#       called to retrieve the more specific event category
events = {}
with open('athlete_events.csv') as original_data_file,\
        open('events.csv', 'w') as events_file:
    reader = csv.reader(original_data_file)
    writer = csv.writer(events_file)
    heading_row = next(reader) # eat up and ignore the heading row of the data file
    for column in reader:
        event_sport = column[12]
        event_category = column[13]
        if event_category not in events:
            event_id = len(events) + 1
            events[event_category] = event_id
            event_category_id = event_categories[event_sport] 
            writer.writerow([event_id, event_category_id, event_category])

# (4) Create a dictionary that maps games_year_season -> games_id
#       and then save the results in games.csv. Note that 
#       games_year_season is only used in the dictionary,
#       and year and season are broken into two separate 
#       columns
games = {}
with open('athlete_events.csv') as original_data_file,\
    open('games.csv', 'w') as games_files:
    reader = csv.reader(original_data_file)
    writer = csv.writer(games_files)
    heading_row = next(reader) # eat up and ignore the heading row of the data file
    for column in reader:
        games_id = column[0]
        games_year = column[9]
        games_season = column[10]
        games_city = column[11]
        games_year_season = column[8]
        if games_year_season not in games:    
            games_id = len(games) + 1
            games[games_year_season] = games_id
            writer.writerow([games_id, games_year, games_season, games_city])

# (4) Create a dictionary that maps regions_noc -> regions_id
#       and then save the results in regions.csv. Note that 
#       games_year_season is only used in the dictionary,
#       and year and season are broken into two separate 
#       columns
regions = {}
with open('noc_regions.csv') as original_data_file,\
        open('regions.csv', 'w') as noc_regions_file:
    reader = csv.reader(original_data_file)
    writer = csv.writer(noc_regions_file)
    heading_row = next(reader) # eat up and ignore the heading row of the data file
    regions_id = 1
    for column in reader:
        regions_noc = column[0]
        if regions_noc == 'SIN':
            regions_noc = 'SGP'
        regions_country = column[1]
        regions_notes = column[2]
        regions[regions_noc] = regions_id
        writer.writerow([regions_id, regions_noc, regions_country, regions_notes])
        regions_id += 1


# (5) For each row in the original athlete_events.csv file, build a row
#       for our new event_results.csv table
with open('athlete_events.csv') as original_data_file,\
        open('event_results.csv', 'w') as event_results_file:
    reader = csv.reader(original_data_file)
    writer = csv.writer(event_results_file)
    heading_row = next(reader) # eat up and ignore the heading row of the data file
    for column in reader:
        athlete_id = column[0]
        event_name = column[13]
        games_year_season = column[8]
        regions_noc = column[7]
        medal = column[14]
        regions_id = regions[regions_noc]
        event_id = events[event_name] 
        games_id = games[games_year_season]
        writer.writerow([athlete_id, event_id, games_id, regions_id, medal])

