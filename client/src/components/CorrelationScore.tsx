export default function CorrelationScore({ correlation }: any) {
  const value = correlation?.confidence || 0;

  return (
    <div className="panel correlation">
      <h3>CORRELATION</h3>
      <div className="score">{value}</div>
    </div>
  );
}