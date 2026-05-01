// components/AssetStatus.tsx

type Asset = {
  id: string;
  name: string;
  kind: string;
  domain: "cyber" | "physical" | "osint" | string;
  status: "operational" | "alerting" | "active" | "degraded" | "offline" | string;
};

type Props = {
  assets?: Asset[];
};

const FALLBACK_ASSETS: Asset[] = [
  {
    id: "asset-auth-gw-01",
    name: "AUTH SERVER",
    kind: "auth_gateway",
    domain: "cyber",
    status: "operational",
  },
  {
    id: "asset-edr-network",
    name: "EDR SENSOR NETWORK",
    kind: "endpoint_detection",
    domain: "cyber",
    status: "operational",
  },
  {
    id: "asset-network-gateway",
    name: "NETWORK GATEWAY",
    kind: "network_gateway",
    domain: "cyber",
    status: "operational",
  },
  {
    id: "asset-uas-monitoring",
    name: "UAS MONITORING",
    kind: "uas_sensor",
    domain: "physical",
    status: "operational",
  },
  {
    id: "asset-ais-monitoring",
    name: "AIS MONITORING",
    kind: "ais_feed",
    domain: "osint",
    status: "operational",
  },
];

export default function AssetStatus({ assets }: Props) {
  const displayAssets = assets && assets.length > 0 ? assets : FALLBACK_ASSETS;

  return (
    <div className="panel asset-panel">
      <div className="panel-header">
        <h2>ASSET STATUS</h2>
        <span>{displayAssets.length} MONITORED</span>
      </div>

      <div className="asset-list">
        {displayAssets.map((asset) => {
          const normalizedStatus = normalizeStatus(asset.status);

          return (
            <div key={asset.id} className={`asset-row ${normalizedStatus}`}>
              <span>{asset.name}</span>
              <strong className={normalizedStatus}>
                {formatStatus(asset.status)}
              </strong>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function normalizeStatus(status: string) {
  const normalized = String(status || "unknown").toLowerCase();

  if (normalized === "active") return "active";
  if (normalized === "alerting") return "alerting";
  if (normalized === "degraded") return "degraded";
  if (normalized === "offline") return "offline";
  if (normalized === "operational") return "operational";

  return "unknown";
}

function formatStatus(status: string) {
  return String(status || "unknown")
    .replace(/_/g, " ")
    .toUpperCase();
}