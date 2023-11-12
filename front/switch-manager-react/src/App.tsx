import { QueryClientProvider, QueryClient } from "react-query";
import Dashboard from "./routes/dashboard";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Connections from "./routes/connections";
import Connection from "./routes/connections/connection";
import "react-toastify/dist/ReactToastify.css";
import { ToastContainer } from "react-toastify";

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
      <ToastContainer />
    </QueryClientProvider>
  );
}

export default App;
