Title: CLI Tool HTTP Client
Date: 2022-10-29 12:05
Modified: 2022-10-29 12:05
Category: MLOps
Tags: search
Slug: cli-tool
Authors: Michel Hua
Summary: CLI Tool HTTP Client

_Day 7 - When we decided the old CLI was still the best interface in 2022._

# What interface to choose?

Today, most interfaces are browser-based because applications run in the cloud with little setup needed. But this was not the case not so long ago, when interfaces were terminal-based and later on desktop-GUI-based.

In 2015, chatbots made their comeback on popular messaging platforms such as Facebook Messenger, Google Home, Siri, and WeChat. The idea was that you could just write a free sentence or an improved textual command, and the server could answer your requests by triggering APIs and by using NLP techniques.

During these years, I have asked myself how to put that in the perspective of Linux command line tools. You can, in fact, ask anything to a computer using a simple text prompt, and the lack of a graphical interface doesn't necessarily mean you are less productive. In fact, I believe it is possible to create a powerful application that relies on user prompts and commands and that is also fully documented by man pages.

In fact, developers often find themselves more productive with just an IDE and a Terminal.

From the user experience when writing technical and scientific documents people use [Leslie Lamport](https://en.wikipedia.org/wiki/Leslie_Lamport)'s LaTeX or Markdown in text editors to produce high quality documents where formulas, sections and fonts are perfectly rendered. We thought that the terminal was the best way to help them due to the focus it provides compared to the average web-browser, that is crowded with distractions.

In the last few years, NLP research has also improved, enabling experiences such as those provided by the _Open AI GPT-3_ based tasks, where you can ask tasks to the computer by just writing or saying a sentence.

To be honest, writing a good frontend web page was also challenging for the short duration of the hackathon, so the CLI appeared to be a good compromise. We were also inspired by old projects such as [`ncurses`](https://www.gnu.org/software/ncurses/), [`jarun/googler`](https://github.com/jarun/googler) and [`gautamkrishnar/socli`](https://github.com/gautamkrishnar/socli) which provide clean command line interfaces to Google and Stack Overflow since new users were still getting interested in this old-fashioned technologies.

# Python frameworks

After briefly studying the list of available libraries in Python from [`awesome-python` / CLI Development](https://github.com/vinta/awesome-python#command-line-interface-development), we finally chose [`prompt-toolkit/python-prompt-toolkit`](https://github.com/prompt-toolkit/python-prompt-toolkit) and [`google/python-fire`](https://github.com/google/python-fire) to deliver a collection of CLI tools for our hackathon project.

- `prompt-toolkit` is the easiest way to approach the `google` and `socli` interface, with interactive capabilities and making the terminal experience less abrupt,
- `fire` is a convenient and fast way to decorate existing Python functions and classes and provide quick CLI interface for background tasks not related to user interface.

To make the background tasks commands more robust and better documented, I would have used [`pallets/click`](https://github.com/pallets/click) or [`docopt/docopt`](https://github.com/docopt/docopt), but the hackathon was all about finding compromise between quickly delivery and rapidity of development.

<iframe width="560" height="315" src="https://www.youtube.com/embed/UTtDb73NkNM" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

<i>I am sure Tom Hanks would have approved our project</i>