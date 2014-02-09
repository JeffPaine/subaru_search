# subaru_search

Subarus are awesome cars. This tool will help you quickly search many Subaru dealer websites at once for subarus for sale.

**NOTE**: You are responsible for acquiring permission to retrieve this data from each source you plan to use. By using this software you agree to do this and be responsible for the repercussions if you do not.

## Installation

```bash
$ wget https://github.com/JeffPaine/subaru_search/archive/master.zip
$ unzip master.zip -d subaru_search
$ cd subaru_search/
$ virtualenv .venv
$ source .venv/bin/activate
(.venv)$ pip install -r requirements.txt
```

## Usage

1. Identify yourself (and your website) by setting `USER_AGENT` at `subaru/settings.py`
1. In `subaru/spiders/subaru_spider.py`:
    1. Add the domains you have permission to retrieve data from to the `DOMAINS` variable
    1. Adjust the `MODELS` variable for the model(s) you'd like to search for e.g. `Outback`
1. Run `scrapy crawl subaru -o subarus.csv -t csv`
1. Open up `subarus.csv` to find the car of your dreams!
