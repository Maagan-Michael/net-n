import House from "@icons/house.svg?react";
import Network from "@icons/network.svg?react";
import Customer from "@icons/customer.svg?react";
import Calandar from "@icons/calandar.svg?react";
import { ListSortEnum, OrderBy } from "@api/types";
import { TableHeaderCell } from "./TableHeaderCell";
import { useTranslation } from "react-i18next";
import clsx from "clsx";

interface TableHeaderProps {
  sort: ListSortEnum;
  order: OrderBy;
  setSearch: (params: any) => void;
}

export interface TableHeaderCellProps extends TableHeaderProps {
  title: string;
  classname?: string;
  children?: React.ReactNode;
  sortValue?: ListSortEnum;
}

const staticHeader = [
  {
    title: "ppp",
    classname: "col-span-2 md:col-span-1",
    sortValue: ListSortEnum.con,
  },
  {
    title: "customer",
    classname: "col-span-3 md:col-span-2",
    sortValue: ListSortEnum.name,
    icon: Customer,
  },
  {
    title: "ID",
    classname: "hidden md:flex col-span-2 lg:col-span-1",
    sortValue: ListSortEnum.cid,
  },
  {
    title: "switch",
    classname: "col-span-3 md:col-span-2",
    sortValue: ListSortEnum.switch,
    icon: Network,
  },
  {
    title: "date",
    classname: "hidden md:flex col-span-2",
    icon: Calandar,
  },
  {
    title: "address",
    classname:
      "col-span-3 [&>.separator]:hidden lg:[&>.separator]:block md:col-span-2",
    sortValue: ListSortEnum.address,
    icon: House,
  },
  {
    title: "type",
    classname: "hidden lg:flex col-span-1",
  },
];

const Header = ({ sort, order, setSearch }: TableHeaderProps) => {
  const { i18n } = useTranslation();
  return (
    <div
      className={clsx(
        "h-full text-xs text-center grid grid-flow-col grid-cols-12 w-full md:gap-x-4 lg:gap-x-8 xl:gap-x-12",
        i18n.dir()
      )}
    >
      <div className="h-full grid grid-flow-col items-center grid-cols-11 col-span-12 lg:col-span-10">
        {staticHeader.map((header, index) => (
          <TableHeaderCell
            key={header.title}
            sort={sort}
            order={order}
            title={header.title}
            classname={header.classname}
            sortValue={header.sortValue}
            setSearch={setSearch}
          >
            {header.icon && <header.icon className="w-5 h-5 md:w-6 md:h-6" />}
          </TableHeaderCell>
        ))}
      </div>
      <div className="hidden h-full grid grid-flow-col items-center lg:flex col-span-2">
        <TableHeaderCell
          sort={sort}
          order={order}
          title="status"
          setSearch={setSearch}
        />
      </div>
    </div>
  );
};

export default Header;
