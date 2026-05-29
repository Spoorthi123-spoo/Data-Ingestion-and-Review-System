import { useEffect, useState } from "react";
import API from "../api/api";

function Audit() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    API.get("audit/").then((res) => setLogs(res.data));
  }, []);

  return (
    <div>
      <h2>Audit Logs</h2>

      {logs.map((log) => (
        <div key={log.id}>
          {log.action} | {log.performed_by} | {log.timestamp}
        </div>
      ))}
    </div>
  );
}

export default Audit;