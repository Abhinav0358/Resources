import React, { useState, useEffect, useRef } from "react";

const App = () => {
  const [cameras, setCameras] = useState([]);
  const [events, setEvents] = useState([]);
  const [wsStatus, setWsStatus] = useState("Disconnected");
  const ws = useRef(null);

  // 1. Initial Data Fetch (Postgres & Mongo) via Nginx Load Balancer
  useEffect(() => {
    // Fetch Cameras from Postgres (via Nginx on port 8080)
    fetch("http://localhost:8080/cameras")
      .then((res) => res.json())
      .then((data) => setCameras(data))
      .catch((err) => console.error("Cameras API error:", err));

    // Fetch Recent Events from MongoDB (via Nginx on port 8080)
    fetch("http://localhost:8080/events")
      .then((res) => res.json())
      .then((data) => setEvents(data))
      .catch((err) => console.error("Events API error:", err));
  }, []);

  // 2. Real-time WebSocket connection (via Nginx Load Balancer)
  useEffect(() => {
    // Pointing to Nginx port 8080 which handles WebSocket upgrade
    ws.current = new WebSocket("ws://localhost:8080/ws/events");

    ws.current.onopen = () => setWsStatus("Connected");
    ws.current.onclose = () => setWsStatus("Disconnected");

    ws.current.onmessage = (e) => {
      const newEvent = JSON.parse(e.data);
      // Prepend new event to the list
      setEvents((prev) => [newEvent, ...prev.slice(0, 19)]);
    };

    return () => ws.current.close();
  }, []);

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1>Pro Vision Dashboard</h1>
        <div style={styles.status}>
          Cluster Status:{" "}
          <span
            style={{ color: wsStatus === "Connected" ? "#4caf50" : "#f44336" }}
          >
            {wsStatus}
          </span>
        </div>
      </header>

      <main style={styles.main}>
        {/* Left Section: Camera List (Postgres Data) */}
        <section style={styles.section}>
          <h2>Managed Cameras (PostgreSQL)</h2>
          <div style={styles.grid}>
            {cameras.map((cam) => (
              <div key={cam.id} style={styles.card}>
                <h3>{cam.name}</h3>
                <p>Location: {cam.location}</p>
                <code>{cam.stream_url}</code>
              </div>
            ))}
            {cameras.length === 0 && <p>No cameras registered.</p>}
          </div>
        </section>

        {/* Right Section: Real-time Feed (Mongo + Redis + WebSocket Data) */}
        <section style={styles.section}>
          <h2>Live Detection Feed (MongoDB + Redis)</h2>
          <div style={styles.feed}>
            {events.map((ev, idx) => (
              <div key={ev._id || idx} style={styles.eventRow}>
                <strong>{ev.label.toUpperCase()}</strong> detected by Camera{" "}
                {ev.camera_id}
                <br />
                <small>
                  {new Date(ev.timestamp).toLocaleTimeString()} - Confidence:{" "}
                  {ev.confidence}
                </small>
              </div>
            ))}
            {events.length === 0 && <p>Waiting for events from worker...</p>}
          </div>
        </section>
      </main>
    </div>
  );
};

const styles = {
  container: {
    padding: "20px",
    backgroundColor: "#121212",
    color: "#e0e0e0",
    minHeight: "100vh",
    fontFamily: "Segoe UI, Tahoma, Geneva, Verdana, sans-serif",
  },
  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    borderBottom: "2px solid #333",
    marginBottom: "20px",
    paddingBottom: "10px",
  },
  main: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: "30px" },
  section: {
    backgroundColor: "#1e1e1e",
    padding: "25px",
    borderRadius: "15px",
    boxShadow: "0 4px 6px rgba(0,0,0,0.3)",
  },
  grid: { display: "grid", gap: "15px" },
  card: {
    padding: "15px",
    backgroundColor: "#2d2d2d",
    borderRadius: "10px",
    borderLeft: "4px solid #2196f3",
  },
  feed: { height: "600px", overflowY: "auto", paddingRight: "10px" },
  eventRow: {
    padding: "12px",
    borderBottom: "1px solid #333",
    marginBottom: "8px",
    backgroundColor: "#252525",
    borderRadius: "5px",
  },
  status: { fontSize: "1.1rem", fontWeight: "600" },
};

export default App;
