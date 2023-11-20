import { useEffect, useCallback, useState, useRef } from "react";
import clsx from "clsx";
import useTimeout from "@/hooks/useTimeout";
import Search from "@icons/search.svg?react";
import { useConnectionsUrlParams } from "@api/queries/getConnections";
import { ConnectionsFilters as cf } from "@api/types";
import { filtersMap, IconFilterElem } from "./filters";

export const SearchBar = ({
  shouldFocus = false,
  onSearchDone = () => {},
}: {
  shouldFocus?: boolean;
  onSearchDone?: () => void;
}) => {
  const [params, setParams] = useConnectionsUrlParams();
  const [search, setSearch] = useState<string>(params.search || "");
  const createTimeout = useTimeout();
  const filter: cf = params.filter || cf.all;
  const currentFilter = filtersMap[filter];
  const inputRef = useRef<HTMLInputElement>(null);
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
  const onSelect = useCallback(
    (filter?: cf) => {
      onSearch(filter);
      onSearchDone();
    },
    [onSearch, onSearchDone]
  );
  useEffect(() => {
    createTimeout(() => onSearch(undefined, false), 500);
  }, [createTimeout, onSearch, search]);
  // useLayoutEffect(() => {
  //   shouldFocus && inputRef.current?.focus();
  // }, [shouldFocus]);
  const searchActive =
    params.search && params.search.length > 0 && search.length !== 0;
  return (
    <div className="rounded-md w-full bg-white lg:bg-neutral-100 flex items-center gap-x-1 px-2 shadow relative [&>.search-popup]:focus-within:block">
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
        ref={inputRef}
      />
      {currentFilter && search.length !== 0 && (
        <IconFilterElem
          sm
          onClick={() => onSelect(cf.all)}
          {...currentFilter}
        />
      )}
      {search.length !== 0 && (
        <div
          className={
            "search-popup absolute w-full mb-4 lg:mb-0 bottom-full lg:bottom-[unset] lg:mt-32 left-0 rounded-md shadow-md p-4 bg-white lg:bg-neutral-100 z-10 hidden"
          }
        >
          <div className="flex items-center justify-evenly w-full">
            {Object.entries(filtersMap).map(([key, props]) => (
              <IconFilterElem
                key={key}
                onClick={(e) => onSearch(key as unknown as cf)}
                disabled={key === filter}
                {...props}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
