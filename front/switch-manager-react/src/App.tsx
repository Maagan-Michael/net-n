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
    separatorClass: "hidden",
  },
  {
    title: "separator",
    containerClass: "w-2 border-b-0 invisible",
    separatorClass: "hidden",
  },
  {
    title: "connexion status",
    separatorClass: "hidden",
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
