import concurrent.futures
import anonsurf_handler
import reg
import send_to_channel
import start_and_admin
import stock

def hello_w():
    # Define the functions to be executed concurrently
    functions_to_run = [
        anonsurf_handler.start_anonsurf,
        start_and_admin,
        reg,
        stock,
        send_to_channel
    ]

    # Use ThreadPoolExecutor to run the functions concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit all functions to the executor and wait for them to complete
        futures = [executor.submit(func) for func in functions_to_run]
        for future in concurrent.futures.as_completed(futures):
            try:
                # Get the result of the function (if any)
                result = future.result()
                # You can process the result here if needed
            except Exception as e:
                # Handle exceptions from the functions
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    hello_w()
