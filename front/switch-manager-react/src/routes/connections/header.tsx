import clsx from "clsx";
import { TableSeparator } from "../../components/tables/generic";
import { ReactComponent as House } from "../../components/icons/house.svg";
import { ReactComponent as Network } from "../../components/icons/network.svg";
import { ReactComponent as Customer } from "../../components/icons/customer.svg";
import { ReactComponent as Calandar } from "../../components/icons/calandar.svg";

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

const Header = () => (
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

export default Header;
