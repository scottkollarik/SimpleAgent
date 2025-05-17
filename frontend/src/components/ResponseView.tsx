type ResponseViewProps = {
  response: string;
};

export default function ResponseView({ response }: ResponseViewProps) {
  return (
    <div className="response-container">
      <h2>Response</h2>
      <pre>{response}</pre>
    </div>
  );
}