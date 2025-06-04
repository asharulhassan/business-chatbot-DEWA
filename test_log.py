import requests

url = "https://script.google.com/macros/s/AKfycbyDCDB4bwyofaQ4F5p2dX0IvzQIHwoDWEOzovgW_LJFTUyf9T7zZz0F8JOlkMGD-KiO/exec"
data = {"message": "Logging test from Python"}

res = requests.post(url, data=data)
print("Response:", res.text)
