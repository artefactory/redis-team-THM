Title: The THM CLI
Date: 2022-11-04 10:25
Modified: 2022-11-04 10:25
Category: THM CLI
Tags: python
Slug: snippets
Authors: Henrique Brito, Michel Hua
Summary: The THM CLI

<script id="asciicast-CGtMSoSe0Fp8dn9nbLpzzbdbM" src="https://asciinema.org/a/CGtMSoSe0Fp8dn9nbLpzzbdbM.js" async></script>

# Running THM CLI

Open the terminal and run the following command,

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

## Gettting Help

```
THM # help
THM Search CLI v1.0
https://artefactory.github.io/redis-team-THM

Usage:
  search [keywords|similar|details]
  find [answer|formula]
  configure
  help
  exit
```

## Configure the tool

You can configure some parameters such as output format, and the number of results to display by default.

```
THM # configure
Choose file format (markdown, bibtex): bibtex
Max Results (eg. 3): 4
```

## Search the arXiv database

### Searching for keywords

Just type in a few words like `category theory` and results will be fetched in [BibTeX article](https://www.bibtex.com/e/article-entry/) format ready you to copy paste bibliography of your research paper.

```
THM # search keywords
Your keywords (eg. social networks): category theory
Papers matching "category theory"...

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
@article{wille17,
    author = "Willem Conradie, Sabine Frittella, Michele Piazzai, Apostolos Tzimoulis, Alessandra Palmigiano and Nachoem M. Wijnberg",
    title = "Categories: How I Learned to Stop Worrying and Love Two Sorts",
    year = "2017",
    url = "https://arxiv.org/pdf/1604.00777.pdf",
    keywords = "..."
}
===

To go further, use 'search similar', 'search details' commands...
with these arXiv IDs as reference ['2009.06334', '2101.07888', '1604.00777']

Total of 309,164 searchable arXiv papers. Last updated 2022-11-04.
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
    cs.LO
}
@article{david21,
    author = "David I. Spivak (Massachusetts Institute of Technology), Jamie Vicary (University of Cambridge)",
    title = "Proceedings of the 3rd Annual International Applied Category Theory Conference 2020",
    year = "2021",
    url = "https://arxiv.org/pdf/2101.07888.pdf",
    keywords = "..."
    cs.DM,cs.PL
}
@article{bened19,
    author = "Benedikt Ahrens and Peter LeFanu Lumsdaine",
    title = "Displayed Categories",
    year = "2019",
    url = "https://arxiv.org/pdf/1705.04296.pdf",
    keywords = "..."
    math.CT,math.LO
}
===

To go further, use 'search similar', 'search details' commands...
with these arXiv IDs as reference ['2009.06334', '2101.07888', '1705.04296']

Total of 309,164 searchable arXiv papers. Last updated 2022-11-04.
```

### Gettings details about a paper

```
THM # search details
arXiv ID (eg. 2205.13980): 1705.04296
Retrieving details for 1705.04296...

Displayed Categories
by Benedikt Ahrens and Peter LeFanu Lumsdaine
================================================================================
  We introduce and develop the notion of *displayed categories*.
  A displayed category over a category C is equivalent to "a category D and
functor F : D --> C", but instead of having a single collection of "objects of
D" with a map to the objects of C, the objects are given as a family indexed by
objects of C, and similarly for the morphisms. This encapsulates a common way
of building categories in practice, by starting with an existing category and
adding extra data/properties to the objects and morphisms.
  The interest of this seemingly trivial reformulation is that various
properties of functors are more naturally defined as properties of the
corresponding displayed categories. Grothendieck fibrations, for example, when
defined as certain functors, use equality on objects in their definition. When
defined instead as certain displayed categories, no reference to equality on
objects is required. Moreover, almost all examples of fibrations in nature are,
in fact, categories whose standard construction can be seen as going via
displayed categories.
  We therefore propose displayed categories as a basis for the development of
fibrations in the type-theoretic setting, and similarly for various other
notions whose classical definitions involve equality on objects.
  Besides giving a conceptual clarification of such issues, displayed
categories also provide a powerful tool in computer formalisation, unifying and
abstracting common constructions and proof techniques of category theory, and
enabling modular reasoning about categories of multi-component structures. As
such, most of the material of this article has been formalised in Coq over the
UniMath library, with the aim of providing a practical library for use in
further developments.


Opening 1705.04296 on arXiv...
```

<div align="center">
    <img src="{static}/images/arxiv.png" width=500>
</div>

## Finding answers

### Asking an open question

```
THM # find answer

TODO Henrique
```

### Asking about a formula

If you have doubts about a theorem you can open a query on Wolfram Alpha from your web browser.

Other sources of data are soon to be added: [Google Knowledge Graph Search API](https://developers.google.com/knowledge-graph/), [DuckDuck Go](https://duckduckgo.com), [StackExchange](https://stackexchange.com)...

```
THM # find formula
Find a formula (eg. cosine law): cauchy inequality

Asking Wolfram Alpha about cauchy inequality...
```

<div align="center">
    <img src="{static}/images/wolfram.png" width=500>
</div>

## End the program

When you are finished, just type `exit`.

```
THM # exit
```
