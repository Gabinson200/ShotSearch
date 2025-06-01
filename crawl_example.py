import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url="https://www.nbcnews.com/business")

        # Save raw markdown to a text file
        with open("nbcnews_output.txt", "w", encoding="utf-8") as f:
            f.write(result.markdown.fit_markdown)

        print("✅ Markdown exported to nbcnews_output.txt")

if __name__ == "__main__":
    asyncio.run(main())
