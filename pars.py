
from driver.chromedriver import driver
from bs4 import BeautifulSoup
import requests


class Reverb():
    def posts(self, category):
        """
        парсит заголовки 
        постов и ссылки на них 
        """

        page = 1
        posts = []
        loop = True
        while loop:
            print(f"Parsing page {page}")
            category_page_url = self._category_page_url(category, page)
            driver.get(category_page_url)
            page += 1
            cards = driver.find_elements_by_class_name('tiles__tile')
            index_link = 1

            for card in cards:
                """
                если не итерирвать то пишет 'list' object has no attribute 'text'
                arturdavidov@archi reverb_pars %
                """
                title = [
                    a.text for a in card.find_elements_by_class_name(
                        'article-card__title')
                ]
                """без итерации не находит нужный елемент"""
                date = [
                    b.text for b in card.find_elements_by_class_name(
                        'article-card__date')
                ]
                """без итерации не находит нужный елемент"""
                link = [
                    c.get_attribute("href")
                    for c in driver.find_elements_by_xpath(
                        f'/html/body/main/section/section[1]/div/div/ul/div[{index_link}]/div/a'
                    )
                ]
                index_link += 1

                posts.append({'title': title, 'date': date, 'link': link})

            if self._no_page_links(card):
                loop = False
                return posts

    def get_post(self, link):
        """
        запускает методы парсинга 
        отдельных элементов поста
        """
        headers = {
            'user-agent':
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
        }

        req = requests.get(link, headers)
        soup = BeautifulSoup(req.text, "lxml")

        driver.get(link)

        return {
            # "POST_HEADER": self._get_post_header(),
            # "POST_IMAGES": self._get_post_images(),
            # "POST_LINKS": self._get_post_links(),
            # "POST_TEXT": self._get_post_text(),
            "GET_HTML": self._get_html(soup)
        }

    def _get_post_header(self):
        """
        парсинг заголовок
        """
        print('\nGetting the post header...')
        return [
            header.text for header in driver.find_elements_by_tag_name('h1')
        ]

    def _get_post_images(self):
        """
        парсит картинки
        """
        print('\nGetting the post images...')
        list_link_images = []
        for atr_class in driver.find_elements_by_class_name(
                'blog-post__content'):
            for image in atr_class.find_elements_by_tag_name('img'):
                list_link_images.append(image.get_attribute("src"))
        return list_link_images

    def _get_post_links(self):
        """
        парсит ссылки на товары
        """
        print('\nGetting the post links...')
        list_link = []
        for atr_class in driver.find_elements_by_class_name(
                'blog-post__content'):
            for link in atr_class.find_elements_by_tag_name('a'):
                list_link.append(link.get_attribute("href"))
        return list_link

    def _get_post_text(self):
        """
        парсит текст поста
        """
        print('\nGetting the post text...\n')

        post_paragraphs = driver.find_elements_by_tag_name('p')
        return [text.text for text in list(post_paragraphs)]

    def _category_page_url(self, category, page):
        """
        возвращает ссылку страницы
        """
        category = '+'.join(category.split())
        return f'https://reverb.com/news?category_name={category}&page={page}'

    def _no_page_links(self, card):
        return [
            e.text for e in card.find_elements_by_xpath(
                '/html/body/main/section/section[1]/div/div[2]/a')
        ]

    def _get_html(self, soup):

        for content in soup.find("div", class_="blog-post__content").find_all(
                "div", class_="size-200 weight-bold scaling-pb-2"):

            newh2 = soup.new_tag('h2')
            try:
                content.replace_with(content.string.wrap(newh2))
            except Exception:
                continue

        for small_name in soup.find(
                "div", class_="blog-post__content").find_all(
                    "div", class_="size-80 align-center mt-half mb-3"):
            for images in soup.find(
                    "div", class_="blog-post__content").find_all(
                        "div", class_="size-80 align-center mt-half mb-3"):
                img = images.find_previous_sibling().find("img")
                img['alt'] = small_name.text
                small_name.decompose()

        for tag in soup():
            for attr in ['class', 'style']:
                try:
                    for value in tag[attr]:
                        print(value)
                        if value.find('%bold', '%italic'):
                            print(value)
                            tag.replace_with(tag.string.wrap(
                                soup.new_tag('b')))

                        else:
                            del tag[attr]
                except Exception as e:
                    print(f'ошибка {e}')

                # if '%%bold' in tag[attr]:
                #     tag[attr].replace_with(soup.new_tag('b'))
                # else:
                #     del tag[attr]

        with open('header_test.html', 'w') as f:
            f.write(soup.prettify())


if __name__ == "__main__":
    r = Reverb()
    r.get_post("https://reverb.com/news/a-timeline-of-les-pauls")
