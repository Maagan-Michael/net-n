import { QueryClientProvider, QueryClient } from "react-query";
import Dashboard from "./routes/dashboard";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Connections from "./routes/connections";
import Connection from "./routes/connections/connection";

const queryClient = new QueryClient();
const router = createBrowserRouter([
  {
    path: "/",
    element: <Dashboard />,
    children: [
      {
        path: "/",
        element: <Connections />,
        children: [
          {
            path: "/connections/:id",
            element: <Connection />,
          },
        ],
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
