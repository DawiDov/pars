from driver.chromedriver import driver


class Reverb():
    def category_select(self, category):
        #выбор категории в новостях
        search_category = '+'.join(category.split())
        self.url = (
            'https://reverb.com/news?category_name=') + f'{search_category}'
        driver.get(url=self.url)
        return self.url

    def paginate(self, url):
        #делает ссылку для перелистывания на след. страницу
        # print(self.url)
        self.new_url = self.url + '&page='
        return self.new_url

    def posts(self, input):
        #парсинг списка постов
        self.url = self.category_select(input)
        self.new_url = self.paginate(self.url)
        driver.implicitly_wait(5)
        tiles = driver.find_element_by_class_name('tiles')
        return tiles

    def pars_posts(self, input):
        #обработка полученного списка постов
        print('Commensing the process')
        tiles = self.posts(input)
        post_list = []
        post_list.append(tiles.text)
        page = 1

        while True:
            try:
                driver.get(self.new_url + str(page))
                page += 1
                driver.implicitly_wait(4)
                tiles = driver.find_element_by_class_name('tiles')
                print('Parsing...')
                if tiles.text:
                    post_list.append(tiles.text)
                    print(f'Page: {page}')
                else:
                    for post in post_list:
                        print(post)
                        print('____________')
                    print('done')
                    break
            except:
                break


reverb = Reverb()
if __name__ == "__main__":
    reverb.pars_posts("Gear History")
