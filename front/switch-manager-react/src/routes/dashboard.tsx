import Table from "../components/tables/generic";
import { Header, Row } from "../components/tables/connections";
import { useConnectionsquery } from "../api/queries/connections";

export default function Dashboard() {
  const { data = [], isLoading } = useConnectionsquery();
  return (
    <div className="p-8">
      <Table data={data} renderHeader={<Header />} renderRow={Row} />
    </div>
  );
}
