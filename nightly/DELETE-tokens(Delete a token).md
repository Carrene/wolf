## Delete a token

### DELETE /apiv1/tokens/:token_id

Delete a token by id

### Url Parameters

Name | Example
--- | ---
token_id | 1

### Response: 200 OK

#### Headers

* Content-Type: application/json; charset=utf-8
* Content-Length: 340

#### Body

```json
{
    "cryptomodule":{
        "id":1,
        "timeInterval":60,
        "oneTimePasswordLength":4
    },
    "name":"first_token",
    "modifiedAt":null,
    "id":1,
    "createdAt":"2018-04-26T15:19:22.763647Z",
    "phone":989121234567,
    "isExpired":true,
    "expireDate":"2000-12-07",
    "isActive":true,
    "provisioning":null
}
```

## WHEN: Trying to delete a none existence token

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

## WHEN: Trying to get a deleted token

### Response: 404 Not Found

#### Headers

* Content-Type: application/json; charset=utf-8
* Content-Length: 69

#### Body

```json
{"message":"Not Found","description":"Nothing matches the given URI"}
```

