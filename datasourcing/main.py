from configs import configs
from datasourcing.scraping import Scrapper
from datasourcing.cleanup import Cleanup

import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


def data_fetching_main():
    cuisine = "mh"

    base_data_dir = configs.base_data_dir
    recipe_pages_info = configs.recipe_pages_info

    s = Scrapper()
    s.scrape(recipe_pages_info, cuisine, base_data_dir)

    c = Cleanup(base_data_dir, cuisine, recipe_pages_info)
    c.remove_tags_word_from_tags()
    c.add_item_name_in_recipe_last_line()
    c.find_lesser_line_of_ing_and_recipe()


if __name__ == '__main__':
    data_fetching_main()
