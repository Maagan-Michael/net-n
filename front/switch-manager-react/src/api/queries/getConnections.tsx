import { useInfiniteQuery } from "react-query";
import {
  ConnectionsOutput,
  ConnectionsListQueryInput,
  ConnectionsFilters,
  ListSortEnum,
  OrderBy,
} from "../types";
import { URLSearchParamsInit, useSearchParams } from "react-router-dom";

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

export type setSearchType = (
  params: Partial<ConnectionsListQueryInput>
) => void;

export function useConnectionsUrlParams(): [
  ConnectionsListQueryInput,
  setSearchType
] {
  const [searchParams, setSearchParams] = useSearchParams();
  const search = searchParams.get("search");
  const parsed: ConnectionsListQueryInput = {
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
    ...(search ? { search } : {}),
    page: Number(searchParams.get("page")) || 0,
    limit: Number(searchParams.get("limit")) || 10,
  };
  const _setSearch: setSearchType = (params) => {
    setSearchParams({
      ...parsed,
      ...params,
    } as unknown as URLSearchParamsInit);
  };
  return [parsed, _setSearch];
}
