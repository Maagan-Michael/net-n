import clsx from "clsx";
import { TableSeparator, Table } from "./generic";
import { ReactComponent as ComputerIcon } from "../icons/computer.svg";
import { ReactComponent as House } from "../icons/house.svg";
import { ReactComponent as Network } from "../icons/network.svg";
import { ReactComponent as Customer } from "../icons/customer.svg";
import { ReactComponent as Calandar } from "../icons/calandar.svg";
import Toggle from "../inputs/toggle";
import { ConnectionOutput, ConnectionsOutput } from "../../api/types";
import {
  useConnectionsQuery,
  useConnectionsUrlParams,
} from "../../api/queries/connections";
import useInfiniteScroller from "../hooks/useInfiniteScroller";

export const TableHeaderCell = ({
  title,
  separate,
  classname,
  children,
}: {
  title: string;
  separate?: boolean;
  classname?: string;
  children?: React.ReactNode;
}) => (
  <div
    key={title}
    className={clsx(
      "relative h-12 border-b-2 border-neutral-100 flex items-center justify-center",
      classname
    )}
  >
    {children ? (
      children
    ) : (
      <div className="font-light text-sm text-center">{title}</div>
    )}
    {separate && <TableSeparator />}
  </div>
);

export const Header = () => (
  <div className="h-14 text-xs text-center grid grid-flow-col grid-cols-12 w-full gap-x-12">
    <div className="h-full grid grid-flow-col items-center grid-cols-11 col-span-10">
      <TableHeaderCell title="ppp" separate classname="col-span-1" />
      <TableHeaderCell title="customer" separate classname="col-span-2">
        <Customer className="w-6 h-6" />
      </TableHeaderCell>
      <TableHeaderCell title="ID" separate classname="col-span-1" />
      <TableHeaderCell title="switch" separate classname="col-span-2">
        <Network className="w-6 h-6" />
      </TableHeaderCell>
      <TableHeaderCell title="date" separate classname="col-span-2">
        <Calandar className="w-6 h-6" />
      </TableHeaderCell>
      <TableHeaderCell title="address" separate classname="col-span-2">
        <House className="w-6 h-6" />
      </TableHeaderCell>
      <TableHeaderCell title="type" classname="col-span-1" />
    </div>
    <div className="h-full grid grid-flow-col items-center col-span-2">
      <TableHeaderCell title="connexion status" />
    </div>
  </div>
);

const DateStatus = ({ toggled }: { toggled: boolean }) => (
  <span
    className={clsx(
      "w-2 h-2 rounded-full  inline-block mr-2",
      toggled ? "bg-red-500" : "bg-green-300"
    )}
  />
);

export const Row = ({
  data,
}: React.PropsWithChildren<{ data: ConnectionOutput }>) => {
  return (
    <div className="w-full h-14 text-xs text-center grid grid-flow-col grid-cols-12 gap-x-12 [&>*]:hover:border-blue-300 cursor-pointer">
      <div className="h-full rounded-md bg-neutral-100 grid grid-flow-col items-center grid-cols-11 col-span-10 border-2 border-neutral-100 transition-colors">
        <div className="col-span-1">{data.name}</div>
        <div className="col-span-2">
          {data.customer.firstname} {data.customer.lastname}
        </div>
        <div className="col-span-1">{data.customer.id}</div>
        <div className="col-span-2">
          {data.switch.name} ({data.switch.ip}) : {data.port}
        </div>
        <div className="col-span-2 flex flex-col items-center gap-x-2 justify-center">
          {data.toggleDate ? (
            <span>
              <DateStatus toggled={data.toggled} />
              <span>{data.toggleDate}</span>
            </span>
          ) : (
            <span>N / A</span>
          )}
        </div>
        <div className="col-span-2">{data.customer.address}</div>
        <div className="col-span-1">{data.customer.type}</div>
      </div>
      <div className="h-full rounded-md bg-neutral-100 p-4 grid grid-flow-col items-center justify-between col-span-2 border-2 border-neutral-100 transition-colors">
        <div className="flex items-center">
          <Toggle name="toggle connexion" toggled={data.toggled} />
        </div>
        <span>{data.adapter}</span>
        <ComputerIcon
          className={clsx(
            "w-6 h-6",
            data.isUp ? "text-green-400" : "text-red-500"
          )}
        />
      </div>
    </div>
  );
};

const LoadingRow = () => (
  <div className="w-full h-14 grid grid-flow-col grid-cols-12 gap-x-12">
    <div className="h-full rounded-md bg-neutral-100 col-span-10"></div>
    <div className="h-full rounded-md bg-neutral-100 grow col-span-2"></div>
  </div>
);

export function ConnectionsTable() {
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
    </div>
  );
}
