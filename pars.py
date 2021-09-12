from driver.chromedriver import driver
import deepl


class Reverb():
    def _create_link(self, category):
        """
        возвращает ссылку страницы
        """
        search_category = '+'.join(category.split())
        url = ('https://reverb.com/news?category_name='
               ) + f'{search_category}' + '&page='
        return url

    def posts(self, category):
        """
        парсит заголовки 
        постов и ссылки на них 
        """
        url = self._create_link(category)
        page_number = 1
        loop = True
        while loop:
            print(f"Parsing page {page_number}")
            new_url = url + str(page_number)
            driver.get(new_url)
            page_number += 1
            article_card = driver.find_elements_by_class_name('tiles__tile')
            index_link = 1
            for texts in article_card:
                title = [
                    a.text for a in texts.find_elements_by_class_name(
                        'article-card__title')
                ]
                date = [
                    b.text for b in texts.find_elements_by_class_name(
                        'article-card__date')
                ]
                link = [
                    c.get_attribute("href")
                    for c in driver.find_elements_by_xpath(
                        f'/html/body/main/section/section[1]/div/div/ul/div[{index_link}]/div/a'
                    )
                ]
                index_link += 1
                if title == date:
                    break

                posts = {'title': title, 'date': date, 'link': link}

                print(posts)

            if [
                    e.text for e in texts.find_elements_by_xpath(
                        '/html/body/main/section/section[1]/div/div[2]/a')
            ]:
                print("Post parsing finished...")
                loop = False





    def get_post(self, link):
        """
        запускает методы парсинга 
        отдельных элементов поста
        """
        driver.get(link)
        dict_post = {
            "POST_HEADER": self._get_post_header(link),
            "POST_IMAGES": self._get_post_images(link),
            "POST_LINKS": self._get_post_links(link),
            "POST_TEXT": self._get_post_text(link),
        }
        return dict_post
      
 

    def _get_post_header(self, link):
        """
        парсинг заголовок
        """
        print('\nGetting the post header...')
        for header in driver.find_elements_by_tag_name('h1'):
            return header.text

    def _get_post_images(self, link):
        """
        парсит ссылки на картинки
        """
        print('\nGetting the post images...')
        list_link_images = []
        for atr_class in driver.find_elements_by_class_name(
                'blog-post__content'):
            for image in atr_class.find_elements_by_tag_name('img'):
                list_link_images.append(image.get_attribute("src"))
        return list_link_images

    def _get_post_links(self, link):
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

    def _get_post_text(self, link):
        """
        парсит текст поста
        """
        print('\nGetting the post text...\n')
        post_paragraphs = driver.find_elements_by_tag_name('p')
        text = []
        try:
            for paragraph in list(post_paragraphs):
                text.append(paragraph.text)
        except:
            print('cannot parse text further')
        
        return text





class Deepl():
    """
    xahava3279@stvbz.com
    klDhd9f7G4h1kj
    """
    def translate(self, text):
        """
        Первеодит принятый текст
        """
        translator = deepl.Translator("f39c003c-f13f-516d-0cd8-97585d4e6b71:fx")
        result = translator.translate_text(text, target_lang="EN-US")
        print(result)  


if __name__ != '__main__':
    Reverb().posts("Gear History")
    print(Reverb().get_post("https://reverb.com/news/70s-martins-what-you-need-to-know"))
    Deepl().translate()