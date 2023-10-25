# Net-N
### A simple micro ISP management solution

[![Repo stars](https://img.shields.io/github/stars/Maagan-Michael/net-n?style=social)](https://github.com/Maagan-Michael/net-n)

Designed to manage local area network with prominent tenants.
These are the input modes:
1. Auto ingestion mode - Designed to read from a view in Oracle DB and perform certain operations given that there's a relevant available budget for the desired operation.
2. Interactive mode - A full management UI for both tenants and network equipment in search-like interface to focus on what matters.

The control plane allows different operations using several types of network equipment control:
1. HPE IMC API - The HPE management software using their native API.
2. SNMP - A highly configurable SNMP plugin that will allow reading relevant information from the network equipment and controlling the relevant ports for connection/disconnection.

The following documents describe some of the inner mechanism of this system.

This system is designed to be fully modular allowing adding more modules for ingestion or control plane along with detaching options for some of the modules to make it more secure.
