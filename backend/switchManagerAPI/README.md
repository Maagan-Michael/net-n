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

## listConnections_api_v1_connections__get

<a id="opIdlistConnections_api_v1_connections__get"></a>

`GET /api/v1/connections/`

*Listconnections*

return a paginated list of connections

<h3 id="listconnections_api_v1_connections__get-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|page|query|integer|false|none|
|limit|query|integer|false|none|
|search|query|any|false|none|
|sort|query|any|false|none|
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

<h3 id="listconnections_api_v1_connections__get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[ConnectionsOutput](#schemaconnectionsoutput)|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## getConnection_api_v1_connections__id__get

<a id="opIdgetConnection_api_v1_connections__id__get"></a>

`GET /api/v1/connections/{id}`

*Getconnection*

return a connection

<h3 id="getconnection_api_v1_connections__id__get-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|

> Example responses

> 200 Response

```json
{
  "id": "string",
  "ppp": "string",
  "port": 0,
  "toggled": false,
  "toggleDate": "2019-08-24T14:15:22Z",
  "type": "copper|fiber",
  "isUp": false,
  "proto": "snmp",
  "speed": 0,
  "switch": {
    "id": "string",
    "ip": "0.0.0.0",
    "gpsLat": 0,
    "gpsLong": 0
  },
  "customer": {
    "id": "string",
    "firstname": "string",
    "lastname": "string",
    "type": "string",
    "address": "string"
  }
}
```

<h3 id="getconnection_api_v1_connections__id__get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[ConnectionOutput](#schemaconnectionoutput)|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## upsertConnection_api_v1_connections_upsert_post

<a id="opIdupsertConnection_api_v1_connections_upsert_post"></a>

`POST /api/v1/connections/upsert`

*Upsertconnection*

upsert or udpate one || multiple connections

> Body parameter

```json
{
  "id": "string",
  "name": "string",
  "port": 0,
  "toggled": true,
  "toggleDate": "2019-08-24T14:15:22Z",
  "type": "string",
  "isUp": true,
  "proto": "string",
  "speed": 0,
  "switchId": 0,
  "customerId": 0
}
```

<h3 id="upsertconnection_api_v1_connections_upsert_post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|any|true|none|

> Example responses

> 200 Response

```json
{
  "items": [],
  "errors": []
}
```

<h3 id="upsertconnection_api_v1_connections_upsert_post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[switchmanagerapi__models__factories__batcheableOutputFactory___locals___BatcheableOutputModel__1](#schemaswitchmanagerapi__models__factories__batcheableoutputfactory___locals___batcheableoutputmodel__1)|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## deleteConnection_api_v1_connections_delete__id__delete

<a id="opIddeleteConnection_api_v1_connections_delete__id__delete"></a>

`DELETE /api/v1/connections/delete/{id}`

*Deleteconnection*

delete a connection

<h3 id="deleteconnection_api_v1_connections_delete__id__delete-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|

> Example responses

> 200 Response

```json
"string"
```

<h3 id="deleteconnection_api_v1_connections_delete__id__delete-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|string|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## listCustomers_api_v1_customers__get

<a id="opIdlistCustomers_api_v1_customers__get"></a>

`GET /api/v1/customers/`

*Listcustomers*

return a list of customers

> Example responses

> 200 Response

```json
[
  {
    "id": "string",
    "firstname": "string",
    "lastname": "string",
    "type": "string",
    "address": "string"
  }
]
```

<h3 id="listcustomers_api_v1_customers__get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|

<h3 id="listcustomers_api_v1_customers__get-responseschema">Response Schema</h3>

Status Code **200**

*Response Listcustomers Api V1 Customers  Get*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|Response Listcustomers Api V1 Customers  Get|[[Customer](#schemacustomer)]|false|none|[Customer Database model]|
|» Customer|[Customer](#schemacustomer)|false|none|Customer Database model|
|»» id|string|true|none|customer id / worker id|
|»» firstname|string|true|none|none|
|»» lastname|string|true|none|none|
|»» type|string|true|none|customer type (company name || person status)|
|»» address|string|true|none|none|

<aside class="success">
This operation does not require authentication
</aside>

## getCustomer_api_v1_customers__id__get

<a id="opIdgetCustomer_api_v1_customers__id__get"></a>

`GET /api/v1/customers/{id}`

*Getcustomer*

return a customer

<h3 id="getcustomer_api_v1_customers__id__get-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|

> Example responses

> 200 Response

```json
{
  "id": "string",
  "firstname": "string",
  "lastname": "string",
  "type": "string",
  "address": "string"
}
```

<h3 id="getcustomer_api_v1_customers__id__get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[Customer](#schemacustomer)|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## upsertCustomer_api_v1_customers_upsert_post

<a id="opIdupsertCustomer_api_v1_customers_upsert_post"></a>

`POST /api/v1/customers/upsert`

*Upsertcustomer*

upsert or udpate one || multiple customer(s)

> Body parameter

```json
{
  "id": "string",
  "firstname": "string",
  "lastname": "string",
  "type": "string",
  "address": "string"
}
```

<h3 id="upsertcustomer_api_v1_customers_upsert_post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|any|true|none|

> Example responses

> 200 Response

```json
{
  "items": [],
  "errors": []
}
```

<h3 id="upsertcustomer_api_v1_customers_upsert_post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[switchmanagerapi__models__factories__batcheableOutputFactory___locals___BatcheableOutputModel__2](#schemaswitchmanagerapi__models__factories__batcheableoutputfactory___locals___batcheableoutputmodel__2)|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## deleteCustomer_api_v1_customers_delete__id__delete

<a id="opIddeleteCustomer_api_v1_customers_delete__id__delete"></a>

`DELETE /api/v1/customers/delete/{id}`

*Deletecustomer*

delete a customer

<h3 id="deletecustomer_api_v1_customers_delete__id__delete-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|

> Example responses

> 200 Response

```json
"string"
```

<h3 id="deletecustomer_api_v1_customers_delete__id__delete-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|string|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## listSwitches_api_v1_switches__get

<a id="opIdlistSwitches_api_v1_switches__get"></a>

`GET /api/v1/switches/`

*Listswitches*

return a list of switches

> Example responses

> 200 Response

```json
[
  {
    "id": "string",
    "ip": "0.0.0.0",
    "gpsLat": 0,
    "gpsLong": 0
  }
]
```

<h3 id="listswitches_api_v1_switches__get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|

<h3 id="listswitches_api_v1_switches__get-responseschema">Response Schema</h3>

Status Code **200**

*Response Listswitches Api V1 Switches  Get*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|Response Listswitches Api V1 Switches  Get|[[Switch](#schemaswitch)]|false|none|[Switch Database model]|
|» Switch|[Switch](#schemaswitch)|false|none|Switch Database model|
|»» id|string|true|none|switch unique name / id|
|»» ip|string|false|none|switch ip address|
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

## getSwitch_api_v1_switches__id__get

<a id="opIdgetSwitch_api_v1_switches__id__get"></a>

`GET /api/v1/switches/{id}`

*Getswitch*

return a switch

<h3 id="getswitch_api_v1_switches__id__get-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|

> Example responses

> 200 Response

```json
{
  "id": "string",
  "ip": "0.0.0.0",
  "gpsLat": 0,
  "gpsLong": 0
}
```

<h3 id="getswitch_api_v1_switches__id__get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[Switch](#schemaswitch)|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## upsertSwitch_api_v1_switches_upsert_post

<a id="opIdupsertSwitch_api_v1_switches_upsert_post"></a>

`POST /api/v1/switches/upsert`

*Upsertswitch*

upsert or udpate one || multiple switch(s)

> Body parameter

```json
{
  "id": "string",
  "ip": "string",
  "gpsLat": 0,
  "gpsLong": 0
}
```

<h3 id="upsertswitch_api_v1_switches_upsert_post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|any|true|none|

> Example responses

> 200 Response

```json
{
  "items": [],
  "errors": []
}
```

<h3 id="upsertswitch_api_v1_switches_upsert_post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[switchmanagerapi__models__factories__batcheableOutputFactory___locals___BatcheableOutputModel__3](#schemaswitchmanagerapi__models__factories__batcheableoutputfactory___locals___batcheableoutputmodel__3)|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## deleteSwitch_api_v1_switches_delete__id__delete

<a id="opIddeleteSwitch_api_v1_switches_delete__id__delete"></a>

`DELETE /api/v1/switches/delete/{id}`

*Deleteswitch*

delete a switch

<h3 id="deleteswitch_api_v1_switches_delete__id__delete-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|

> Example responses

> 200 Response

```json
"string"
```

<h3 id="deleteswitch_api_v1_switches_delete__id__delete-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|string|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

# Schemas

<h2 id="tocS_BatchError">BatchError</h2>
<!-- backwards compatibility -->
<a id="schemabatcherror"></a>
<a id="schema_BatchError"></a>
<a id="tocSbatcherror"></a>
<a id="tocsbatcherror"></a>

```json
{
  "id": "",
  "error": ""
}

```

BatchError

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|string|false|none|none|
|error|string|false|none|none|

<h2 id="tocS_ConnectionOutput">ConnectionOutput</h2>
<!-- backwards compatibility -->
<a id="schemaconnectionoutput"></a>
<a id="schema_ConnectionOutput"></a>
<a id="tocSconnectionoutput"></a>
<a id="tocsconnectionoutput"></a>

```json
{
  "id": "string",
  "ppp": "string",
  "port": 0,
  "toggled": false,
  "toggleDate": "2019-08-24T14:15:22Z",
  "type": "copper|fiber",
  "isUp": false,
  "proto": "snmp",
  "speed": 0,
  "switch": {
    "id": "string",
    "ip": "0.0.0.0",
    "gpsLat": 0,
    "gpsLong": 0
  },
  "customer": {
    "id": "string",
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
|id|string|true|none|connection id|
|ppp|string|true|none|connection name|
|port|integer|false|none|port number on the switch|
|toggled|boolean|false|none|define if the port is opened|
|toggleDate|any|false|none|date at which the port should open / close based on currrent port status|

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
|type|string|false|none|physical connection type|
|isUp|boolean|false|none|none|
|proto|string|false|none|none|
|speed|integer|false|none|none|
|switch|[Switch](#schemaswitch)|false|none|Switch Database model|
|customer|[Customer](#schemacustomer)|false|none|Customer Database model|

<h2 id="tocS_ConnectionUpsertInput">ConnectionUpsertInput</h2>
<!-- backwards compatibility -->
<a id="schemaconnectionupsertinput"></a>
<a id="schema_ConnectionUpsertInput"></a>
<a id="tocSconnectionupsertinput"></a>
<a id="tocsconnectionupsertinput"></a>

```json
{
  "id": "string",
  "name": "string",
  "port": 0,
  "toggled": true,
  "toggleDate": "2019-08-24T14:15:22Z",
  "type": "string",
  "isUp": true,
  "proto": "string",
  "speed": 0,
  "switchId": 0,
  "customerId": 0
}

```

ConnectionUpsertInput

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|name|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|port|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|integer|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|toggled|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|boolean|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
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
|type|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|isUp|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|boolean|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|proto|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|speed|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|integer|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|switchId|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|integer|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|customerId|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|integer|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

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
  "id": "string",
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
|id|string|true|none|customer id / worker id|
|firstname|string|true|none|none|
|lastname|string|true|none|none|
|type|string|true|none|customer type (company name || person status)|
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

<h2 id="tocS_ListSortEnum">ListSortEnum</h2>
<!-- backwards compatibility -->
<a id="schemalistsortenum"></a>
<a id="schema_ListSortEnum"></a>
<a id="tocSlistsortenum"></a>
<a id="tocslistsortenum"></a>

```json
"con"

```

ListSortEnum

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|ListSortEnum|string|false|none|none|

#### Enumerated Values

|Property|Value|
|---|---|
|ListSortEnum|con|
|ListSortEnum|name|
|ListSortEnum|cid|
|ListSortEnum|address|
|ListSortEnum|switch|

<h2 id="tocS_OrderBy">OrderBy</h2>
<!-- backwards compatibility -->
<a id="schemaorderby"></a>
<a id="schema_OrderBy"></a>
<a id="tocSorderby"></a>
<a id="tocsorderby"></a>

```json
"asc"

```

OrderBy

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|OrderBy|string|false|none|to order results in a paginated request|

#### Enumerated Values

|Property|Value|
|---|---|
|OrderBy|asc|
|OrderBy|desc|

<h2 id="tocS_Switch">Switch</h2>
<!-- backwards compatibility -->
<a id="schemaswitch"></a>
<a id="schema_Switch"></a>
<a id="tocSswitch"></a>
<a id="tocsswitch"></a>

```json
{
  "id": "string",
  "ip": "0.0.0.0",
  "gpsLat": 0,
  "gpsLong": 0
}

```

Switch

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|string|true|none|switch unique name / id|
|ip|string|false|none|switch ip address|
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

<h2 id="tocS_UpserCustomerInput">UpserCustomerInput</h2>
<!-- backwards compatibility -->
<a id="schemaupsercustomerinput"></a>
<a id="schema_UpserCustomerInput"></a>
<a id="tocSupsercustomerinput"></a>
<a id="tocsupsercustomerinput"></a>

```json
{
  "id": "string",
  "firstname": "string",
  "lastname": "string",
  "type": "string",
  "address": "string"
}

```

UpserCustomerInput

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|firstname|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|lastname|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|type|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|address|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

<h2 id="tocS_UpsertSwitchInput">UpsertSwitchInput</h2>
<!-- backwards compatibility -->
<a id="schemaupsertswitchinput"></a>
<a id="schema_UpsertSwitchInput"></a>
<a id="tocSupsertswitchinput"></a>
<a id="tocsupsertswitchinput"></a>

```json
{
  "id": "string",
  "ip": "string",
  "gpsLat": 0,
  "gpsLong": 0
}

```

UpsertSwitchInput

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|ip|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
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

<h2 id="tocS_switchmanagerapi__models__factories__batcheableOutputFactory___locals___BatcheableOutputModel__1">switchmanagerapi__models__factories__batcheableOutputFactory___locals___BatcheableOutputModel__1</h2>
<!-- backwards compatibility -->
<a id="schemaswitchmanagerapi__models__factories__batcheableoutputfactory___locals___batcheableoutputmodel__1"></a>
<a id="schema_switchmanagerapi__models__factories__batcheableOutputFactory___locals___BatcheableOutputModel__1"></a>
<a id="tocSswitchmanagerapi__models__factories__batcheableoutputfactory___locals___batcheableoutputmodel__1"></a>
<a id="tocsswitchmanagerapi__models__factories__batcheableoutputfactory___locals___batcheableoutputmodel__1"></a>

```json
{
  "items": [],
  "errors": []
}

```

BatcheableOutputModel

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|items|[[ConnectionOutput](#schemaconnectionoutput)]|false|none|[Connection model API output]|
|errors|[[BatchError](#schemabatcherror)]|false|none|[Batch error model]|

<h2 id="tocS_switchmanagerapi__models__factories__batcheableOutputFactory___locals___BatcheableOutputModel__2">switchmanagerapi__models__factories__batcheableOutputFactory___locals___BatcheableOutputModel__2</h2>
<!-- backwards compatibility -->
<a id="schemaswitchmanagerapi__models__factories__batcheableoutputfactory___locals___batcheableoutputmodel__2"></a>
<a id="schema_switchmanagerapi__models__factories__batcheableOutputFactory___locals___BatcheableOutputModel__2"></a>
<a id="tocSswitchmanagerapi__models__factories__batcheableoutputfactory___locals___batcheableoutputmodel__2"></a>
<a id="tocsswitchmanagerapi__models__factories__batcheableoutputfactory___locals___batcheableoutputmodel__2"></a>

```json
{
  "items": [],
  "errors": []
}

```

BatcheableOutputModel

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|items|[[Customer](#schemacustomer)]|false|none|[Customer Database model]|
|errors|[[BatchError](#schemabatcherror)]|false|none|[Batch error model]|

<h2 id="tocS_switchmanagerapi__models__factories__batcheableOutputFactory___locals___BatcheableOutputModel__3">switchmanagerapi__models__factories__batcheableOutputFactory___locals___BatcheableOutputModel__3</h2>
<!-- backwards compatibility -->
<a id="schemaswitchmanagerapi__models__factories__batcheableoutputfactory___locals___batcheableoutputmodel__3"></a>
<a id="schema_switchmanagerapi__models__factories__batcheableOutputFactory___locals___BatcheableOutputModel__3"></a>
<a id="tocSswitchmanagerapi__models__factories__batcheableoutputfactory___locals___batcheableoutputmodel__3"></a>
<a id="tocsswitchmanagerapi__models__factories__batcheableoutputfactory___locals___batcheableoutputmodel__3"></a>

```json
{
  "items": [],
  "errors": []
}

```

BatcheableOutputModel

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|items|[[Switch](#schemaswitch)]|false|none|[Switch Database model]|
|errors|[[BatchError](#schemabatcherror)]|false|none|[Batch error model]|

