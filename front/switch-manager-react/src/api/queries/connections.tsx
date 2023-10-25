import { useInfiniteQuery } from "react-query";
import {
  ConnectionsOutput,
  ConnectionsListQueryInput,
  ConnectionsFilters,
  ListSortEnum,
  OrderBy,
} from "../types";
import { SetURLSearchParams, useSearchParams } from "react-router-dom";

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

export function useConnectionsUrlParams(): [
  ConnectionsListQueryInput,
  SetURLSearchParams
] {
  const [searchParams, setSearchParams] = useSearchParams();
  const ParsedParameters: ConnectionsListQueryInput = {
    filter:
      ConnectionsFilters[
        (searchParams.get("filter") as keyof typeof ConnectionsFilters) ||
          ConnectionsFilters.all
      ],
    sort: ListSortEnum[
      (searchParams.get("sort") as keyof typeof ListSortEnum) ||
        ListSortEnum.con
    ],
    order:
      OrderBy[
        (searchParams.get("order") as keyof typeof OrderBy) || OrderBy.asc
      ],
    search: searchParams.get("search") || undefined,
    page: Number(searchParams.get("page")) || 0,
    limit: Number(searchParams.get("limit")) || 10,
  };
  return [ParsedParameters, setSearchParams];
}
