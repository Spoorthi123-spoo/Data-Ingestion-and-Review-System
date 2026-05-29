import { useState } from "react";
import API from "../api/api";
import { useNavigate } from "react-router-dom";

function Login() {

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleLogin = () => {

    // VALIDATION
    if (!username.trim() || !password.trim()) {
      setError("Username and Password are required");
      return;
    }

    setLoading(true);
    setError("");

    API.post("token/", {
      username: username.trim(),
      password: password.trim(),
    })
      .then((res) => {

        // Save tokens
        localStorage.setItem("access", res.data.access);
        localStorage.setItem("refresh", res.data.refresh);

        setLoading(false);

        alert("✅ Login Successful");

        // 🔥 IMPORTANT FIX: notify App.js immediately
        window.dispatchEvent(new Event("storage"));

        // redirect to dashboard
        navigate("/", { replace: true });

      })
      .catch((err) => {

        console.log("LOGIN ERROR:", err);

        setError("Invalid username or password OR server error");

        setLoading(false);
      });
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>

        <h2 style={{ marginBottom: "10px" }}>🌱 ESG Login</h2>

        <p style={{ marginBottom: "20px", color: "#666" }}>
          Sign in to access dashboard
        </p>

        <input
          style={styles.input}
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <input
          style={styles.input}
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        {error && <p style={styles.error}>{error}</p>}

        <button
          onClick={handleLogin}
          disabled={loading}
          style={{
            ...styles.button,
            opacity: loading ? 0.6 : 1,
            cursor: loading ? "not-allowed" : "pointer"
          }}
        >
          {loading ? "Logging in..." : "Login"}
        </button>

      </div>
    </div>
  );
}

const styles = {
  container: {
    height: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "linear-gradient(135deg, #4facfe, #00f2fe)",
  },

  card: {
    width: "320px",
    padding: "30px",
    borderRadius: "20px",
    background: "rgba(255,255,255,0.2)",
    backdropFilter: "blur(15px)",
    boxShadow: "0 8px 32px rgba(0,0,0,0.2)",
    textAlign: "center",
    color: "#000",
  },

  input: {
    width: "100%",
    padding: "10px",
    margin: "10px 0",
    borderRadius: "10px",
    border: "none",
    outline: "none",
  },

  button: {
    width: "100%",
    padding: "10px",
    marginTop: "10px",
    borderRadius: "10px",
    border: "none",
    background: "#00c6ff",
    color: "white",
    cursor: "pointer",
    fontWeight: "bold",
  },

  error: {
    color: "red",
    fontSize: "14px",
  },
};

export default Login;