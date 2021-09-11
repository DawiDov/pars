from driver.chromedriver import driver


class Reverb():
    def create_link(self, category):
        #создание ссылки
        search_category = '+'.join(category.split())
        url = ('https://reverb.com/news?category_name='
               ) + f'{search_category}' + '&page='
        return url

    def posts(self, category):
        url = self.create_link(category)
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
        #запускает методы парсинга отдельных элементов поста
        print('\nGetting the post header...')
        try:
            driver.implicitly_wait(5)
            get_post_header = self.get_post_header(link)
            print('Done!')
        except Exception as ex:
            print(ex)
            print('Could not get the post header :(')

        print('\nGetting the post images...')

        try:
            driver.implicitly_wait(5)
            get_post_image = self.get_post_image(link)
            print('Done!')
        except:
            print('Could not get the post images:(')
        print('\nGetting the post links...')
        try:
            driver.implicitly_wait(5)
            get_post_link = self.get_post_link(link)
            print('Done!')
        except:
            print('Could not get the post links :(')
        print('\nGetting the post text...')
        try:
            driver.implicitly_wait(5)
            get_post_text = self.get_post_text(link)
            print('Done!')
        except:
            print('Could not get the post text :(')

        dict_post = {
            "POST_HEADER": get_post_header,
            "POST_IMAGES": get_post_image,
            "POST_LINKS": get_post_link,
            "POST_TEXT": get_post_text,
        }
        print(dict_post)
        # return dict_post

    def get_post_header(self, link):
        #парсинг заголовок
        driver.get(link)
        for header in driver.find_elements_by_tag_name('h1'):
            return header.text

    def get_post_image(self, link):
        #парсит ссылки на картинки
        driver.get(link)
        list_link_image = []
        for atr_class in driver.find_elements_by_class_name(
                'blog-post__content'):
            for image in atr_class.find_elements_by_tag_name('img'):
                list_link_image.append(image.get_attribute("src"))
        return list_link_image

    def get_post_link(self, link):
        #парсит ссылки на товары
        driver.get(link)
        list_link = []
        for atr_class in driver.find_elements_by_class_name(
                'blog-post__content'):
            for link in atr_class.find_elements_by_tag_name('a'):
                list_link.append(link.get_attribute("href"))
        return list_link

    def get_post_text(self, link):
        #парсит текст поста
        driver.get(link)
        post_paragraphs = driver.find_elements_by_tag_name('p')
        text = []
        try:
            for paragraph in list(post_paragraphs):
                text.append(paragraph.text)
        except:
            print('cannot parse text further')
        return text
