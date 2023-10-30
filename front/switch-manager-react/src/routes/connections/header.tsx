import clsx from "clsx";
import { TableSeparator } from "../../components/tables/generic";
import { ReactComponent as House } from "../../components/icons/house.svg";
import { ReactComponent as Network } from "../../components/icons/network.svg";
import { ReactComponent as Customer } from "../../components/icons/customer.svg";
import { ReactComponent as Calandar } from "../../components/icons/calandar.svg";
import { ReactComponent as Carret } from "../../components/icons/carret.svg";
import { ListSortEnum, OrderBy } from "../../api/types";

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
        "relative h-12 border-b-2 border-neutral-100 flex items-center justify-center",
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
  <div className="h-14 text-xs text-center grid grid-flow-col grid-cols-12 w-full gap-x-12">
    <div className="h-full grid grid-flow-col items-center grid-cols-11 col-span-10">
      <TableHeaderCell
        sort={sort}
        order={order}
        title="ppp"
        separate
        classname="col-span-1"
        sortValue={ListSortEnum.con}
        setSearch={setSearch}
      />
      <TableHeaderCell
        sort={sort}
        order={order}
        sortValue={ListSortEnum.name}
        title="customer"
        separate
        classname="col-span-2"
        setSearch={setSearch}
      >
        <Customer className="w-6 h-6" />
      </TableHeaderCell>
      <TableHeaderCell
        sort={sort}
        order={order}
        sortValue={ListSortEnum.cid}
        title="ID"
        separate
        classname="col-span-1"
        setSearch={setSearch}
      />
      <TableHeaderCell
        sort={sort}
        order={order}
        sortValue={ListSortEnum.switch}
        title="switch"
        separate
        classname="col-span-2"
        setSearch={setSearch}
      >
        <Network className="w-6 h-6" />
      </TableHeaderCell>
      <TableHeaderCell
        sort={sort}
        order={order}
        title="date"
        separate
        classname="col-span-2"
        setSearch={setSearch}
      >
        <Calandar className="w-6 h-6" />
      </TableHeaderCell>
      <TableHeaderCell
        sort={sort}
        order={order}
        sortValue={ListSortEnum.address}
        title="address"
        separate
        classname="col-span-2"
        setSearch={setSearch}
      >
        <House className="w-6 h-6" />
      </TableHeaderCell>
      <TableHeaderCell
        sort={sort}
        order={order}
        title="type"
        classname="col-span-1"
        setSearch={setSearch}
      />
    </div>
    <div className="h-full grid grid-flow-col items-center col-span-2">
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
