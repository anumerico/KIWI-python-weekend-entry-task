# Python weekend entry task

**This was a task given by kiwi.com in order to enroll in upcomming code camp in Košice, Slovakia**

## How to run it?
The easiest way to run this code is by running it as:

`python -m solution PATH ORIGIN DESTINATION --bags=INT --ret --exp=String`

where:

- `PATH` should be existing path to csv file
- `ORIGIN` , `DESTINATION` should contain the existing point in the csv file

- `--bags` is set to default as 0, user does not have a prefference in the number of his luggage
user can specify the number of bags using:
`--bags=Int` or `--bags Int` he flights allowing less luggage then preffered will be excluded.

- `--ret` is a simple flag triggering the possibility to get a return ticket, defaultly set to False, 
currently allowing no less then 12h to spend in the destination country

- `--exp=String` flag to save the json under specified name, saves is made as String.json, when the 'String' not specified, defaultly as export.json

No special distros, installations are needed.
## OUTPUT

**Output is a json printed into the terminal, flights are ordered by price**

For `python -m solution example0.csv WIW ECV --bags=1 --ret` it looks as:


```json
{
    "allflights": [
        {
            "flights": [
                {
                    "flight_no": "ZH214",
                    "origin": "WIW",
                    "destination": "RFZ",
                    "departure": "2021-09-01T23:20:00",
                    "arrival": "2021-09-02T03:50:00",  
                    "base_price": 168.0,
                    "bag_price": 12.0,
                    "bags_allowed": 2
                },
                {
                    "flight_no": "ZH665",
                    "origin": "RFZ",
                    "destination": "ECV",
                    "departure": "2021-09-02T07:40:00",
                    "arrival": "2021-09-02T20:10:00",  
                    "base_price": 58.0,
                    "bag_price": 12.0,
                    "bags_allowed": 2
                },
                {
                    "flight_no": "ZH151",
                    "origin": "ECV",
                    "destination": "WIW",
                    "departure": "2021-09-06T15:35:00",
                    "arrival": "2021-09-06T20:45:00",  
                    "base_price": 245.0,
                    "bag_price": 12.0,
                    "bags_allowed": 2
                }
            ],
            "bags_allowed": 2,
            "bags_count": 1,
            "destination": "WIW",
            "origin": "WIW",
            "totalprice": 507.0,
            "travel_time": "4 days, 21:25:00"
        },
        {
            .
            .
            .
        }
    ]
}```

