// components/MapView.tsx
import "../styles/map.css";

export default function MapView({ map }: any) {
  const tracks = map?.tracks || [];
  const riskLevel = map?.risk_level || "normal";

  const hasDrone =
    tracks.some((track: any) => track.kind === "physical.drone") ||
    riskLevel === "critical";

  const hasVessel =
    tracks.some((track: any) => track.kind === "osint.ais_anomaly") ||
    map?.threat_paths?.some((path: any) => path.kind === "osint_path");

  const isElevated = riskLevel === "critical" || riskLevel === "high";

  return (
    <div className={`panel map-panel risk-${riskLevel}`}>
      <div className="panel-header">
        <h2>OPERATIONAL VIEW</h2>
        <span className={`map-risk-badge ${riskLevel}`}>
          RISK: {riskLevel.toUpperCase()}
        </span>
      </div>

      <div className="map-canvas">
        <div className="map-background" />
        <div className="map-grid-overlay" />
        <div className="map-scanline" />

        <div className="map-legend">
          <span><b className="blue" /> FRIENDLY ASSET</span>
          <span><b className="red" /> THREAT</span>
          <span><b className="gray" /> NEUTRAL</span>
          <span><b className="orange-line" /> UAS TRACK</span>
          <span><b className="cyan-line" /> VESSEL TRACK</span>
        </div>

        <svg
          className="tactical-overlay"
          viewBox="0 0 1000 420"
          preserveAspectRatio="none"
          aria-hidden="true"
        >
          <defs>
            <filter id="mapGlow">
              <feGaussianBlur stdDeviation="3" result="coloredBlur" />
              <feMerge>
                <feMergeNode in="coloredBlur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>

            <radialGradient id="sectorGradient" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="rgba(255,64,64,0.34)" />
              <stop offset="55%" stopColor="rgba(255,64,64,0.16)" />
              <stop offset="100%" stopColor="rgba(255,64,64,0.02)" />
            </radialGradient>
          </defs>

          {/* geographic contour / road-like lines */}
          <path
            className="terrain-line faint"
            d="M0 310 C120 280 190 340 290 300 S470 230 570 260 780 340 1000 250"
          />
          <path
            className="terrain-line"
            d="M0 235 C130 210 260 245 390 205 S620 150 740 190 900 225 1000 160"
          />
          <path
            className="terrain-line faint"
            d="M120 420 C170 330 220 260 310 190 S500 70 610 0"
          />
          <path
            className="terrain-line faint"
            d="M760 420 C730 330 750 250 820 160 S910 65 1000 20"
          />

          {/* friendly network route */}
          <path
            className="friendly-link"
            d="M245 342 C315 318 365 300 438 260"
          />

          {/* UAS track */}
          <path
            className={`uas-path ${hasDrone ? "active" : ""}`}
            d="M460 420 C500 325 548 270 620 232 S720 178 790 176"
          />

          {/* vessel track */}
          <path
            className={`vessel-path ${hasVessel ? "active" : ""}`}
            d="M1000 342 C895 338 825 336 742 332 S595 322 486 302"
          />

          {/* Sector B risk zone */}
          <circle
            className={`sector-zone ${isElevated ? "active" : ""}`}
            cx="760"
            cy="180"
            r="74"
          />
          <circle
            className={`sector-pulse ${isElevated ? "active" : ""}`}
            cx="760"
            cy="180"
            r="74"
          />

          {/* active UAS point */}
          <circle
            className={`uas-dot ${hasDrone ? "active" : ""}`}
            cx="760"
            cy="180"
            r="10"
          />

          {/* vessel point */}
          <circle
            className={`vessel-dot ${hasVessel ? "active" : ""}`}
            cx="905"
            cy="328"
            r="9"
          />
        </svg>

        <div className="map-coordinate x16">16</div>
        <div className="map-coordinate x17">17</div>
        <div className="map-coordinate x18">18</div>
        <div className="map-coordinate x19">19</div>
        <div className="map-coordinate x20">20</div>
        <div className="map-coordinate x21">21</div>

        <div className="map-node gateway">
          <span className="node-icon">◇</span>
          GATEWAY-01
        </div>

        <div className="map-node hq">
          <span className="node-icon">⬢</span>
          HQ NODE
        </div>

        <div className={`sector-ring ${isElevated ? "active" : ""}`}>
          <span>SECTOR B</span>
          {hasDrone && <strong>UAS</strong>}
        </div>

        {hasDrone && (
          <div className="map-threat">
            <span className="threat-icon">◉</span>
            UAS
          </div>
        )}

        <div className={`vessel ${hasVessel ? "active" : ""}`}>
          <span className="vessel-icon">▲</span>
          UNKNOWN VESSEL
        </div>
      </div>
    </div>
  );
}