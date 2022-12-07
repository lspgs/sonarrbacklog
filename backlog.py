import requests
import random
import os
from dotenv import load_dotenv

# Gets list of shows from Sonarr using existing Sonarr API
def getShows(key,base):
  
    url = f'{base}/api/series'
    headers = {
          'X-Api-Key': key
    }
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json()

# Gets the user's show selection
def getShowSelection(key,base):
    shows = getShows(key,base)
    for show in shows:
        print(f"{show['id']}: {show['title']}")
    show_id = int(input("Please select a show by ID: "))
    return show_id

# Gets the number of seasons and episodes from the show
def getSeasonsEpisodes(key,base,show_id):
    url = f"{base}/api/series/{show_id}"
    headers = {
  'X-Api-Key': key
    }    
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        show = r.json()
        return show['seasonCount'], show['totalEpisodeCount']

# Gets the number of episodes the user wants
def getEpisodesWanted():
    num_episodes = int(input("Please enter the number of episodes you want: "))
    return num_episodes

# Gets the randomly selected episodes from the show
def getRandomEpisodes(key,base,show_id, num_episodes):
    url = f"{base}/api/episode?seriesId={show_id}"
    headers = {
          'X-Api-Key': key
    }
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        #ignore specials and already monitored episdoes
        episodes = r.json()
        episodes = [x for x in episodes if(x['seasonNumber'] != 0 and x['monitored'] != True)]
        random_episodes = random.sample(episodes, num_episodes)
        return random_episodes

def monitorEpisode(key,base,episode):
    url = f'{base}/api/v3/episode/monitor'
    headers = {
        'X-Api-Key': key,
        'Content-Type': 'application/json'
    }
    data = {
        'episodeIds': [episode],
        'monitored': True
    }
    r = requests.put(url, headers=headers, json=data)
    if r.status_code == 200:
        resp = r.json()
        return ()


# Main
def main():
    load_dotenv()
    key=os.getenv('api_key')
    url=os.getenv('api_url')
    show_id = getShowSelection(key,url)
    seasons, episodes = getSeasonsEpisodes(key,url,show_id)
    print(f"There are {seasons} seasons and {episodes} total episodes.")
    num_episodes = getEpisodesWanted()
    random_episodes = getRandomEpisodes(key,url,show_id, num_episodes)
    for episode in random_episodes:
        episode_id=episode['id']
        #monitorEpisode(key,url,episode_id)
        print(f"Season: {episode['seasonNumber']}, Episode: {episode['episodeNumber']}, Title: {episode['title']} marked as monitored.")
if __name__ == "__main__":
    main()