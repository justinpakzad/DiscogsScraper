import scrapy


class DiscogsSpider(scrapy.Spider):
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    }
    name = "discogs_scraper"
    base_url = "https://www.discogs.com"

    def start_requests(self):
        start_year = getattr(self, "start_year", "1990")
        end_year = getattr(self, "end_year", "2000")
        genre = getattr(self, "genre", "Electronic")
        formats = getattr(self, "format", "Vinyl")
        style = getattr(self, "style", None)
        pages = int(getattr(self, "pages", 20))
        start_url = f"{self.base_url}/sell/list?year1={start_year}&year2={end_year}&genre={genre}&format={formats}&page=1"
        if style:
            start_url += f"&style={style}"
        yield scrapy.Request(start_url, self.parse)

    def parse(self, response):
        releases = response.css("a.item_release_link.hide_mobile::attr(href)").getall()
        for rel_page in releases:
            full_url = response.urljoin(rel_page)
            yield scrapy.Request(full_url, callback=self.parse_release_details)


        pages_limit = int(getattr(self, "pages", 20))


        query_params = response.url.split("?")[-1].split("&")
        current_page_number = 1  # Default to 1 in case it's not found
        for param in query_params:
            if "page=" in param:
                try:
                    current_page_number = int(param.split("page=")[-1])
                    break
                except ValueError:
                    continue

        if current_page_number < pages_limit:
            next_page_number = current_page_number + 1
            next_page_url = (
                f"{self.base_url}/sell/list?"
                f"year1={getattr(self, 'start_year', '1990')}&"
                f"year2={getattr(self, 'end_year', '2000')}&"
                f"genre={getattr(self, 'genre', 'Electronic')}&"
                f"format={getattr(self, 'format', 'Vinyl')}&"
                f"page={next_page_number}"
            )
            if getattr(self, "style", None):
                next_page_url += f"&style={getattr(self, 'style')}"
            yield scrapy.Request(next_page_url, self.parse)

    def parse_release_details(self, response):
        artist = response.css("a.link_1ctor.link_15cpV::text").get()
        title = response.xpath('//h1[@class="title_1q3xW"]/text()[last()]').get()
        label = response.css('th:contains("Label") + td a::text').get()
        rel_format = response.css('th:contains("Format") + td a::text').get()
        release_date = response.css(
            'th:contains("Released") + td time::attr(datetime)'
        ).extract_first()
        genre
        genre = response.css('th:contains("Genre") + td a::text').get()
        styles
        styles = response.css('th:contains("Style") + td a::text').getall()
        items_data = response.css("div.items_3gMeU a::text").extract()
        have = items_data[0] if len(items_data) > 0 else None
        want = items_data[1] if len(items_data) > 1 else None
        ratings = items_data[2] if len(items_data) > 2 else None
        country = response.xpath(
            '//*[@id="page"]/div/div[2]/div/div[2]/table/tbody/tr[3]/td/a/text()'
        ).get()
        avg_rating = response.css(
            'span:contains("Avg Rating") + span::text'
        ).extract_first()
        low_price = response.xpath(
            '//*[@id="release-stats"]/div/div/ul[2]/li[2]/span[2]/text()'
        ).get()
        median_price = response.xpath(
            '//*[@id="release-stats"]/div/div/ul[2]/li[3]/span[2]/text()'
        ).get()
        high_price = response.xpath(
            '//*[@id="release-stats"]/div/div/ul[2]/li[4]/span[2]/text()'
        ).get()
        yield {
            "artist": artist,
            "title": title,
            "label": label,
            "country": country,
            "format": rel_format,
            "release_date": release_date,
            "genre": genre,
            "styles": styles,
            "have": have,
            "want": want,
            "num_ratings": ratings,
            "average_rating": avg_rating,
            "lowest_price": low_price,
            "median_price": median_price,
            "highest_price": high_price,
        }
