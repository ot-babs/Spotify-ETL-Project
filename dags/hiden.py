import base64
import requests
import datetime


SPOTIFY_TOKEN = "BQCTcY1FhtwEJLiJ9QCbQ8nVYqTdmbGWQGZe1_e67hIbNVPDPe0D-Q28ElzYNdM9TnvfqmxrCV5y7wYmnflBMkm42wpjt2CMtA1k-8FCrIgy0eohli0GF8ZbbVZEdaJLHSy5aOfURHxWQKVRJCafyhHFFge-wbzwtjxU2u5VrfPyzg6RhVs"
USER_ID = "11125726624"
CLIENT_ID = "6ccbd78d67084e2bae883fe7a9d9bce9"
CLIENT_SECRETE = "7c98342f7f274ba2bed3c3e4bd5f61e3"
refresh_token = "AQCXz4D4VQoCrXTSkcGnlVpzJWDAv85_UMb3zEweKAryS5lBQ7A1bQaBAOFKxEnND5wAP6p1BpQ02Bkpqu9JHoCSBtMRNUToiDJJ0lHdX6EdgC4LESg605aBGqM48wuJF_g"
base_64 = "NmNjYmQ3OGQ2NzA4NGUyYmFlODgzZmU3YTlkOWJjZTk6N2M5ODM0MmY3ZjI3NGJhMmJlZDNjM2U0YmQ1ZjYxZTM="


#https://accounts.spotify.com/en/authorize?client_id=6ccbd78d67084e2bae883fe7a9d9bce9&response_type=code&redirect_uri=https%3A%2F%2Fgithub.com%2Fot-babs&scope=user-read-recently-played

#curl -H "Authorization: Basic NmNjYmQ3OGQ2NzA4NGUyYmFlODgzZmU3YTlkOWJjZTk6N2M5ODM0MmY3ZjI3NGJhMmJlZDNjM2U0YmQ1ZjYxZTM=" -d grant_type=authorization_code -d code=AQDtTFPx4ypHamVf_GpS9W3IK5eUSvt5Q1Md297QAduFfK23d41YIJZS0pPXhVp_KgWDb155ReG4hyDnAd9KDdCyDpI3SQO9ru0S4_a1m9vmlTYWCBTIfg2uNydT-iYYc0TPH3_dCh6W-NOaP1L_kEHzPFkBe8Teyfx65Evgxd8dW-mKFEdPpeqdltZfFosWsRF8NwrEis55 -d redirect_uri=https%3A%2F%2Fgithub.com%2Fot-babs https://accounts.spotify.com/api/token
headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=SPOTIFY_TOKEN)
    }

#Want time in unix milliseconds to convert yesterdaytes date to this. Allows us to see what songs are played in the last 24 hours
today = datetime.datetime.now()
yesterday =  today - datetime.timedelta(days=1)
yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

r = requests.get("https://api.spotify.com/v1/me/player/recently-played?limit=50&after={time}".format(time=yesterday_unix_timestamp), headers = headers) 
