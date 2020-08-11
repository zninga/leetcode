import asyncio
import os
import time

import aiohttp


async def get_problems_stat(url):
    """获取问题列表"""

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json(content_type="text/html", encoding="utf-8")


async def get_problem_details(url, title):
    """获取问题详细信息"""

    print(f"[Fetch] {title}")
    data = {
        "operationName": "questionData",
        "variables": {"titleSlug": title},
        "query": "query questionData($titleSlug:String!){\nquestion(titleSlug:$titleSlug){\nquestionFrontendId\ntitleSlug\ntranslatedTitle\ntranslatedContent\ndifficulty\ncodeSnippets{\nlang\nlangSlug\ncode\n__typename\n}\n}\n}\n",
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            return await response.json()


def format_and_save_data(results):
    """将结果存为 Markdown 格式"""

    save_dir = "template"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    url_prefix = "https://leetcode-cn.com/problems/"
    trans_level = {"Hard": "困难", "Medium": "中等", "Easy": "简单"}

    for r in results:
        q = r.get("data").get("question")

        file_name = f'{q.get("questionFrontendId")}. {q.get("translatedTitle")}.md'
        title = f'# [{file_name}]({url_prefix+q.get("titleSlug")})'
        level = f'难度：`{trans_level[q.get("difficulty")]}`'
        content = q.get("translatedContent")

        with open(os.path.join(save_dir, file_name), "w") as f:
            f.write("\n\n".join([title, level, "---", content]))


def main():
    problems_url = "https://leetcode-cn.com/api/problems/algorithms/"
    graphql_url = "https://leetcode-cn.com/graphql/"

    loop = asyncio.get_event_loop()
    response = loop.run_until_complete(get_problems_stat(problems_url))

    stats = response.get("stat_status_pairs")

    title_slugs = [
        p.get("stat").get("question__title_slug")
        for p in stats
        if not p.get("paid_only")
    ]

    tasks = []
    for title in title_slugs:
        task = asyncio.ensure_future(get_problem_details(graphql_url, title))
        tasks.append(task)

    results = loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()

    format_and_save_data(results)


if __name__ == "__main__":
    start = time.time()

    main()

    end = time.time()
    print(f"Time cost: {end - start}''")
