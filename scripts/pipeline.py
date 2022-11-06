from metaflow import FlowSpec, step, Parameter
from generate_index import run as run_g
from load_data import run as run_l
from datetime import datetime


class RedisEmbeddingsFlow(FlowSpec):
    """
    A flow to generate index from arXiv corpus.
    """
    current_month = datetime.now().strftime("%Y%m")
    year_month = Parameter("year_month", help="year-month to run at", default=current_month)

    @step
    def start(self):
        self.next(self.generate_index)

    @step
    def generate_index(self):
        run_g(year_month=self.current_month)
        self.next(self.join)

    @step
    def join(self, inputs):
        "Joins parallel branches and merges results."
        self.next(self.load_data)

    @step
    def load_data(self):
        for sub_path in self.embeddings_paths:
            run_l(embeddings_path=sub_path)
        self.next(self.end)

    @step
    def end(self):
        "Ends the flow."
        pass


if __name__ == '__main__':
    RedisEmbeddingsFlow()