// Java (conceptual):
// volatile boolean running = true;
// synchronized void publish() { data = 42; }
// Thread B synchronized read sees 42 after unlock/lock.
