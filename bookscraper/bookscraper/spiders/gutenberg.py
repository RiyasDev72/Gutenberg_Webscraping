import scrapy
import random
from ..items import GutenbergItem


class GutenbergSpider(scrapy.Spider):
    name = "gutenberg"
    allowed_domains = ["www.gutenberg.org"]
    start_urls = ["https://www.gutenberg.org/ebooks/bookshelf/671"]
    custom_settings = {
        "FEEDS": {
            "library.json": {"format": "json"},
            "library.csv": {"format": "csv"},
            # "books.xml": {"format": "xml"},
        }
    }

    def parse(self, response):
        books = response.css("li.booklink")
        for book in books:
            relative_url = book.css("a::attr(href)").get()
            book_url = response.urljoin(relative_url)
            yield response.follow(
                book_url,
                callback=self.parse_book,
                headers={
                    "User-Agent": self.User_list_agent[
                        random.randint(0, len(self.User_list_agent) - 1)
                    ]
                },
            )
        next_page = response.css(
            "span.links a[title='Go to the next page of results.']::attr(href)"
        ).get()
        if next_page is not None:
            next_page_url = response.urljoin(next_page)
            yield response.follow(
                next_page_url,
                callback=self.parse,
                headers={
                    "User-Agent": self.User_list_agent[
                        random.randint(0, len(self.User_list_agent) - 1)
                    ]
                },
            )

    def generate_user_agents(n=100):
        user_agents = []

        chrome_versions = list(range(120, 141))  # Chrome versions
        firefox_versions = list(range(110, 130))  # Firefox versions
        safari_versions = ["16.0", "16.1", "17.0"]
        edge_versions = list(range(120, 141))  # Edge versions

        os_list = [
            "Windows NT 10.0; Win64; x64",
            "Macintosh; Intel Mac OS X 13_4_0",
            "X11; Linux x86_64",
        ]

        for _ in range(n):
            os_choice = random.choice(os_list)
            browser_type = random.choice(["chrome", "firefox", "safari", "edge"])

            if browser_type == "chrome":
                version = random.choice(chrome_versions)
                agent = f"Mozilla/5.0 ({os_choice}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.0.0 Safari/537.36"

            elif browser_type == "firefox":
                version = random.choice(firefox_versions)
                agent = f"Mozilla/5.0 ({os_choice}; rv:{version}.0) Gecko/20100101 Firefox/{version}.0"

            elif browser_type == "safari":
                version = random.choice(safari_versions)
                agent = f"Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{version} Safari/605.1.15"

            elif browser_type == "edge":
                version = random.choice(edge_versions)
                agent = f"Mozilla/5.0 ({os_choice}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.0.0 Safari/537.36 Edg/{version}.0.0.0"

            user_agents.append(agent)

        return user_agents

    # Generate 100 user agents
    User_list_agent = generate_user_agents(100)

    def parse_book(self, response):
        bookItems = GutenbergItem()

        bookItems["name"] = response.css("div.page_content h1::text").get()
        bookItems["url"] = response.url
        Full_URL = response.css("td.noscreen::text").get()
        if Full_URL.endswith(".html.images"):
            kf8_url = Full_URL.replace(".html.images", ".kf8.images")
        bookItems["kindle_book"] = kf8_url
        discribtion = response.css("span.readmore-container::text").getall()
        bookItems["about_book"] = discribtion[1].strip("\n")
        yield bookItems
