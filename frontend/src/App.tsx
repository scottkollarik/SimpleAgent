import React, { useState, useRef, useEffect } from "react";
import PromptInput from "./components/PromptInput";
import TracePanel from "./components/TracePanel";

interface TraceEntry {
  step: string;
  tool: string;
  response: string;
}

interface PromptHistoryEntry {
  prompt: string;
  response: string;
}

export default function App() {
  const [prompt, setPrompt] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [trace, setTrace] = useState<TraceEntry[]>([]);
  const [history, setHistory] = useState<PromptHistoryEntry[]>([]);
  const historyEndRef = useRef<HTMLDivElement>(null);

  const handleSubmit = async () => {
    if (!prompt.trim()) return;

    setIsLoading(true);
    setTrace([]);

    try {
      const res = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });

      const data = await res.json();
      const cleanResponse = data.response || "";
      const steps = data.steps || [];

      setHistory((prev) => [...prev, { prompt, response: cleanResponse }]);

      setTrace(steps);
      setPrompt("");
    } catch (error) {
      setHistory((prev) => [
        ...prev,
        { prompt, response: "Error: Could not reach backend." },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    historyEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [history]);

  return (
    <div className="flex h-screen">
      <aside className="w-1/3 p-4 bg-gray-100 border-r overflow-y-auto">
        <h2 className="text-xl font-semibold mb-4">Trace</h2>
        <TracePanel trace={trace} />
      </aside>

      <main className="flex-1 flex flex-col p-4 space-y-4 overflow-hidden">
        <PromptInput
          prompt={prompt}
          setPrompt={setPrompt}
          onSubmit={handleSubmit}
          isLoading={isLoading}
        />

        <div className="flex-1 overflow-y-auto border-t pt-4">
          {history.map((entry, idx) => (
            <div
              key={idx}
              className="mb-4 p-4 bg-white border rounded shadow space-y-2"
            >
              <div>
                <span className="font-semibold text-sm text-gray-600">
                  You:
                </span>{" "}
                {entry.prompt}
              </div>
              <div>
                <span className="font-semibold text-sm text-blue-600">
                  Response:
                </span>{" "}
                {entry.response}
              </div>
            </div>
          ))}
          <div ref={historyEndRef} />
        </div>
      </main>
    </div>
  );
}
