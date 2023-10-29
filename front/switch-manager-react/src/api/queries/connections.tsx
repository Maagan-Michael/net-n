import { useInfiniteQuery, useQuery } from "react-query";
import {
  ConnectionsOutput,
  ConnectionsListQueryInput,
  ConnectionsFilters,
  ListSortEnum,
  OrderBy,
  ConnectionOutput,
} from "../types";
import { SetURLSearchParams, useSearchParams } from "react-router-dom";

const fetchConnection = async (params: { id: string }) => {
  const res = await fetch(
    `${process.env.REACT_APP_API_URL}/api/v1/connections/${params.id}`
  );
  return res.json();
};

export function useConnectionQuery(params: { id: string }) {
  return useQuery<ConnectionOutput>(["connection", { id: params.id }], () =>
    fetchConnection(params)
  );
}
const fetchConnections = async (params: ConnectionsListQueryInput) => {
  const { page = 0, limit = 10 } = params;
  const queryString = new URLSearchParams({
    ...params,
    page: page.toString(),
    limit: limit.toString(),
  }).toString();
  const res = await fetch(
    `${process.env.REACT_APP_API_URL}/api/v1/connections?${queryString}`
  );
  return res.json();
};

export function useConnectionsQuery(params: ConnectionsListQueryInput) {
  return useInfiniteQuery<ConnectionsOutput>(
    [
      "connections",
      {
        filters: params.filter,
        sort: params.sort,
        order: params.order,
        search: params.search,
      },
    ],
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
