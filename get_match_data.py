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


class Riot():
    def __init__(self):
        with open('./project/riot/API_KEY.txt', 'r') as f:
            self.API_KEYS = f.read().strip()

    def get_summoner_info(self, sum_name):
        url = 'https://kr.api.riotgames.com/lol/summoners/v4/by-name/'
        url += sum_name
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://developer.riotgames.com",
            "X-Riot-Token": self.API_KEYS
        }  
