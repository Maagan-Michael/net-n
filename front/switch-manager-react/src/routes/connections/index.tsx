import { Outlet } from "react-router-dom";
import { Table } from "../../components/tables/generic";
import { ConnectionOutput, ConnectionsOutput } from "../../api/types";
import {
  useConnectionsQuery,
  useConnectionsUrlParams,
} from "../../api/queries/getConnections";
import useInfiniteScroller from "../../components/hooks/useInfiniteScroller";
import Header from "./header";
import Row from "./row";
import LoadingRow from "./loadingRow";

function Connections() {
  const [queryParams, setParams] = useConnectionsUrlParams();
  const { data, isLoading, fetchNextPage, isFetchingNextPage, hasNextPage } =
    useConnectionsQuery(queryParams);
  const onReady = useInfiniteScroller(
    () => !isLoading && !isFetchingNextPage && fetchNextPage(),
    {
      threshold: 0.8,
    }
  );
  const pagesContent: ConnectionOutput[] = (data?.pages || []).reduce(
    (r: ConnectionOutput[], page: ConnectionsOutput) => [
      ...r,
      ...page.connections,
    ],
    []
  );
  return (
    <div>
      <Table
        data={pagesContent || []}
        renderHeader={
          <Header
            sort={queryParams.sort}
            order={queryParams.order}
            setSearch={setParams}
          />
        }
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
      {!isLoading && pagesContent.length === 0 && (
        <div className="flex flex-col items-center justify-center gap-y-4 mt-8">
          <h3 className="font-bold text-xl">no connections found</h3>
        </div>
      )}
      {!isLoading && pagesContent.length > 0 && !hasNextPage && (
        <div className="flex flex-col items-center justify-center gap-y-4 mt-4 mb-4 md:mt-8 md:mb-8">
          <h3 className="font-bold text-md">no more connections</h3>
        </div>
      )}
      <Outlet />
    </div>
  );
}

export default Connections;
