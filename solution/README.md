# Python weekend entry task

**This was a task given by kiwi.com in order to enroll in the upcoming BCN code camp**

**ACK to Adam Mikulášek**

## How to run it?
The easiest way to run this code is by running it as:

`python -m solution PATH ORIGIN DESTINATION --bags=INT --return --days=INT --exp=String`

where:

- `PATH` should be existing path to csv file
- `ORIGIN` , `DESTINATION` should contain an existing Airport code from the csv file

- `--bags` default is set to 0 meaning user does not have a requirement regarding baggage,
user can specify the minimum number of bags to carry using:
`--bags=Int` or `--bags Int` flights allowing less luggage than selected will be excluded.

- `--return` is a simple flag triggering the possibility to get a return ticket, default is set to False. 

- `--days` default is set to 0 meaning user does not have a preference regarding the minimum days to spend on destination
user can specify the number of days before return flight using:
`--days=Int` or `--days Int`

- `--exp=String` or `--exp String` flag to save the json under specified name, save is made as String.json, when the 'String' not specified, defaultly as export.json

Code runs as is, no environment setup is required other than having python installed.

## OUTPUT

**Output is a json printed into the terminal, flights are ordered by price**

For `python -m solution ./example/example0.csv WIW ECV --bags=1 --return --days 9` it looks as:


```json
[
    {
        "flights": [
            {
                "flight_no": "ZH151",
                "origin": "WIW",
                "destination": "ECV",
                "departure": "2021-09-01T07:25:00",
                "arrival": "2021-09-01T12:35:00",
                "base_price": 245.0,
                "bag_price": 12.0,
                "bags_allowed": 2
            },
            {
                "flight_no": "ZH151",
                "origin": "ECV",
                "destination": "WIW",
                "departure": "2021-09-11T15:35:00",
                "arrival": "2021-09-11T20:45:00",
                "base_price": 245.0,
                "bag_price": 12.0,
                "bags_allowed": 2
            }
        ],
        "bags_allowed": 2,
        "bags_count": 1,
        "destination": "ECV",
        "origin": "WIW",
        "totalprice": 514.0,
        "travel_time": "10:20:00"
    },
    {
        "flights": [
            {
                "flight_no": "ZH151",
                "origin": "WIW",
                "destination": "ECV",
                "departure": "2021-09-02T07:25:00",
                "arrival": "2021-09-02T12:35:00",
                "base_price": 245.0,
                "bag_price": 12.0,
                "bags_allowed": 2
            },
            {
                "flight_no": "ZH151",
                "origin": "ECV",
                "destination": "WIW",
                "departure": "2021-09-11T15:35:00",
                "arrival": "2021-09-11T20:45:00",
                "base_price": 245.0,
                "bag_price": 12.0,
                "bags_allowed": 2
            }
        ],
        "bags_allowed": 2,
        "bags_count": 1,
        "destination": "ECV",
        "origin": "WIW",
        "totalprice": 514.0,
        "travel_time": "10:20:00"
    }
]
```
