# import requests
#
# url = "https://raw.githubusercontent.com/y-india/images_hosting/main/all_billionaires.txt"
#
# response = requests.get(url)
#
# if response.status_code == 200:
#     data = response.text
#     print(data)
# else:
#     print("Failed to fetch:", response.status_code)
#
#


import urllib.request
import os

url = "https://raw.githubusercontent.com/y-india/images_hosting/main/all_billionaires.txt"

# choose your folder
folder = r"billion_anaysis"
filename = "../all_billionaires.txt"

# create folder if it doesn't exist
os.makedirs(folder, exist_ok=True)

file_path = os.path.join(folder, filename)

# download and save
urllib.request.urlretrieve(url, file_path)

print("Downloaded to:", file_path)