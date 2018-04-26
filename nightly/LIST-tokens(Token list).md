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
        "cryptomodule":{
            "id":1,
            "timeInterval":60,
            "oneTimePasswordLength":4
        },
        "name":"first_token",
        "modifiedAt":null,
        "id":1,
        "createdAt":"2018-04-26T15:19:24.556097Z",
        "phone":989121234567,
        "isExpired":false,
        "expireDate":"2099-12-07",
        "isActive":true,
        "provisioning":null
    },
    {
        "cryptomodule":{
            "id":1,
            "timeInterval":60,
            "oneTimePasswordLength":4
        },
        "name":"second_token",
        "modifiedAt":null,
        "id":2,
        "createdAt":"2018-04-26T15:19:24.558853Z",
        "phone":989121234567,
        "isExpired":true,
        "expireDate":"2018-04-25",
        "isActive":true,
        "provisioning":null
    },
    {
        "cryptomodule":{
            "id":1,
            "timeInterval":60,
            "oneTimePasswordLength":4
        },
        "name":"third_token",
        "modifiedAt":null,
        "id":3,
        "createdAt":"2018-04-26T15:19:24.559814Z",
        "phone":989121234568,
        "isExpired":true,
        "expireDate":"2018-04-25",
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
        "cryptomodule":{
            "id":1,
            "timeInterval":60,
            "oneTimePasswordLength":4
        },
        "name":"first_token",
        "modifiedAt":null,
        "id":1,
        "createdAt":"2018-04-26T15:19:24.556097Z",
        "phone":989121234567,
        "isExpired":false,
        "expireDate":"2099-12-07",
        "isActive":true,
        "provisioning":null
    },
    {
        "cryptomodule":{
            "id":1,
            "timeInterval":60,
            "oneTimePasswordLength":4
        },
        "name":"second_token",
        "modifiedAt":null,
        "id":2,
        "createdAt":"2018-04-26T15:19:24.558853Z",
        "phone":989121234567,
        "isExpired":true,
        "expireDate":"2018-04-25",
        "isActive":true,
        "provisioning":null
    },
    {
        "cryptomodule":{
            "id":1,
            "timeInterval":60,
            "oneTimePasswordLength":4
        },
        "name":"third_token",
        "modifiedAt":null,
        "id":3,
        "createdAt":"2018-04-26T15:19:24.559814Z",
        "phone":989121234568,
        "isExpired":true,
        "expireDate":"2018-04-25",
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
        "cryptomodule":{
            "id":1,
            "timeInterval":60,
            "oneTimePasswordLength":4
        },
        "name":"third_token",
        "modifiedAt":null,
        "id":3,
        "createdAt":"2018-04-26T15:19:24.559814Z",
        "phone":989121234568,
        "isExpired":true,
        "expireDate":"2018-04-25",
        "isActive":true,
        "provisioning":null
    },
    {
        "cryptomodule":{
            "id":1,
            "timeInterval":60,
            "oneTimePasswordLength":4
        },
        "name":"second_token",
        "modifiedAt":null,
        "id":2,
        "createdAt":"2018-04-26T15:19:24.558853Z",
        "phone":989121234567,
        "isExpired":true,
        "expireDate":"2018-04-25",
        "isActive":true,
        "provisioning":null
    },
    {
        "cryptomodule":{
            "id":1,
            "timeInterval":60,
            "oneTimePasswordLength":4
        },
        "name":"first_token",
        "modifiedAt":null,
        "id":1,
        "createdAt":"2018-04-26T15:19:24.556097Z",
        "phone":989121234567,
        "isExpired":false,
        "expireDate":"2099-12-07",
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
        "cryptomodule":{
            "id":1,
            "timeInterval":60,
            "oneTimePasswordLength":4
        },
        "name":"first_token",
        "modifiedAt":null,
        "id":1,
        "createdAt":"2018-04-26T15:19:24.556097Z",
        "phone":989121234567,
        "isExpired":false,
        "expireDate":"2099-12-07",
        "isActive":true,
        "provisioning":null
    },
    {
        "cryptomodule":{
            "id":1,
            "timeInterval":60,
            "oneTimePasswordLength":4
        },
        "name":"second_token",
        "modifiedAt":null,
        "id":2,
        "createdAt":"2018-04-26T15:19:24.558853Z",
        "phone":989121234567,
        "isExpired":true,
        "expireDate":"2018-04-25",
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
        "cryptomodule":{
            "id":1,
            "timeInterval":60,
            "oneTimePasswordLength":4
        },
        "name":"first_token",
        "modifiedAt":null,
        "id":1,
        "createdAt":"2018-04-26T15:19:24.556097Z",
        "phone":989121234567,
        "isExpired":false,
        "expireDate":"2099-12-07",
        "isActive":true,
        "provisioning":null
    },
    {
        "cryptomodule":{
            "id":1,
            "timeInterval":60,
            "oneTimePasswordLength":4
        },
        "name":"second_token",
        "modifiedAt":null,
        "id":2,
        "createdAt":"2018-04-26T15:19:24.558853Z",
        "phone":989121234567,
        "isExpired":true,
        "expireDate":"2018-04-25",
        "isActive":true,
        "provisioning":null
    }
]
```

