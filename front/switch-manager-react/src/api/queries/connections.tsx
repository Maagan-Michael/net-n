import { useInfiniteQuery } from "react-query";
import { ConnectionsOutput, ConnectionsListQueryInput } from "../types";

const fetchConnections = async (params: ConnectionsListQueryInput) => {
  const { page = 0, limit = 10 } = params;
  const queryString = new URLSearchParams({
    ...params,
    page: page.toString(),
    limit: limit.toString(),
  }).toString();
  console.log(queryString);
  const res = await fetch(
    `${process.env.REACT_APP_API_URL}/api/v1/connections?${queryString}`
  );
  return res.json();
};

export function useConnectionsQuery(params: ConnectionsListQueryInput) {
  return useInfiniteQuery<ConnectionsOutput>(
    "connections",
    () => fetchConnections(params),
    {
      getNextPageParam: (lastPage) => {
        if (lastPage.hasNext) {
          return { ...params, page: (params.page || 0) + 1 };
        }
        return undefined;
      },
    }
  );
}
