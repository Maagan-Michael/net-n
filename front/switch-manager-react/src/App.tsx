import Table, { TableHeaderCell, TableRow } from "./components/tables/generic";

const tableColumns = [
  {
    data: {
      id: "ppp",
      title: "ppp",
    },
    render: TableHeaderCell,
  },
  {
    data: {
      id: "customer",
      title: "customer",
    },
    render: TableHeaderCell,
  },
  {
    data: {
      id: "ID",
      title: "ID",
    },
    render: TableHeaderCell,
  },
  {
    data: {
      id: "switch",
      title: "switch",
    },
    render: TableHeaderCell,
  },
  {
    data: {
      id: "date",
      title: "date",
    },
    render: TableHeaderCell,
  },
  {
    data: {
      id: "address",
      title: "address",
    },
    render: TableHeaderCell,
  },
  {
    data: {
      id: "type",
      title: "type",
    },
    render: TableHeaderCell,
  },
  {
    data: {
      id: "status",
      title: "connexion status",
    },
    render: TableHeaderCell,
  },
];

const mockupData = [
    {
      data: {
        id: "1",
        ppp: "NR12",
        customer: "woody Allen",
        ID: "NR12",
        switch: "NR12",
        date: "NR12",
        address: "NR12",
        type: "NR12",
        status: "NR12",
      },
      render: TableRow,
    },
    {
      data: {
        id: "2",
        ppp: "NR12",
        customer: "woody Allen",
        ID: "NR12",
        switch: "NR12",
        date: "NR12",
        address: "NR12",
        type: "NR12",
        status: "NR12",
      },
      render: TableRow,
    },
    {
      data: {
        id: "3",
        ppp: "NR12",
        customer: "woody Allen",
        ID: "NR12",
        switch: "NR12",
        date: "NR12",
        address: "NR12",
        type: "NR12",
        status: "NR12",
      },
      render: TableRow,
    },
    {
      data: {
        id: "4",
        ppp: "NR12",
        customer: "woody Allen",
        ID: "NR12",
        switch: "NR12",
        date: "NR12",
        address: "NR12",
        type: "NR12",
        status: "NR12",
      },
      render: TableRow,
    }
];

function App() {
  return (
    <div className="p-8">
      <Table columns={tableColumns} data={mockupData} />
    </div>
  );
}

export default App;
