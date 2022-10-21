SELECT regions.noc 
FROM regions;

SELECT firstname, nickname, lastname 
FROM athletes 
WHERE athletes.team = 'Jamaica';

SELECT athletes.firstname, athletes.nickname, athletes.lastname, event_results.medal, games.year, games.season, events.event
FROM athletes, games, events, event_results 
WHERE athletes.id = event_results.athlete_id 
AND events.id = event_results.event_id
AND games.id = event_results.games_id
AND athletes.nickname = 'Greg' 
AND athletes.lastname = 'Louganis' 
AND event_results.medal !='NA'
ORDER BY games.year;

SELECT regions.noc, COUNT(event_results.medal) AS medal_count
FROM regions, event_results
WHERE regions.id = event_results.regions_id
AND event_results.medal = 'Gold'
GROUP BY regions.noc
ORDER By medal_count DESC;


SELECT athletes.firstname, athletes.lastname 
FROM athletes, regions, event_results
WHERE athletes.id = event_results.athlete_id 
AND regions.id = event_results.regions_id 
AND regions.noc = 'FRA'
GROUP BY athletes.firstname, athletes.lastname;

SELECT athletes.firstname, athletes.lastname, athletes.team, games.season, event_categories.name, COUNT(event_results.medal) AS medal_count
FROM athletes, games, event_results, events, event_categories
WHERE athletes.id = event_results.athlete_id
AND games.id = event_results.games_id
AND games.year = 1956 
AND events.id = event_results.event_id
AND event_categories.id = events.event_category_id
AND event_results.medal !='NA'
GROUP BY athletes.lastname, athletes.firstname, athletes.team, games.season, event_categories.name
ORDER BY medal_count DESC
LIMIT 10;




