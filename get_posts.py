from driver.chromedriver import driver
from pars import Reverb


class ReverbGetPost(Reverb):
    def get_link_posts(self, category):
        driver.get(Reverb.category_select(self, category))
        posts = driver.find_elements_by_class_name('tiles')
        for post in posts:
            tags = post.find_elements_by_tag_name('a')
            for tag in tags:
                link = tag.get_attribute('href')
                print(link)
                print(self.pars_post(link))

    def pars_post(self, link):
        get_post_header = self.get_post_header(link)
        get_post_image = self.get_post_image(link)
        get_post_link = self.get_post_link(link)
        # get_post_text = self.get_post_text(link)
        # print(get_post_text)

        dict_post = {
            "POST_HEADER": get_post_header,
            "POST_IMAGES": get_post_image,
            "POST_LINKS": get_post_link,
        }

        return dict_post

    def get_post_header(self, link):
        driver.get(link)
        for header in driver.find_elements_by_tag_name('h1'):
            return header.text

    def get_post_image(self, link):
        driver.get(link)
        list_link_image = []
        for atr_class in driver.find_elements_by_class_name(
                'blog-post__content'):
            for image in atr_class.find_elements_by_tag_name('img'):
                list_link_image.append(image.get_attribute("src"))
        return list_link_image

    def get_post_link(self, link):
        driver.get(link)
        list_link = []
        for atr_class in driver.find_elements_by_class_name(
                'blog-post__content'):
            for link in atr_class.find_elements_by_tag_name('a'):
                list_link.append(link.get_attribute("href"))
        return list_link

    # def get_post_text(self, link):
    #     driver.get(link)
    #     for text in driver.find_elements_by_tag_name('p'):
    #         print(text)
    #         return text.txt


rgp = ReverbGetPost()
rgp.get_link_posts("Gear History")