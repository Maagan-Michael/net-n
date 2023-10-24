import { useInfiniteQuery } from "react-query";
import { ConnectionsOutput } from "../types";

const fetchConnections = async () => {
  const res = await fetch(
    `${process.env.REACT_APP_API_URL}/api/v1/connections`
  );
  return res.json();
};

export function useConnectionsQuery() {
  return useInfiniteQuery<ConnectionsOutput>("connections", fetchConnections);
}
