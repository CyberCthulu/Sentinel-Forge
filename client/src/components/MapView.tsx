//components/MapView.tsx


import "../styles/map.css";

export default function MapView({ map }: any) {
  const tracks = map?.tracks || [];

  return (
    <div className="panel map-panel">
      <div className="panel-header">
        <h2>OPERATIONAL VIEW</h2>
      </div>

      <div className="map-canvas">
        <div className="map-legend">
          <span><b className="blue" /> FRIENDLY ASSET</span>
          <span><b className="red" /> THREAT</span>
          <span><b className="gray" /> NEUTRAL</span>
          <span><b className="orange-line" /> UAS TRACK</span>
          <span><b className="cyan-line" /> VESSEL TRACK</span>
        </div>

        <div className="map-node gateway">GATEWAY-01</div>
        <div className="map-node hq">HQ NODE</div>
        <div className="sector-ring">SECTOR B</div>

        {tracks.map((t: any) => (
          <div key={t.id} className="map-threat">
            UAS
          </div>
        ))}

        <div className="vessel">UNKNOWN VESSEL</div>
      </div>
    </div>
  );
}