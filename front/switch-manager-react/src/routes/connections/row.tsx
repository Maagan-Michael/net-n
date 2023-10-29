import clsx from "clsx";
import { useNavigate } from "react-router-dom";
import { ReactComponent as ComputerIcon } from "../../components/icons/computer.svg";
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
    navigate(`/connections/${id}`);
  }, [navigate, id]);
  return (
    <div className="w-full h-14 text-xs text-center grid grid-flow-col grid-cols-12 gap-x-12 [&>*]:hover:border-blue-300 cursor-pointer">
      <div
        className="h-full rounded-md bg-neutral-100 grid grid-flow-col items-center grid-cols-11 col-span-10 border-2 border-neutral-100 transition-colors"
        onClick={onclick}
      >
        <div className="col-span-1">{name}</div>
        <div className="col-span-2">
          {customer.firstname} {customer.lastname}
        </div>
        <div className="col-span-1">{customer.id}</div>
        <div className="col-span-2">
          {sw.name} ({sw.ip}) : {port}
        </div>
        <div className="col-span-2 flex flex-col items-center gap-x-2 justify-center">
          {toggleDate ? (
            <span>
              <DateStatus toggled={toggled} />
              <span>{toggleDate}</span>
            </span>
          ) : (
            <span>N / A</span>
          )}
        </div>
        <div className="col-span-2">{customer.address}</div>
        <div className="col-span-1">{customer.type}</div>
      </div>
      <div className="h-full rounded-md bg-neutral-100 p-4 grid grid-flow-col items-center justify-between col-span-2 border-2 border-neutral-100 transition-colors">
        <div className="flex items-center">
          <Toggle name="toggle connexion" toggled={toggled} />
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
