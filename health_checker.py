import time
import threading
from concurrent.futures import ThreadPoolExecutor
from utils import load_data
from domain_stats import DomainStatistics
from logger import logger
from urllib.parse import urlparse
import requests
import sys


class HealthChecker:
    """
    A class to check the health of different domains by going through a list of endpoints by 
    checking their availability status based on HTTP response code and latency. 
    Health checks are performed concurrently using a thread pool, 
    and results are logged to console periodically (every 15s).
    """

    def __init__(self, input_file):
        """
        Initializes the HealthChecker object by loading the input data from input yaml file,
        setting up necessary variables, and creating a thread pool for concurrent task execution.

        Args:
            input_file (str): Path to the input file (YAML) containing endpoint information.
        """

        self.input_data = load_data(input_file)
        self.domains_stats = {}
        self.lock = threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=10)

    def get_domain(self, url):
        """
        Extracts the domain from the given URL.

        Args:
            url (str): The URL to extract the domain from.

        Returns:
            str: The domain part of the URL.
        """

        parsed_url = urlparse(url)
        return parsed_url.netloc

    def check_url_status(self, url, headers):
        """
        Checks the status of the given URL by sending an HTTP request. 
        A URL is considered "UP" if the HTTP status code is between 200-299
        and the latency is less than 500 ms.

        Args:
            url (str): The URL to check.
            headers (dict): HTTP headers to send with the request.

        Returns:
            bool: True if the URL is "UP", False otherwise.
        """

        try:
            response = requests.get(url, headers=headers, timeout=1)
            latency = response.elapsed.total_seconds() * 1000
            return 200 <= response.status_code < 300 and latency < 500
        except requests.RequestException as e:
            logger.error(f"Error checking {url}: {e}")
            return False

    def process_url(self, url, headers):
        """
        Processes a URL by checking its status and updating domain statistics.

        Args:
            url (str): The URL to process.
            headers (dict): HTTP headers to send with the request.
        """

        domain = self.get_domain(url)
        is_up = self.check_url_status(url, headers)
        with self.lock:
            if domain not in self.domains_stats:
                self.domains_stats[domain] = DomainStatistics()
            self.domains_stats[domain].update(is_up)

    def check_endpoints(self):
        """
        Iterates through all endpoints from the input data and submits the task 
        of checking each URL's status to the thread pool for concurrent execution.
        """

        futures = []
        for endpoint in self.input_data:
            url = endpoint.get('url')
            headers = endpoint.get('headers', {})
            futures.append(self.executor.submit(
                self.process_url, url, headers))
        for future in futures:
            try:
                future.result()
            except Exception as e:
                logger.error(f"Error processing future: {e}")

    def log_availability(self):
        """
        Logs the availability percentage (hit ratio) of each domain based on the 
        health check results gathered so far.
        """

        for domain, stats in self.domains_stats.items():
            hit_ratio = stats.get_hit_ratio()
            logger.info(
                f"{domain} has {hit_ratio:.2f}% availability percentage.")

    def start(self):
        """
        Starts the health checker, continuously checking the endpoints and logging 
        the availability every 15 seconds. This loop continues until manually interrupted.
        """

        try:
            while True:
                self.check_endpoints()
                self.log_availability()
                time.sleep(15)
        except KeyboardInterrupt:
            logger.info("Health check process stopped manually.")


if __name__ == "__main__":

    # Ensure correct usage by checking if the input file (YAML) is provided
    if len(sys.argv) != 2:
        logger.error("Usage: python health_checker.py <config.yaml>")
        sys.exit(1)

    # Get the input YAML file from the command-line arguments
    yaml_file = sys.argv[1]

    # Create a HealthChecker instance and start the health checking process
    checker = HealthChecker(yaml_file)
    checker.start()
