Title: Submission Day
Date: 2022-11-05 17:42
Modified: 2022-11-05 17:42
Category: MLOps
Tags: redis
Slug: 11_submission
Authors: Michel Hua
Summary: Submission Day

_Day 11 - The day we had to submit our project._

# Final thoughts

The project went very quickly as we were busy with our normal jobs, and it was challenging to find time committing is the hackathon.

But overall, the project was very exciting and allowed us to discover how easy it was to use RediSearch and Saturn Cloud. Doing things in very limited time made us thought about was to prioritize, we had many ideas but had to make things as simple as possible.

We would like to thank "Redis Ventures" for providing the opportunity to show our project and our skills, but also for the quality of information and resources they provided for every team to do their best.

Other teams at Artefact kept also a competitive but friendly mindset, that's why we like our company [so much](https://artefactory.github.io/redis-team-THM/category/team.html).

# Other interesting things

Forking the [sample repository](https://github.com/RedisVentures/redis-arXiv-search) was very easy and enabled us not to start from scratch, we made a few MLOps-related, improvements over the original project,

- generated index and loaded data faster to make it production ready, `struct.pack`(https://github.com/artefactory/redis-team-THM/blob/main/scripts/load_data.py#L42) is a faster way to pack the [array of float of embeddings](https://stackoverflow.com/a/9941024/1360476) an is critical in the workflow, and using smaller embeddings
- extracted code from notebooks to make it modulable and enabling reusing code in a modern orchestration tool.
- managed credentials and project settings using Pydantic [`BaseSettings`](https://github.com/artefactory/redis-team-THM/blob/main/backend/thm/config/settings.py)

We didn't find time to look at these topics, but it will a great ideas to make the project move forward,

- [`docarray` has a binding to Redis](https://docarray.jina.ai/advanced/document-store/redis/)
- Publishing the CLI to PyPI
- Evaluate other sources of data
- Instant suggestion after a few keystrokes like in [this AlgoliaSearch demo](https://algoliacom-search-demo.netlify.app)
- Using fuzzy matching techniques to improve quality of results
- "I am feeling lucky" button like in Google
- scheduling using Saturn Cloud Jobs

If you want to contribute don't hesitate, changes and improvements are welcome! Feel free to fork and open a pull request into `main`.
