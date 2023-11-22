import { Suspense } from "react";
import { QueryClientProvider, QueryClient } from "react-query";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Dashboard from "@routes/dashboard";
import Connections from "@routes/connections";
import Connection from "@routes/connections/connection";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

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
      <Suspense fallback={<div>Loading...</div>}>
        <RouterProvider router={router} />
      </Suspense>
      <ToastContainer />
    </QueryClientProvider>
  );
}

export default App;
