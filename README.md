# RAG Pipeline Monitoring

Monitor your Retrieval-Augmented Generation (RAG) pipeline using Prometheus metrics.

## Features

- Comprehensive metrics tracking for RAG pipelines
- Built-in Prometheus integration
- Ready-to-use metric collectors for:
  - Query processing statistics
  - Retrieval phase performance
  - Generation phase metrics
  - Vector store monitoring
  - Cache performance tracking

## Prerequisites

- Python 3.8+
- Prometheus server (for metrics collection)
- Grafana (optional, for visualization)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/ashtilawat23/rag-prometheus-demo.git
cd rag-prometheus-demo
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

1. Start the monitoring server:
```bash
python3 main.py
```

2. The metrics will be available at `http://localhost:8000/metrics`

3. Configure your Prometheus server to scrape these metrics by adding this to your `prometheus.yml`:
```yaml
scrape_configs:
  - job_name: 'rag_pipeline'
    static_configs:
      - targets: ['localhost:8000']
```

## Available Metrics

### Query Processing
- `rag_queries_total`: Total number of queries processed (labeled by status)
- `rag_query_duration_seconds`: Query processing time histogram

### Retrieval Phase
- `rag_documents_retrieved`: Number of documents retrieved per query
- `rag_retrieval_duration_seconds`: Time spent in retrieval phase

### Generation Phase
- `rag_generation_duration_seconds`: Time spent in generation phase
- `rag_generated_tokens`: Token count histogram for generated responses

### Vector Store
- `rag_vector_store_documents`: Total documents in vector store
- `rag_embedding_queue_size`: Current embedding queue size

### Cache
- `rag_cache_hits_total`: Number of cache hits
- `rag_cache_misses_total`: Number of cache misses

## Customization

You can extend the metrics by modifying the `RAGMetrics` class. Common customizations include:

- Adjusting histogram buckets for your latency distribution
- Adding new metrics for specific components
- Modifying labels for better categorization

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.