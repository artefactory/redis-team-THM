Title: Setting up the Services
Date: 2022-10-25 14:30
Modified: 2022-10-25 14:30
Category: MLOps
Tags: technology
Slug: saturn-redis-cloud
Authors: Michel Hua, Tom Darmon, Corentin Roineau
Summary: Setting up the Services

_Day 4 - When we have set up the services._

# Setting Up the Services

The kickoff call gave us precious instructions on how we could use cloud resources to deliver our project.

<iframe width="560" height="315" src="https://www.youtube.com/embed/uS9ZGi8RyPM" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Blog posts were also helpful in understanding how RediSearch could be used, [Ed Sandoval's LinkedIn activity feed](https://www.linkedin.com/in/edsandovaluk/) had was a mine of information and helped us find the most relevant blog posts.

## Saturn Cloud

The first resource that was available was [Saturn Cloud](https://saturncloud.io). Saturn Cloud provide environment where data science teams can contribute on managed Jupyter Notebook, and also use powerful servers with lots of RAM, CPUs and GPUs to perform their compute workfloads. It has services to run notebooks, jobs and APIs with very little setup.

You can sign up and [try it for free](https://app.community.saturnenterprise.io/auth/hosted-registration). Once this is done you, can create resources and user [recipes](https://saturncloud.io/docs/using-saturn-cloud/recipes/) which are infrastructure as code-like templates to quickstart your configuration.

<div align="center">
    <img src="{static}/images/configure_saturn.png" width=500>
</div>

You just hit Create New Python Server to get a Jupyter server with GPU and CUDA enabled with [Nvidia's RAPIDS framework](https://developer.nvidia.com/rapids).

<div align="center">
    <img src="{static}/images/configure_saturn2.png" width=500>
</div>

Configuring our IDE's with a [SSH connection to Saturn Cloud](https://saturncloud.io/docs/using-saturn-cloud/ide_ssh/) was also an easy process, and enabled data scientists to work directly within VSCode with the classical terminal and file explorer.

The process of configuring this took about 30 minutes overall.

## Redis Enterprise Cloud

<div align="center">
    <img src="{static}/images/configure_redis.png" width=500>
</div>

The second resource we used is [Redis Enterprise Cloud](https://redis.com/redis-enterprise-cloud/overview/). This tool also comes up with a [free trial](https://redis.com/try-free/) which is limited in memory.

But during the Hackathon, Redis Ventures provided us credits to use both products with the full developer experience.

We created a new subscription, using a flexible plan. Redis Cloud Enterprise can support AWS, GCP and Azure. After setting up the cloud provider, we chose AWS, and region were to deploy, we configured advanced settings such as database replication, we did't need it and lastly the size of 26 GB for the database, and high availability.

Redis Cloud Enterprise really has a lot of configuration settings if you want to fine tune your production workloads.

## Install Redis Insights

After gettings our Redis credentials from Redis Cloud, we configured a desktop graphical user interface called [Redis Insights](https://redis.com/redis-enterprise/redis-insight/)

<div align="center">
    <img src="{static}/images/redis_insights.png" width=500>
</div>

Redis insights enabled us to easily inspect for hashes, and also run some low level Redis commands using its terminal.
