import os

import pandas as pd
import logging


class cleanup(object):
    def __init__(self, base_data_dir, cuisine, recipe_pages_info):
        self.base_data_dir = base_data_dir
        self.cuisine = cuisine
        self.recipe_pages_info = recipe_pages_info

    def get_recipes_df(self, page_id):
        pg_location = f"{self.base_data_dir}/recipe_page_{page_id}.csv"
        if not os.path.exists(pg_location):
            logging.warning(f"[Get Recipes df] Page Id Missing: {page_id}")
            return pd.DataFrame()
        return pd.read_csv(pg_location)

    def find_lesser_line_of_ing_and_recipe(self):
        """
        Method to find if there's any lesser ingredients or recipe fetched for an item.
        So it can be manually added or verify.
        :return:
        """
        log_tag = "Lesser_Ing_or_Recipe"
        for page_id in range(1, self.recipe_pages_info[self.cuisine]["last_list_page_num"] + 1):
            df = self.get_recipes_df(page_id)
            if df.empty:
                continue
            logging.info(f"[{log_tag}] Page Idx Processed: {page_id}")
            for idx, row in df.iterrows():
                if len(df.loc[idx, "recipe_ing"].split("\n")) <= 3:
                    logging.warning(f'[{log_tag}]Less ing for {row["recipe_url"]}')
            for idx, row in df.iterrows():
                if len(df.loc[idx, "recipe"].split("\n")) <= 3:
                    logging.warning(f'[{log_tag}]Less recipe for {row["recipe_url"]}')

    def remove_tags_word_from_tags(self):
        """Remove Tags word from tags column and save it back"""
        for page_id in range(1, self.recipe_pages_info[self.cuisine]["last_list_page_num"] + 1):
            df = self.get_recipes_df(page_id)
            if df.empty:
                continue
            logging.info(f"[Tags_Cleanup] Page Idx Processed: {page_id}")
            df['tags'] = df['tags'].str.replace("Tags", "").str.strip()
            df.to_csv(f"{self.base_data_dir}/recipe_page_{page_id}.csv", index=False)

    def add_item_name_in_recipe_last_line(self):
        """
        Many of the recipes scraping doesn't add a recipe name in the last line when there're phrases like `Serve the`
        or `Cool the` etc. So we need to insert the recipe name there to make the sentence looks better
        :return:
        """

        half_sent_samples = ["Do with", "Cool the", "Divide the", "Use the", "Store the", "Drain the",
                             "Refrigerate the", "Garnish the", "Break the", "Allow the", "Serve the", "Cut the",
                             "Brush each", "Cool and store the", "Serve", "Serve or store the"]
        half_sent = half_sent_samples.copy()

        for hs in half_sent_samples:
            half_sent.append(hs + " ")

        for page_id in range(1, self.recipe_pages_info[self.cuisine]["last_list_page_num"] + 1):
            df = self.get_recipes_df(page_id)
            if df.empty:
                continue
            logging.info(f"[Fix_Last_Line] Page Idx Processed: {page_id}")
            df = df.drop([x for x in ['Unnamed: 0.1', 'Unnamed: 0'] if x in df.columns], axis=1)
            for idx, row in df.iterrows():
                recipe = df.loc[idx, "recipe"]
                lines = recipe.split("\n")
                for sentence in half_sent:
                    if sentence in lines:
                        rn = row["recipe_name"]
                        if '(' in rn:
                            rn = rn.split('(')[0].strip()
                        elif '|' in rn:
                            rn = rn.split('|')[0].strip()
                        elif ',' in rn:
                            rn = rn.split(',')[0].strip()

                        rn = rn.lower()
                        for word in ["raw", "how", "recipe", self.cuisine, "to", "make"]:
                            if word in rn:
                                rn = rn.replace(word, "")
                        ln_idx = lines.index(sentence)
                        lines[ln_idx] = f"{lines[ln_idx].strip()} {rn.lower().strip()} {lines[ln_idx + 1].strip()}"
                        del lines[ln_idx + 1]
                        new_recipe = "\n".join(lines)
                        df.loc[idx, "recipe"] = new_recipe
            df.to_csv(f"{self.base_data_dir}/recipe_page_{page_id}.csv", index=False)