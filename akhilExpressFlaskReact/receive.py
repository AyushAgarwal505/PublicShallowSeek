import requests

url = "http://localhost:5001/process"

text = input("Enter your text: ")

try:
    response = requests.post(url, json={"text": text}, timeout=5)
    if response.status_code == 200:
        print("Server Response:", response.json().get("response"))
    else:
        print(f"Error: {response.status_code}, {response.text}")
except requests.exceptions.ConnectionError:
    print("Error: Could not connect to the server. Ensure it is running.")
except requests.exceptions.Timeout:
    print("Error: Request timed out. Try again later.")
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
