export interface CustomerOutput {
    id: string
    firstname: string
    lastname: string
    type: string
}

export interface SwitchOuput {
    id: string
    ip: string
    name: string
    description?: string
    gpsLat?: number
    gpsLong?: number
    restricted: boolean
}

export interface ConnectionOutput {
    id: string
    name: string
    toggled: boolean
    toggleDate?: Date
    type: string
    customer: CustomerOutput
    switch: SwitchOuput
    port: number
    isUp: boolean
    adapter: string
    speed?: number
    autoUpdate: boolean
    address: string
}

export interface ConnectionsOutput {
    connections: ConnectionOutput[]
    hasNext: boolean
    hasPrevious: boolean
}

export enum ConnectionsFilters {
    all = "all",
    customer = "customer",
    customerId = "customerId",
    address = "address",
    enabled = "enabled",
    disabled = "disabled",
    up = "up",
    down = "down",
    port = "port",
    switch = "switch",
}

export enum OrderBy {
    asc = "asc",
    desc = "desc",
}

export enum ListSortEnum {
    con = "con",
    name = "name",
    cid = "cid",
    address = "address",
    switch = "switch",
}

export interface ConnectionsListQueryInput {
    page?: number
    limit?: number
    search?: string
    sort: ListSortEnum
    order: OrderBy
    filter?: ConnectionsFilters
}

export interface CustomerInput {
    id: string
    firstname?: string
    lastname?: string
    type?: string
}

export interface SwitchInput {
    id: string
    ip?: string
    name?: string
    description?: string
    gpsLat?: number
    gpsLong?: number
    restricted?: boolean
}

export interface ConnectionInput {
    id: string
    name?: string
    toggled?: boolean
    toggleDate?: string
    type?: string
    customerId?: string
    switchId?: string
    port?: number
    isUp?: boolean
    adapter?: string
    speed?: number
    autoUpdate?: boolean
    address?: string
}

export interface BatchError {
    id: string
    error: string
}

export interface BatcheableOutput<T> {
    items: T[]
    errors: BatchError[]
}

export interface fullConnectionUpdateInput {
    sw?: SwitchInput;
    customer?: CustomerInput;
    con?: ConnectionInput;
}