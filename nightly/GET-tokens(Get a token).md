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
    "cryptomodule":{
        "oneTimePasswordLength":4,
        "timeInterval":60,
        "id":1
    },
    "name":"first_token",
    "expireDate":"2099-12-07",
    "isExpired":false,
    "createdAt":"2018-04-25T11:31:19.306875Z",
    "phone":989121234567,
    "modifiedAt":null,
    "id":1,
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

