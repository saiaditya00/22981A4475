
import requests

def Log(stack, level, package, message):
    url = "http://20.244.56.144/evaluation-service/logs"
    payload = {
        "stack": stack.lower(),
        "level": level.lower(),
        "package": package.lower(),
        "message": message
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("Log sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send log: {e}")
