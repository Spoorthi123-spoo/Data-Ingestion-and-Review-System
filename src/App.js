import "./App.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useState, useEffect } from "react";

import Upload from "./pages/Upload";
import Dashboard from "./pages/Dashboard";
import Review from "./pages/Review";
import Audit from "./pages/Audit";
import Login from "./pages/Login";

function App() {

  const [auth, setAuth] = useState(false);
  const [loading, setLoading] = useState(true);

  // ✅ CHECK AUTH FUNCTION
  const checkAuth = () => {
    const token = localStorage.getItem("access");
    setAuth(!!token);
    setLoading(false);
  };

  useEffect(() => {
    checkAuth();
  }, []);

  // 🔥 IMPORTANT: listen for login/logout changes
  useEffect(() => {
    const interval = setInterval(() => {
      const token = localStorage.getItem("access");
      setAuth(!!token);
    }, 500);

    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return <div style={{ padding: "40px" }}>Loading...</div>;
  }

  return (
    <BrowserRouter>
      <Routes>

        {/* LOGIN FIRST */}
        <Route
          path="/login"
          element={!auth ? <Login /> : <Navigate to="/" replace />}
        />

        {/* DASHBOARD */}
        <Route
          path="/"
          element={auth ? <Dashboard /> : <Navigate to="/login" replace />}
        />

        {/* UPLOAD */}
        <Route
          path="/upload"
          element={auth ? <Upload /> : <Navigate to="/login" replace />}
        />

        {/* REVIEW */}
        <Route
          path="/review"
          element={auth ? <Review /> : <Navigate to="/login" replace />}
        />

        {/* AUDIT */}
        <Route
          path="/audit"
          element={auth ? <Audit /> : <Navigate to="/login" replace />}
        />

        {/* FALLBACK */}
        <Route path="*" element={<Navigate to="/login" replace />} />

      </Routes>
    </BrowserRouter>
  );
}

export default App;