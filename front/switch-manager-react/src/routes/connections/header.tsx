import House from "@icons/house.svg?react";
import Network from "@icons/network.svg?react";
import Customer from "@icons/customer.svg?react";
import Calandar from "@icons/calandar.svg?react";
import { ListSortEnum, OrderBy } from "@api/types";
import { TableHeaderCell } from "./TableHeaderCell";

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

const Header = ({ sort, order, setSearch }: TableHeaderProps) => (
  <div className="h-full text-xs text-center grid grid-flow-col grid-cols-12 w-full md:gap-x-4 lg:gap-x-8 xl:gap-x-12">
    <div className="h-full grid grid-flow-col items-center grid-cols-11 col-span-12 lg:col-span-10">
      <TableHeaderCell
        sort={sort}
        order={order}
        title="ppp"
        classname="col-span-2 md:col-span-1"
        sortValue={ListSortEnum.con}
        setSearch={setSearch}
      />
      <TableHeaderCell
        sort={sort}
        order={order}
        sortValue={ListSortEnum.name}
        title="customer"
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
        classname="hidden md:flex col-span-2 lg:col-span-1"
        setSearch={setSearch}
      />
      <TableHeaderCell
        sort={sort}
        order={order}
        sortValue={ListSortEnum.switch}
        title="switch"
        classname="col-span-3 md:col-span-2"
        setSearch={setSearch}
      >
        <Network className="w-5 h-5 md:w-6 md:h-6" />
      </TableHeaderCell>
      <TableHeaderCell
        sort={sort}
        order={order}
        title="date"
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
        classname="col-span-3 [&>.separator]:hidden lg:[&>.separator]:block md:col-span-2"
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
