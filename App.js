import React, { useState } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  const [url, setUrl] = useState("");
  const [category, setCategory] = useState("");

  const handleSubmit = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:5000", { url });
      setCategory(response.data.category);
    } catch (error) {
      console.error("Error:", error);
      setCategory("Error fetching category");
    }
  };

  return (
    <div className="container mt-5">
      <h2>AI-Based Website Categorization</h2>
      <input
        type="text"
        className="form-control"
        placeholder="Enter website URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />
      <button className="btn btn-primary mt-3" onClick={handleSubmit}>Categorize</button>
      {category && <h3 className="mt-3">Category: {category}</h3>}
    </div>
  );
}

export default App;