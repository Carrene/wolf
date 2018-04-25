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
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "name":"first_token",
        "phone":989121234567,
        "isExpired":false,
        "expireDate":"2099-12-07",
        "createdAt":"2018-04-25T11:28:36.450442Z",
        "id":1,
        "isActive":true,
        "provisioning":null
    },
    {
        "modifiedAt":null,
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "name":"second_token",
        "phone":989121234567,
        "isExpired":true,
        "expireDate":"2018-04-24",
        "createdAt":"2018-04-25T11:28:36.452346Z",
        "id":2,
        "isActive":true,
        "provisioning":null
    },
    {
        "modifiedAt":null,
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "name":"third_token",
        "phone":989121234568,
        "isExpired":true,
        "expireDate":"2018-04-24",
        "createdAt":"2018-04-25T11:28:36.453050Z",
        "id":3,
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
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "name":"first_token",
        "phone":989121234567,
        "isExpired":false,
        "expireDate":"2099-12-07",
        "createdAt":"2018-04-25T11:28:36.450442Z",
        "id":1,
        "isActive":true,
        "provisioning":null
    },
    {
        "modifiedAt":null,
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "name":"second_token",
        "phone":989121234567,
        "isExpired":true,
        "expireDate":"2018-04-24",
        "createdAt":"2018-04-25T11:28:36.452346Z",
        "id":2,
        "isActive":true,
        "provisioning":null
    },
    {
        "modifiedAt":null,
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "name":"third_token",
        "phone":989121234568,
        "isExpired":true,
        "expireDate":"2018-04-24",
        "createdAt":"2018-04-25T11:28:36.453050Z",
        "id":3,
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
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "name":"third_token",
        "phone":989121234568,
        "isExpired":true,
        "expireDate":"2018-04-24",
        "createdAt":"2018-04-25T11:28:36.453050Z",
        "id":3,
        "isActive":true,
        "provisioning":null
    },
    {
        "modifiedAt":null,
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "name":"second_token",
        "phone":989121234567,
        "isExpired":true,
        "expireDate":"2018-04-24",
        "createdAt":"2018-04-25T11:28:36.452346Z",
        "id":2,
        "isActive":true,
        "provisioning":null
    },
    {
        "modifiedAt":null,
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "name":"first_token",
        "phone":989121234567,
        "isExpired":false,
        "expireDate":"2099-12-07",
        "createdAt":"2018-04-25T11:28:36.450442Z",
        "id":1,
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
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "name":"first_token",
        "phone":989121234567,
        "isExpired":false,
        "expireDate":"2099-12-07",
        "createdAt":"2018-04-25T11:28:36.450442Z",
        "id":1,
        "isActive":true,
        "provisioning":null
    },
    {
        "modifiedAt":null,
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "name":"second_token",
        "phone":989121234567,
        "isExpired":true,
        "expireDate":"2018-04-24",
        "createdAt":"2018-04-25T11:28:36.452346Z",
        "id":2,
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
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "name":"first_token",
        "phone":989121234567,
        "isExpired":false,
        "expireDate":"2099-12-07",
        "createdAt":"2018-04-25T11:28:36.450442Z",
        "id":1,
        "isActive":true,
        "provisioning":null
    },
    {
        "modifiedAt":null,
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "name":"second_token",
        "phone":989121234567,
        "isExpired":true,
        "expireDate":"2018-04-24",
        "createdAt":"2018-04-25T11:28:36.452346Z",
        "id":2,
        "isActive":true,
        "provisioning":null
    }
]
```

