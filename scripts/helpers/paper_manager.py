from collections import deque
from dataclasses import dataclass
from typing import List, Tuple, Union

from helpers.models import Paper


@dataclass
class PriorityPapersManager:
    """TODO"""
    
    paper_contexts: List[str]
    """List of preprocessed contexts of the prioritized papers."""
    paper_content: List[Paper]
    """List of the papers associated to passed contexts."""
    joining_key: str = " "
    """Key that separates a paper's context from the next."""
    
    def __post_init__(self) -> None:
        self.n_papers = len(self.paper_contexts)
        self.starts, self.ends = self._compute_starts_ends()
        self.merged_context = self._generate_merged_context()
        
    
    def _compute_starts_ends(self) -> Tuple[List[int], List[int]]:
        # generates two lists containing starting and ending positions of each paper's context.
        starts = [] # init instance variables
        ends = []
        start = 0 # init sequence of starts
        
        for context in self.paper_contexts:
            end = start + len(context) + len(self.joining_key)
            starts.append(start)
            ends.append(end)
            
            start = end
        
        return starts, ends
        
    def _generate_merged_context(self) -> str:
        # Joins all papers' contexts into a single text
        return self.joining_key.join(self.paper_contexts)
        
    
    def find_paper(self, target_start: int, target_end: int, return_paper_idx: bool=False) -> Union[Paper, Tuple[Paper, int]]:
        """TODO

        Args:
            target_start (int): _description_
            target_end (int): _description_
            return_paper_idx (bool, optional): _description_. Defaults to False.

        Raises:
            NotImplementedError: _description_

        Returns:
            Union[str, Tuple[str, int]]: _description_
        """
        # extract last element before the start index
        deque_filtered_starts = deque(filter(lambda paper_start: paper_start <= target_start, self.starts), maxlen=1)
        start_paper = deque_filtered_starts.pop()
        # extract last element after the end
        end_paper = next(filter(lambda paper_end: paper_end > target_end, self.ends))
        # extract paper information
        start_paper_idx = self.starts.index(start_paper)
        end_paper_idx = self.ends.index(end_paper)
        
        if start_paper_idx != end_paper_idx: 
            pass # TODO: handle case
        else:
            paper = self.paper_content[start_paper_idx]
            if return_paper_idx:
                return (paper, start_paper_idx)
            else:
                return paper
