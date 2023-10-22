import { QueryClientProvider, QueryClient } from "react-query";
import Dashboard from "./routes/dashboard";

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Dashboard />
    </QueryClientProvider>
  );
}

export default App;
