// components/CorrelationScore.tsx
import { useEffect, useMemo, useState } from "react";
import "../styles/correlation.css";

type Correlation = {
  confidence?: number;
};

type EventLike = {
  timestamp?: string;
};

type Props = {
  correlation: Correlation | null;
  events?: EventLike[];
};

type TrendPoint = {
  confidence: number;
  label: string;
};

type SvgPoint = {
  x: number;
  y: number;
};

const MAX_POINTS = 8;

export default function CorrelationScore({ correlation, events = [] }: Props) {
  const confidence = correlation?.confidence ?? 0;
  const percentage = Math.round(confidence * 100);

  const latestTimestamp = getLatestEventTime(events);

  const [history, setHistory] = useState<TrendPoint[]>([
    { confidence: 0, label: "--:--" },
  ]);

  useEffect(() => {
    setHistory((prev) => {
      if (events.length === 0 && confidence === 0) {
        return [{ confidence: 0, label: "--:--" }];
      }

      const last = prev[prev.length - 1];

      if (last.confidence === confidence && last.label === latestTimestamp) {
        return prev;
      }

      const next = [...prev, { confidence, label: latestTimestamp }];
      return next.slice(-MAX_POINTS);
    });
  }, [confidence, latestTimestamp, events.length]);

  const level = getLevel(percentage);

  const displaySeries = useMemo(() => buildDisplaySeries(history), [history]);
  const linePoints = useMemo(() => buildSvgLinePoints(displaySeries), [displaySeries]);
  const areaPoints = useMemo(() => buildSvgAreaPoints(displaySeries), [displaySeries]);
  const xLabels = useMemo(() => getXAxisLabels(history), [history]);

  const markerLeft = `${Math.min(Math.max(confidence, 0), 1) * 100}%`;

  return (
    <div className={`panel correlation-panel ${level.className}`}>
      <div className="panel-header">
        <h2>CORRELATION SCORE</h2>
      </div>

      <div className="correlation-content">
        <div className="score-ring">
          <div className="score-value">{percentage}%</div>
          <div className="score-level">{level.label}</div>
        </div>

        <div className="trend-box">


          <div className="trend-chart">
            <svg viewBox="0 0 260 120" preserveAspectRatio="none">
              <defs>
                <linearGradient id="riskAreaGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="currentColor" stopOpacity="0.34" />
                  <stop offset="65%" stopColor="currentColor" stopOpacity="0.12" />
                  <stop offset="100%" stopColor="currentColor" stopOpacity="0" />
                </linearGradient>
              </defs>

              {/* Grid */}
              <line className="axis-line" x1="32" y1="14" x2="32" y2="94" />
              <line className="axis-line" x1="32" y1="94" x2="248" y2="94" />

              <line className="grid-line" x1="32" y1="14" x2="248" y2="14" />
              <line className="grid-line" x1="32" y1="54" x2="248" y2="54" />
              <line className="grid-line" x1="32" y1="94" x2="248" y2="94" />

              <line className="grid-line" x1="82" y1="14" x2="82" y2="94" />
              <line className="grid-line" x1="132" y1="14" x2="132" y2="94" />
              <line className="grid-line" x1="182" y1="14" x2="182" y2="94" />
              <line className="grid-line" x1="232" y1="14" x2="232" y2="94" />

              {/* Axis labels */}
              <text className="y-axis-label" x="4" y="18">1.0</text>
              <text className="y-axis-label" x="4" y="58">0.5</text>
              <text className="y-axis-label" x="4" y="98">0.0</text>

              <text className="x-axis-label" x="62" y="114">{xLabels[0]}</text>
              <text className="x-axis-label" x="136" y="114">{xLabels[1]}</text>
              <text className="x-axis-label" x="214" y="114">{xLabels[2]}</text>

              {/* Risk area */}
              <polygon
                points={areaPoints}
                fill="url(#riskAreaGradient)"
              />

              {/* Trend line */}
              <polyline
                points={linePoints}
                fill="none"
                stroke="currentColor"
                strokeWidth="3.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </div>
        </div>
      </div>

      <div className="threshold-line">
        <div className="threshold-track">
          <span className="threshold-marker" style={{ left: markerLeft }} />
        </div>

        <div className="threshold-labels">
          <span>0% LOW</span>
          <span>30% MEDIUM</span>
          <span>70% HIGH</span>
          <span>100% CRITICAL</span>
        </div>
      </div>
    </div>
  );
}

function getLevel(percentage: number) {
  if (percentage >= 80) {
    return { label: "CRITICAL", className: "critical" };
  }

  if (percentage >= 60) {
    return { label: "HIGH CONFIDENCE", className: "high" };
  }

  if (percentage >= 40) {
    return { label: "MEDIUM", className: "medium" };
  }

  if (percentage > 10) {
    return { label: "ELEVATED LOW", className: "elevated" };
  }

  return { label: "LOW", className: "low" };
}

/**
 * Turns sparse scenario states into a denser display series.
 * This makes the graph read like live telemetry while preserving
 * the actual confidence endpoint.
 */
function buildDisplaySeries(history: TrendPoint[]) {
  const rawValues = history.map((point) => point.confidence);

  if (rawValues.length <= 1) {
    return [0, 0, 0];
  }

  const output: number[] = [];

  for (let i = 0; i < rawValues.length - 1; i++) {
    const start = rawValues[i];
    const end = rawValues[i + 1];

    output.push(start);

    const samples = 3;

    for (let j = 1; j <= samples; j++) {
      const t = j / (samples + 1);
      const base = start + (end - start) * t;

      // Small deterministic variation so the line feels like a sensor trend.
      const wiggle = Math.sin((i + 1) * (j + 2)) * 0.025;
      const value = clamp(base + wiggle, 0, 1);

      output.push(value);
    }
  }

  output.push(rawValues[rawValues.length - 1]);

  return output;
}

function buildSvgLinePoints(values: number[]) {
  return toSvgPoints(values)
    .map((point) => `${point.x},${point.y}`)
    .join(" ");
}

function buildSvgAreaPoints(values: number[]) {
  const points = toSvgPoints(values);

  if (points.length === 0) {
    return "";
  }

  const first = points[0];
  const last = points[points.length - 1];

  return [
    `${first.x},94`,
    ...points.map((point) => `${point.x},${point.y}`),
    `${last.x},94`,
  ].join(" ");
}

function toSvgPoints(values: number[]): SvgPoint[] {
  const maxIndex = values.length - 1 || 1;

  return values.map((value, index) => {
    const x = 32 + (index / maxIndex) * 216;
    const clamped = clamp(value, 0, 1);
    const y = 94 - clamped * 80;

    return { x, y };
  });
}

function getXAxisLabels(history: TrendPoint[]) {
  if (history.length <= 1) {
    return ["--:--", "--:--", "--:--"];
  }

  const first = history[0]?.label ?? "--:--";
  const middle = history[Math.floor(history.length / 2)]?.label ?? "--:--";
  const last = history[history.length - 1]?.label ?? "--:--";

  return [shortTime(first), shortTime(middle), shortTime(last)];
}

function getLatestEventTime(events: EventLike[]) {
  const latest = events[events.length - 1];

  if (!latest?.timestamp) {
    return "--:--";
  }

  const date = new Date(latest.timestamp);

  if (Number.isNaN(date.getTime())) {
    return "--:--";
  }

  return date.toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  });
}

function shortTime(value: string) {
  if (!value || value === "--:--") return "--:--";

  const parts = value.split(":");

  if (parts.length >= 2) {
    return `${parts[0]}:${parts[1]}`;
  }

  return value;
}

function clamp(value: number, min: number, max: number) {
  return Math.min(Math.max(value, min), max);
}