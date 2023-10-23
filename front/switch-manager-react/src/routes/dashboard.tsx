import clsx from "clsx";
import { FunctionComponent, useCallback, useState } from "react";
import { Outlet } from "react-router-dom";
import { ReactComponent as Search } from "../components/icons/search.svg";
import TextButton from "../components/inputs/textBtn";
import { ReactComponent as Customer } from "../components/icons/customer.svg";
import { ReactComponent as House } from "../components/icons/house.svg";
import { ReactComponent as Network } from "../components/icons/network.svg";
import { ReactComponent as Computer } from "../components/icons/computer.svg";
import IconRoundBtn from "../components/inputs/iconRoundBtn";
import { ConnectionsFilters as cf } from "../api/types";

interface IconFilterElemProps {
  sm?: boolean;
  onClick?: (e: React.MouseEvent<HTMLElement, MouseEvent>) => void;
  icon?: FunctionComponent<React.SVGAttributes<SVGElement>>;
  text?: string;
}

const IconFilterElem = ({
  sm,
  icon: Icon,
  onClick,
  text,
}: IconFilterElemProps) => (
  <IconRoundBtn
    onClick={onClick}
    icon={Icon != null && <Icon className={clsx(sm ? "w-3 h-3" : "w-6 h-6")} />}
    className={sm ? "w-6 h-6 text-xs" : "w-10 h-10"}
    text={text}
  />
);

const filtersMap: { [x: string]: IconFilterElemProps } = {
  [cf.customer]: { icon: Customer },
  [cf.address]: { icon: House },
  [cf.switch]: { icon: Network },
  [cf.up]: { icon: Computer },
  [cf.customerId]: { text: "ID" },
  [cf.enabled]: { text: "ON" },
};

export default function Dashboard() {
  const [search, setSearch] = useState<string>("");
  const [filters, setFilters] = useState<cf[]>([]);
  const onFilterClick = useCallback(
    (e: cf) =>
      setFilters((prev) => {
        if (prev.includes(e)) {
          return prev.filter((f) => f !== e);
        }
        return [...prev, e];
      }),
    [setFilters]
  );
  return (
    <div className="p-12">
      <section>
        <h1 className="font-thin text-3xl">SwitchManager</h1>
        <section>
          <div className="rounded-md bg-neutral-100 w-[440px] mt-6 flex items-center gap-x-1 px-2 shadow relative [&>.search-popup]:focus-within:block">
            <Search className={clsx("w-12 h-12", "text-red-400")} />
            <input
              type="search"
              placeholder="search..."
              className="bg-transparent outline-none text-sm grow"
              onChange={(e) => setSearch(e.target.value)}
              value={search}
            />
            {filters.map((f) => {
              const props = filtersMap[f as cf];
              return (
                <IconFilterElem
                  key={f}
                  sm
                  onClick={() => onFilterClick(f)}
                  {...props}
                />
              );
            })}
            {search.length !== 0 && (
              <div className="search-popup absolute w-full mt-48 left-0 rounded-md shadow-md p-4 bg-neutral-100 z-10 block">
                <div className="flex items-center justify-evenly pb-4 w-full">
                  {Object.entries(filtersMap).map(([key, props]) => (
                    <IconFilterElem
                      key={key}
                      onClick={(e) => onFilterClick(key as unknown as cf)}
                      {...props}
                    />
                  ))}
                </div>
                <TextButton label="search" />
              </div>
            )}
          </div>
        </section>
      </section>
      <Outlet />
    </div>
  );
}
