## main architecture

```plantuml
@startuml
!define AzurePuml https://raw.githubusercontent.com/plantuml-stdlib/Azure-PlantUML/master/dist

!includeurl AzurePuml/AzureCommon.puml
!includeurl AzurePuml/AzureSimplified.puml
!includeurl AzurePuml/Databases/AzureSqlDatabase.puml
!includeurl AzurePuml/General/Azure.puml

' Kubernetes
'https://github.com/dcasati/kubernetes-PlantUML
!define KubernetesPuml https://raw.githubusercontent.com/dcasati/kubernetes-PlantUML/master/dist
!includeurl KubernetesPuml/kubernetes_Common.puml
!includeurl KubernetesPuml/kubernetes_Context.puml
!includeurl KubernetesPuml/kubernetes_Simplified.puml
!includeurl KubernetesPuml/OSS/KubernetesApi.puml
!includeurl KubernetesPuml/OSS/KubernetesIng.puml
!includeurl KubernetesPuml/OSS/KubernetesPod.puml

actor "User" as user
node "Network" as network

Cluster_Boundary(cluster, "Backend") {
    Namespace_Boundary(nsBackEnd, "Back End") {
        KubernetesPod(KubernetesBE4, "front-end", "")
        KubernetesPod(KubernetesBE1, "Api", "")
        KubernetesPod(KubernetesBE2, "DB Ingestion module", "")
        KubernetesPod(KubernetesBE3, "Adapter Module", "")
        AzureSqlDatabase(backendSQL, "BackendDB", "")
    }
}
AzureSqlDatabase(cloudSQL, "MMDB", "")

Rel(user, KubernetesBE4, "HTTPS")
Rel(user, KubernetesBE1, "HTTPS")
Rel(KubernetesBE4, KubernetesBE1, "HTTPS")

Rel(KubernetesBE2, cloudSQL, "HTTPS")
Rel(KubernetesBE2, backendSQL, "HTTPS")
Rel(KubernetesBE2, KubernetesBE1, "HTTPS")

Rel(KubernetesBE1, KubernetesBE3, "HTTPS")

Rel(KubernetesBE3, network, "SNMP")
Rel(KubernetesBE3, network, "HTTPS")
@enduml
```
