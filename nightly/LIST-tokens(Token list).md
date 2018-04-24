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
        "name":"first_token",
        "createdAt":"2018-04-24T23:31:42.821926Z",
        "id":1,
        "phone":989121234567,
        "modifiedAt":null,
        "isExpired":false,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "expireDate":"2099-12-07",
        "isActive":true,
        "provisioning":null
    },
    {
        "name":"second_token",
        "createdAt":"2018-04-24T23:31:42.823820Z",
        "id":2,
        "phone":989121234567,
        "modifiedAt":null,
        "isExpired":true,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "expireDate":"2018-04-23",
        "isActive":true,
        "provisioning":null
    },
    {
        "name":"third_token",
        "createdAt":"2018-04-24T23:31:42.824359Z",
        "id":3,
        "phone":989121234568,
        "modifiedAt":null,
        "isExpired":true,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "expireDate":"2018-04-23",
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
        "name":"first_token",
        "createdAt":"2018-04-24T23:31:42.821926Z",
        "id":1,
        "phone":989121234567,
        "modifiedAt":null,
        "isExpired":false,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "expireDate":"2099-12-07",
        "isActive":true,
        "provisioning":null
    },
    {
        "name":"second_token",
        "createdAt":"2018-04-24T23:31:42.823820Z",
        "id":2,
        "phone":989121234567,
        "modifiedAt":null,
        "isExpired":true,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "expireDate":"2018-04-23",
        "isActive":true,
        "provisioning":null
    },
    {
        "name":"third_token",
        "createdAt":"2018-04-24T23:31:42.824359Z",
        "id":3,
        "phone":989121234568,
        "modifiedAt":null,
        "isExpired":true,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "expireDate":"2018-04-23",
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
        "name":"third_token",
        "createdAt":"2018-04-24T23:31:42.824359Z",
        "id":3,
        "phone":989121234568,
        "modifiedAt":null,
        "isExpired":true,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "expireDate":"2018-04-23",
        "isActive":true,
        "provisioning":null
    },
    {
        "name":"second_token",
        "createdAt":"2018-04-24T23:31:42.823820Z",
        "id":2,
        "phone":989121234567,
        "modifiedAt":null,
        "isExpired":true,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "expireDate":"2018-04-23",
        "isActive":true,
        "provisioning":null
    },
    {
        "name":"first_token",
        "createdAt":"2018-04-24T23:31:42.821926Z",
        "id":1,
        "phone":989121234567,
        "modifiedAt":null,
        "isExpired":false,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
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
        "name":"first_token",
        "createdAt":"2018-04-24T23:31:42.821926Z",
        "id":1,
        "phone":989121234567,
        "modifiedAt":null,
        "isExpired":false,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "expireDate":"2099-12-07",
        "isActive":true,
        "provisioning":null
    },
    {
        "name":"second_token",
        "createdAt":"2018-04-24T23:31:42.823820Z",
        "id":2,
        "phone":989121234567,
        "modifiedAt":null,
        "isExpired":true,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "expireDate":"2018-04-23",
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
        "name":"first_token",
        "createdAt":"2018-04-24T23:31:42.821926Z",
        "id":1,
        "phone":989121234567,
        "modifiedAt":null,
        "isExpired":false,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "expireDate":"2099-12-07",
        "isActive":true,
        "provisioning":null
    },
    {
        "name":"second_token",
        "createdAt":"2018-04-24T23:31:42.823820Z",
        "id":2,
        "phone":989121234567,
        "modifiedAt":null,
        "isExpired":true,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "expireDate":"2018-04-23",
        "isActive":true,
        "provisioning":null
    }
]
```

