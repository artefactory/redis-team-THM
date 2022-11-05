Title: CLI Tool HTTP Client
Date: 2022-10-29 12:05
Modified: 2022-10-29 12:05
Category: MLOps
Tags: search
Slug: cli-tool
Authors: Michel Hua
Summary: CLI Tool HTTP Client

_Day 7 - When we decided the old CLI was still the best interface in 2022._

# CLI tool

In 2015, chatbots
- textual command,
- Open AI GPT-3 based tasks

From the user experience when writing technical and scientific documents people use [Leslie Lamport](https://en.wikipedia.org/wiki/Leslie_Lamport) LaTeX in Markdown and text editors to produce high quality documents were formulas, sections and fonts are perfectly rendered. We thought that the terminal was the best way to help them due to the focus it provides and compared to distractful web-browser

<iframe width="560" height="315" src="https://www.youtube.com/embed/UTtDb73NkNM" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

We were inspired by old project such as [`jarun/googler`](https://github.com/jarun/googler) and [`gautamkrishnar/socli`](https://github.com/gautamkrishnar/socli) which provide distractful command line interfaces to Google and Stackoverflow.

# Python frameworks

After briefly studying the list of available libraries, from [`awesome-python` / CLI Development](https://github.com/vinta/awesome-python#command-line-interface-development), we finally chose [`prompt-toolkit/python-prompt-toolkit`](https://github.com/prompt-toolkit/python-prompt-toolkit) and [`google/python-fire`](https://github.com/google/python-fire) to deliver a collection of CLI tools for our hackathon project.
