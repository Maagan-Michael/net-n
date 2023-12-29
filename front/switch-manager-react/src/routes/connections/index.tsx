import { Outlet } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { Table } from "@components/tables/generic";
import { ConnectionOutput, ConnectionsOutput } from "@api/types";
import {
  useConnectionsQuery,
  useConnectionsUrlParams,
} from "@api/queries/getConnections";
import useInfiniteScroller from "@hooks/useInfiniteScroller";
import Header from "./table/header";
import Row from "./table/row";
import LoadingRow from "./table/loadingRow";

function ConnectionsContent() {
  const { t } = useTranslation("translation", { keyPrefix: "connections" });
  const [queryParams, setParams] = useConnectionsUrlParams();
  const { data, isLoading, fetchNextPage, isFetchingNextPage, hasNextPage } =
    useConnectionsQuery(queryParams);
  const onReady = useInfiniteScroller(
    () => {
      if (!isLoading && !isFetchingNextPage && hasNextPage) {
        fetchNextPage();
      }
    },
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
    <>
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
        <div className="flex flex-col gap-y-1 md:gap-y-1 lg:gap-y-4">
          {[...Array(queryParams.limit)].map((i, idx) => (
            <LoadingRow key={idx} />
          ))}
        </div>
      )}
      {!isLoading && pagesContent.length === 0 && (
        <div className="flex flex-col items-center justify-center gap-y-4 mt-8">
          <h3 className="font-bold text-xl">{t("notFound")}</h3>
        </div>
      )}
      {!isLoading && pagesContent.length > 0 && !hasNextPage && (
        <div className="flex flex-col items-center justify-center gap-y-4 mt-4 mb-4 md:mt-8 md:mb-8">
          <h3 className="font-bold text-md">{t("noMore")}</h3>
        </div>
      )}
    </>
  );
}
function Connections() {
  return (
    <div>
      <ConnectionsContent />
      <Outlet />
    </div>
  );
}

export default Connections;
