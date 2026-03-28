import {useState} from "react"; 

export default function ComputeComponent() {
  const [value, setValue] = useState<number>(0);
  const [result, setResult] = useState<number | null>(null);

  const handleClick = async () => {
    const data = await compute(value);
    setResult(data.result);
  };

  return (
    <div>
      <input
        type="number"
        value={value}
        onChange={(e) => setValue(Number(e.target.value))}
      />
      <button onClick={handleClick}>Compute</button>
      {result !== null && <p>Result: {result}</p>}
    </div>
  );
}
async function compute(value: number) {
  const response = await fetch("http://localhost:8000/api/compute", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ value }),
  });

  return response.json();
}