Title: The THM CLI
Date: 2022-11-30 10:25
Modified: 2022-11-30 10:25
Category: THM CLI
Tags: python
Slug: snippets
Authors: Tom Darmon, Henrique Brito, Michel Hua
Summary: The THM CLI

[![asciicast](https://asciinema.org/a/CGtMSoSe0Fp8dn9nbLpzzbdbM.svg)](https://asciinema.org/a/CGtMSoSe0Fp8dn9nbLpzzbdbM)

<script id="asciicast-CGtMSoSe0Fp8dn9nbLpzzbdbM" src="https://asciinema.org/a/CGtMSoSe0Fp8dn9nbLpzzbdbM.js" async></script>

# Running THM CLI

Open the terminal and run the following command,

```sh
thm-cli
```

You will have access to a prompt where you can type commands,

```txt
THM Search CLI
Your arXiv-BibTeX terminal assistant.

---
The single most important thing in life is to believe in yourself regardless of what everyone else says.
Hikaru Nakamura
---


THM #
```

# The THM prompt

## Gettting Help

```txt
THM # help
```

## Search the arXiv database

### Searching for keywords

```txt
THM # search keywords
```

Enter a search query to discover scholarly papers.
Your keywords (eg. social networks): category theory
Papers matching "category theory"...

'''bibtex
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
'''

Total of 309,164 searchable arXiv papers. Last updated 2022-11-04.
```

### Searching similar papers

```txt
THM # search similar
```

### Gettings details about a paper

```txt
THM # search details
```

## Finding answers

### Asking an open question

```txt
THM # find answer
```

### Asking about a formula

```txt
THM # find formula
```
