Title: The THM CLI
Date: 2022-11-04 10:25
Modified: 2022-11-04 10:25
Category: THM CLI
Tags: python
Slug: snippets
Authors: Henrique Brito, Michel Hua
Summary: The THM CLI

The **THM CLI** is the ultimate CLI tool to help researchers and technical writers. It can help them in every day tasks such as building bibliography and finding answers to their questions.

See here why the [CLI is still the way to go]({filename}07_cli_tool.md). To install the tool go to [`scripts/`](https://github.com/artefactory/redis-team-THM/tree/main/scripts).

<script id="asciicast-CGtMSoSe0Fp8dn9nbLpzzbdbM" src="https://asciinema.org/a/CGtMSoSe0Fp8dn9nbLpzzbdbM.js" async></script>

# Running THM CLI

To use **THM CLI**, just open the terminal and run the following command,

```sh
% thm-cli
```

You will have access to a interactive prompt where you can type commands, with auto-completion and history capabilities.

```
THM Search CLI
Your arXiv-BibTeX terminal assistant.

---
A mathematician is a device for turning coffee into theorems..
Paul Erdos
---


THM #
```

# The THM prompt

## Getting Help

```
THM # help
THM Search CLI v1.0
https://artefactory.github.io/redis-team-THM/

Usage:
  search [keywords|similar|details]
  find [answer|formula|stackexchange]
  configure
  help
  exit
```

## Configuring the tool

You can configure some parameters such as output format, and the number of results to display by default.

```
THM # configure
Choose file format (markdown, bibtex): bibtex
Max Results (eg. 3): 4
```

## Searching the arXiv database

<script id="asciicast-5e9QHIS62HZDL1VkSFtAVlvjF" src="https://asciinema.org/a/5e9QHIS62HZDL1VkSFtAVlvjF.js" async></script>

### Searching for keywords

Just type a few words like `category theory` and results will be fetched in [BibTeX article](https://www.bibtex.com/e/article-entry/) format, ready for the bibliography part of your research paper.

```
THM # search keywords
Your keywords (eg. social networks): category theory
Papers matching "category theory"...

===bibtex
@article{bobc06,         
    author = "Bob Coecke",
    title = "Introducing categories to the practicing physicist",
    year = "2006",
    url = "https://arxiv.org/pdf/0808.1032.pdf",
}
@article{charl01,        
    author = "Charles Rezk",
    title = "A model for the homotopy theory of homotopy theory",
    year = "2001",
    url = "https://arxiv.org/pdf/math/9811037.pdf",
}
@article{niles21,        
    author = "Niles Johnson, Donald Yau",
    title = "A bicategorical pasting theorem",
    year = "2021",
    url = "https://arxiv.org/pdf/1910.01220.pdf",
}
===

To go further, use 'search similar', 'search details' commands...
with these arXiv IDs as reference ['0808.1032', 'math/9811037', '1910.01220']

Total of 59,114 searchable arXiv papers. Last updated 2022-11-04.
```

### Searching similar papers

```
THM # search similar
arXiv ID (eg. 2205.13980): 2009.06334
Papers similar to 2009.06334...

===bibtex
@article{john20,
    author = "John Baez, Bob Coecke",
    title = "Proceedings Applied Category Theory 2019",
    year = "2020",
    url = "https://arxiv.org/pdf/2009.06334.pdf",
    keywords = "..."
}
@article{david21,
    author = "David I. Spivak (Massachusetts Institute of Technology), Jamie Vicary (University of Cambridge)",
    title = "Proceedings of the 3rd Annual International Applied Category Theory Conference 2020",
    year = "2021",
    url = "https://arxiv.org/pdf/2101.07888.pdf",
    keywords = "..."
}
@article{bened19,
    author = "Benedikt Ahrens and Peter LeFanu Lumsdaine",
    title = "Displayed Categories",
    year = "2019",
    url = "https://arxiv.org/pdf/1705.04296.pdf",
    keywords = "..."
}
===

To go further, use 'search similar', 'search details' commands...
with these arXiv IDs as reference ['2009.06334', '2101.07888', '1705.04296']

Total of 309,164 searchable arXiv papers. Last updated 2022-11-04.
```

### Getting details about a paper

This feature displays the main information about a paper. It also shows the categories our [model]({filename}06_soft_labels.md) predicted. 

```
THM # search details
arXiv ID (eg. 2205.13980): 0809.0632
Retrieving details for 0809.0632...

How to cope with climate's complexity
by Michel Crucifix
================================================================================
Categories:

* Atmospheric and Oceanic Physics
Categories(extracted using machine learning):

* Earth and Planetary Astrophysics (0.1)
* Physics and Society (0.1)
================================================================================
  Climate exhibits a vast range of dissipative structures. Some have
characteristic times of a few days; others evolve on thousands of years. All
these structures are interdependent; in other words, they communicate. It is
often considered that the only way to cope with climate complexity is to
integrate the equations of atmospheric and oceanic motion with the finer
possible mesh. Is this the sole strategy? Aren't we missing another
characteristic of the climate system: its ability to destroy and generate
information at the macroscopic scale? Paleoclimatologists consider that much of
this information is present in palaeoclimate archives. It is therefore natural
to build climate models such as to get the most of these archives. The strategy
proposed here is based on Bayesian statistics and low-order non-linear
dynamical systems, in a modelling approach that explicitly includes the effects
of uncertainties. Its practical interest is illustrated through the problem of
the timing of the next great glaciation. Is glacial inception overdue, or do we
need to wait for another 50,000 years before ice caps grow again? Our results
indicate a glaciation inception in 50,000 years.


Opening 0809.0632 on arXiv...
```

<div align="center">
    <img src="{static}/images/arxiv.png" width=500>
</div>

## Finding answers

### Asking an open question

This features allows the user to ask an open-ended scientific question leveraging the capabilities of out [Question Answering pipeline]({filename}08_question_answering.md)

```
THM # find answer

This is a beta feature! Ask question and we will look for the article that seems to answer it best.
Ask what is on your mind: how big is the universe?
We're looking for your answer. This can take a minute...

--------------------------------------------------------------------------------
I am 12% sure about my answer:
Answer: '5x10^60'

This answer came from here:
Fractal universe and the speed of light: Revision of the universal constants
by Antonio Alfonso-Faus
================================================================================
Categories:

* General Physics
Categories(extracted using machine learning):

* General Relativity and Quantum Cosmology (0.8)
* Cosmology and Nongalactic Astrophysics (0.3)
* High Energy Physics - Theory (0.2)
================================================================================
  We apply the property of selfsimilarity that corresponds to the concept of a
fractal universe, to the dimension of time. It follows that any interval of
time, given by any tick of any clock, is proportional to the age of the
universe. The fractality of time gives the fractality of space and mass. First
consequence is that the speed of light decreases inversely proportional to
time, same as the Hubble parameter. We then revise the universal constants and,
...
```

(TODO Henrique)


### Asking about a formula

If you have doubts about a theorem you can open a query on Wolfram Alpha from your web browser.

Other sources of data are soon to be added: [Google Knowledge Graph Search API](https://developers.google.com/knowledge-graph/), [DuckDuck Go](https://duckduckgo.com)...

```
THM # find formula
Find a formula (eg. cosine law): cauchy inequality

Asking Wolfram Alpha about cauchy inequality...
```

<div align="center">
    <img src="{static}/images/wolfram.png" width=500>
</div>

## Ending the program

When you are finished, just type `exit`.

```
THM # exit


Thank you for using the service!
Have a good day!
```
