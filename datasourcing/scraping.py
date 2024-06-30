import logging
import pandas as pd
from utils import get_webpage
import yaml

class Scrapper(object):

    def _get_ingredients(self, soup, page_link):
        recipes_ingredients = ""
        try:
            ing_list = []
            rdiv = soup.find('div', id="rcpinglist")
            for sp in rdiv.select('span'):
                if sp.has_attr('itemprop'):
                    ing_list.append(sp.text.strip())
                elif sp.has_attr('class') and 'recipe_subheader' in sp['class']:
                    ing_list.append(sp.text.strip() + ":")
            recipes_ingredients = "\n ".join(ing_list)
        except:
            logging.exception(f"Exception when finding ingrediants of {page_link}")

        if not recipes_ingredients:
            logging.warning(f"Cannot find recipe ingredients for {page_link}")
        return recipes_ingredients

    def _get_recipe(self, soup, page_link):
        recipe = ""
        try:
            rec = soup.find('div', id="recipe_small_steps").get_text("\n").strip()
            recipe = "\n".join(list(dict.fromkeys(rec.split("\n"))))
        except:
            logging.exception(f"Exception when finding recipe for {page_link}")

        if not recipe:
            logging.warning(f"Cannot find recipe method for {page_link}")
        return recipe

    def _get_time_and_serving(self, soup, page_link):
        times = ""
        servings = ""
        other_info = ""
        try:
            prep_time = ""
            cook_time = ""
            total_time = ""

            servings_tag = soup.find('span', attrs=dict(itemprop="recipeYield"))
            if servings_tag:
                servings = str(servings_tag.text)

            prep_tag = soup.find('time', attrs=dict(itemprop="prepTime"))
            if prep_tag:
                prep_time = prep_tag.text
                times += "Preparation Time: " + prep_time + ", "

            cook_tag = soup.find('time', attrs=dict(itemprop="cookTime"))
            if cook_tag:
                cook_time = cook_tag.text
                times += "Cooking Time: " + cook_time + ", "

            total_time_tag = soup.find('time', itemprop='totalTime')
            if total_time_tag:
                span_tag = total_time_tag.find('span')
                if span_tag:
                    span_tag.decompose()
                total_time = total_time_tag.text
                times += "Total Time: " + total_time + ", "

            # Other time or coocking related info
            tags_div = soup.find('div', id='recipe_tags')
            if not tags_div:
                tags_div = soup.find('div', id='ctl00_cntrightpanel_lblrecipeNameH2')

            p_tag = tags_div.find_next('p')
            for t in p_tag.find_all('time'):
                t.decompose()
            if servings:
                for serv_time in p_tag.find_all('span', attrs=dict(id="ctl00_cntrightpanel_lblServes")):
                    serv_time.decompose()

            other_info = p_tag.get_text().replace("&nbsp", " ").split("Show me for")[0].strip()
            if prep_time:
                other_info = other_info.replace("Preparation Time:", "")
            if cook_time:
                other_info = other_info.replace("Cooking Time:", "")
            if total_time:
                other_info = other_info.replace("Total Time:", "")

            times += other_info

        except:
            logging.exception(f"Error while finding time and serving for {page_link}")

        if not times or not servings:
            logging.warning(f"Cannot find times, or servings for {page_link}")
        return times, servings

    def scrape(self, recipe_pages_info, cuisine, base_data_dir):
        recipe_url_prefix = "https://www.tarladalal.com/"
        for recipe_list_page_idx in range(1, recipe_pages_info[cuisine]["last_list_page_num"] + 1):
            recipe_list = []
            print(f"Getting recipies from page {recipe_list_page_idx}")
            list_url = recipe_pages_info[cuisine]["list_page_url"].format(recipe_list_page_idx)
            recipe_list_page = get_webpage(list_url)
            if not recipe_list_page:
                continue
            for recipe_span in recipe_list_page.find_all('span', attrs={"class": "rcc_recipename"}):
                df_row = {}
                df_row["recipe_list_url"] = list_url
                df_row["recipe_name"] = recipe_span.text
                recipe_url = recipe_url_prefix + recipe_span.find('a', href=True)['href']
                df_row["recipe_url"] = recipe_url
                # print(recipe_url)
                recipe_page = get_webpage(recipe_url)
                if not recipe_page:
                    logging.warn(f"Couldn't find recipe page for {recipe_url}")
                    continue
                df_row["recipe_long_name"] = recipe_page.find('span', id='ctl00_cntrightpanel_lblrecipeNameH2').text
                df_row["ingredients"] = self._get_ingredients(recipe_page, recipe_url)
                df_row["recipe"] = self._get_recipe(recipe_page, recipe_url)
                df_row["tags"] = recipe_page.find('div', id='recipe_tags').get_text("\n").strip()
                if not df_row["tags"]:
                    logging.warn(f"Couldn't find tags for {recipe_url}")
                times, servings = self._get_time_and_serving(recipe_page, recipe_url)
                df_row["times"] = times
                df_row["servings"] = servings
                recipe_list.append(df_row)
            recipe_df = pd.DataFrame(recipe_list)
            recipe_df.to_csv(f"{base_data_dir}/recipe_page_{recipe_list_page_idx}.csv", index=False)


if __name__ == '__main__':
    with open("./configs.yaml") as f:
        configs = yaml.safe_load(f)
    recipe_pages_info = configs["recipe_pages_info"]
    cuisine = "mh"
    base_data_dir = f"../data"

    s = Scrapper()
    s.scrape(recipe_pages_info, cuisine, base_data_dir)