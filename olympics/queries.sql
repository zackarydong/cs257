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




