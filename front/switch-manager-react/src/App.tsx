import Table from "./components/table";

const tableColumns = [
  {
    title: "ppp",
  },
  {
    title: "customer",
  },
  {
    title: "ID",
  },
  {
    title: "switch",
  },
  {
    title: "date",
  },
  {
    title: "address",
  },
  {
    title: "type",
  },
  {
    title: "connexion status",
  },
];

const mockupData = [
  [
    {
      title: "NR12",
      property: "ppp"
    },
    {
      title: "woody Allen",
      property: "customer"
    },
    {
      title: "NR12",
      property: "ppp"
    },
    {
      title: "NR12",
      property: "ppp"
    },
    {
      title: "NR12",
      property: "ppp"
    },
    {
      title: "NR12",
      property: "ppp"
    },
    {
      title: "NR12",
      property: "ppp"
    }
]]

function App() {
  return (
    <div className="p-8">
      <Table columns={tableColumns} />
    </div>
  );
}

export default App;
