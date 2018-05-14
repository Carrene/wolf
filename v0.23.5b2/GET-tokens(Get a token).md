## Get a token

### GET /apiv1/tokens/:token_id

Get a single token by id

### Url Parameters

Name | Example
--- | ---
token_id | 1

### Response: 200 OK

#### Headers

* Content-Type: application/json; charset=utf-8
* Content-Length: 341

#### Body

```json
{
    "modifiedAt":null,
    "expireDate":"2099-12-07",
    "createdAt":"2018-04-26T15:21:50.571638Z",
    "cryptomodule":{
        "id":1,
        "timeInterval":60,
        "oneTimePasswordLength":4
    },
    "id":1,
    "phone":989121234567,
    "isExpired":false,
    "name":"first_token",
    "isActive":true,
    "provisioning":null
}
```

## WHEN: Trying to get a none existence token

### Url Parameters

Name | Example
--- | ---
token_id | 0

### Response: 404 Not Found

#### Headers

* Content-Type: application/json; charset=utf-8
* Content-Length: 69

#### Body

```json
{"message":"Not Found","description":"Nothing matches the given URI"}
```

## WHEN: Trying to get a token with an invalid token id

### Response: 404 Not Found

#### Headers

* Content-Type: text/plain; charset=utf-8
* Content-Length: 39

#### Body

```
Not Found
Nothing matches the given URI
```
