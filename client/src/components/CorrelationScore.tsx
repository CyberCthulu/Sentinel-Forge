export default function CorrelationScore({ correlation }: any) {
  const confidence = correlation?.confidence || 0;
  const percentage = Math.round(confidence * 100);
  const level = getLevel(percentage);

  return (
    <div className="panel correlation">
      <h3>CORRELATION CONFIDENCE</h3>

      <div className="score-value">
        {percentage}% - {level}
      </div>

    </div>
  );
}

function getLevel(confidence: number) {
  if (confidence >= 80) return "CRITICAL";
  if (confidence >= 60) return "HIGH";
  if (confidence >= 40) return "MEDIUM";
  return "LOW";
}