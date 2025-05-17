import React from "react";

export interface TraceEntry {
  step: string;
  tool: string;
  response: string;
}

interface TracePanelProps {
  trace: TraceEntry[];
}

// Generate a consistent Tailwind border color from a tool name hash
const colorPool = [
  "border-red-400",
  "border-green-400",
  "border-blue-400",
  "border-yellow-400",
  "border-purple-400",
  "border-pink-400",
  "border-indigo-400",
  "border-emerald-400",
  "border-cyan-400",
  "border-rose-400",
];

// Simple hash function to pick a color based on the tool name
function getColorForTool(toolName: string): string {
  let hash = 0;
  for (let i = 0; i < toolName.length; i++) {
    hash = toolName.charCodeAt(i) + ((hash << 5) - hash);
  }
  const index = Math.abs(hash) % colorPool.length;
  return colorPool[index];
}

export default function TracePanel({ trace }: TracePanelProps) {
  if (!trace || trace.length === 0) return null;

  return (
    <div className="w-1/3 p-4 border-r overflow-y-auto bg-gray-50">
      <h2 className="text-lg font-bold mb-4">Trace</h2>
      {trace.map((entry, index) => {
        const borderColor = getColorForTool(entry.tool);

        return (
          <div
            key={index}
            className={`bg-white shadow p-2 rounded mb-2 border-l-4 ${borderColor}`}
          >
            <div className="text-sm font-semibold text-gray-800">
              {entry.tool}
            </div>
            <div className="text-xs text-gray-500 italic">{entry.step}</div>
            <div className="text-xs text-gray-700">{entry.response}</div>
          </div>
        );
      })}
    </div>
  );
}
