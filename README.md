Proyecto Final – Despliegue Full Stack con Docker, AWS y Observabilidad

Este proyecto implementa una aplicación web utilizando Flask + Apache + MySQL, orquestada con Docker Compose, desplegada en una instancia AWS EC2, y monitorizada mediante Prometheus, Node Exporter y Grafana.

Incluye:

Infraestructura local con Docker

Despliegue en la nube

Sistema de observabilidad completo

Dashboards personalizados en Grafana

1. Arquitectura General del Proyecto
                 ┌──────────────────────────┐
                 │         Usuario          │
                 └─────────────┬────────────┘
                               │
                        HTTP / HTTPS
                               │
                 ┌─────────────▼────────────┐
                 │         Apache           │
                 └─────────────┬────────────┘
                               │ Reverse Proxy
                 ┌─────────────▼────────────┐
                 │         Flask            │
                 └─────────────┬────────────┘
                               │
                 ┌─────────────▼────────────┐
                 │         MySQL            │
                 └──────────────────────────┘

Monitorización en paralelo:
- Prometheus → Recolección de métricas
- Node Exporter → Métricas del sistema
- Grafana → Dashboards

2. Sección 1 – Despliegue con Docker en entorno local
Construcción de contenedores

Se implementaron tres servicios en docker-compose.yml:

apache

flask-app

mysql

Cada contenedor se construyó desde su propio Dockerfile y se verificó:

Acceso a MySQL desde Flask

Comunicación interna entre contenedores

Servido correcto de la aplicación web

Pruebas realizadas

Flask responde correctamente desde Apache.

Base de datos inicializada con las tablas esperadas.

Rutas HTTP funcionales.

3. Sección 2 – Despliegue en AWS EC2
1. Inicio de instancia EC2

AMI: Ubuntu Server 22.04

Tipo: t2.micro

Grupos de seguridad:

Puerto 22 (SSH)

Puerto 80 (HTTP)

Puerto 3000 (Grafana)

Puerto 9090 (Prometheus)

Puerto 9100 (Node Exporter)

Puerto 5000 (Flask)

2. Instalación de Docker y Docker Compose
sudo apt update
sudo apt install docker.io -y
sudo snap install docker
sudo apt install docker-compose -y

3. Clonado del repositorio
git clone https://github.com/velascopripra/ParcialFinalST.git
cd ParcialFinalST

4. Construcción de la aplicación
sudo docker compose up -d --build

5. Verificación

Abrir en navegador:

http://<IP_PUBLICA>  (la ip varía cada que inicio un laboratorio nuevo, por eso no la especifico)

4. Sección 3 – Monitoreo con Prometheus y Node Exporter
Instalación de Prometheus

Ruta de instalación:

/etc/prometheus
/usr/local/bin/prometheus
/usr/local/bin/promtool

Servicio en systemd

Archivo: /etc/systemd/system/prometheus.service

La instancia quedó accesible en:

http://<IP_PUBLICA>:9090

Instalación de Node Exporter

Node Exporter se instaló y ejecutó como servicio:

http://<IP_PUBLICA>:9100/metrics

Configuración de prometheus.yml
global:
  scrape_interval: 5s
scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']

Métricas documentadas
1. node_cpu_seconds_total

Indica tiempo de CPU en diferentes modos (user, system, idle).

Útil para detectar saturación del procesador.

2. node_memory_MemAvailable_bytes

Memoria física disponible real.

Permite detectar fugas de memoria o procesos descontrolados.

3. node_filesystem_avail_bytes

Espacio disponible en particiones.

Ayuda a prevenir fallos por falta de disco.

Configuración de alertas (rules.yml)
groups:
  - name: node-alerts
    rules:
      - alert: HighCPUUsage
        expr: (100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[2m])) * 100)) > 80
        for: 2m
        labels:
          severity: warning
        annotations:
          description: "CPU mayor al 80%"

5. Sección 4 – Visualización con Grafana
Instalación de Grafana
sudo apt-get install -y apt-transport-https software-properties-common wget
sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
sudo apt update
sudo apt install grafana -y
sudo systemctl enable grafana-server

Acceso:

http://<IP_PUBLICA>:3000

Agregar Prometheus como Data Source

Dashboards creados
1. Dashboard: Uso de CPU y memoria
Panel 1 – CPU (%)

Consulta utilizada:

100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[2m])) * 100)

Panel 2 – Memoria

Fórmula de memoria usada:

node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes * 100

2. Gauge – Espacio disponible en disco

Consulta:

node_filesystem_avail_bytes{mountpoint="/",fstype!="rootfs"}

Unidad: GB

Dashboard importado

Se importó un dashboard de la librería oficial:

ID: 1860  (Node Exporter Full)


Conclusión Técnica
¿Qué aprendí al integrar Docker, AWS y Prometheus?

Aprendí cómo desplegar una aplicación real usando contenedores Docker, crear un entorno replicable tanto local como en la nube y aplicar principios de observabilidad mediante Prometheus y Grafana. También entendí la importancia de separar servicios (web, backend, base de datos) y gestionarlos de forma independiente.

¿Qué fue lo más desafiante y cómo lo resolvería en un entorno real?

Lo más desafiante fue configurar la comunicación entre servicios y asegurar que funcionaran igual en local y en AWS. En un entorno real usaría:

Docker Compose para desarrollo

Kubernetes para producción

Pipelines CI/CD para automatizar despliegues

Infrastructure as Code (Terraform) para evitar errores manuales


¿Qué beneficio aporta la observabilidad en el ciclo DevOps?

La observabilidad permite:

Detectar problemas antes de que generen fallos

Medir el rendimiento del sistema

Responder rápidamente a incidentes

Optimizar recursos y costos

Entender el comportamiento real de la aplicación

Sin observabilidad, DevOps no puede garantizar confiabilidad ni escalabilidad.

-------------------------------------------------------------------------------
EVIDENCIAS:

Para el apartado de las evidencias, las subí en un drive, el link es el siguiente: https://drive.google.com/drive/folders/15oFe8_Vp_rYbns_27vFxrctu0FsIeD4v?usp=sharing
