import { useState } from "react";
import API from "../api/api";

function Upload() {
  const [file, setFile] = useState(null);
  const [source, setSource] = useState("SAP");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const uploadFile = () => {
    if (!file) {
      setMessage("⚠ Please select a file first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("source_type", source);

    setLoading(true);
    setMessage("");

    API.post("upload/", formData)
      .then((res) => {
        setMessage("✅ " + res.data.message + " | Rows: " + res.data.rows_inserted);
        setFile(null);
        setLoading(false);
      })
      .catch((err) => {
        console.log(err);
        setMessage("❌ Upload failed. Check backend.");
        setLoading(false);
      });
  };

  return (
    <div style={{ padding: "30px", fontFamily: "Arial" }}>
      <h2>📤 ESG Data Upload</h2>

      <div
        style={{
          border: "2px dashed #4facfe",
          borderRadius: "12px",
          padding: "30px",
          marginTop: "20px",
          textAlign: "center",
          background: "#f5f9ff"
        }}
      >
        <input
          type="file"
          accept=".csv"
          onChange={(e) => setFile(e.target.files[0])}
        />

        {file && (
          <p style={{ marginTop: "10px" }}>
            📄 Selected File: <b>{file.name}</b>
          </p>
        )}

        <div style={{ marginTop: "15px" }}>
          <label>Source Type: </label>
          <select
            value={source}
            onChange={(e) => setSource(e.target.value)}
            style={{ padding: "5px", marginLeft: "10px" }}
          >
            <option value="SAP">SAP</option>
            <option value="UTILITY">UTILITY</option>
            <option value="TRAVEL">TRAVEL</option>
          </select>
        </div>

        <button
          onClick={uploadFile}
          disabled={loading}
          style={{
            marginTop: "20px",
            padding: "10px 20px",
            background: loading ? "#ccc" : "#4facfe",
            color: "white",
            border: "none",
            borderRadius: "8px",
            cursor: "pointer"
          }}
        >
          {loading ? "Uploading..." : "Upload File"}
        </button>

        {message && (
          <p style={{ marginTop: "15px", fontWeight: "bold" }}>
            {message}
          </p>
        )}
      </div>
    </div>
  );
}

export default Upload;