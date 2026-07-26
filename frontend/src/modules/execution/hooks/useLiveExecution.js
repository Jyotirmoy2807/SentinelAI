import { useMemo, useRef, useState } from "react";
import { executionService } from "../services/executionService.js";
import { useUiStore } from "../../../store/uiStore.js";

export function useLiveExecution(isSimulation = false) {
  const socketRef = useRef(null);
  const storeKey = isSimulation ? "simulationState" : "liveState";
  const stateData = useUiStore((state) => state[storeKey]);
  const setExecutionState = useUiStore((state) => state.setExecutionState);
  const resetExecutionState = useUiStore((state) => state.resetExecutionState);

  const events = stateData?.events || [];
  const finalResponse = stateData?.finalResponse || null;
  const rawState = stateData?.rawState || null;

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
    setExecutionState(isSimulation, { events: [], finalResponse: null, rawState: null });
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
        setExecutionState(isSimulation, {
          events: [...(useUiStore.getState()[storeKey].events || []), payload.event]
        });
      }
      if (payload.type === "final") {
        setExecutionState(isSimulation, {
          finalResponse: payload.response,
          rawState: payload.state
        });
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

  function reset() {
    socketRef.current?.close();
    resetExecutionState(isSimulation);
    setConnected(false);
    setError("");
  }

  return {
    events,
    finalResponse,
    rawState,
    connected,
    error,
    nodeStatuses,
    start,
    reset
  };
}
