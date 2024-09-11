
# Music-Separation-as-a-Service (MSaaS)

## Overview
I developed the Music-Separation-as-a-Service (MSaaS) platform, a Kubernetes-based solution providing a REST API for automatic music separation. This service allows users to upload MP3 files, separate the different audio tracks (vocals, drums, bass, etc.), and retrieve them individually. The backend services are deployed on a Kubernetes cluster, leveraging Google Kubernetes Engine (GKE) for scalability and resilience.

## Architecture
The architecture is composed of several microservices, each deployed in its own container, and orchestrated by Kubernetes. Below is a breakdown of the key components:

### REST API Service
- **Purpose**: The REST API serves as the frontend interface, accepting API requests for music analysis and handling queries related to MP3 files.
- **Implementation**: I built the REST API using Flask, which queues tasks to worker nodes via Redis. The API is responsible for managing incoming requests and directing them to the appropriate workers for processing.

### Worker Nodes
- **Purpose**: Worker nodes perform the core task of separating audio tracks from uploaded MP3 files. This process involves heavy computation, as it utilizes waveform source separation techniques.
- **Implementation**: I utilized Facebook’s open-source Demucs software for waveform source separation. Each worker node listens for tasks in the Redis queue, processes the MP3 files, and stores the resulting tracks in MinIO, a cloud object storage solution.

### Redis
- **Purpose**: Redis is used as a message broker to queue and distribute tasks to the worker nodes.
- **Deployment**: I deployed Redis within the Kubernetes cluster to facilitate fast and reliable message queuing.

### MinIO Object Storage
- **Purpose**: MinIO serves as the storage backend for both the original MP3 files and the separated audio tracks.
- **Implementation**: I chose MinIO for its compatibility with the S3 API and its ease of integration with Kubernetes. The storage is divided into two buckets: one for incoming MP3 files (`queue`) and another for the separated tracks (`output`).

## Deployment Process

### Kubernetes Cluster Setup
I set up the Kubernetes cluster on Google Kubernetes Engine (GKE) to take advantage of Google Cloud's managed Kubernetes service. This ensured high availability, automatic scaling, and robust cluster management. I initially performed development and testing on a local Kubernetes setup using Docker, before migrating to GKE for production deployment.

### Containerization
Each service (REST API, Worker, Redis, MinIO) is containerized using Docker. I built Docker images for each service, pushed them to a container registry, and deployed them on Kubernetes. I utilized versioning for the container images to ensure that I could manage and roll back versions as needed during the development cycle.

### Redis and MinIO Setup
- **Redis**: I deployed Redis using a Kubernetes deployment script, ensuring that it is accessible to both the REST API and Worker services.
- **MinIO**: I configured MinIO with a dedicated namespace in the cluster and set up port forwarding for local development. During production, I ensured that MinIO was properly secured and accessible only within the cluster.

### Waveform Source Separation
The worker nodes use the Demucs waveform source separation library from Facebook to perform the actual separation of audio tracks. This is a resource-intensive process, and I configured Kubernetes to allocate sufficient memory and CPU resources to the worker pods to handle the workload.

## Port Forwarding for Local Development
To facilitate development, I used Kubernetes port forwarding to connect the Redis and MinIO services running in the Kubernetes cluster to my local development environment. This allowed me to develop and test the REST API and Worker services locally while still interacting with the full backend setup in the Kubernetes cluster.

Commands used:
```bash
kubectl port-forward --address 0.0.0.0 service/redis 6379:6379 &
kubectl port-forward --namespace minio-ns svc/myminio-proj 9000:9000 &
```

## Testing and Optimization
- **Sample Data**: I used the provided sample MP3 files to test the system. Initially, I ran tests with shorter audio samples to minimize resource usage and expedite the debugging process. After ensuring stability and correctness, I transitioned to full-length MP3 files for final testing.
- **Resource Management**: Given the high memory consumption of the Demucs software, I monitored the resource usage of the worker nodes closely. I adjusted Kubernetes resource limits and requests to optimize the performance of the worker pods without overcommitting cluster resources.
- **Logging**: I deployed a logging service using Redis to collect and monitor logs from the REST API and Worker services. This was crucial for identifying issues during development and deployment.

## Conclusion
The Music-Separation-as-a-Service platform successfully leverages Kubernetes to provide a scalable, reliable, and efficient service for separating audio tracks. By using Redis for task queuing, MinIO for object storage, and GKE for container orchestration, the system is well-suited to handle the computational demands of audio processing while maintaining high availability and scalability.

The project demonstrated my ability to design, develop, and deploy a complex microservices architecture on Kubernetes, as well as my proficiency in using cloud-native tools and technologies to solve real-world problems.

