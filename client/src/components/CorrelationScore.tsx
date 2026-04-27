//components/CorrelationScore.tsx
import "../styles/correlation.css";

export default function CorrelationScore({ correlation }: any) {
  const confidence = correlation?.confidence || 0;
  const percentage = Math.round(confidence * 100);

  const level =
    percentage >= 80 ? "CRITICAL" :
    percentage >= 60 ? "HIGH CONFIDENCE" :
    percentage >= 40 ? "MEDIUM" :
    "LOW";

  return (
    <div className="panel correlation-panel">
      <div className="panel-header">
        <h2>CORRELATION SCORE</h2>
      </div>

      <div className="correlation-content">
        <div className="score-ring">
          <div className="score-value">{percentage}%</div>
          <div className="score-level">{level}</div>
        </div>

        <div className="trend-box">
          <span>TREND</span>
          <div className="trend-chart">
            <svg viewBox="0 0 240 100" preserveAspectRatio="none">
              <polyline
                points="0,90 40,70 80,42 120,44 160,25 200,38 240,15"
                fill="none"
                stroke="currentColor"
                strokeWidth="3"
              />
            </svg>
          </div>
        </div>
      </div>

      <div className="threshold-line">
        <span>0 LOW</span>
        <span>0.3 MEDIUM</span>
        <span>0.7 HIGH</span>
        <span>1.0 CRITICAL</span>
      </div>
    </div>
  );
}