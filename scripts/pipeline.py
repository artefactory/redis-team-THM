from metaflow import FlowSpec, step, IncludeFile, Parameter
from generate_index import run

class GenerateIndexFlow(FlowSpec):
    """
    A flow to generate index from arXiv corpus.
    """

    @step
    def start(self):
        """
        The start step:
        1) Loads the arXiv corpus into pandas dataframe.

        """

        self.next(self.end)

    @step
    def end(self):
        "Ends the flow."
        pass


if __name__ == '__main__':
    GenerateIndexFlow()