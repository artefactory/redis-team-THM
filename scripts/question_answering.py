from typing import Dict, List, Tuple

from helpers.models import Paper
from helpers.paper_manager import PriorityPapersManager
from helpers.search_engine import SearchEngine
from helpers.settings import Settings
from transformers import pipeline

settings = Settings()


def get_prioritized_articles(
    user_prompt: str, engine: SearchEngine
) -> PriorityPapersManager:
    search_papers, _ = engine.search(
        user_prompt, max_results=settings.question_answering_priority_papers
    )

    # parse list of papers
    papers = []
    papers_text = []
    for paper_ in search_papers:
        paper = engine.paper(paper_.paper_id)
        if not paper: # sometimes the research does not yield a result
            continue
        papers.append(paper)

        if paper.abstract and paper.title:
            paper_text = paper.title + " " + paper.abstract
        elif paper.title:
            paper_text = paper.title
        elif paper.abstract:
            paper_text = paper.abstract

        papers_text.append(paper_text)

    return PriorityPapersManager(papers_text, papers)


def _validate_prompt(user_prompt: str):
    # TODO: implement checks
    return user_prompt


def _build_answer(
    qa_output: List[Dict], priority_papers: PriorityPapersManager
) -> List[Tuple[str, float, Paper]]:
    answer = []

    for output in qa_output:
        start_answer = output["start"]
        end_answer = output["end"]
        text_answer = output["answer"]
        confidence = output["score"]
        paper = priority_papers.find_paper(
            target_start=start_answer, target_end=end_answer
        )

        answer.append((text_answer, confidence, paper))

    return answer


def get_answer_to_prompt(engine, question: str, top_k: int = 1):
    validated_question = _validate_prompt(question)
    priority_papers = get_prioritized_articles(validated_question, engine)

    # instantiate model
    model = pipeline(
        task="question-answering",
        model=settings.question_answering_model,
        tokenizer=settings.question_answering_tokenizer,
    )
    # get predictions
    model_outputs = model(
        {"question": validated_question, "context": priority_papers.merged_context},
        top_k=top_k,
    )
    if top_k == 1:
        model_outputs = [model_outputs]

    return _build_answer(model_outputs, priority_papers)
