import { useState } from "react";

export default function UploadBox() {
  const [response, setResponse] = useState(null);

  async function handleUpload(e) {
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://localhost:8000/upload/file", {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    setResponse(data);
  }

  return (
    <div>
      <input type="file" onChange={handleUpload} />
      <pre>{response && JSON.stringify(response, null, 2)}</pre>
    </div>
  );
}
