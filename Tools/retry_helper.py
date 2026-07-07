import time
import sys

def execute_with_retry(func, *args, retries=3, initial_delay=1.0, backoff_factor=2.0, **kwargs):
    """
    Executes a callable function with exponential backoff retries.
    
    Args:
        func: Callable function to execute.
        *args: Variable positional arguments for func.
        retries: Total number of retry attempts.
        initial_delay: Starting delay duration in seconds.
        backoff_factor: Multiplier applied to delay after each failure.
        **kwargs: Variable keyword arguments for func.
        
    Returns:
        The successful result of the callable function.
    """
    delay = initial_delay
    last_exception = None
    
    for attempt in range(retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            last_exception = e
            if attempt < retries - 1:
                print(f"⚠️ EOC Warning: Attempt {attempt + 1} failed ({e}). Retrying in {delay:.2f}s...", file=sys.stderr)
                time.sleep(delay)
                delay *= backoff_factor
            else:
                print(f"❌ EOC Error: All {retries} execution attempts failed. Final error: {e}", file=sys.stderr)
                
    if last_exception:
        raise last_exception
