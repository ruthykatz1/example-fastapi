import requests
import json

############################## Authentication ##############################
# payload = {"username":"example@gmail.com", "password":"example"}
# resp = requests.post("http://127.0.0.1:8000/login", data=payload)
# print(resp.status_code)
# print(json.dumps(json.loads(resp.text), indent=4))
#
# headers = {"Authorization":f"Bearer {json.loads(resp.text)['access_token']}"}
#
# resp = requests.get("http://127.0.0.1:8000")
# print(resp.text)

############################## Post ##############################
# resp = requests.get("http://127.0.0.1:8000/posts", headers=headers)
# print(json.dumps(json.loads(resp.text), indent=4))
# params = {"limit":3, "skip":2, "search":"Animals"}
# resp = requests.get("http://127.0.0.1:8000/posts", headers=headers, params=params)
# print(json.dumps(json.loads(resp.text), indent=4))
# resp = requests.get("http://127.0.0.1:8000/posts?limit=3&skip=2&search=Animals", headers=headers)
# print(json.dumps(json.loads(resp.text), indent=4))

# payload = {"title":"Awsome beaches in Florida", "content":"No aligators there"}
# resp = requests.post("http://127.0.0.1:8000/posts", json=payload, headers=headers)
# print(resp.status_code)
# print(json.dumps(json.loads(resp.text), indent=4))

# resp = requests.get("http://127.0.0.1:8000/posts/5", headers=headers)
# print(resp.status_code)
# print(json.dumps(json.loads(resp.text), indent=4))

# resp = requests.delete("http://127.0.0.1:8000/posts/1", headers=headers)
# print(resp.status_code)
# print(resp.text)
# resp = requests.get("http://127.0.0.1:8000/posts", headers=headers)
# print(resp.text)

# payload = {"title":"Favorite foods", "content":"I like Pizza and chips"}
# resp = requests.put("http://127.0.0.1:8000/posts/6", json=payload, headers=headers)
# print(resp.status_code)
# print(json.dumps(json.loads(resp.text), indent=4))
# resp = requests.get("http://127.0.0.1:8000/posts", headers=headers)
# print(resp.text)


############################## User ##############################
# payload = {"email":"example@gmail.com", "password":"example"}
# resp = requests.post("http://127.0.0.1:8000/users", json=payload)
# print(resp.status_code)
# print(json.dumps(json.loads(resp.text), indent=4))

# resp = requests.get("http://127.0.0.1:8000/users/1", headers=headers)
# print(resp.status_code)
# print(json.dumps(json.loads(resp.text), indent=4))



############################## Vote ##############################
# payload = {"post_id":7, "dir":1}
# resp = requests.post("http://127.0.0.1:8000/vote", json=payload, headers=headers)
# print(resp.status_code)
# print(json.dumps(json.loads(resp.text), indent=4))
