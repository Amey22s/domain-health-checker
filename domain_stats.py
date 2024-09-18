class DomainStatistics:
    """
    A class to track the statistics of domain availability.
    It records the total number of requests and the number of successful requests,
    and calculates the hit ratio (availability percentage).
    """

    def __init__(self):
        """
        Initializes the DomainStatistics object with counters for total and 
        successful requests, both initially set to zero.
        """
        self.total_requests = 0
        self.successful_requests = 0

    def update(self, is_up):
        """
        Updates the statistics based on whether a request was successful or not.

        Args:
            is_up (bool): Indicates if the request was successful (True) or not (False).
        """
        self.total_requests += 1
        if is_up:
            self.successful_requests += 1

    def get_hit_ratio(self):
        """
        Calculates the hit ratio (availability percentage) based on the recorded statistics.

        Returns:
            float: The hit ratio as a percentage. Returns 0 if no requests have been made.
        """

        # This part helps us avoid divide by 0 error in the main calculation.
        if self.total_requests == 0:
            return 0

        # Calculate and return the hit ratio as a percentage
        return 100 * (self.successful_requests / self.total_requests)
