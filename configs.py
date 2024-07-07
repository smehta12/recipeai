from dotenv import load_dotenv, find_dotenv
import yaml
import os

_ = load_dotenv(find_dotenv())


class Configs(object):
    def __init__(self):
        with open(os.path.dirname(os.path.abspath(__file__)) + "/" + "configs.yaml") as f:
            self.yaml_configs = yaml.safe_load(f)

        abs_base_path = os.path.dirname(os.path.abspath(__file__))
        self.yaml_configs["base_data_dir"] = abs_base_path + "/" + self.yaml_configs['base_data_dir']
        self.yaml_configs["vector_store"]["dir"] = abs_base_path + "/" + self.yaml_configs["vector_store"]["dir"]

    def __getattr__(self, item):
        return self.yaml_configs.get(item, None)


configs = Configs()
