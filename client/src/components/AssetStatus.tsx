export default function AssetStatus() {
  return (
    <div className="panel asset-panel">
      <div className="panel-header">
        <h2>ASSET STATUS</h2>
        <span>VIEW ALL ›</span>
      </div>

      <div className="asset-list">
        <div><span>AUTH SERVER</span><strong>OPERATIONAL</strong></div>
        <div><span>EDR SENSOR NETWORK</span><strong>OPERATIONAL</strong></div>
        <div><span>NETWORK GATEWAY</span><strong>OPERATIONAL</strong></div>
        <div><span>UAS MONITORING</span><strong className="active">ACTIVE</strong></div>
        <div><span>AIS MONITORING</span><strong className="active">ACTIVE</strong></div>
      </div>
    </div>
  );
}