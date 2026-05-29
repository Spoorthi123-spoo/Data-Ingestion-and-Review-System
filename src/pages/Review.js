import { useEffect, useState } from "react";
import API from "../api/api";

function Review() {
  const [records, setRecords] = useState([]);

  const loadData = () => {
    API.get("pending/").then((res) => setRecords(res.data));
  };

  useEffect(() => {
    loadData();
  }, []);

  const approve = (id) => {
    API.post(`approve/${id}/`).then(() => loadData());
  };

  const reject = (id) => {
    API.post(`reject/${id}/`).then(() => loadData());
  };

  return (
    <div>
      <h2>Review Panel</h2>

      {records.map((r) => (
        <div key={r.id} style={{ marginBottom: "10px" }}>
          <span>
            {r.category} | {r.activity_value} | CO₂: {r.emissions_kg_co2e}
          </span>

          <button onClick={() => approve(r.id)}>Approve</button>
          <button onClick={() => reject(r.id)}>Reject</button>
        </div>
      ))}
    </div>
  );
}

export default Review;