import requests

def get_menu():
  url = "https://dksh.awskorea.kr"
  response = requests.get(url)
  data = response.json()
  
  return f'{data["menu"]} ([이미지]({data["image"]}))'