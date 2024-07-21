### Crawler System

System consists of 4 parts:

-   Crawler
-   Scheduler
-   Explorer
-   Controller

Crawler:
Crawls [tagesschau's](https://www.tagesschau.de/) home page and news pages and saves it into a PostgreSQL database.
Crawler function with several modes, developed with Beautiful Soup 4 and SQLAlchemy.

Scheduler:
Schedules periodic crawls to run on the background. Provides tools to have control over the Crawler.
Periodic job executer, planner and rescheduler developed with APScheduler.

Controller:
Utilizes Scheduler's tools to provide control over the Crawler.
Has multiple options to control jobs and instant crawls.
RESTApi developed with Flask, SQLAlchemy, Flask-SQLAlchemy

Endpoints:

-   "/crawler/pages": Get a list of pages
-   "/crawler/instant/<page>": Crawl a page
-   "/crawler/instant": Crawl overview page
-   "/job/increase": Increases the interval of job execution by one hour
-   "/job/decrease": Decreases the interval of job execution by one hour
-   "/job/reschedule/<hour>": Reschedules the crawler job if found
-   "/job/enable": Enables crawler job if found
-   "/job/disable": Disables crawler job if found

Explorer:
Allows exploration of the information gathered by all 3 other services.
RESTApi developed with Flask, SQLAlchemy, Flask-SQLAlchemy.
Consists solely of information retrievening endpoints.

Endpoints:

-   "/articles": Get a list of articles
-   "/articles-with-versions": Get a list of articles with versions
-   "/articles/<keyword>": Get a list of articles that contains a keyword
-   "/article/<id\_>/versions": Get all the different versions of an article

##### How to run the Crawler System

All apps are containerised for convenience.

**With Docker:**

To run the system using Docker containers, run the following command:
`docker-compose -f docker-compose.yml up`

**Local:**

To run the applications locally:

-   Create a `.env.local` file
-   Insert `DB_NAME=<NAME_OF_YOUR_CHOOSING>` into `.env.local`
-   Create a virtual python environment
-   Activate the environment
-   Run `pip install -r requirements.txt`
-   Run `pip install python-dotenv`
-   Spin up your local PostgreSQL server
-   On one shell run `python3 controller.py`
-   On another shell run `python3 explorer.py`

##### Tests:

There are 18 tests in total.
Test files have the *test\_<FILE*NAME>\* prefix and the system they are for as their name.
To check out the tests, please refer to `apps/tests`

**How to run the tests:**

-   Create a file called `.env.local`
-   Insert `CONNECTION_STR=sqlite:///mock.sqlite` into your `.env.local` file
-   Create a virtual python environment
-   Activate the environment
-   Run `pip install -r requirements.txt`
-   Run `pytest` in your shell

##### Assumptions:

-   Assumed all the news pages have headlines, toplines and some texts. If even one of those elements are absent, I did not keep record of said page.
