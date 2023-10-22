export interface CustomerOutput {
    id: string
    firstname: string
    lastname: string
    type: string
    address: string
}

export interface SwitchOuput {
    id: string
    ip: string
    name: string
    description?: string
    gpsLat?: number
    gpsLong?: number
}

export interface ConnectionOutput {
    id: string
    name: string
    toggled: boolean
    toggleDate?: string
    type: string
    customer: CustomerOutput
    switch: SwitchOuput
    port: number
    isUp: boolean
    adapter: string
    speed?: number
}

export interface ConnectionsOutput {
    connections: ConnectionOutput[]
    hasNext: boolean
    hasPrevious: boolean
}