from api import Posts, Ping
import requests
import json

def test_posts_api_endpoint():
    url = "http://127.0.0.1:5000/api/posts?tags=tech&direction=desc"
    resp = requests.get(url)
    assert resp.status_code == 200
    assert resp.url == url

def test_ping_api_endpoint():
    url = "http://127.0.0.1:5000/api/ping"
    resp = requests.get(url)
    assert resp.status_code == 200
    assert json.loads(resp.text)["success"] == True