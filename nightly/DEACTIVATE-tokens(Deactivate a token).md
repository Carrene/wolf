## Deactivate a token

### DEACTIVATE /apiv1/tokens/:token_id

Deactivate a token by id

### Url Parameters

Name | Example
--- | ---
token_id | 1

### Response: 200 OK

#### Headers

* Content-Type: application/json; charset=utf-8
* Content-Length: 367

#### Body

```json
{
    "cryptomodule":{
        "oneTimePasswordLength":4,
        "timeInterval":60,
        "id":1
    },
    "name":"active_token",
    "expireDate":"2000-12-07",
    "isExpired":true,
    "createdAt":"2018-04-25T11:31:17.415752Z",
    "phone":989121234567,
    "modifiedAt":"2018-04-25T11:31:17.426509Z",
    "id":1,
    "isActive":false,
    "provisioning":null
}
```

## WHEN: Trying to deactivate a none existence token

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

## WHEN: Trying to deactivate a active token

### Url Parameters

Name | Example
--- | ---
token_id | 2

### Response: 463 Token is deactivated

#### Headers

* Content-Type: application/json; charset=utf-8
* Content-Length: 78

#### Body

```json
{"message":"Token is deactivated","description":"Token has been deactivated."}
```

