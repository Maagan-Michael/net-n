---
title: FastAPI v0.1.0
language_tabs:
  - shell: Shell
  - http: HTTP
  - javascript: JavaScript
  - ruby: Ruby
  - python: Python
  - php: PHP
  - java: Java
  - go: Go
toc_footers: []
includes: []
search: true
highlight_theme: darkula
headingLevel: 2

---

<!-- Generator: Widdershins v4.0.1 -->

<h1 id="fastapi">FastAPI v0.1.0</h1>

> Scroll down for code samples, example requests and responses. Select a language for code samples from the tabs above or the mobile navigation menu.

<h1 id="fastapi-v1">v1</h1>

## listConnections_api_v1_connections_get

<a id="opIdlistConnections_api_v1_connections_get"></a>

`GET /api/v1/connections`

*Listconnections*

return a paginated list of connections

<h3 id="listconnections_api_v1_connections_get-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|page|query|integer|false|none|
|limit|query|integer|false|none|
|sort|query|string|false|none|
|search|query|any|false|none|
|order|query|any|false|none|
|filter|query|any|false|none|

> Example responses

> 200 Response

```json
{
  "connections": [],
  "hasPrevious": false,
  "hasNext": false
}
```

<h3 id="listconnections_api_v1_connections_get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[ConnectionsOutput](#schemaconnectionsoutput)|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## getConnection_api_v1_connection__id__get

<a id="opIdgetConnection_api_v1_connection__id__get"></a>

`GET /api/v1/connection/{id}`

*Getconnection*

return a connection

<h3 id="getconnection_api_v1_connection__id__get-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "ppp": "string",
  "port": 0,
  "toggled": false,
  "toggleDate": "2019-08-24T14:15:22Z",
  "type": "copper|fiber",
  "isUp": false,
  "proto": "snmp",
  "speed": 0,
  "switch": {
    "id": 0,
    "name": "string",
    "ip": "0.0.0.0",
    "gpsLat": 0,
    "gpsLong": 0
  },
  "customer": {
    "id": 0,
    "firstname": "string",
    "lastname": "string",
    "type": "string",
    "address": "string"
  }
}
```

<h3 id="getconnection_api_v1_connection__id__get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[ConnectionOutput](#schemaconnectionoutput)|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## createConnection_api_v1_connection_create_post

<a id="opIdcreateConnection_api_v1_connection_create_post"></a>

`POST /api/v1/connection/create`

*Createconnection*

create a connection

> Body parameter

```json
{
  "id": 0,
  "ppp": "string",
  "port": 0,
  "toggled": false,
  "toggleDate": "2019-08-24T14:15:22Z",
  "type": "copper|fiber",
  "isUp": false,
  "proto": "snmp",
  "speed": 0,
  "switchId": 0,
  "customerId": 0
}
```

<h3 id="createconnection_api_v1_connection_create_post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[ConnectionInput](#schemaconnectioninput)|true|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "ppp": "string",
  "port": 0,
  "toggled": false,
  "toggleDate": "2019-08-24T14:15:22Z",
  "type": "copper|fiber",
  "isUp": false,
  "proto": "snmp",
  "speed": 0,
  "switch": {
    "id": 0,
    "name": "string",
    "ip": "0.0.0.0",
    "gpsLat": 0,
    "gpsLong": 0
  },
  "customer": {
    "id": 0,
    "firstname": "string",
    "lastname": "string",
    "type": "string",
    "address": "string"
  }
}
```

<h3 id="createconnection_api_v1_connection_create_post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[ConnectionOutput](#schemaconnectionoutput)|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## updateConnection_api_v1_connection_update__id__post

<a id="opIdupdateConnection_api_v1_connection_update__id__post"></a>

`POST /api/v1/connection/update/{id}`

*Updateconnection*

update a connection

> Body parameter

```json
{
  "id": 0,
  "ppp": "string",
  "port": 0,
  "toggled": false,
  "toggleDate": "2019-08-24T14:15:22Z",
  "type": "copper|fiber"
}
```

<h3 id="updateconnection_api_v1_connection_update__id__post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[UpdateConnectionInput](#schemaupdateconnectioninput)|true|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "ppp": "string",
  "port": 0,
  "toggled": false,
  "toggleDate": "2019-08-24T14:15:22Z",
  "type": "copper|fiber",
  "isUp": false,
  "proto": "snmp",
  "speed": 0,
  "switch": {
    "id": 0,
    "name": "string",
    "ip": "0.0.0.0",
    "gpsLat": 0,
    "gpsLong": 0
  },
  "customer": {
    "id": 0,
    "firstname": "string",
    "lastname": "string",
    "type": "string",
    "address": "string"
  }
}
```

<h3 id="updateconnection_api_v1_connection_update__id__post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[ConnectionOutput](#schemaconnectionoutput)|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## deleteConnection_api_v1_connection_delete__id__delete

<a id="opIddeleteConnection_api_v1_connection_delete__id__delete"></a>

`DELETE /api/v1/connection/delete/{id}`

*Deleteconnection*

delete a connection

<h3 id="deleteconnection_api_v1_connection_delete__id__delete-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|

> Example responses

> 200 Response

```json
"string"
```

<h3 id="deleteconnection_api_v1_connection_delete__id__delete-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|string|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## listSwitches_api_v1_switches_get

<a id="opIdlistSwitches_api_v1_switches_get"></a>

`GET /api/v1/switches`

*Listswitches*

return a list of switches

> Example responses

> 200 Response

```json
[
  {
    "id": 0,
    "name": "string",
    "ip": "0.0.0.0",
    "gpsLat": 0,
    "gpsLong": 0
  }
]
```

<h3 id="listswitches_api_v1_switches_get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|

<h3 id="listswitches_api_v1_switches_get-responseschema">Response Schema</h3>

Status Code **200**

*Response Listswitches Api V1 Switches Get*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|Response Listswitches Api V1 Switches Get|[[Switch](#schemaswitch)]|false|none|[Switch Database model]|
|» Switch|[Switch](#schemaswitch)|false|none|Switch Database model|
|»» id|integer|true|none|none|
|»» name|string|true|none|none|
|»» ip|string|false|none|none|
|»» gpsLat|any|false|none|none|

*anyOf*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»»» *anonymous*|number|false|none|none|

*or*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»»» *anonymous*|null|false|none|none|

*continued*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»» gpsLong|any|false|none|none|

*anyOf*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»»» *anonymous*|number|false|none|none|

*or*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»»» *anonymous*|null|false|none|none|

<aside class="success">
This operation does not require authentication
</aside>

## getSwitch_api_v1_switch__id__get

<a id="opIdgetSwitch_api_v1_switch__id__get"></a>

`GET /api/v1/switch/{id}`

*Getswitch*

return a switch

<h3 id="getswitch_api_v1_switch__id__get-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "name": "string",
  "ip": "0.0.0.0",
  "gpsLat": 0,
  "gpsLong": 0
}
```

<h3 id="getswitch_api_v1_switch__id__get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[Switch](#schemaswitch)|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## createSwitch_api_v1_switch_create_post

<a id="opIdcreateSwitch_api_v1_switch_create_post"></a>

`POST /api/v1/switch/create`

*Createswitch*

create a switch

> Body parameter

```json
{
  "id": 0,
  "name": "string",
  "ip": "0.0.0.0",
  "gpsLat": 0,
  "gpsLong": 0
}
```

<h3 id="createswitch_api_v1_switch_create_post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[Switch](#schemaswitch)|true|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "name": "string",
  "ip": "0.0.0.0",
  "gpsLat": 0,
  "gpsLong": 0
}
```

<h3 id="createswitch_api_v1_switch_create_post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[Switch](#schemaswitch)|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## updateSwitch_api_v1_switch_update__id__post

<a id="opIdupdateSwitch_api_v1_switch_update__id__post"></a>

`POST /api/v1/switch/update/{id}`

*Updateswitch*

update a switch

> Body parameter

```json
{
  "id": 0,
  "name": "string",
  "ip": "0.0.0.0",
  "gpsLat": 0,
  "gpsLong": 0
}
```

<h3 id="updateswitch_api_v1_switch_update__id__post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[Switch](#schemaswitch)|true|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "name": "string",
  "ip": "0.0.0.0",
  "gpsLat": 0,
  "gpsLong": 0
}
```

<h3 id="updateswitch_api_v1_switch_update__id__post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[Switch](#schemaswitch)|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## deleteSwitch_api_v1_switch_delete__id__delete

<a id="opIddeleteSwitch_api_v1_switch_delete__id__delete"></a>

`DELETE /api/v1/switch/delete/{id}`

*Deleteswitch*

delete a switch

<h3 id="deleteswitch_api_v1_switch_delete__id__delete-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|

> Example responses

> 200 Response

```json
"string"
```

<h3 id="deleteswitch_api_v1_switch_delete__id__delete-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|string|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## listCustomers_api_v1_customers_get

<a id="opIdlistCustomers_api_v1_customers_get"></a>

`GET /api/v1/customers`

*Listcustomers*

return a list of customers

> Example responses

> 200 Response

```json
[
  {
    "id": 0,
    "firstname": "string",
    "lastname": "string",
    "type": "string",
    "address": "string"
  }
]
```

<h3 id="listcustomers_api_v1_customers_get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|

<h3 id="listcustomers_api_v1_customers_get-responseschema">Response Schema</h3>

Status Code **200**

*Response Listcustomers Api V1 Customers Get*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|Response Listcustomers Api V1 Customers Get|[[Customer](#schemacustomer)]|false|none|[Customer Database model]|
|» Customer|[Customer](#schemacustomer)|false|none|Customer Database model|
|»» id|integer|true|none|none|
|»» firstname|string|true|none|none|
|»» lastname|string|true|none|none|
|»» type|string|true|none|none|
|»» address|string|true|none|none|

<aside class="success">
This operation does not require authentication
</aside>

## getCustomer_api_v1_customer__id__get

<a id="opIdgetCustomer_api_v1_customer__id__get"></a>

`GET /api/v1/customer/{id}`

*Getcustomer*

return a customer

<h3 id="getcustomer_api_v1_customer__id__get-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "firstname": "string",
  "lastname": "string",
  "type": "string",
  "address": "string"
}
```

<h3 id="getcustomer_api_v1_customer__id__get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[Customer](#schemacustomer)|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## createCustomer_api_v1_customer_create_post

<a id="opIdcreateCustomer_api_v1_customer_create_post"></a>

`POST /api/v1/customer/create`

*Createcustomer*

create a customer

> Body parameter

```json
{
  "id": 0,
  "firstname": "string",
  "lastname": "string",
  "type": "string",
  "address": "string"
}
```

<h3 id="createcustomer_api_v1_customer_create_post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[Customer](#schemacustomer)|true|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "firstname": "string",
  "lastname": "string",
  "type": "string",
  "address": "string"
}
```

<h3 id="createcustomer_api_v1_customer_create_post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[Customer](#schemacustomer)|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## updateCustomer_api_v1_customer_update__id__post

<a id="opIdupdateCustomer_api_v1_customer_update__id__post"></a>

`POST /api/v1/customer/update/{id}`

*Updatecustomer*

update a customer

> Body parameter

```json
{
  "id": 0,
  "firstname": "string",
  "lastname": "string",
  "type": "string",
  "address": "string"
}
```

<h3 id="updatecustomer_api_v1_customer_update__id__post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[Customer](#schemacustomer)|true|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "firstname": "string",
  "lastname": "string",
  "type": "string",
  "address": "string"
}
```

<h3 id="updatecustomer_api_v1_customer_update__id__post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[Customer](#schemacustomer)|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## deleteCustomer_api_v1_customer_delete__id__delete

<a id="opIddeleteCustomer_api_v1_customer_delete__id__delete"></a>

`DELETE /api/v1/customer/delete/{id}`

*Deletecustomer*

delete a customer

<h3 id="deletecustomer_api_v1_customer_delete__id__delete-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|

> Example responses

> 200 Response

```json
"string"
```

<h3 id="deletecustomer_api_v1_customer_delete__id__delete-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|string|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

# Schemas

<h2 id="tocS_ConnectionInput">ConnectionInput</h2>
<!-- backwards compatibility -->
<a id="schemaconnectioninput"></a>
<a id="schema_ConnectionInput"></a>
<a id="tocSconnectioninput"></a>
<a id="tocsconnectioninput"></a>

```json
{
  "id": 0,
  "ppp": "string",
  "port": 0,
  "toggled": false,
  "toggleDate": "2019-08-24T14:15:22Z",
  "type": "copper|fiber",
  "isUp": false,
  "proto": "snmp",
  "speed": 0,
  "switchId": 0,
  "customerId": 0
}

```

ConnectionInput

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|true|none|none|
|ppp|string|true|none|none|
|port|integer|false|none|none|
|toggled|boolean|false|none|none|
|toggleDate|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string(date-time)|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|type|string|false|none|none|
|isUp|boolean|false|none|none|
|proto|string|false|none|none|
|speed|integer|false|none|none|
|switchId|integer|false|none|none|
|customerId|integer|false|none|none|

<h2 id="tocS_ConnectionOutput">ConnectionOutput</h2>
<!-- backwards compatibility -->
<a id="schemaconnectionoutput"></a>
<a id="schema_ConnectionOutput"></a>
<a id="tocSconnectionoutput"></a>
<a id="tocsconnectionoutput"></a>

```json
{
  "id": 0,
  "ppp": "string",
  "port": 0,
  "toggled": false,
  "toggleDate": "2019-08-24T14:15:22Z",
  "type": "copper|fiber",
  "isUp": false,
  "proto": "snmp",
  "speed": 0,
  "switch": {
    "id": 0,
    "name": "string",
    "ip": "0.0.0.0",
    "gpsLat": 0,
    "gpsLong": 0
  },
  "customer": {
    "id": 0,
    "firstname": "string",
    "lastname": "string",
    "type": "string",
    "address": "string"
  }
}

```

ConnectionOutput

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|true|none|none|
|ppp|string|true|none|none|
|port|integer|false|none|none|
|toggled|boolean|false|none|none|
|toggleDate|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string(date-time)|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|type|string|false|none|none|
|isUp|boolean|false|none|none|
|proto|string|false|none|none|
|speed|integer|false|none|none|
|switch|[Switch](#schemaswitch)|false|none|Switch Database model|
|customer|[Customer](#schemacustomer)|false|none|Customer Database model|

<h2 id="tocS_ConnectionsOutput">ConnectionsOutput</h2>
<!-- backwards compatibility -->
<a id="schemaconnectionsoutput"></a>
<a id="schema_ConnectionsOutput"></a>
<a id="tocSconnectionsoutput"></a>
<a id="tocsconnectionsoutput"></a>

```json
{
  "connections": [],
  "hasPrevious": false,
  "hasNext": false
}

```

ConnectionsOutput

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|connections|[[ConnectionOutput](#schemaconnectionoutput)]|false|none|[Connection model API output]|
|hasPrevious|boolean|false|none|none|
|hasNext|boolean|false|none|none|

<h2 id="tocS_Customer">Customer</h2>
<!-- backwards compatibility -->
<a id="schemacustomer"></a>
<a id="schema_Customer"></a>
<a id="tocScustomer"></a>
<a id="tocscustomer"></a>

```json
{
  "id": 0,
  "firstname": "string",
  "lastname": "string",
  "type": "string",
  "address": "string"
}

```

Customer

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|true|none|none|
|firstname|string|true|none|none|
|lastname|string|true|none|none|
|type|string|true|none|none|
|address|string|true|none|none|

<h2 id="tocS_HTTPValidationError">HTTPValidationError</h2>
<!-- backwards compatibility -->
<a id="schemahttpvalidationerror"></a>
<a id="schema_HTTPValidationError"></a>
<a id="tocShttpvalidationerror"></a>
<a id="tocshttpvalidationerror"></a>

```json
{
  "detail": [
    {
      "loc": [
        "string"
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}

```

HTTPValidationError

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|detail|[[ValidationError](#schemavalidationerror)]|false|none|none|

<h2 id="tocS_ListFilterEnum">ListFilterEnum</h2>
<!-- backwards compatibility -->
<a id="schemalistfilterenum"></a>
<a id="schema_ListFilterEnum"></a>
<a id="tocSlistfilterenum"></a>
<a id="tocslistfilterenum"></a>

```json
"all"

```

ListFilterEnum

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|ListFilterEnum|string|false|none|to filter down connections search results|

#### Enumerated Values

|Property|Value|
|---|---|
|ListFilterEnum|all|
|ListFilterEnum|customer|
|ListFilterEnum|address|
|ListFilterEnum|enabled|
|ListFilterEnum|disabled|
|ListFilterEnum|up|
|ListFilterEnum|down|
|ListFilterEnum|port|
|ListFilterEnum|switch|

<h2 id="tocS_OrderEnum">OrderEnum</h2>
<!-- backwards compatibility -->
<a id="schemaorderenum"></a>
<a id="schema_OrderEnum"></a>
<a id="tocSorderenum"></a>
<a id="tocsorderenum"></a>

```json
"asc"

```

OrderEnum

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|OrderEnum|string|false|none|to order results in a paginated request|

#### Enumerated Values

|Property|Value|
|---|---|
|OrderEnum|asc|
|OrderEnum|desc|

<h2 id="tocS_Switch">Switch</h2>
<!-- backwards compatibility -->
<a id="schemaswitch"></a>
<a id="schema_Switch"></a>
<a id="tocSswitch"></a>
<a id="tocsswitch"></a>

```json
{
  "id": 0,
  "name": "string",
  "ip": "0.0.0.0",
  "gpsLat": 0,
  "gpsLong": 0
}

```

Switch

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|true|none|none|
|name|string|true|none|none|
|ip|string|false|none|none|
|gpsLat|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|number|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|gpsLong|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|number|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

<h2 id="tocS_UpdateConnectionInput">UpdateConnectionInput</h2>
<!-- backwards compatibility -->
<a id="schemaupdateconnectioninput"></a>
<a id="schema_UpdateConnectionInput"></a>
<a id="tocSupdateconnectioninput"></a>
<a id="tocsupdateconnectioninput"></a>

```json
{
  "id": 0,
  "ppp": "string",
  "port": 0,
  "toggled": false,
  "toggleDate": "2019-08-24T14:15:22Z",
  "type": "copper|fiber"
}

```

UpdateConnectionInput

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|true|none|none|
|ppp|string|true|none|none|
|port|integer|false|none|none|
|toggled|boolean|false|none|none|
|toggleDate|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string(date-time)|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|type|string|false|none|none|

<h2 id="tocS_ValidationError">ValidationError</h2>
<!-- backwards compatibility -->
<a id="schemavalidationerror"></a>
<a id="schema_ValidationError"></a>
<a id="tocSvalidationerror"></a>
<a id="tocsvalidationerror"></a>

```json
{
  "loc": [
    "string"
  ],
  "msg": "string",
  "type": "string"
}

```

ValidationError

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|loc|[anyOf]|true|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|integer|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|msg|string|true|none|none|
|type|string|true|none|none|

