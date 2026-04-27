import "../styles/map.css";

export default function MapView({ map }: any) {
  return (
    <div className="panel map">
      <h3>OPERATIONAL VIEW</h3>
      <pre>{JSON.stringify(map, null, 2)}</pre>
    </div>
  );
}