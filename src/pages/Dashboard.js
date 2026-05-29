import { useEffect, useState } from "react";
import API from "../api/api";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend
} from "recharts";

function Dashboard() {

  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {

    API.get("records/")
      .then((res) => {
        setData(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.log(err);
        setError("Failed to load dashboard data");
        setLoading(false);
      });

  }, []);

  // ---------------- LOADING ----------------
  if (loading) {
    return (
      <div style={styles.center}>
        ⏳ Loading ESG Dashboard...
      </div>
    );
  }

  // ---------------- ERROR ----------------
  if (error) {
    return (
      <div style={{ ...styles.center, color: "#ff4d4f" }}>
        ❌ {error}
      </div>
    );
  }

  // ---------------- CALCULATIONS ----------------
  const total = data.length;

  const pending = data.filter(
    (r) => r.review_status === "PENDING"
  ).length;

  const approved = data.filter(
    (r) => r.review_status === "APPROVED"
  ).length;

  const rejected = data.filter(
    (r) => r.review_status === "REJECTED"
  ).length;

  const suspicious = data.filter(
    (r) => r.suspicious === true
  ).length;

  const totalCO2 = data.reduce(
    (sum, r) => sum + (r.emissions_kg_co2e || 0),
    0
  );

  // ---------------- CHART DATA ----------------
  const chartData = [
    {
      name: "Pending",
      value: pending
    },
    {
      name: "Approved",
      value: approved
    },
    {
      name: "Rejected",
      value: rejected
    }
  ];

  const COLORS = [
    "#f6d365",
    "#43e97b",
    "#fa709a"
  ];

  // ---------------- LOGOUT ----------------
  const handleLogout = () => {
    localStorage.clear();
    window.location.href = "/login";
  };

  return (
    <div style={styles.container}>

      {/* HEADER */}
      <div style={styles.header}>

        <div>
          <h1 style={styles.title}>
            🌱 ESG Analytics Dashboard
          </h1>

          <p style={styles.subtitle}>
            Advanced Carbon Emission Monitoring System
          </p>
        </div>

        <button
          onClick={handleLogout}
          style={styles.logoutButton}
        >
          Logout
        </button>

      </div>

      {/* STATS CARDS */}
      <div style={styles.grid}>

        {[
          {
            title: "Total Records",
            value: total,
            color: "#4facfe"
          },

          {
            title: "Pending",
            value: pending,
            color: "#f6d365"
          },

          {
            title: "Approved",
            value: approved,
            color: "#43e97b"
          },

          {
            title: "Rejected",
            value: rejected,
            color: "#fa709a"
          },

          {
            title: "Suspicious",
            value: suspicious,
            color: "#a18cd1"
          },

          {
            title: "CO₂ Emissions",
            value: totalCO2.toFixed(2),
            color: "#30cfd0"
          }

        ].map((item, index) => (

          <div
            key={index}
            style={{
              ...styles.card,
              background: item.color
            }}
          >

            <h3 style={styles.cardTitle}>
              {item.title}
            </h3>

            <h1 style={styles.cardValue}>
              {item.value}
            </h1>

          </div>

        ))}

      </div>

      {/* CHARTS */}
      <div style={styles.chartContainer}>

        {/* BAR CHART */}
        <div style={styles.chartBox}>

          <h2 style={styles.chartTitle}>
            📊 Review Status Overview
          </h2>

          <ResponsiveContainer width="100%" height={350}>

            <BarChart
              data={chartData}
              margin={{
                top: 20,
                right: 20,
                left: 0,
                bottom: 5
              }}
            >

              <CartesianGrid
                strokeDasharray="3 3"
                stroke="#334155"
              />

              <XAxis
                dataKey="name"
                stroke="#ffffff"
              />

              <YAxis stroke="#ffffff" />

              <Tooltip />

              <Bar
                dataKey="value"
                fill="#4facfe"
                radius={[12, 12, 0, 0]}
              />

            </BarChart>

          </ResponsiveContainer>

        </div>

        {/* PIE CHART */}
        <div style={styles.chartBox}>

          <h2 style={styles.chartTitle}>
            🥧 Record Distribution
          </h2>

          <ResponsiveContainer width="100%" height={350}>

            <PieChart>

              <Pie
                data={chartData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={120}
                label
              >

                {chartData.map((entry, index) => (

                  <Cell
                    key={`cell-${index}`}
                    fill={COLORS[index % COLORS.length]}
                  />

                ))}

              </Pie>

              <Tooltip />

              <Legend />

            </PieChart>

          </ResponsiveContainer>

        </div>

      </div>

    </div>
  );
}

export default Dashboard;

// ---------------- STYLES ----------------
const styles = {

  container: {
    minHeight: "100vh",
    padding: "30px",
    background: "linear-gradient(135deg, #0f172a, #1e293b)",
    fontFamily: "Arial",
    color: "white"
  },

  center: {
    minHeight: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    fontSize: "22px",
    background: "#0f172a",
    color: "white"
  },

  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "30px",
    flexWrap: "wrap"
  },

  title: {
    fontSize: "34px",
    margin: 0,
    fontWeight: "bold"
  },

  subtitle: {
    color: "#cbd5e1",
    marginTop: "8px"
  },

  logoutButton: {
    padding: "10px 18px",
    border: "none",
    borderRadius: "10px",
    background: "#ef4444",
    color: "white",
    fontWeight: "bold",
    cursor: "pointer"
  },

  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
    gap: "20px"
  },

  card: {
    padding: "25px",
    borderRadius: "18px",
    color: "black",
    boxShadow: "0 10px 30px rgba(0,0,0,0.3)",
    transition: "0.3s"
  },

  cardTitle: {
    margin: 0,
    fontSize: "18px"
  },

  cardValue: {
    marginTop: "10px",
    fontSize: "32px"
  },

  chartContainer: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(450px, 1fr))",
    gap: "25px",
    marginTop: "40px"
  },

  chartBox: {
    background: "rgba(255,255,255,0.06)",
    padding: "25px",
    borderRadius: "18px",
    backdropFilter: "blur(10px)",
    boxShadow: "0 10px 30px rgba(0,0,0,0.3)"
  },

  chartTitle: {
    marginBottom: "20px",
    fontSize: "22px"
  }

};