import React from "react";

interface Props {
  prompt: string;
  setPrompt: (value: string) => void;
  onSubmit: () => void;
  isLoading: boolean;
}

export default function PromptInput({
  prompt,
  setPrompt,
  onSubmit,
  isLoading,
}: Props) {
  return (
    <div className="flex flex-col space-y-2">
      <textarea
        className="border p-3 rounded w-full resize-none text-sm"
        rows={4}
        placeholder="Ask something..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />
      <button
        onClick={onSubmit}
        disabled={isLoading}
        className={`px-4 py-2 rounded text-white font-semibold ${
          isLoading
            ? "bg-gray-400 cursor-not-allowed"
            : "bg-blue-600 hover:bg-blue-700"
        }`}
      >
        {isLoading ? "Thinking..." : "Run"}
      </button>
    </div>
  );
}
