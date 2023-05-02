import threading


# Create an event object
event = threading.Event()

def do_something():
    print("Doing something...")
    # Set the event flag to True
    event.set()

def do_something_else():
    print("Waiting for event to be set...")
    # Wait for the event flag to be set
    event.wait()
    print("Event has been set!")

# Start two threads
t1 = threading.Thread(target=do_something)
t2 = threading.Thread(target=do_something_else)
t2.start()
t1.start()

t1.join()
t2.join()
