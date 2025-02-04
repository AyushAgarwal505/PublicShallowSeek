import { useState } from "react";

export default function TextSender() {
  const [text, setText] = useState("");
  const [response, setResponse] = useState("");

  const handleSubmit = async () => {
    try {
      const res = await fetch("http://127.0.0.1:5000/process", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      });
      const data = await res.json();
      setResponse(data.response);
    } catch (error) {
      console.error("Error communicating with the server", error);
    }
  };

  return (
    <div style={{ padding: "16px", maxWidth: "400px", margin: "0 auto", backgroundColor: "white", boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)", borderRadius: "8px" }}>
      <h2 style={{ fontSize: "20px", fontWeight: "bold", marginBottom: "8px" }}>Send Text to Flask Server</h2>
      <textarea
        style={{ width: "100%", padding: "8px", border: "1px solid #ccc", borderRadius: "4px" }}
        rows="4"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Enter text here..."
      />
      <button
        style={{ marginTop: "8px", padding: "8px 16px", backgroundColor: "#007BFF", color: "white", border: "none", borderRadius: "4px", cursor: "pointer" }}
        onClick={handleSubmit}
      >
        Submit
      </button>
      {response && (
        <div style={{ marginTop: "16px", padding: "8px", backgroundColor: "#f8f9fa", border: "1px solid #ccc", borderRadius: "4px" }}>
          <strong>Response:</strong> {response}
        </div>
      )}
    </div>
  );
}

