import { useState } from "react";
import { useMovieContext } from "../contexts/MovieContext";
import '../css/LoginModal.css';
const LoginModal = () => {
  const { setShowLoginModal, setUser } = useMovieContext();
  console.log("LoginModal rendered");
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);


  const handleClose = () => {
    setShowLoginModal(false);
  };

const handleSubmit = async (e) => {
  e.preventDefault();
  setLoading(true);
  setMessage("Processing...");

  const endpoint = isLogin
    ? "http://127.0.0.1:5000/api/login"
    : "http://127.0.0.1:5000/api/register";

  try {
    const res = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    const data = await res.json();

    if (res.ok) {
      setUser(data.user);

      setMessage(
        isLogin
          ? "Login successful ✅"
          : "Account created successfully 🎉"
      );

      setTimeout(() => {
        setShowLoginModal(false);
        setMessage("");
      }, 1200);
    } else {
      setMessage(data.message || "Authentication failed ❌");
    }
  } catch (error) {
    console.error("Auth error:", error);
    setMessage("Backend server not running ❌");
  } finally {
    setLoading(false);
  }
};





  return (
    <div className="login-overlay">
      <div className="login-modal">
        <h2>{isLogin ? "Login" : "Sign Up"}</h2>

        <form onSubmit={handleSubmit}>
          <input
            type="email"
            placeholder="Enter Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <input
            type="password"
            placeholder="Enter Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button type="submit">
            {isLogin ? "Login" : "Create Account"}
          </button>
        </form>
        {message && (
  <p
    style={{
      marginTop: "12px",
      fontWeight: "bold",
      color: message.includes("successful") ? "#4CAF50" : "#ff4d4d",
    }}
  >
    {message}
  </p>
)}

        <p
          onClick={() => setIsLogin(!isLogin)}
          style={{ cursor: "pointer", marginTop: "10px" }}
        >
          {isLogin
            ? "Don't have an account? Sign Up"
            : "Already have an account? Login"}
        </p>

        <button onClick={handleClose} style={{ marginTop: "10px" }}>
          Close
        </button>
        
      </div>
      
    </div>



  );
};

export default LoginModal;
