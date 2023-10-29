import { Outlet } from "react-router-dom";
import { Table } from "../../components/tables/generic";
import { ConnectionOutput, ConnectionsOutput } from "../../api/types";
import {
  useConnectionsQuery,
  useConnectionsUrlParams,
} from "../../api/queries/connections";
import useInfiniteScroller from "../../components/hooks/useInfiniteScroller";
import Header from "./header";
import Row from "./row";
import LoadingRow from "./loadingRow";

function Connections() {
  const [queryParams] = useConnectionsUrlParams();
  const { data, isLoading, fetchNextPage, isFetchingNextPage } =
    useConnectionsQuery(queryParams);
  const onReady = useInfiniteScroller(
    () => !isLoading && !isFetchingNextPage && fetchNextPage(),
    {
      threshold: 0.8,
    }
  );
  const pagesContent: ConnectionOutput[] = (data?.pages || []).reduce(
    (r: ConnectionOutput[], page: ConnectionsOutput) => [
      ...page.connections,
      ...r,
    ],
    []
  );
  return (
    <div>
      <Table
        data={pagesContent || []}
        renderHeader={<Header />}
        renderRow={Row}
        onReady={onReady}
      />
      {(isFetchingNextPage || isLoading) && (
        <div className="flex flex-col gap-y-8 mt-8 animate-pulse">
          {[...Array(queryParams.limit)].map((i, idx) => (
            <LoadingRow key={idx} />
          ))}
        </div>
      )}
      <Outlet />
    </div>
  );
}

export default Connections;
