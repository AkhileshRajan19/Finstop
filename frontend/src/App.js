import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [token, setToken] = useState("");
  const [result, setResult] = useState(null);

  const upload = async () => {
    if (!file || !token) return alert("Provide file and token");
    const form = new FormData();
    form.append("file", file);
    const res = await axios.post("http://localhost:8000/upload", form, {
      headers: { Authorization: `Bearer ${token}`, "Content-Type": "multipart/form-data" }
    });
    setResult(res.data);
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Finstop - Upload financial statements</h2>
      <div>
        <input type="text" placeholder="JWT token" onChange={e => setToken(e.target.value)} style={{width:400}}/>
      </div>
      <div style={{ marginTop: 10 }}>
        <input type="file" onChange={e => setFile(e.target.files[0])} />
      </div>
      <div style={{ marginTop: 10 }}>
        <button onClick={upload}>Upload & Analyze</button>
      </div>
      <pre style={{ whiteSpace: "pre-wrap", marginTop: 20 }}>{JSON.stringify(result, null, 2)}</pre>
    </div>
  );
}

export default App;
