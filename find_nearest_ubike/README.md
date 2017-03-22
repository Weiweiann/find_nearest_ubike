# Find two nearest ubike stations in Taipei City

### Instructions

1. set up virtualenv
2. `pip install -r requirements.txt`
3. run migrate 
4. run server

### API usage

- /v1/ubike-station/taipei
  - Method: `GET`
  
  - Parameters: 
  
	    - `lat` (latitude)
	    
	    - `lng` (longitude)

  - Response:
  
		- code: 
		    
		  - 1: all ubkie stations are full
		  - 0: OK
		  - -1: invalid latitude and longitude
		  - -2: location not in Taipei city
		  - -3: system error
		  
		- result: 
		  - station: $name-of-the-station 
		  - num_ubike: $number-of-avaliable-bike 

  - example 
    
    ```
    GET /v1/ubike-station/taipei?lat=25.017966&lng=121.543967

    {
      "code": 0,
      "result": [
        {
          "station": "基隆長興路口",
          "num_ubike": 41
        },
        {
          "station": "臺大資訊大樓",
          "num_ubike": 53
        }
      ]
    }
    ```


    ```
    GET /v1/ubike-station/taipei?lat=24.950208&lng=121.351406

    {
      "code": -2,
      "result": []
    }
    ```
