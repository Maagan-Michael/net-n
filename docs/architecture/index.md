## main architecture

```plantuml
@startuml
!include <C4/C4_Container.puml>
!theme C4_united from <C4/themes>
HIDE_STEREOTYPE()

!define DEVICONS https://raw.githubusercontent.com/tupadr3/plantuml-icon-font-sprites/master/devicons
!define DEVICONS2 https://raw.githubusercontent.com/tupadr3/plantuml-icon-font-sprites/master/devicons2
!define FONTAWESOME https://raw.githubusercontent.com/tupadr3/plantuml-icon-font-sprites/master/font-awesome-5

!include DEVICONS/python.puml
!include DEVICONS/react.puml
!include DEVICONS2/oracle_original.puml
!include DEVICONS2/postgresql.puml
!include FONTAWESOME/users.puml
!include FONTAWESOME/sync_alt.puml
!include FONTAWESOME/user_circle.puml
!include FONTAWESOME/ethernet.puml
!include FONTAWESOME/network_wired.puml

title Multilayer Network Management Architecture

ContainerDb(db, "Database", "Oracle DB", "Holds residency correlation records", $sprite="oracle_original")
Person(user, "User", "Directly interacting with the system", $sprite="users")

Boundary(c1, "Input layer") {
  Container(syncmodule, "Sync Module", "python", "A worker to process DB changes, Requires DB access", $sprite="sync_alt")
  Container(ui, "UI", "react", "User interface component", $sprite="user_circle")
}

Boundary(c2, "Logic layer", "Main layer") {
  Container(backend, "Backend", "python", "The main interface that the customer interacts with", $sprite="python")
  ContainerDb(internaldb,"Internal Database", "pgsql","Stores relations, system components, state and access credentials",$sprite="postgresql")
}

Boundary(c3, "Controller layer", "IMC/Mgmt VLAN Access") {
  Container(imc, "IMC", "HPE Proprietary", "Adapter interface to control HPE IMC using API, Requires IMC access", $sprite="network_wired")
  Container(snmp, "SNMP Controller", "python", "Used for legacy units w/o central mgmt, Requires mgmt VLAN access", $sprite="ethernet")
}

Lay_L(user,ui)
Rel_R(user, ui, "Rest API", "http")
Lay_R(syncmodule,db)
Rel_R(syncmodule, db, "Read View", "SQL")
Rel(ui, backend, "Rest API", "http")
Rel(syncmodule, backend, "Trigger", "http")
Rel(backend,snmp,"Rest API", "http")
Rel(backend,imc,"Rest API","http")
Rel_R(backend,internaldb,"Store Status", "SQL")
Rel(syncmodule,internaldb,"Update","SQL")
@enduml
```
