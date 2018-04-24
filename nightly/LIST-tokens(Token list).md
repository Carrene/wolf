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
```

```[
    {
        "id":1,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "createdAt":"2018-04-24T22:34:16.011021Z",
        "phone":989121234567,
        "name":"first_token",
        "modifiedAt":null,
        "isExpired":false,
        "expireDate":"2099-12-07",
        "isActive":true,
        "provisioning":null
    },
    {
        "id":2,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "createdAt":"2018-04-24T22:34:16.013459Z",
        "phone":989121234567,
        "name":"second_token",
        "modifiedAt":null,
        "isExpired":true,
        "expireDate":"2018-04-23",
        "isActive":true,
        "provisioning":null
    },
    {
        "id":3,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "createdAt":"2018-04-24T22:34:16.014217Z",
        "phone":989121234568,
        "name":"third_token",
        "modifiedAt":null,
        "isExpired":true,
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
```

```[
    {
        "id":1,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "createdAt":"2018-04-24T22:34:16.011021Z",
        "phone":989121234567,
        "name":"first_token",
        "modifiedAt":null,
        "isExpired":false,
        "expireDate":"2099-12-07",
        "isActive":true,
        "provisioning":null
    },
    {
        "id":2,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "createdAt":"2018-04-24T22:34:16.013459Z",
        "phone":989121234567,
        "name":"second_token",
        "modifiedAt":null,
        "isExpired":true,
        "expireDate":"2018-04-23",
        "isActive":true,
        "provisioning":null
    },
    {
        "id":3,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "createdAt":"2018-04-24T22:34:16.014217Z",
        "phone":989121234568,
        "name":"third_token",
        "modifiedAt":null,
        "isExpired":true,
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
```

```[
    {
        "id":3,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "createdAt":"2018-04-24T22:34:16.014217Z",
        "phone":989121234568,
        "name":"third_token",
        "modifiedAt":null,
        "isExpired":true,
        "expireDate":"2018-04-23",
        "isActive":true,
        "provisioning":null
    },
    {
        "id":2,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "createdAt":"2018-04-24T22:34:16.013459Z",
        "phone":989121234567,
        "name":"second_token",
        "modifiedAt":null,
        "isExpired":true,
        "expireDate":"2018-04-23",
        "isActive":true,
        "provisioning":null
    },
    {
        "id":1,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "createdAt":"2018-04-24T22:34:16.011021Z",
        "phone":989121234567,
        "name":"first_token",
        "modifiedAt":null,
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
```

```[
    {
        "id":1,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "createdAt":"2018-04-24T22:34:16.011021Z",
        "phone":989121234567,
        "name":"first_token",
        "modifiedAt":null,
        "isExpired":false,
        "expireDate":"2099-12-07",
        "isActive":true,
        "provisioning":null
    },
    {
        "id":2,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "createdAt":"2018-04-24T22:34:16.013459Z",
        "phone":989121234567,
        "name":"second_token",
        "modifiedAt":null,
        "isExpired":true,
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
```

```[
    {
        "id":1,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "createdAt":"2018-04-24T22:34:16.011021Z",
        "phone":989121234567,
        "name":"first_token",
        "modifiedAt":null,
        "isExpired":false,
        "expireDate":"2099-12-07",
        "isActive":true,
        "provisioning":null
    },
    {
        "id":2,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "createdAt":"2018-04-24T22:34:16.013459Z",
        "phone":989121234567,
        "name":"second_token",
        "modifiedAt":null,
        "isExpired":true,
        "expireDate":"2018-04-23",
        "isActive":true,
        "provisioning":null
    }
]
```

