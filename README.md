# SynapseNet: Distributed Multi-Agent Orchestration Framework

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Deployment](https://img.shields.io/badge/Deployment-AWS_Fargate-orange.svg)
![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)

**SynapseNet** is an enterprise-grade framework designed to scale autonomous multi-agent systems (MAS) through distributed intelligence. By decoupling stateful orchestration from high-throughput event streaming, SynapseNet enables intelligent agents to collaborate seamlessly across heterogeneous cloud and edge environments.

This project bridges the gap between local LLM workflow orchestration and production-ready distributed systems, addressing the critical bottlenecks of multi-agent scalability, memory persistence, and cross-node coordination.

---

## 📖 Project Details & Objectives

As AI transitions from single-prompt interactions to complex, multi-agent reasoning, the bottleneck is no longer the intelligence of the model, but the orchestration of the system. SynapseNet was engineered to solve three specific enterprise challenges:

1. **The Scalability Wall:** Standard Python-based agent frameworks block synchronously. SynapseNet treats agents as independent microservices linked by a real-time data pipeline, allowing horizontal scaling across AWS compute clusters.
2. **Edge-to-Cloud Synchronization:** By utilizing gRPC and Kafka, the framework allows heavy orchestration to sit in the cloud while lightweight agent nodes execute tasks on edge devices (e.g., IoT, robotics, or remote logistics nodes), ensuring state consistency across the network.
3. **Continuous Contextual Memory:** Agents often suffer from "amnesia" between sessions. By integrating `pgvector`, the system maintains a persistent, searchable memory bank of past interactions, creating a continuous feedback loop that improves accuracy over time.

---

## 🗂️ Project Structure

The codebase is modularized to separate orchestration logic, inter-service communication, and cognitive storage.

```text
synapsenet/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions CI/CD pipeline for AWS ECS deployment
├── agents/
│   ├── __init__.py
│   ├── base.py                 # Abstract base class enforcing stateful agent contracts
│   ├── research.py             # Implementation: Financial Research & Data Synthesis Agent
│   └── triage.py               # Implementation: Healthcare Triage & Routing Agent
├── communication/
│   ├── __init__.py
│   ├── event_bus.py            # Async Kafka (Amazon MSK) producer/consumer wrappers
│   ├── synapse.proto           # gRPC Protocol Buffer definitions for node contracts
│   └── synapse_pb2_grpc.py     # Auto-generated gRPC Python stubs (DO NOT EDIT)
├── config/
│   └── settings.py             # Environment variable management (AWS keys, DB URIs)
├── memory/
│   ├── __init__.py
│   └── vector_store.py         # pgvector storage, embeddings generation, and RAG retrieval
├── models/
│   ├── __init__.py
│   └── state.py                # Strict Pydantic models defining the LangGraph state
├── orchestrator/
│   ├── __init__.py
│   └── graph.py                # LangGraph DAG compilation, workflow routing, and edges
├── docker-compose.yml          # Local infrastructure manifest (Zookeeper, Kafka, Postgres)
├── Dockerfile                  # Production-ready Docker container for AWS Fargate
├── main.py                     # CLI Entry point for orchestrator and agent nodes
├── README.md                   # Project documentation
└── requirements.txt            # Python dependencies

```

---

## 🚀 Enterprise Capabilities

* **Decentralized Agent Mesh:** Agents operate as independent, fault-tolerant microservices rather than monolithic processes.
* **Dual-Channel Communication:** * *Synchronous:* Native **gRPC** integration for low-latency, strongly-typed direct task execution.
* *Asynchronous:* **Apache Kafka** event bus for high-throughput, decoupled state broadcasting and publish/subscribe workflows.


* **Stateful DAG Orchestration:** Utilizes **LangGraph** to manage complex, non-linear agent reasoning loops with persistent context windows.
* **Vectorized Long-Term Memory:** Implements **pgvector** (PostgreSQL) for semantic retrieval (RAG), allowing agents to index and recall historical solutions.
* **Continuous Adaptive Learning:** Features an integrated Reinforcement Learning (RL) feedback loop via a "Critic Agent" that dynamically scores and refines system outputs.

---

## 🏗️ System Architecture

SynapseNet is built on a highly modular, three-tier architecture designed for horizontal scalability:

1. **Orchestration Layer:** Defines the Directed Acyclic Graph (DAG) logic, managing entry points, conditional routing, and global state persistence.
2. **Event & Transport Layer:** Facilitates cross-node intelligence sharing. Eliminates traditional REST overhead in favor of HTTP/2 (gRPC) and distributed logs (Kafka/MSK).
3. **Cognitive Storage Layer:** A secure, localized vector database ensuring proprietary agent experiences and sensitive data (e.g., PII, financial records) remain within the secure VPC boundary.

---

## 🛠️ Technology Stack

* **Core AI/Orchestration:** LangChain, LangGraph, OpenAI Models
* **Distributed Systems:** Apache Kafka (Confluent), gRPC, Protocol Buffers (Protobuf)
* **Data & Memory:** PostgreSQL, `pgvector`, Pydantic (Strict Typing)
* **Infrastructure & CI/CD:** Docker, Docker Compose, GitHub Actions, AWS (ECS Fargate, ALB, MSK, RDS)

---

## ⚙️ Local Setup & Development

### Prerequisites

* Python 3.10+
* Docker and Docker Compose
* AWS CLI (configured for your target deployment environment)
* Valid LLM API Key (e.g., OpenAI)

### 1. Repository Initialization

```bash
git clone [https://github.com/your-username/synapsenet.git](https://github.com/your-username/synapsenet.git)
cd synapsenet

```

### 2. Environment Configuration

Create a `.env` file in the root directory to store your secrets and connection strings safely:

```env
OPENAI_API_KEY=sk-your-api-key-here
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
POSTGRES_CONNECTION_STRING=postgresql://admin:password@localhost:5432/synapsenet

```

### 3. Provision Local Infrastructure

Start the local development environment, which includes Zookeeper, Kafka, and the `pgvector` enabled PostgreSQL database:

```bash
docker-compose up -d

```

### 4. Install Dependencies

It is recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

```

### 5. Compile Protocol Buffers

If you make changes to the gRPC contract (`communication/synapse.proto`), regenerate the Python interfaces:

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. communication/synapse.proto

```

---

## 🏃‍♂️ Usage Examples

SynapseNet nodes can be instantiated in different roles depending on their deployment target.

**Launch an Edge Agent Node:**
Start a standalone worker that listens for gRPC tasks.

```bash
python main.py --role agent --id "Triage_Node_1" --port 50051

```

**Trigger the Cloud Orchestrator:**
Initialize a multi-step workflow across the distributed mesh.

```bash
python main.py --role orchestrator --task "Analyze patient symptoms: severe chest pain, history of hypertension."

```

---

## ☁️ Cloud Deployment (AWS)

SynapseNet is optimized for serverless, containerized deployment on AWS.

* **CI/CD Pipeline:** The included GitHub Actions workflow (`.github/workflows/deploy.yml`) automatically lints, builds, and pushes the Docker image to **Amazon ECR**.
* **Compute:** Designed to run on **AWS ECS Fargate**, scaling automatically based on agent workload.
* **Networking:** Requires an Application Load Balancer (ALB) configured with HTTP/2 listener rules to correctly route gRPC traffic to the Fargate tasks.
* **Streaming & Storage:** Replaces local containers with **Amazon MSK** (Managed Kafka) and **Amazon RDS** (PostgreSQL).

---

## 🤝 Contributing

We encourage contributions from the community, especially regarding new agent implementations and optimization of the LangGraph state handlers. Please review `CONTRIBUTING.md` for our code of conduct and pull request guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

---
