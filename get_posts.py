from driver.chromedriver import driver
from pars import Reverb


class ReverbGetPost(Reverb):
    def paginate_page(self, category):
        #листает страницы
        page_link = self.category_select(category)
        self.get_posts(page_link)
        page = 1
        next_page = self.paginate(page_link)
        self.loop = True
        while self.loop:
            try:
                page += 1
                p = open('parsing.txt', 'a')
                p.write(f'\n\n________PAGE:{page}________\n\n')
                p.close()
                print(f'\nParsing page {page}....\n')
                self.get_posts(next_page + str(page))

            except:
                break

    def export(self, data):
        #сохраняет в фаил
        p = open('parsing.txt', 'a')
        p.write(f'\n________POST!________\n')
        p.write(str(data))
        p.close()

    def get_posts(self, link):
        #парсит посты
        try:
            driver.implicitly_wait(3)
            posts = driver.find_elements_by_class_name('tiles')
            for post in posts:
                try:
                    links = self.list_link(post.find_elements_by_tag_name('a'))
                    print(links)
                    for link in links:
                        print('\nParsing post...')
                        try:
                            post_content = self.pars_post(link)

                        except Exception as e:
                            print('\n Could not parse the post :(')
                            print(e)

                        try:
                            self.export(post_content.values())
                        except Exception as ex:
                            print(ex)
                            print('\Could not export :(')
                except Exception:
                    print('issue with posts')
                    print(Exception)
                    continue

        except:
            print('\nThe files are over')
            self.loop = False
            return self.loop

    def list_link(self, links):
        #создает список ссылок на посты текущей страницы
        list_link = []
        for link in links:
            list_link.append(link.get_attribute('href'))
        
        return list_link

    def pars_post(self, link):
        #запускает методы парсинга отдельных элементов поста
        print('\nGetting the post header...')
        try:
            driver.implicitly_wait(4)
            get_post_header = self.get_post_header(link)
            print('Done!')
        except:
            print('Could not get the post header :(')

        print('\nGetting the post images...')

        try:
            driver.implicitly_wait(4)
            get_post_image = self.get_post_image(link)
            print('Done!')
        except:
            print('Could not get the post images:(')
        print('\nGetting the post links...')
        try:
            driver.implicitly_wait(4)
            get_post_link = self.get_post_link(link)
            print('Done!')
        except:
            print('Could not get the post links :(')
        print('\nGetting the post text...')
        try:
            driver.implicitly_wait(4)
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

        return dict_post

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


rgp = ReverbGetPost()
rgp.paginate_page("Gear History")