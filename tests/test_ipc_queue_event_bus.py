import multiprocessing
import time
from multiprocessing.queues import Queue as MQueue

from sagittarius_engine.infrastructure.event_bus import IPCQueueEventBus


def test_single_process_ipc_queue_event_bus(ipc_bus_factory):
    """Test standard EventBus pub/sub in a single process without a broker"""
    import queue

    # Use standard queue for single process testing, type hinted correctly
    sub_q = queue.Queue()
    pub_q = queue.Queue()

    bus = ipc_bus_factory(subscriber_queue=sub_q, publish_queue=pub_q)  # type: ignore

    received = []

    def handler(data):
        received.append(data)

    bus.on("test.event", handler)
    bus.start()

    bus.emit("test.event", {"hello": "world"})

    # In single process test without a broker, we manually move the message
    msg = pub_q.get(timeout=1.0)
    sub_q.put(msg)

    # Wait for processing
    time.sleep(0.2)

    assert len(received) == 1
    assert received[0] == {"hello": "world"}


def test_ipc_broker_forwarding(ipc_broker_factory):
    """Test broker forwards messages to subscriber queues"""
    import queue

    pub_q = queue.Queue()
    sub_q1 = queue.Queue()
    sub_q2 = queue.Queue()

    broker = ipc_broker_factory(publish_queue=pub_q)  # type: ignore
    broker.add_subscriber(sub_q1)  # type: ignore
    broker.add_subscriber(sub_q2)  # type: ignore

    broker.start()

    pub_q.put(("test.event", "data"))

    msg1 = sub_q1.get(timeout=1.0)
    msg2 = sub_q2.get(timeout=1.0)

    assert msg1 == ("test.event", "data")
    assert msg2 == ("test.event", "data")


def child_process_worker(sub_q: MQueue, pub_q: MQueue, ready_event, done_event):
    bus = IPCQueueEventBus(subscriber_queue=sub_q, publish_queue=pub_q)

    received_in_child = []

    def handler(data):
        received_in_child.append(data)
        if len(received_in_child) == 2:
            # Tell parent we are done
            pub_q.put(("child.done", received_in_child))

    bus.on("parent.ping", handler)
    bus.start()

    ready_event.set()

    # Wait for the done signal from parent
    done_event.wait(timeout=5.0)

    bus.stop()


def test_ipc_broker_unpicklable_data(ipc_broker_factory, ipc_bus_factory, caplog):
    """Test broker and bus handle unpicklable data without crashing"""
    import logging
    import multiprocessing

    caplog.set_level(logging.ERROR)

    manager = multiprocessing.Manager()
    pub_q = manager.Queue()
    sub_q = manager.Queue()

    broker = ipc_broker_factory(publish_queue=pub_q)
    broker.add_subscriber(sub_q)
    broker.start()

    bus = ipc_bus_factory(subscriber_queue=sub_q, publish_queue=pub_q)

    # Emitting an unpicklable object (lambda function)
    def unpicklable_data(x):
        return x

    bus.emit("unpicklable.event", unpicklable_data)

    # Allow time for processing
    import time
    time.sleep(0.2)

    # Assert that an error was logged instead of a crash
    assert any("Failed to emit event 'unpicklable.event' to publish_queue" in record.message for record in caplog.records)

    manager.shutdown()


def test_inter_process_communication(ipc_broker_factory, ipc_bus_factory):
    """Test full cross-process communication with broker"""
    # Use multiprocessing manager for queues across processes
    manager = multiprocessing.Manager()
    pub_q = manager.Queue()
    parent_sub_q = manager.Queue()
    child_sub_q = manager.Queue()

    ready_event = manager.Event()
    done_event = manager.Event()

    # Setup Broker
    broker = ipc_broker_factory(publish_queue=pub_q)
    broker.add_subscriber(parent_sub_q)
    broker.add_subscriber(child_sub_q)
    broker.start()

    # Setup Parent Bus
    parent_bus = ipc_bus_factory(subscriber_queue=parent_sub_q, publish_queue=pub_q)

    child_responses = []

    def parent_handler(data):
        child_responses.append(data)

    parent_bus.on("child.done", parent_handler)
    parent_bus.start()

    # Start Child Process
    child_p = multiprocessing.Process(
        target=child_process_worker, args=(child_sub_q, pub_q, ready_event, done_event)
    )
    child_p.start()

    # Wait for child to be ready
    ready_event.wait(timeout=2.0)

    # Emit events from parent
    parent_bus.emit("parent.ping", "ping1")
    parent_bus.emit("parent.ping", "ping2")

    # Wait for child to process and respond
    time.sleep(1.0)

    assert len(child_responses) == 1
    assert child_responses[0] == ["ping1", "ping2"]

    # Cleanup
    done_event.set()
    child_p.join(timeout=2.0)
    manager.shutdown()
