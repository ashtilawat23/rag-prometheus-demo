from prometheus_client import start_http_server, Counter, Histogram, Summary, Gauge
from contextlib import contextmanager
import time
import random

# Initialize Prometheus metrics
class RAGMetrics:
    def __init__(self):
        # Query processing metrics
        self.query_counter = Counter(
            'rag_queries_total',
            'Total number of queries processed',
            ['status']  # success/failure
        )
        
        self.query_latency = Histogram(
            'rag_query_duration_seconds',
            'Time spent processing queries',
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0]
        )
        
        # Retrieval metrics
        self.docs_retrieved = Histogram(
            'rag_documents_retrieved',
            'Number of documents retrieved per query',
            buckets=[1, 5, 10, 20, 50]
        )
        
        self.retrieval_latency = Histogram(
            'rag_retrieval_duration_seconds',
            'Time spent in retrieval phase',
            buckets=[0.05, 0.1, 0.25, 0.5, 1.0]
        )
        
        # Generation metrics
        self.generation_latency = Histogram(
            'rag_generation_duration_seconds',
            'Time spent in generation phase',
            buckets=[0.5, 1.0, 2.0, 5.0, 10.0]
        )
        
        self.token_count = Histogram(
            'rag_generated_tokens',
            'Number of tokens in generated responses',
            buckets=[50, 100, 200, 500, 1000]
        )
        
        # Vector store metrics
        self.vector_store_size = Gauge(
            'rag_vector_store_documents',
            'Total number of documents in vector store'
        )
        
        self.embedding_queue_size = Gauge(
            'rag_embedding_queue_size',
            'Number of documents waiting to be embedded'
        )
        
        # Cache metrics
        self.cache_hits = Counter(
            'rag_cache_hits_total',
            'Number of cache hits'
        )
        
        self.cache_misses = Counter(
            'rag_cache_misses_total',
            'Number of cache misses'
        )

class RAGPipeline:
    def __init__(self):
        self.metrics = RAGMetrics()
    
    @contextmanager
    def time_retrieval(self):
        start_time = time.time()
        yield
        duration = time.time() - start_time
        self.metrics.retrieval_latency.observe(duration)
    
    @contextmanager
    def time_generation(self):
        start_time = time.time()
        yield
        duration = time.time() - start_time
        self.metrics.generation_latency.observe(duration)
    
    def process_query(self, query: str) -> str:
        try:
            with self.metrics.query_latency.time():
                # Retrieval phase
                with self.time_retrieval():
                    num_docs = self._retrieve_documents(query)
                    self.metrics.docs_retrieved.observe(num_docs)
                
                # Generation phase
                with self.time_generation():
                    response = self._generate_response(query)
                    num_tokens = len(response.split())  # Simple approximation
                    self.metrics.token_count.observe(num_tokens)
                
                self.metrics.query_counter.labels(status='success').inc()
                return response
                
        except Exception as e:
            self.metrics.query_counter.labels(status='failure').inc()
            raise e
    
    def _retrieve_documents(self, query: str) -> int:
        # Simulate document retrieval
        time.sleep(random.uniform(0.1, 0.3))
        return random.randint(3, 15)
    
    def _generate_response(self, query: str) -> str:
        # Simulate response generation
        time.sleep(random.uniform(0.5, 2.0))
        return "This is a simulated response " * random.randint(5, 20)
    
    def update_vector_store_metrics(self):
        # Update vector store metrics periodically
        self.metrics.vector_store_size.set(random.randint(10000, 20000))
        self.metrics.embedding_queue_size.set(random.randint(0, 100))

# Example usage
if __name__ == '__main__':
    # Start Prometheus HTTP server
    start_http_server(8000)
    
    # Initialize RAG pipeline
    rag = RAGPipeline()
    
    # Simulate queries
    while True:
        rag.process_query("Sample query")
        rag.update_vector_store_metrics()
        time.sleep(random.uniform(1, 5))