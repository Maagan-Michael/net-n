import Table from "./components/tables/generic";
import { Header, Row, mockupData } from "./components/tables/connections";
function App() {
  return (
    <div className="p-8">
      <Table data={mockupData} renderHeader={<Header />} renderRow={Row} />
    </div>
  );
}

export default App;
