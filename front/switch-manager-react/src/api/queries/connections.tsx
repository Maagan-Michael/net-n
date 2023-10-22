import { useQuery } from "react-query";

const fetchConnections = async () => {
  const res = await fetch(
    `${process.env.REACT_APP_API_URL}/api/v1/connections`
  );
  return res.json();
};

export function useConnectionsquery() {
  return useQuery("connections", fetchConnections);
}
