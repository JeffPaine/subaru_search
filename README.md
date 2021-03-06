# subaru_search

Subarus are awesome cars. This tool will help you quickly search many Subaru dealer websites at once by giving you a nice spreadsheet of cars to easily sort through. No more clicking through dozens of websites!.

You can take the resulting spreadsheet to the next level by calculating [Standard Scores](http://en.wikipedia.org/wiki/Standard_score) for things like mileage and price and then combining them to give you a sortable, comparable value for each car.

**NOTE**: You are responsible for acquiring permission to retrieve data from each source. By using this software you agree to be responsible for the repercussions if you do not.

## Installation

```bash
$ wget https://github.com/JeffPaine/subaru_search/archive/master.zip
$ unzip master.zip -d subaru_search
$ cd subaru_search/
$ virtualenv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

## Usage

1. Although not required, you should be a good netizen and identify yourself (and your website) by setting `USER_AGENT` at `subaru/settings.py`
1. In `subaru/spiders/subaru_spider.py`:
    1. Add the domains you have permission to retrieve data from to the `DOMAINS` variable
    1. Adjust the `MODELS` variable for the model(s) you'd like to search for. Options:
        * `Forester`
        * `Impreza`
        * `Impreza WRX`
        * `Legacy`
        * `Outback`
        * `WRX`
        * `XV Crosstrek`
1. Run `scrapy crawl subaru -o subarus.csv -t csv`
1. Open up `subarus.csv` to find the car of your dreams!
