import requests
import schedule
import time
from bs4 import BeautifulSoup
import openai

# OpenAI API key
openai.api_key = "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"

def scrape_bloomberg():
    url = "https://www.bloomberg.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    top_stories = soup.find_all("article", class_="card")

    summaries = []
    for story in top_stories:
        headline = story.find("h2").text.strip()
        link = url + story.find("a")["href"]

        article_text = requests.get(link).text
        article_soup = BeautifulSoup(article_text, "html.parser")

        paragraphs = article_soup.find_all("p")
        content = " ".join(p.text for p in paragraphs)

        summary = summarize(content)
        summaries.append({"headline": headline, "summary": summary})

    return summaries

def summarize(text):
    prompt = f"Please provide a brief summary of the following text:\n\n{text}"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].text.strip()

def write_markdown(summaries):
    with open("bloomberg_summary.md", "w") as f:
        for summary in summaries:
            f.write(f"## {summary['headline']}\n\n")
            f.write(f"{summary['summary']}\n\n")

def main():
    summaries = scrape_bloomberg()
    write_markdown(summaries)
    print("Top market news summaries have been updated.")

schedule.every(1).hour.do(main)

if __name__ == "__main__":
    main()
    while True:
        schedule.run_pending()
        time.sleep(60)
