## Token list

### LIST /apiv1/tokens

List of tokens

### Response: 200 OK

#### Headers

* Content-Type: application/json; charset=utf-8
* X-Pagination-Take: 100
* X-Pagination-Skip: 0
* X-Pagination-Count: 3
* Content-Length: 1222

#### Body

```json
[
    {
        "modifiedAt":null,
        "expireDate":"2099-12-07",
        "createdAt":"2018-04-26T15:21:51.037567Z",
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
    },
    {
        "modifiedAt":null,
        "expireDate":"2018-04-25",
        "createdAt":"2018-04-26T15:21:51.039672Z",
        "cryptomodule":{
            "id":1,
            "timeInterval":60,
            "oneTimePasswordLength":4
        },
        "id":2,
        "phone":989121234567,
        "isExpired":true,
        "name":"second_token",
        "isActive":true,
        "provisioning":null
    },
    {
        "modifiedAt":null,
        "expireDate":"2018-04-25",
        "createdAt":"2018-04-26T15:21:51.040375Z",
        "cryptomodule":{
            "id":1,
            "timeInterval":60,
            "oneTimePasswordLength":4
        },
        "id":3,
        "phone":989121234568,
        "isExpired":true,
        "name":"third_token",
        "isActive":true,
        "provisioning":null
    }
]
```

## WHEN: Trying to get list of tokens sorted by id ascending

### Query Strings

Name | Example
--- | ---
sort | id

### Response: 200 OK

#### Headers

* Content-Type: application/json; charset=utf-8
* X-Pagination-Take: 100
* X-Pagination-Skip: 0
* X-Pagination-Count: 3
* Content-Length: 1222

#### Body

```json
[
    {
        "modifiedAt":null,
        "expireDate":"2099-12-07",
        "createdAt":"2018-04-26T15:21:51.037567Z",
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
    },
    {
        "modifiedAt":null,
        "expireDate":"2018-04-25",
        "createdAt":"2018-04-26T15:21:51.039672Z",
        "cryptomodule":{
            "id":1,
            "timeInterval":60,
            "oneTimePasswordLength":4
        },
        "id":2,
        "phone":989121234567,
        "isExpired":true,
        "name":"second_token",
        "isActive":true,
        "provisioning":null
    },
    {
        "modifiedAt":null,
        "expireDate":"2018-04-25",
        "createdAt":"2018-04-26T15:21:51.040375Z",
        "cryptomodule":{
            "id":1,
            "timeInterval":60,
            "oneTimePasswordLength":4
        },
        "id":3,
        "phone":989121234568,
        "isExpired":true,
        "name":"third_token",
        "isActive":true,
        "provisioning":null
    }
]
```

## WHEN: Trying to get list of tokens sorted by id descending

### Query Strings

Name | Example
--- | ---
sort | -id

### Response: 200 OK

#### Headers

* Content-Type: application/json; charset=utf-8
* X-Pagination-Take: 100
* X-Pagination-Skip: 0
* X-Pagination-Count: 3
* Content-Length: 1222

#### Body

```json
[
    {
        "modifiedAt":null,
        "expireDate":"2018-04-25",
        "createdAt":"2018-04-26T15:21:51.040375Z",
        "cryptomodule":{
            "id":1,
            "timeInterval":60,
            "oneTimePasswordLength":4
        },
        "id":3,
        "phone":989121234568,
        "isExpired":true,
        "name":"third_token",
        "isActive":true,
        "provisioning":null
    },
    {
        "modifiedAt":null,
        "expireDate":"2018-04-25",
        "createdAt":"2018-04-26T15:21:51.039672Z",
        "cryptomodule":{
            "id":1,
            "timeInterval":60,
            "oneTimePasswordLength":4
        },
        "id":2,
        "phone":989121234567,
        "isExpired":true,
        "name":"second_token",
        "isActive":true,
        "provisioning":null
    },
    {
        "modifiedAt":null,
        "expireDate":"2099-12-07",
        "createdAt":"2018-04-26T15:21:51.037567Z",
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
]
```

## WHEN: Trying to get list of tokens with phone query string

### Query Strings

Name | Example
--- | ---
phone | 989121234567

### Response: 200 OK

#### Headers

* Content-Type: application/json; charset=utf-8
* X-Pagination-Take: 100
* X-Pagination-Skip: 0
* X-Pagination-Count: 2
* Content-Length: 816

#### Body

```json
[
    {
        "modifiedAt":null,
        "expireDate":"2099-12-07",
        "createdAt":"2018-04-26T15:21:51.037567Z",
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
    },
    {
        "modifiedAt":null,
        "expireDate":"2018-04-25",
        "createdAt":"2018-04-26T15:21:51.039672Z",
        "cryptomodule":{
            "id":1,
            "timeInterval":60,
            "oneTimePasswordLength":4
        },
        "id":2,
        "phone":989121234567,
        "isExpired":true,
        "name":"second_token",
        "isActive":true,
        "provisioning":null
    }
]
```

## WHEN: Trying to get list of tokens with take query string

### Query Strings

Name | Example
--- | ---
take | 2

### Response: 200 OK

#### Headers

* Content-Type: application/json; charset=utf-8
* X-Pagination-Take: 2
* X-Pagination-Skip: 0
* X-Pagination-Count: 3
* Content-Length: 816

#### Body

```json
[
    {
        "modifiedAt":null,
        "expireDate":"2099-12-07",
        "createdAt":"2018-04-26T15:21:51.037567Z",
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
    },
    {
        "modifiedAt":null,
        "expireDate":"2018-04-25",
        "createdAt":"2018-04-26T15:21:51.039672Z",
        "cryptomodule":{
            "id":1,
            "timeInterval":60,
            "oneTimePasswordLength":4
        },
        "id":2,
        "phone":989121234567,
        "isExpired":true,
        "name":"second_token",
        "isActive":true,
        "provisioning":null
    }
]
```

