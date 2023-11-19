import { FunctionComponent, useEffect, useCallback, useState } from "react";
import clsx from "clsx";
import { Outlet } from "react-router-dom";
import useTimeout from "@/hooks/useTimeout";
import TextButton from "@components/inputs/textBtn";
import IconRoundBtn from "@components/inputs/iconRoundBtn";
import Search from "@icons/search.svg?react";
import Customer from "@icons/customer.svg?react";
import House from "@icons/house.svg?react";
import Network from "@icons/network.svg?react";
import Computer from "@icons/computer.svg?react";
import { useConnectionsUrlParams } from "@api/queries/getConnections";
import { ConnectionsFilters as cf } from "@api/types";

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
  const [params, setParams] = useConnectionsUrlParams();
  const [search, setSearch] = useState<string>(params.search || "");
  const createTimeout = useTimeout();
  const filter: cf = params.filter || cf.all;
  const currentFilter = filtersMap[filter];
  const onSearch = useCallback(
    (_filter?: cf, blur: boolean = true) => {
      setParams({
        search,
        filter: _filter || filter,
      });
      blur && (document.activeElement as HTMLElement)?.blur();
    },
    [filter, search, setParams]
  );
  const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearch(e.target.value);
    if (e.target.value.length === 0) {
      setParams({
        search: "",
        filter: cf.all,
      });
    }
  };
  useEffect(() => {
    createTimeout(() => onSearch(undefined, false), 500);
  }, [createTimeout, onSearch, search]);
  const searchActive =
    params.search && params.search.length > 0 && search.length !== 0;
  return (
    <div className="p-1 md:p-2 lg:p-8">
      <section className="flex items-center gap-x-4 mt-4 md:block md:mt-0">
        <h1 className="font-thin text-xl md:text-3xl">SwitchManager</h1>
        <section className="grow md:w-[440px] md:mt-4 lg:mt-6">
          <div className="rounded-md w-full bg-neutral-100 flex items-center gap-x-1 px-2 shadow relative [&>.search-popup]:focus-within:block">
            <Search
              className={clsx(
                "w-12 h-12",
                searchActive ? "text-blue-400" : "text-red-400"
              )}
            />
            <input
              type="search"
              placeholder="search..."
              className="bg-transparent outline-none text-sm grow"
              onChange={onChange}
              value={search}
            />
            {currentFilter && (
              <IconFilterElem
                sm
                onClick={() => onSearch(cf.all)}
                {...currentFilter}
              />
            )}
            {search.length !== 0 && (
              <div className="search-popup absolute w-full mt-48 left-0 rounded-md shadow-md p-4 bg-neutral-100 z-10 hidden">
                <div className="flex items-center justify-evenly pb-4 w-full">
                  {Object.entries(filtersMap).map(([key, props]) => (
                    <IconFilterElem
                      key={key}
                      onClick={(e) => onSearch(key as unknown as cf)}
                      {...props}
                    />
                  ))}
                </div>
                <TextButton label="search" onClick={() => onSearch()} />
              </div>
            )}
          </div>
        </section>
      </section>
      <Outlet />
    </div>
  );
}
