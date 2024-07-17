## Endpoints
> :information_source: all the responses will be encrypted, also the requests must be encrypted, this a protection layer, so not everyone can see the victims.
### 1. Upload a file.
- URL: `/up`
- Method: `POST`
- Description: Upload a file to the server.
- Status Codes:
  - 200: Successfully uploaded the file.
- Response: None.  
### 2. Check the API.
- URL: `/check`
- Method: `GET`
- Description: Check if the API cryptographic parameters matches the ones in the CLI.
- Status Codes:
  - 200: The cryptographic parameters matches the ones in the CLI.
  - 400: The cryptographic parameters did not matches the ones in the CLI.
- Response:
```json
{
  "cc": "encrypted message"
}
```
### 3. Get victim list.
- URL: `/GetAll`
- Method: `GET`
- Description: retrieve a list of dicts, containing information about each victims.
- Status Codes:
  - Always 200.
- Response Body:
```json

{
    "127.0.0.1": {
        "browsers": [
            {
                "extentions": {
                    "METAMASK": [
                    ]
                },
                "browserfiles": [
                    "KEY",
                    "COOKIES.DB",
                    "LOGIN.DB"
                ]
            }
        ],
        "BrowserCount": 1
    }
}
```
### 4. Get victim's browser data.
- URL: `/GetVictimData`
- Method: `GET`
- Description: retrieve a list of dicts, containing victim's browser data.
- Request Headers:
  - `TARGET`: (str) Victim's ip.
- Status Codes:
  - 200: the requested victim exists.
  - 204: the requested victim does not exist.
  - 400: the request contains wrong data.
- Response Body:
```json
{
  "PASSWORDS": [
    [
      ...
    ]
  ],
  "COOKIES": [
    [
      ...
    ]
  ]
}
```
### 5. Get victim's all data.
- URL: `/down`
- Method: `GET`
- Description: download all victim's data.
- Request Headers:
  - `TARGET`: (str) Victim's ip.
- Status Codes:
  - 200: the requested victim exists.
  - 204: the requested victim does not exist.
  - 400: the request contains wrong data.
- Response Body: a Zip file containing victim's data.