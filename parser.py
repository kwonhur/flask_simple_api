import request, json
from requests_futures.sessions import FuturesSession

def parse(tags) -> list:
    urls = [f"https://hatchways.io/api/assessment/blog/posts?tag={tag}" for tag in tags]
    print (urls)
    final_list = []
    with FuturesSession() as session:
        futures = [session.get(url) for url in urls]
        for future in futures:
            response_obj = future.result()
            for post in json.loads(response_obj.text)["posts"]:
                final_list.append(post)
        return list({v["id"]:v for v in final_list}.values())

