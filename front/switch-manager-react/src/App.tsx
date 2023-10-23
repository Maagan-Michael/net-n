import { QueryClientProvider, QueryClient } from "react-query";
import Dashboard from "./routes/dashboard";
import { createBrowserRouter, Router, RouterProvider } from "react-router-dom";
import { ConnectionsTable } from "./components/tables/connections";

const queryClient = new QueryClient();
const router = createBrowserRouter([
  {
    path: "/",
    element: <Dashboard />,
    children: [
      {
        path: "/",
        element: <ConnectionsTable />,
      },
    ],
  },
]);

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  );
}

export default App;
