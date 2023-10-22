import clsx from "clsx";
import { TableSeparator } from "./generic";
import { ReactComponent as ComputerIcon } from "../icons/computer.svg";
import { ReactComponent as House } from "../icons/house.svg";
import { ReactComponent as Network } from "../icons/network.svg";
import { ReactComponent as Customer } from "../icons/customer.svg";
import { ReactComponent as Calandar } from "../icons/calandar.svg";
import Toggle from "../inputs/toggle";

export const mockupData = [
  {
    ppp: "NR12",
    customer: "woody Allen",
    id: "6554367",
    switch: "switch X (110.168.86.1) : 43",
    date: "12 / 10 / 2023",
    address: "270/03",
    type: "haverim",
    isUp: true,
    toggled: true,
    adapter: "snmp",
  },
  {
    ppp: "NR12",
    customer: "woody Allen",
    id: "6554367",
    switch: "switch X (110.168.86.1) : 43",
    date: "12 / 10 / 2023",
    address: "270/03",
    type: "haverim",
    isUp: true,
    toggled: true,
    adapter: "snmp",
  },
  {
    ppp: "NR12",
    customer: "woody Allen",
    id: "6554367",
    switch: "switch X (110.168.86.1) : 43",
    date: "12 / 10 / 2023",
    address: "270/03",
    type: "haverim",
    isUp: true,
    toggled: true,
    adapter: "snmp",
  },
  {
    ppp: "NR12",
    customer: "woody Allen",
    id: "6554367",
    switch: "switch X (110.168.86.1) : 43",
    date: "12 / 10 / 2023",
    address: "270/03",
    type: "haverim",
    isUp: true,
    toggled: true,
    adapter: "snmp",
  },
];

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
      <TableHeaderCell title="switch" separate classname="col-span-3">
        <Network className="w-6 h-6" />
      </TableHeaderCell>
      <TableHeaderCell title="date" separate classname="col-span-2">
        <Calandar className="w-6 h-6" />
      </TableHeaderCell>
      <TableHeaderCell title="address" separate classname="col-span-1">
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
}: React.PropsWithChildren<{ data: (typeof mockupData)[0] }>) => {
  return (
    <div className="w-full h-14 text-xs text-center grid grid-flow-col grid-cols-12 gap-x-12 [&>*]:hover:border-blue-300 cursor-pointer">
      <div className="h-full rounded-md bg-neutral-100 grid grid-flow-col items-center grid-cols-11 col-span-10 border-2 border-neutral-100 transition-colors">
        <div className="col-span-1">{data.ppp}</div>
        <div className="col-span-2">{data.customer}</div>
        <div className="col-span-1">{data.id}</div>
        <div className="col-span-3">{data.switch}</div>
        <div className="col-span-2 flex flex-col items-center gap-x-2 justify-center">
          {data.date ? (
            <span>
              <DateStatus toggled={data.toggled} />
              <span>{data.date}</span>
            </span>
          ) : (
            <span>N / A</span>
          )}
        </div>
        <div className="col-span-1">{data.address}</div>
        <div className="col-span-1">{data.type}</div>
      </div>
      <div className="h-full rounded-md bg-neutral-100 p-4 grid grid-flow-col items-center justify-between col-span-2 border-2 border-neutral-100 transition-colors">
        <div className="flex items-center">
          <Toggle name="toggle connexion" toggled={data.toggled} />
        </div>
        <span>{data.adapter}</span>
        <ComputerIcon
          className={clsx(
            "w-6 h-6",
            data.isUp ? "fill-green-400" : "fill-red-500"
          )}
        />
      </div>
    </div>
  );
};
