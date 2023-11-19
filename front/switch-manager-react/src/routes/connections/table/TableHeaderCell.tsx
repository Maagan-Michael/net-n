import clsx from "clsx";
import { TableSeparator } from "@components/tables/generic";
import Carret from "@icons/carret.svg?react";
import { OrderBy } from "@api/types";
import { TableHeaderCellProps } from "./header";

export const TableHeaderCell = ({
  sort,
  sortValue,
  setSearch,
  order,
  title,
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
        "relative h-12 border-b-2 border-neutral-100 flex items-center justify-center w-full [&:last-child>.separator]:hidden",
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
      <TableSeparator />
    </div>
  );
};
