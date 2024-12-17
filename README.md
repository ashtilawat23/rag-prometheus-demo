# RAG Prometheus Demo

A complete monitoring solution for Retrieval-Augmented Generation (RAG) pipelines using Prometheus and Grafana.

## Project Structure
```
rag-prometheus-demo/
├── main.py            # Main monitoring code
├── requirements.txt   # Python dependencies
├── prometheus/          
│   └── prometheus.yml # Prometheus configuration
└── README.md
```

## Prerequisites

- Python 3.8+
- Prometheus
- Grafana
- pip (Python package manager)

## Step-by-Step Setup

### 1. Set Up Python Environment

```bash
# Create and enter project directory
mkdir rag-prometheus-demo
cd rag-prometheus-demo

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Monitoring Code

Create `main.py` with the provided monitoring code that sets up:
- Query processing metrics
- Retrieval phase metrics
- Generation phase metrics
- Vector store monitoring
- Cache performance tracking

### 3. Set Up Prometheus

```bash
# On macOS
brew install prometheus

# Create Prometheus config directory
mkdir prometheus
```

Create `prometheus/prometheus.yml`:
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

# Scrape configurations
scrape_configs:
  - job_name: 'rag_pipeline'
    static_configs:
      - targets: ['localhost:8000']
```

### 4. Install and Configure Grafana

```bash
# On macOS
brew install grafana

# On Ubuntu
sudo apt-get install -y adduser libfontconfig1
wget https://dl.grafana.com/oss/release/grafana_10.2.0_amd64.deb
sudo dpkg -i grafana_10.2.0_amd64.deb
```

### 5. Start All Services

Open three terminal windows:

```bash
# Terminal 1: Start RAG monitoring
python main.py

# Terminal 2: Start Prometheus
prometheus --config.file=prometheus/prometheus.yml

# Terminal 3: Start Grafana
# On macOS
brew services start grafana
# On Ubuntu
sudo systemctl start grafana-server
```

### 6. Configure Grafana

1. Access Grafana UI:
   - Open `http://localhost:3000`
   - Login with admin/admin
   - Change password when prompted

2. Add Prometheus data source:
   - Go to Settings → Data Sources
   - Add Prometheus
   - URL: `http://localhost:9090`
   - Click "Save & Test"

3. Import the dashboard:
   - Click + icon → Import
   - Paste the provided dashboard JSON
   - Select Prometheus data source
   - Click Import

### 7. View Your Metrics

- RAG Metrics: `http://localhost:8000/metrics`
- Prometheus UI: `http://localhost:9090`
- Grafana Dashboard: `http://localhost:3000`

### 8. Stopping Services

```bash
# Stop Grafana
brew services stop grafana  # macOS
sudo systemctl stop grafana-server  # Ubuntu

# Stop Prometheus and RAG monitoring with Ctrl+C in their respective terminals
```

## Available Metrics

### Query Processing
- `rag_queries_total`: Total processed queries
- `rag_query_duration_seconds`: Query processing time

### Retrieval Phase
- `rag_documents_retrieved`: Documents per query
- `rag_retrieval_duration_seconds`: Retrieval time

### Generation Phase
- `rag_generation_duration_seconds`: Generation time
- `rag_generated_tokens`: Generated token counts

### Vector Store
- `rag_vector_store_documents`: Total documents
- `rag_embedding_queue_size`: Embedding queue size

## Testing

Test your setup with these Prometheus queries:
```
# Basic query count
rag_queries_total

# Query rate
rate(rag_queries_total[5m])

# Average duration
rate(rag_query_duration_seconds_sum[5m]) / rate(rag_query_duration_seconds_count[5m])
```

## Troubleshooting

1. If metrics aren't showing:
   - Check if RAG app is running (`localhost:8000/metrics`)
   - Verify Prometheus config (`localhost:9090/targets`)
   - Check Grafana data source connection

2. Common issues:
   - Port conflicts: Ensure ports 8000, 9090, and 3000 are available
   - Prometheus config syntax: Validate YAML format
   - Python environment: Verify all dependencies are installed

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.