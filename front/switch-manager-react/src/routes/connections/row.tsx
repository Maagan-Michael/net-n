import clsx from "clsx";
import { useNavigate } from "react-router-dom";
import { ReactComponent as ComputerIcon } from "../../components/icons/computer.svg";
import { ReactComponent as Ethernet } from "../../components/icons/ethernet.svg";
import Toggle from "../../components/inputs/toggle";
import { ConnectionOutput } from "../../api/types";
import { useCallback } from "react";

const DateStatus = ({ toggled }: { toggled: boolean }) => (
  <span
    className={clsx(
      "w-2 h-2 rounded-full  inline-block mr-2",
      toggled ? "bg-red-500" : "bg-green-300"
    )}
  />
);

const Row = ({ data }: React.PropsWithChildren<{ data: ConnectionOutput }>) => {
  const {
    id,
    name,
    customer,
    switch: sw,
    port,
    toggleDate,
    toggled,
    adapter,
    isUp,
  } = data;
  const navigate = useNavigate();
  const onclick = useCallback(() => {
    navigate(`/connections/${id}${window.location.search}`);
  }, [navigate, id]);
  return (
    <div className="w-full h-16 lg:h-14 text-xs text-center grid grid-flow-col grid-cols-12 md:gap-x-4 lg:gap-x-8 xl:gap-x-12 [&>*]:hover:border-blue-300 cursor-pointer">
      <div
        className="h-full rounded-md bg-neutral-100 grid grid-flow-col items-center grid-cols-11 col-span-12 lg:col-span-10 border-2 border-neutral-100 transition-colors"
        onClick={onclick}
      >
        <div className="col-span-2 md:col-span-1 flex flex-col items-center justify-center">
          <span>{name}</span>
          <div className="flex items-center gap-x-2 lg:hidden">
            <Ethernet
              className={clsx(
                "w-4 h-4",
                toggled ? "text-green-400" : "text-red-500"
              )}
            />
            <ComputerIcon
              className={clsx(
                "w-4 h-4",
                isUp ? "text-green-400" : "text-red-500"
              )}
            />
          </div>
        </div>
        <div className="col-span-3 md:col-span-2 flex flex-col">
          <span>
            {customer.lastname} {customer.firstname}
          </span>
          <span className="md:hidden">ID: {customer.id}</span>
        </div>
        <div className="hidden md:block col-span-2 lg:col-span-1">
          {customer.id}
        </div>
        <div className="col-span-3 md:col-span-2 flex flex-col break-words">
          <span>{sw.name}</span>
          <span>
            {sw.ip}:{port}
          </span>
        </div>
        <div className="hidden col-span-2 md:flex flex-col items-center gap-x-2 justify-center">
          {toggleDate ? (
            <span>
              <DateStatus toggled={toggled} />
              <span>{new Date(toggleDate).toLocaleDateString()}</span>
            </span>
          ) : (
            <span>N / A</span>
          )}
        </div>
        <div className="col-span-3 md:col-span-2">{customer.address}</div>
        <div className="hidden lg:block col-span-1">{customer.type}</div>
      </div>
      <div className="hidden h-full rounded-md bg-neutral-100 p-4 lg:grid grid-flow-col items-center justify-between col-span-2 border-2 border-neutral-100 transition-colors">
        <div className="flex items-center">
          <Ethernet
            className={clsx(
              "w-7 h-7",
              toggled ? "text-green-400" : "text-red-500"
            )}
          />
        </div>
        <span>{adapter}</span>
        <ComputerIcon
          className={clsx("w-6 h-6", isUp ? "text-green-400" : "text-red-500")}
        />
      </div>
    </div>
  );
};

export default Row;
