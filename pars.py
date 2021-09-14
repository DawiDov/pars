from driver.chromedriver import driver


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
        driver.get(link)

        return {
            "POST_HEADER": self._get_post_header(),
            "POST_IMAGES": self._get_post_images(),
            "POST_LINKS": self._get_post_links(),
            "POST_TEXT": self._get_post_text(),
        }

    def _get_post_header(self):
        """
        парсинг заголовок
        """
        print('\nGetting the post header...')
        return [header.text for header in driver.find_elements_by_tag_name('h1')]
     

    def _get_post_images(self):
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
        return [e.text for e in card.find_elements_by_xpath('/html/body/main/section/section[1]/div/div[2]/a')]
            


if __name__ != "__main__":
    r = Reverb()
    r.posts("Gear History")