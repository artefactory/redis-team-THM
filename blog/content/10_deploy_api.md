Title: Deploying the application
Date: 2022-11-03 12:12
Modified: 2022-11-03 12:12
Category: MLOps
Tags: redis
Slug: 10_tbd
Authors: Michel Hua
Summary: Deploying the application

_Day 10 - Deploying the application_

# Running locally

After making sure a Redis database is available, we start the ASGI webserver using this command

```sh
cd backend/
uvicorn api:app --host 0.0.0.0 --port 8080 --workers 4
# INFO: Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```

You can choose to install `redis` locally or connect to Redis Cloud Enterprise if you have good internet access and want very little setup.

# Running from Saturn Cloud

There are plenty of platform as a service choices to deploy this simple FastAPI web server, Heroku, Deta, AWS Elastic Beanstalk. But for this project we choose to try Saturn Cloud Deployment, the process was straightforward.

<div align="center">
    <img src="{static}/images/configure_deployment.png" width=500>
</div>

After copying our database connection secrets, we can run our server, connecting to it using SSH just like for Jupyter Notebooks.

<div align="center">
    <img src="{static}/images/configure_secrets.png" width=500>
</div>

The domain name in the form of `*.community.saturnenterprise.io` can be chosen. We deployed, then finally configured the HTTP client, the CLI tool we built since day 7.

<div align="center">
    <a href="https://thm-cli.community.saturnenterprise.io/api/docs">https://thm-cli.community.saturnenterprise.io</a>
</div>

# References

- [Saturn Cloud Git Repo](https://saturncloud.io/docs/using-saturn-cloud/gitrepo/)
- [Saturn Cloud Deployment](https://saturncloud.io/docs/using-saturn-cloud/resources/deployments/)