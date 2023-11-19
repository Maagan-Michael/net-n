import clsx from "clsx";
import { TableSeparator } from "@components/tables/generic";
import House from "@icons/house.svg?react";
import Network from "@icons/network.svg?react";
import Customer from "@icons/customer.svg?react";
import Calandar from "@icons/calandar.svg?react";
import Carret from "@icons/carret.svg?react";
import { ListSortEnum, OrderBy } from "@api/types";

interface TableHeaderProps {
  sort: ListSortEnum;
  order: OrderBy;
  setSearch: (params: any) => void;
}

interface TableHeaderCellProps extends TableHeaderProps {
  title: string;
  separate?: boolean;
  classname?: string;
  children?: React.ReactNode;
  sortValue?: ListSortEnum;
}

export const TableHeaderCell = ({
  sort,
  sortValue,
  setSearch,
  order,
  title,
  separate,
  classname,
  children,
}: TableHeaderCellProps) => {
  const canSort = sortValue !== undefined;
  const isSort = canSort && sort === sortValue;
  const isDesc = isSort && order === OrderBy.desc;
  const onClick = () => {
    if (canSort) {
      if (isSort) {
        return setSearch({
          order: isDesc ? OrderBy.asc : OrderBy.desc,
        });
      }
      return setSearch({
        sort: sortValue,
        order: OrderBy.asc,
      });
    }
  };
  return (
    <div
      onClick={onClick}
      key={title}
      className={clsx(
        "relative h-12 border-b-2 border-neutral-100 flex items-center justify-center w-full",
        classname,
        canSort
          ? isSort
            ? "cursor-pointer first:[&>svg]:opacity-100 first:[&>svg]:hover:animate-pulse"
            : "cursor-pointer first:[&>svg]:opacity-30 [&>svg]:hover:opacity-100"
          : "cursor-default",
        isDesc && "first:[&>svg]:rotate-180"
      )}
    >
      {canSort && (
        <Carret className="mt-1 w-4 transition-all duration-300 transform opacity-0" />
      )}
      {children ? (
        children
      ) : (
        <div className="font-light text-sm text-center">{title}</div>
      )}
      {separate && <TableSeparator />}
    </div>
  );
};

const Header = ({ sort, order, setSearch }: TableHeaderProps) => (
  <div className="h-full text-xs text-center grid grid-flow-col grid-cols-12 w-full md:gap-x-4 lg:gap-x-8 xl:gap-x-12">
    <div className="h-full grid grid-flow-col items-center grid-cols-11 col-span-12 lg:col-span-10">
      <TableHeaderCell
        sort={sort}
        order={order}
        title="ppp"
        separate
        classname="col-span-2 md:col-span-1"
        sortValue={ListSortEnum.con}
        setSearch={setSearch}
      />
      <TableHeaderCell
        sort={sort}
        order={order}
        sortValue={ListSortEnum.name}
        title="customer"
        separate
        classname="col-span-3 md:col-span-2"
        setSearch={setSearch}
      >
        <Customer className="w-5 h-5 md:w-6 md:h-6" />
      </TableHeaderCell>
      <TableHeaderCell
        sort={sort}
        order={order}
        sortValue={ListSortEnum.cid}
        title="ID"
        separate
        classname="hidden md:flex col-span-2 lg:col-span-1"
        setSearch={setSearch}
      />
      <TableHeaderCell
        sort={sort}
        order={order}
        sortValue={ListSortEnum.switch}
        title="switch"
        separate
        classname="col-span-3 md:col-span-2"
        setSearch={setSearch}
      >
        <Network className="w-5 h-5 md:w-6 md:h-6" />
      </TableHeaderCell>
      <TableHeaderCell
        sort={sort}
        order={order}
        title="date"
        separate
        classname="hidden md:flex col-span-2"
        setSearch={setSearch}
      >
        <Calandar className="w-5 h-5 md:w-6 md:h-6" />
      </TableHeaderCell>
      <TableHeaderCell
        sort={sort}
        order={order}
        sortValue={ListSortEnum.address}
        title="address"
        separate
        classname="col-span-3 md:col-span-2"
        setSearch={setSearch}
      >
        <House className="w-5 h-5 md:w-6 md:h-6" />
      </TableHeaderCell>
      <TableHeaderCell
        sort={sort}
        order={order}
        title="type"
        classname="hidden lg:flex col-span-1"
        setSearch={setSearch}
      />
    </div>
    <div className="hidden h-full grid grid-flow-col items-center lg:flex col-span-2">
      <TableHeaderCell
        sort={sort}
        order={order}
        title="connexion status"
        setSearch={setSearch}
      />
    </div>
  </div>
);

export default Header;
