import pandas as pd
from configs import configs
import os
import logging

from typing import Any, Iterator, List, Union

from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings


class VectorStore(object):
    def __init__(self, vector_store_type, embedding_model):
        """

        :param vector_store_type: Type of vector store like FAISS, Chroma etc
        :param embedding_model object
        """
        self.embedding_model = embedding_model
        self.vector_store_type = vector_store_type

    def create_and_save_vector_store(self):
        """
        Create vector db for the application and save it at the given path in config

        :param db_path: Path to save the database
        :return: None
        """

        csv_df = self._load_raw_data()
        loader = DataFrameLoader(csv_df, page_content_column=configs.recipe_pages_info["columns_to_use"])
        docs = loader.load()

        if not os.path.exists(configs.vector_store["dir"]):
            os.mkdir(configs.vector_store["dir"])

        __vector_db = self.vector_store_type.from_documents(docs, self.embedding_model)
        __vector_db.save_local(configs.vector_store["dir"], index_name=configs.vector_store["index_name"])

    def get_saved_vector_store(self):
        vector_store_file_name = configs.vector_store["dir"] + "/" + configs.vector_store["index_name"]
        if not os.path.exists(configs.vector_store["dir"]) or not os.path.exists(vector_store_file_name + ".pkl"):
            raise RuntimeError("Required Files for vector store doesn't exists")

        return self.vector_store_type.load_local(configs.vector_store["dir"], embeddings=self.embedding_model,
                                                 index_name=configs.vector_store["index_name"],
                                                 allow_dangerous_deserialization=True)

    def _load_raw_data(self):
        csv_df = pd.DataFrame()

        data_root = configs.base_data_dir

        for d in os.listdir(data_root):
            cuisine_dir = f"{data_root}/{d}"
            for f in os.listdir(cuisine_dir):
                file = f"{cuisine_dir}/{f}"
                try:
                    recipe_df = pd.read_csv(file, usecols=["recipe_name", "ingredients", "recipe", "tags", "times",
                                                           "servings"])
                    csv_df = pd.concat([csv_df, recipe_df], ignore_index=True)
                except:
                    logging.exception(f"Error when loading {file}")
        return csv_df


def get_vector_store(vector_store_type, create_store=False):
    # TODO: Can we cache?
    if configs.embedding_model == 'text-embedding-3-large':
        embedding_model = OpenAIEmbeddings(model='text-embedding-3-large')
    else:
        embedding_model = HuggingFaceEmbeddings(model_name=configs.embedding_model,
                                        model_kwargs=dict(trust_remote_code=True))

    vs = VectorStore(vector_store_type, embedding_model)
    if create_store:
        vs.create_and_save_vector_store()
    return vs


class BaseDataFrameLoader(BaseLoader):
    def __init__(self, data_frame: Any, *, page_content_column: Union[str, List[str]] = "text"):
        """Initialize with dataframe object.

        Args:
            data_frame: DataFrame object.
            page_content_column: Name of the column or list of column names containing the page content.
              Defaults to "text".
        """
        self.data_frame = data_frame
        self.page_content_column = page_content_column

    def lazy_load(self) -> Iterator[Document]:
        """Lazy load records from dataframe."""

        for idx, row in self.data_frame.iterrows():
            if isinstance(self.page_content_column, list):
                text = ' '.join(f'{col}:{row[col]}' for col in self.page_content_column)
            else:
                text = f'{col}:{row[self.page_content_column]}'
            metadata = row.to_dict()
            if isinstance(self.page_content_column, list):
                for col in self.page_content_column:
                    metadata.pop(col, None)
            else:
                metadata.pop(self.page_content_column, None)
            yield Document(page_content=text, metadata=metadata)

    def load(self) -> List[Document]:
        """Load full dataframe."""
        return list(self.lazy_load())


class DataFrameLoader(BaseDataFrameLoader):
    """Load `Pandas` DataFrame."""

    def __init__(self, data_frame: Any, page_content_column: Union[str, List[str]] = "text"):
        """Initialize with dataframe object.

        Args:
            data_frame: Pandas DataFrame object.
            page_content_column: Name of the column or list of column names containing the page content.
              Defaults to "text".
        """
        try:
            import pandas as pd
        except ImportError as e:
            raise ImportError(
                "Unable to import pandas, please install with `pip install pandas`."
            ) from e

        if not isinstance(data_frame, pd.DataFrame):
            raise ValueError(
                f"Expected data_frame to be a pd.DataFrame, got {type(data_frame)}"
            )
        super().__init__(data_frame, page_content_column=page_content_column)
