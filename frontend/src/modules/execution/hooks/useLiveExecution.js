import { useMemo, useRef, useState } from "react";
import { executionService } from "../services/executionService.js";

export function useLiveExecution() {
  const socketRef = useRef(null);
  const [events, setEvents] = useState([]);
  const [finalResponse, setFinalResponse] = useState(null);
  const [rawState, setRawState] = useState(null);
  const [connected, setConnected] = useState(false);
  const [error, setError] = useState("");

  const nodeStatuses = useMemo(() => {
    return events.reduce((acc, event) => {
      acc[event.node] = event.status;
      return acc;
    }, {});
  }, [events]);

  function start(request, simulation = false) {
    socketRef.current?.close();
    setEvents([]);
    setFinalResponse(null);
    setRawState(null);
    setError("");
    const socket = new WebSocket(executionService.liveSocketUrl());
    socketRef.current = socket;
    socket.onopen = () => {
      setConnected(true);
      socket.send(JSON.stringify({ request, simulation }));
    };
    socket.onmessage = (message) => {
      const payload = JSON.parse(message.data);
      if (payload.type === "node_event") {
        setEvents((current) => [...current, payload.event]);
      }
      if (payload.type === "final") {
        setFinalResponse(payload.response);
        setRawState(payload.state);
        setConnected(false);
        socket.close();
      }
    };
    socket.onerror = () => {
      setError("Live execution connection failed");
      setConnected(false);
    };
    socket.onclose = () => setConnected(false);
  }

  return {
    events,
    finalResponse,
    rawState,
    connected,
    error,
    nodeStatuses,
    start
  };
}
