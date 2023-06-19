# 다이아 이상 유저, 챔피언 플레이 전적 20판 이상
# 기준 플레이어 선택, 팀원 중 조건에 부합하는 사용자를 저장
# 플레이어의 특정 클라 버전 내의 칼바람 매치를 가져온다. (queue=450으로 하면 칼바람만 가져올 수 있음)
# 칼바람 매치를 다 가져왔다면 매치 id를 저장한다.
# 다음 플레이어로 넘어가서 매치를 가져오되 수집되었던 매치가 아닌 매치만을 가져온다.
# 목표 매치 수 한국 1만, 미국 1만 / 2분에 100리퀘, 최선은 200분정도 예상
# 차선책: 1주일 동안의 데이터를 모아 패치노트의 내용과 비교
import requests
import json
import os
import pandas as pd
import time
from urllib import parse

class Riot():
    def __init__(self, server='kr'):
        with open('API_KEY.txt', 'r') as f:
            self.API_KEYS = f.read().strip()

        self.headers = {
            'X-Riot-Token': self.API_KEYS
        }
        
        self.server = server # la1이 북미, kr이 한국

    def request_url(self, url):
        while True:
            response = requests.get(url, headers=self.headers)
            code = response.status_code
            if code == 429:
                print('Rate Limit! Wait for 60 second')
                time.sleep(60)
            if code == 200:
                break
            if code == 403:
                print("Forbidden! Check if API Key is expired.")
                break

        json_data = response.json()
        return json_data

    def get_summoner_info(self, sum_name):
        url = f'https://{self.server}.api.riotgames.com/lol/summoner/v4/summoners/by-name/'
        url += parse.quote(sum_name)

        json_data = self.request_url(url)
        print(json_data)

    def get_diamond_summoners(self, division, page=1):
        division_dict = {1: 'I', 2:'II', 3:'III', 4:'IV'}
        url = f'https://{self.server}.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/DIAMOND/'
        url += division_dict[division] + '?page=' + str(page)

        json_data = self.request_url(url)
        return json_data

    def get_grandmaster_summoners(self):
        url = f'https://{self.server}.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5'

        json_data = self.request_url(url)
        return json_data

    def get_master_summoners(self):
        url = f'https://{self.server}.api.riotgames.com/lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5'

        json_data = self.request_url(url)
        return json_data

    def get_challenger_summoners(self):
        url = f'https://{self.server}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5'

        json_data = self.request_url(url)
        return json_data
    
    def make_summoner_df(self):
        df = pd.DataFrame()
        for i in range(1, 5):
            js = self.get_diamond_summoners(i, 1)
            df = pd.concat([df, pd.DataFrame(js)], ignore_index=True)

        js = self.get_master_summoners()
        m = pd.DataFrame(js['entries'])
        m['tier'] = 'MASTER'
        df = pd.concat([df, m], ignore_index=True)

        js = self.get_grandmaster_summoners()
        gm = pd.DataFrame(js['entries'])
        gm['tier'] = 'GRANDMASTER'
        df = pd.concat([df, gm], ignore_index=True)

        js = self.get_challenger_summoners()
        c = pd.DataFrame(js['entries'])
        c['tier'] = 'CHALLENGER'
        df = pd.concat([df, c], ignore_index=True)

        df = df[['summonerId','summonerName', 'tier']]
        df.to_csv('data/summoners.csv', index=False)


if __name__ == '__main__':

    r = Riot('kr')
    #r.get_summoner_info("만 당")
    #r.get_summoner_by_tier(1, 1)
    #r.get_grandmaster_summoners()
    #r.get_master_summoners()
    #r.make_summoner_df()
            