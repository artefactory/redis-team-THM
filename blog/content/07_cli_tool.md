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

Today most interfaces are browser based because applications are running in the cloud and with little setup needed as just loading a page, it is more convenient. But this wasn't already the case, at the beginning of computing, interfaces were terminal-based and then desktop-GUI-based.

In 2015, chatbots made their come back on popular messaging platforms such as Facebook Messenger, Google Home, Siri, and WeChat. The idea was you could just write a free sentence or an improved textual command, and that the server could answer your requests by triggering APIs and also using NLP techniques.

During these years, I have asked myself how to put that in the perspective of Linux command line tools where the Linux user got at hand and prompt a large variety of commands and fully documented by manpages. You can in fact ask anything to a computer using a simple text prompt and and not having graphical interface doesn't necessarly mean you are less productive.

In fact, developpers often find themselves more productive with just an IDE and a Terminal.

From the user experience when writing technical and scientific documents people use [Leslie Lamport](https://en.wikipedia.org/wiki/Leslie_Lamport)'s LaTeX or Markdown in text editors to produce high quality documents were formulas, sections and fonts are perfectly rendered. We thought that the terminal was the best way to help them due to the focus it provides and compared to distractful web-browser

In the last few years, NLP research has also improved enabling experiences such as those provided by the _Open AI GPT-3_ based tasks, where you can ask tasks to the computer by just writing or saying a sentence.

To be honest, writing a good frontend web page was also challenging for the short duration of the hackathon, so it appeared to be a good compromise to go the CLI way. We were also inspired by old projects such as [`ncurses`](https://www.gnu.org/software/ncurses/), [`jarun/googler`](https://github.com/jarun/googler) and [`gautamkrishnar/socli`](https://github.com/gautamkrishnar/socli) which provide clean command line interfaces to Google and Stackoverflow, and knew users were still interested in this old-fashioned way of doing.

# Python frameworks

After briefly studying the list of available libraries in Python from [`awesome-python` / CLI Development](https://github.com/vinta/awesome-python#command-line-interface-development), we finally chose [`prompt-toolkit/python-prompt-toolkit`](https://github.com/prompt-toolkit/python-prompt-toolkit) and [`google/python-fire`](https://github.com/google/python-fire) to deliver a collection of CLI tools for our hackathon project.

- `prompt-toolkit` is the easiest way to approach the `google` and `socli` interface, with interactive capabilities and making the terminal experience less abrupt,
- `fire` is a convenient and fast way to decorate existing Python functions and classes and provide quick CLI interface for background tasks not related to user interface.

To make the background tasks commands more robust and better documented, I would have used [`pallets/click`](https://github.com/pallets/click) or [`docopt/docopt`](https://github.com/docopt/docopt), but Hackathon was all about finding compromise between quickly delivery and rapidity of development.

<iframe width="560" height="315" src="https://www.youtube.com/embed/UTtDb73NkNM" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

<i>I am sure Tom Hanks would have definetly approved our project</i>