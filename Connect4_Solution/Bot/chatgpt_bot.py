import os


from dotenv import load_dotenv

import numpy as np

from haystack import Pipeline, Document
from haystack.utils import Secret
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders.answer_builder import AnswerBuilder
from haystack.components.builders.prompt_builder import PromptBuilder


class Connect4Bot:

    def __init__(self) -> None:
        

        print(F"creating Connect4Bot with ChatGPT connection")

        load_dotenv()

        api_key = os.getenv('API_KEY')

        if not api_key:
            raise ValueError(F"No API Key in .env File --> buy a ChatGPT Licence first $$$ ")


        # Write documents to InMemoryDocumentStore
        self.document_store = InMemoryDocumentStore()
        self.document_store.write_documents([
            Document(content="You are a Player for the Game Connect Four"), 
            Document(content="You need to select the a Column between 0 and 7 to select where you drop the next coin"),
            Document(content="The different coins are represented with 'X' and 'O', empty cells contain an just a ' '"),
            Document(content="Answer always just with the correct Column Number"),
        ])

        # # Build a RAG pipeline
        # self.prompt_template = """
        # Given these documents, answer the question.
        # Documents:
        # {% for doc in documents %}
        #     {{ doc.content }}
        # {% endfor %}
        # Question: {{question}}
        # Answer:
        # """

        # Build a RAG pipeline
        self.prompt_template = """
        Given these game instructions, select the correct column:
        {% for doc in documents %}
            {{ doc.content }}
        {% endfor %}
        {{question}}:
        """

       

        self.retriever = InMemoryBM25Retriever(document_store=self.document_store)
        self.prompt_builder = PromptBuilder(template=self.prompt_template)
        self.llm = OpenAIGenerator(api_key=Secret.from_token(api_key))

        self.rag_pipeline = Pipeline()
        self.rag_pipeline.add_component("retriever", self.retriever)
        self.rag_pipeline.add_component("prompt_builder", self.prompt_builder)
        self.rag_pipeline.add_component("llm", self.llm)
        self.rag_pipeline.connect("retriever", "prompt_builder.documents")
        self.rag_pipeline.connect("prompt_builder", "llm")


    def post_process_prompt(self,prompt:str)->int:
        """
        Post Process Prompt Response from ChatGPT
        Return just column as int

        Parameters:
            prompt (str):   First Answer from ChatGPT
        Returns:
            column (int):   selected column (defaults to 0)
        """
        all_numbers = []
        for char in prompt:
            try:
                num = int(char)
                all_numbers.append(num)
            except:
                pass

        # select most mentioned column as actual value
        column = max(set(all_numbers), key=all_numbers.count)

        # clip values to be between 0 and 7
        column = max(0, min(column, 7))

        return column


    def make_move(self,board:np.ndarray, active_icon:str)->int:
        """
        makes a move based on a given board state

        Parameters:
            board (ndarray):    8x7 Numpy array filled with O and X
            active_icon (str):        Active Player Icon
        Returns:
            column (int)       Selected Column Nr between 0 and 7
        """

        question = f"You are player {active_icon} and this is your board: \n {board}. Just answer with the chosen column as a number"

        results = self.rag_pipeline.run(
            {
                "retriever": {"query": question},
                "prompt_builder": {"question": question},
            }
        )

        result = results["llm"]["replies"][0]

        column = self.post_process_prompt(result)
            
        return column


if __name__ == "__main__":
    
    bot = Connect4Bot()

    # create test board
    board = np.empty(shape=(8,8), dtype=str)
    board[:,:] = " "
    board[0,:] = [str(i) for i in range(8)]
    board[7,1] = "O"
    board[7,7] = "O"
    board[7,2:5] = "X"
    print(f"the board is \n{board}")

    col = bot.make_move(board,active_icon="X")
    print(f"ChatGPT chose column {col}, the board is now:")

    for i in range(7,0,-1):
        if board[i,col] == " ":
            board[i,col] = "X"
            break
    print(board)


    
