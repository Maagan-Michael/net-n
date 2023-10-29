import clsx from "clsx";
import { FunctionComponent, useState } from "react";
import { Outlet, URLSearchParamsInit } from "react-router-dom";
import { ReactComponent as Search } from "../components/icons/search.svg";
import TextButton from "../components/inputs/textBtn";
import { ReactComponent as Customer } from "../components/icons/customer.svg";
import { ReactComponent as House } from "../components/icons/house.svg";
import { ReactComponent as Network } from "../components/icons/network.svg";
import { ReactComponent as Computer } from "../components/icons/computer.svg";
import IconRoundBtn from "../components/inputs/iconRoundBtn";
import { useConnectionsUrlParams } from "../api/queries/getConnections";
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
  const [params, setParams] = useConnectionsUrlParams();
  const [search, setSearch] = useState<string>(params.search || "");
  const filter: cf = params.filter || cf.all;
  const currentFilter = filtersMap[filter];
  const onSearch = (_filter?: cf) => {
    setParams({
      ...params,
      search,
      filter: _filter || filter,
    } as unknown as URLSearchParamsInit);
    (document.activeElement as HTMLElement)?.blur();
  };
  const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearch(e.target.value);
    if (e.target.value.length === 0) {
      setParams({
        ...params,
        search: "",
        filter: cf.all,
      } as unknown as URLSearchParamsInit);
    }
  };
  const searchActive =
    params.search && params.search.length > 0 && search.length !== 0;
  return (
    <div className="p-12">
      <section>
        <h1 className="font-thin text-3xl">SwitchManager</h1>
        <section>
          <div className="rounded-md bg-neutral-100 w-[440px] mt-6 flex items-center gap-x-1 px-2 shadow relative [&>.search-popup]:focus-within:block">
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
